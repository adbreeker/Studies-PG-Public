using analytics_service.Application.Queries;
using analytics_service.Domain;
using analytics_service.Infrastructure;
using Microsoft.EntityFrameworkCore;

namespace analytics_service.Application.Handlers
{
    public class GetDepartureDirectionPreferencesQueryHandler
    {
        private readonly AnalyticsDbContext _dbContext;

        public GetDepartureDirectionPreferencesQueryHandler(AnalyticsDbContext dbContext)
        {
            _dbContext = dbContext;
        }        public async Task<List<DepartureDirectionPreference>> Handle(GetDepartureDirectionPreferencesQuery query)
        {
            var reservationsQuery = _dbContext.ReservationAnalytics.AsQueryable();

            // Apply filters with UTC conversion - use DepartureDate for trip scheduling analytics
            if (query.StartDate.HasValue)
            {
                var startDateUtc = query.StartDate.Value.Kind == DateTimeKind.Unspecified 
                    ? DateTime.SpecifyKind(query.StartDate.Value, DateTimeKind.Utc) 
                    : query.StartDate.Value.ToUniversalTime();
                reservationsQuery = reservationsQuery.Where(r => r.DepartureDate >= startDateUtc);
            }

            if (query.EndDate.HasValue)
            {
                var endDateUtc = query.EndDate.Value.Kind == DateTimeKind.Unspecified 
                    ? DateTime.SpecifyKind(query.EndDate.Value, DateTimeKind.Utc) 
                    : query.EndDate.Value.ToUniversalTime();
                reservationsQuery = reservationsQuery.Where(r => r.DepartureDate <= endDateUtc);
            }

            if (!string.IsNullOrEmpty(query.DepartureStation))
            {
                reservationsQuery = reservationsQuery.Where(r => r.DepartureStation.Contains(query.DepartureStation));
            }

            // Get all reservations to process grouping in memory
            var reservations = await reservationsQuery.ToListAsync();

            // Group by route AND time period based on the period parameter
            var groupedData = reservations
                .GroupBy(r => new 
                { 
                    r.DepartureStation, 
                    r.ArrivalStation,
                    TimePeriod = GetTimePeriod(r.DepartureDate, query.Period)
                })
                .Select(g => new
                {
                    DepartureStation = g.Key.DepartureStation,
                    ArrivalStation = g.Key.ArrivalStation,
                    TimePeriod = g.Key.TimePeriod,
                    Count = g.Count(),
                    Reservations = g.ToList()
                })
                .OrderByDescending(g => g.Count)
                .Take(query.Limit ?? 10)
                .ToList();

            // Calculate total reservations for percentage calculation
            var totalReservations = reservations.Count;

            var result = groupedData.Select(g => 
            {
                var (periodStart, periodEnd) = CalculatePeriodBounds(g.TimePeriod, query.Period);
                
                return new DepartureDirectionPreference(
                    g.DepartureStation,
                    g.ArrivalStation,
                    g.Count,
                    totalReservations > 0 ? (double)g.Count / totalReservations * 100 : 0
                )
                {
                    // Set period boundaries based on the time period grouping
                    PeriodStart = periodStart,
                    PeriodEnd = periodEnd
                };
            }).ToList();

            return result;
        }

        private string GetTimePeriod(DateTime departureDate, string period)
        {
            return period?.ToLower() switch
            {
                "daily" => departureDate.Date.ToString("yyyy-MM-dd"),
                "weekly" => GetWeekPeriod(departureDate),
                "monthly" => departureDate.ToString("yyyy-MM"),
                _ => departureDate.Date.ToString("yyyy-MM-dd") // Default to daily
            };
        }

        private string GetWeekPeriod(DateTime date)
        {
            // Get the Monday of the week
            var dayOfWeek = (int)date.DayOfWeek;
            var daysToSubtract = dayOfWeek == 0 ? 6 : dayOfWeek - 1; // Handle Sunday (0) as last day of week
            var monday = date.Date.AddDays(-daysToSubtract);
            return $"{monday:yyyy-MM-dd}_week";
        }

        private (DateTime periodStart, DateTime periodEnd) CalculatePeriodBounds(string timePeriod, string period)
        {
            return period?.ToLower() switch
            {
                "daily" => CalculateDailyBounds(timePeriod),
                "weekly" => CalculateWeeklyBounds(timePeriod),
                "monthly" => CalculateMonthlyBounds(timePeriod),
                _ => CalculateDailyBounds(timePeriod)
            };
        }

        private (DateTime start, DateTime end) CalculateDailyBounds(string timePeriod)
        {
            if (DateTime.TryParse(timePeriod, out var date))
            {
                return (date.Date, date.Date.AddDays(1).AddTicks(-1));
            }
            return (DateTime.UtcNow.Date, DateTime.UtcNow.Date.AddDays(1).AddTicks(-1));
        }

        private (DateTime start, DateTime end) CalculateWeeklyBounds(string timePeriod)
        {
            var datePart = timePeriod.Replace("_week", "");
            if (DateTime.TryParse(datePart, out var monday))
            {
                var sunday = monday.AddDays(6).AddHours(23).AddMinutes(59).AddSeconds(59);
                return (monday, sunday);
            }
            return (DateTime.UtcNow.Date, DateTime.UtcNow.Date.AddDays(7).AddTicks(-1));
        }

        private (DateTime start, DateTime end) CalculateMonthlyBounds(string timePeriod)
        {
            if (DateTime.TryParseExact(timePeriod, "yyyy-MM", null, System.Globalization.DateTimeStyles.None, out var monthStart))
            {
                var monthEnd = monthStart.AddMonths(1).AddTicks(-1);
                return (monthStart, monthEnd);
            }
            var now = DateTime.UtcNow;
            var firstDayOfMonth = new DateTime(now.Year, now.Month, 1);
            var lastDayOfMonth = firstDayOfMonth.AddMonths(1).AddTicks(-1);
            return (firstDayOfMonth, lastDayOfMonth);
        }
    }
}
