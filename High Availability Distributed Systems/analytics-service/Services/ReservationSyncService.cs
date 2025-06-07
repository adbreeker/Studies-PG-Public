using analytics_service.Domain;
using analytics_service.Infrastructure;
using Microsoft.EntityFrameworkCore;
using Microsoft.AspNetCore.SignalR;
using analytics_service.Hubs;
using analytics_service.Application.Handlers;
using analytics_service.Application.Queries;
using System.Text.Json;

namespace analytics_service.Services
{
    public class ReservationSyncService : BackgroundService
    {
        private readonly IServiceScopeFactory _scopeFactory;
        private readonly ILogger<ReservationSyncService> _logger;
        private readonly IHubContext<AnalyticsHub> _hubContext;
        private readonly IHttpClientFactory _httpClientFactory;

        public ReservationSyncService(
            IServiceScopeFactory scopeFactory,
            ILogger<ReservationSyncService> logger,
            IHubContext<AnalyticsHub> hubContext,
            IHttpClientFactory httpClientFactory)
        {
            _scopeFactory = scopeFactory;
            _logger = logger;
            _hubContext = hubContext;
            _httpClientFactory = httpClientFactory;
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            _logger.LogInformation("Reservation Sync Service started");

            while (!stoppingToken.IsCancellationRequested)
            {
                try
                {
                    await SyncReservations();
                    await SendRealTimeUpdates();
                    
                    // Wait 30 seconds before next sync
                    await Task.Delay(TimeSpan.FromSeconds(30), stoppingToken);
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error during reservation sync");
                    await Task.Delay(TimeSpan.FromMinutes(1), stoppingToken);
                }
            }
        }
        private async Task SyncReservations()
        {
            using var scope = _scopeFactory.CreateScope();
            var analyticsContext = scope.ServiceProvider.GetRequiredService<AnalyticsDbContext>();

            // Get last sync time
            var lastSyncTime = await GetLastSyncTime(analyticsContext);

            // Call transaction-manager API to get real reservations
            var newReservations = await FetchRealReservations(analyticsContext, lastSyncTime);

            if (newReservations.Any())
            {
                await analyticsContext.ReservationAnalytics.AddRangeAsync(newReservations);
                await analyticsContext.SaveChangesAsync();

                _logger.LogInformation($"Synced {newReservations.Count} new reservations from transaction-manager");
            }
        }

        private async Task<DateTime> GetLastSyncTime(AnalyticsDbContext context)
        {
            var lastReservation = await context.ReservationAnalytics
                .OrderByDescending(r => r.CreatedAt)
                .FirstOrDefaultAsync();

            return lastReservation?.CreatedAt ?? DateTime.UtcNow.AddDays(-30);
        }
        private async Task<List<ReservationAnalytics>> FetchRealReservations(AnalyticsDbContext analyticsContext, DateTime lastSyncTime)
        {
            try
            {
                var httpClient = _httpClientFactory.CreateClient("TransactionManager");

                _logger.LogInformation($"Fetching reservations from transaction-manager since {lastSyncTime}");

                // Call the transaction-manager API to get all reservations
                var response = await httpClient.GetAsync("/api/reservation/queries/all");

                if (!response.IsSuccessStatusCode)
                {
                    _logger.LogWarning($"Failed to fetch reservations: {response.StatusCode} - {response.ReasonPhrase}");
                    return new List<ReservationAnalytics>();
                }

                var jsonContent = await response.Content.ReadAsStringAsync();
                var options = new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                };

                var transactionReservations = JsonSerializer.Deserialize<List<TransactionManagerReservation>>(jsonContent, options)
                    ?? new List<TransactionManagerReservation>();

                _logger.LogInformation($"Received {transactionReservations.Count} reservations from transaction-manager");

                // Get existing analytics reservation IDs to avoid duplicates - using the same context
                var existingIdsList = await analyticsContext.ReservationAnalytics
                    .Select(r => r.Id)
                    .ToListAsync();                    
                var existingIds = existingIdsList;

                // Convert to analytics format and filter out existing reservations
                var analyticsReservations = new List<ReservationAnalytics>();

                foreach (var reservation in transactionReservations)
                {
                    // Check if this reservation ID already exists in analytics
                    if (!existingIds.Contains(reservation.Id))
                    {
                        var analyticsReservation = new ReservationAnalytics(
                            reservation.Id, // Use original ID to prevent duplicates
                            reservation.AccountId,
                            reservation.TrainId,
                            reservation.DepartureDate,
                            reservation.DepartureStation,
                            reservation.ArrivalDate,
                            reservation.ArrivalStation,
                            reservation.TrainCars
                        );

                        analyticsReservations.Add(analyticsReservation);
                    }
                }

                _logger.LogInformation($"Converted {analyticsReservations.Count} new reservations for analytics");
                return analyticsReservations;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error fetching real reservations from transaction-manager");
                return new List<ReservationAnalytics>();
            }
        }        private async Task SendRealTimeUpdates()
        {
            using var scope = _scopeFactory.CreateScope();
            var analyticsContext = scope.ServiceProvider.GetRequiredService<AnalyticsDbContext>();
            var realTimeHandler = scope.ServiceProvider.GetRequiredService<GetRealTimeAnalyticsQueryHandler>();

            try
            {
                // Get complete real-time analytics data using the same handler as the API endpoint
                var query = new analytics_service.Application.Queries.GetRealTimeAnalyticsQuery
                {
                    From = null,
                    To = null,
                    GroupBy = "hour"
                };

                var completeAnalyticsData = await realTimeHandler.Handle(query);

                // Validate the data before sending
                if (completeAnalyticsData != null)
                {
                    // Send complete analytics update to all connected clients
                    await _hubContext.Clients.Group("Analytics")
                        .SendAsync("AnalyticsUpdated", completeAnalyticsData);

                    _logger.LogInformation("Sent complete real-time analytics update via SignalR");
                }
                else
                {
                    _logger.LogWarning("Real-time analytics handler returned null data, sending fallback");
                    await SendFallbackAnalyticsData(analyticsContext);
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error sending real-time analytics updates");
                await SendFallbackAnalyticsData(analyticsContext);
            }
        }

        private async Task SendFallbackAnalyticsData(AnalyticsDbContext analyticsContext)
        {
            try
            {
                // Fallback to basic data if the full handler fails
                var totalReservations = await analyticsContext.ReservationAnalytics.CountAsync();

                var fallbackUpdate = new
                {
                    totalReservations = totalReservations,
                    lastUpdated = DateTime.UtcNow
                };

                await _hubContext.Clients.Group("Analytics")
                    .SendAsync("AnalyticsUpdated", fallbackUpdate);

                _logger.LogInformation($"Sent fallback analytics update: {totalReservations} total reservations");
            }
            catch (Exception fallbackEx)
            {
                _logger.LogError(fallbackEx, "Error sending fallback analytics data");
            }
        }
    }
}
