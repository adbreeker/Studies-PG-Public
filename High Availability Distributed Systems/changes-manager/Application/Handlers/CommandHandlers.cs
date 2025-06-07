// Application/Handlers/CommandHandlers.cs
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using changes_manager.Application.Commands;
using changes_manager.Domain.Events;
using changes_manager.Infrastructure.EventStore;
using Microsoft.Extensions.Logging;

namespace changes_manager.Application.Handlers
{
    public interface ICommandHandler<in TCommand> where TCommand : ICommand
    {
        Task HandleAsync(TCommand command);
    }

    public class StartMonitoringCommandHandler : ICommandHandler<StartMonitoringCommand>
    {
        private readonly IEventStore _eventStore;
        private readonly ILogger<StartMonitoringCommandHandler> _logger;

        public StartMonitoringCommandHandler(IEventStore eventStore, ILogger<StartMonitoringCommandHandler> logger)
        {
            _eventStore = eventStore;
            _logger = logger;
        }

        public async Task HandleAsync(StartMonitoringCommand command)
        {
            var @event = new TrainMonitoringStarted
            {
                SessionId = command.SessionId,
                TrainIds = command.TrainIds,
                UserId = command.UserId,
                StartedAt = DateTime.UtcNow
            };

            await _eventStore.SaveEventAsync(@event);
            _logger.LogInformation($"Monitoring started for session {command.SessionId} with {command.TrainIds.Count} trains");
        }
    }

    public class DetectPriceChangeCommandHandler : ICommandHandler<DetectPriceChangeCommand>
    {
        private readonly IEventStore _eventStore;
        private readonly ILogger<DetectPriceChangeCommandHandler> _logger;
        private static readonly Dictionary<string, decimal> _currentPrices = new();

        public DetectPriceChangeCommandHandler(IEventStore eventStore, ILogger<DetectPriceChangeCommandHandler> logger)
        {
            _eventStore = eventStore;
            _logger = logger;
        }

        public async Task HandleAsync(DetectPriceChangeCommand command)
        {
            // Get current price or set default
            if (!_currentPrices.TryGetValue(command.TrainId, out var oldPrice))
            {
                oldPrice = new Random().Next(15, 55); // Initial price
                _currentPrices[command.TrainId] = oldPrice;
            }

            // Only create event if price actually changed
            if (Math.Abs(oldPrice - command.NewPrice) > 0.01m)
            {
                var @event = new PriceChangeDetected
                {
                    TrainId = command.TrainId,
                    OldPrice = oldPrice,
                    NewPrice = command.NewPrice,
                    SessionId = command.SessionId
                };

                await _eventStore.SaveEventAsync(@event);
                _currentPrices[command.TrainId] = command.NewPrice;
                
                _logger.LogInformation($"Price change detected for train {command.TrainId}: {oldPrice} -> {command.NewPrice}");
            }
        }
    }

    public class DetectAvailabilityChangeCommandHandler : ICommandHandler<DetectAvailabilityChangeCommand>
    {
        private readonly IEventStore _eventStore;
        private readonly ILogger<DetectAvailabilityChangeCommandHandler> _logger;
        private static readonly Dictionary<string, bool> _currentAvailability = new();

        public DetectAvailabilityChangeCommandHandler(IEventStore eventStore, ILogger<DetectAvailabilityChangeCommandHandler> logger)
        {
            _eventStore = eventStore;
            _logger = logger;
        }

        public async Task HandleAsync(DetectAvailabilityChangeCommand command)
        {
            // Get current availability or set default
            if (!_currentAvailability.TryGetValue(command.TrainId, out var oldAvailability))
            {
                oldAvailability = true; // Default to available
                _currentAvailability[command.TrainId] = oldAvailability;
            }

            // Only create event if availability changed
            if (oldAvailability != command.NewAvailability)
            {
                var @event = new AvailabilityChangeDetected
                {
                    TrainId = command.TrainId,
                    OldAvailability = oldAvailability,
                    NewAvailability = command.NewAvailability,
                    Reason = command.Reason,
                    SessionId = command.SessionId
                };

                await _eventStore.SaveEventAsync(@event);
                _currentAvailability[command.TrainId] = command.NewAvailability;
                
                _logger.LogInformation($"Availability change detected for train {command.TrainId}: {oldAvailability} -> {command.NewAvailability}");
            }
        }
    }
}