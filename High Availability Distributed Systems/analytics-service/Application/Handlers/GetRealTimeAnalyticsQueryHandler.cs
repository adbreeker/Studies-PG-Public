using analytics_service.Application.Queries;
using analytics_service.Infrastructure;
using Microsoft.EntityFrameworkCore;

namespace analytics_service.Application.Handlers
{
    public class GetRealTimeAnalyticsQueryHandler
    {
        private readonly AnalyticsDbContext _dbContext;

        public GetRealTimeAnalyticsQueryHandler(AnalyticsDbContext dbContext)
        {
            _dbContext = dbContext;
        }

        public async Task<object> Handle(GetRealTimeAnalyticsQuery query)
        {
            var reservationsQuery = _dbContext.ReservationAnalytics.AsQueryable();

            // Apply time filters
            if (query.From.HasValue)
            {
                reservationsQuery = reservationsQuery.Where(r => r.CreatedAt >= query.From.Value);
            }

            if (query.To.HasValue)
            {
                reservationsQuery = reservationsQuery.Where(r => r.CreatedAt <= query.To.Value);
            }

            // Group by time period and departure direction
            var timeGroupedData = query.GroupBy?.ToLower()
            switch
            {
                "day" => (await reservationsQuery
                    .GroupBy(r => new
                    {
                        Date = r.CreatedAt.Date,
                        r.DepartureStation,
                        r.ArrivalStation
                    })
                    .Select(g => new
                    {
                        Date = g.Key.Date,
                        DepartureStation = g.Key.DepartureStation,
                        ArrivalStation = g.Key.ArrivalStation,
                        Count = g.Count()
                    })
                    .OrderBy(g => g.Date)
                    .ToListAsync())
                    .Select(g => new
                    {
                        TimePeriod = g.Date.ToString("yyyy-MM-dd"),
                        DepartureStation = g.DepartureStation,
                        ArrivalStation = g.ArrivalStation,
                        Count = g.Count
                    })
                    .ToList(),
                "week" => (await reservationsQuery
                    .GroupBy(r => new
                    {
                        Week = new DateTime(r.CreatedAt.Year, r.CreatedAt.Month, r.CreatedAt.Day).AddDays(-(int)r.CreatedAt.DayOfWeek),
                        r.DepartureStation,
                        r.ArrivalStation
                    })
                    .Select(g => new
                    {
                        Week = g.Key.Week,
                        DepartureStation = g.Key.DepartureStation,
                        ArrivalStation = g.Key.ArrivalStation,
                        Count = g.Count()
                    })
                    .OrderBy(g => g.Week)
                    .ToListAsync())
                    .Select(g => new
                    {
                        TimePeriod = g.Week.ToString("yyyy-MM-dd"),
                        DepartureStation = g.DepartureStation,
                        ArrivalStation = g.ArrivalStation,
                        Count = g.Count
                    })
                    .ToList(),
                _ => (await reservationsQuery // Default to hour
                    .GroupBy(r => new
                    {
                        Hour = new DateTime(r.CreatedAt.Year, r.CreatedAt.Month, r.CreatedAt.Day, r.CreatedAt.Hour, 0, 0),
                        r.DepartureStation,
                        r.ArrivalStation
                    })
                    .Select(g => new
                    {
                        Hour = g.Key.Hour,
                        DepartureStation = g.Key.DepartureStation,
                        ArrivalStation = g.Key.ArrivalStation,
                        Count = g.Count()
                    })
                    .OrderBy(g => g.Hour)
                    .ToListAsync())
                    .Select(g => new
                    {
                        TimePeriod = g.Hour.ToString("yyyy-MM-dd HH:00"),
                        DepartureStation = g.DepartureStation,
                        ArrivalStation = g.ArrivalStation,
                        Count = g.Count
                    })
                    .ToList()
            };

            // Get overall statistics
            var totalReservations = await reservationsQuery.CountAsync();
            var uniqueRoutes = await reservationsQuery
                .Select(r => new { r.DepartureStation, r.ArrivalStation })
                .Distinct()
                .CountAsync();

            var topRoutes = await reservationsQuery
                .GroupBy(r => new { r.DepartureStation, r.ArrivalStation })
                .Select(g => new
                {
                    Route = $"{g.Key.DepartureStation} ? {g.Key.ArrivalStation}",
                    Count = g.Count()
                })
                .OrderByDescending(g => g.Count)
                .Take(5)
                .ToListAsync();

            return new
            {
                // Frontend expects these at root level
                totalReservations = totalReservations,
                lastUpdated = DateTime.UtcNow,

                // Keep detailed data for future use
                Summary = new
                {
                    TotalReservations = totalReservations,
                    UniqueRoutes = uniqueRoutes,
                    TopRoutes = topRoutes,
                    TimeRange = new
                    {
                        From = query.From,
                        To = query.To,
                        GroupBy = query.GroupBy
                    }
                },
                TimeSeriesData = timeGroupedData
            };
        }
    }
}
