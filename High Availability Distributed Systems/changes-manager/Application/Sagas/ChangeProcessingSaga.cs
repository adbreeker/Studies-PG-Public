// Application/Sagas/ChangeProcessingSaga.cs
using System;
using System.Threading.Tasks;
using changes_manager.Domain.Events;
using changes_manager.Infrastructure.EventStore;
using Microsoft.Extensions.Logging;

namespace changes_manager.Application.Sagas
{
    public interface ISaga
    {
        Task HandleAsync(IEvent @event);
    }

    public class ChangeProcessingSaga : ISaga
    {
        private readonly IEventStore _eventStore;
        private readonly ILogger<ChangeProcessingSaga> _logger;

        public ChangeProcessingSaga(IEventStore eventStore, ILogger<ChangeProcessingSaga> logger)
        {
            _eventStore = eventStore;
            _logger = logger;
        }

        public async Task HandleAsync(IEvent @event)
        {
            switch (@event)
            {
                case PriceChangeDetected priceChange:
                    await ProcessPriceChange(priceChange);
                    break;
                case AvailabilityChangeDetected availabilityChange:
                    await ProcessAvailabilityChange(availabilityChange);
                    break;
                case TrainMonitoringStarted monitoringStarted:
                    await ProcessMonitoringStarted(monitoringStarted);
                    break;
            }
        }

        private async Task ProcessPriceChange(PriceChangeDetected @event)
        {
            _logger.LogInformation($"Saga: Processing price change for train {@event.TrainId}");

            // Step 1: Validate the change
            var isValidChange = Math.Abs(@event.NewPrice - @event.OldPrice) > 0.01m;
            
            if (isValidChange)
            {
                // Step 2: Send notification
                var notificationEvent = new ChangeNotificationSent
                {
                    ChangeId = @event.Id,
                    TrainId = @event.TrainId,
                    NotificationType = "PRICE_CHANGE",
                    Success = true
                };

                await _eventStore.SaveEventAsync(notificationEvent);
                _logger.LogInformation($"Saga: Price change notification sent for train {@event.TrainId}");
            }
        }

        private async Task ProcessAvailabilityChange(AvailabilityChangeDetected @event)
        {
            _logger.LogInformation($"Saga: Processing availability change for train {@event.TrainId}");

            // Send notification
            var notificationEvent = new ChangeNotificationSent
            {
                ChangeId = @event.Id,
                TrainId = @event.TrainId,
                NotificationType = "AVAILABILITY_CHANGE",
                Success = true
            };

            await _eventStore.SaveEventAsync(notificationEvent);
            _logger.LogInformation($"Saga: Availability change notification sent for train {@event.TrainId}");
        }

        private async Task ProcessMonitoringStarted(TrainMonitoringStarted @event)
        {
            _logger.LogInformation($"Saga: Monitoring session {@event.SessionId} started with {@event.TrainIds.Count} trains");
            
            // Could trigger initial price/availability checks here
            await Task.CompletedTask;
        }
    }
}