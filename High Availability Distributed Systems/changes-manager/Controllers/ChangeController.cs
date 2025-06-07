using Microsoft.AspNetCore.Mvc;
using changes_manager.Application.Commands;
using changes_manager.Application.Handlers;
using changes_manager.Application.Sagas;
using changes_manager.Infrastructure.EventStore;
using changes_manager.Domain.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace changes_manager.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ChangesController : ControllerBase
    {
        private readonly ICommandHandler<StartMonitoringCommand> _startMonitoringHandler;
        private readonly ICommandHandler<DetectPriceChangeCommand> _priceChangeHandler;
        private readonly ICommandHandler<DetectAvailabilityChangeCommand> _availabilityChangeHandler;
        private readonly IEventStore _eventStore;
        private readonly ChangeProcessingSaga _saga;
        private static readonly Random _random = new();
        private static string _currentSessionId = null;
        private static List<string> _monitoredTrains = new();
        private static DateTime _lastChangeTime = DateTime.MinValue;

        public ChangesController(
            ICommandHandler<StartMonitoringCommand> startMonitoringHandler,
            ICommandHandler<DetectPriceChangeCommand> priceChangeHandler,
            ICommandHandler<DetectAvailabilityChangeCommand> availabilityChangeHandler,
            IEventStore eventStore,
            ChangeProcessingSaga saga)
        {
            _startMonitoringHandler = startMonitoringHandler;
            _priceChangeHandler = priceChangeHandler;
            _availabilityChangeHandler = availabilityChangeHandler;
            _eventStore = eventStore;
            _saga = saga;
        }

        [HttpGet("recent")]
        public async Task<ActionResult<IEnumerable<Change>>> GetRecentChanges(int count = 10)
        {
            try
            {
                var now = DateTime.UtcNow;
                
                // Generate changes using CQRS pattern with timing control
                if (_monitoredTrains.Count > 0 && !string.IsNullOrEmpty(_currentSessionId) 
                    && (now - _lastChangeTime).TotalSeconds >= 8)
                {
                    await GenerateRandomChange();
                    _lastChangeTime = now;
                }

                // Get all events and convert to Change objects
                var allEvents = await _eventStore.GetAllEventsAsync(0, count * 2);
                var changes = new List<Change>();

                foreach (var eventObj in allEvents)
                {
                    if (eventObj == null) continue;

                    // Use reflection to get properties safely
                    var eventType = eventObj.GetType();
                    var eventTypeProp = eventType.GetProperty("EventType");
                    var eventTypeValue = eventTypeProp?.GetValue(eventObj)?.ToString();

                    if (eventTypeValue == "PriceChangeDetected")
                    {
                        var id = (Guid)eventType.GetProperty("Id")?.GetValue(eventObj);
                        var trainId = eventType.GetProperty("TrainId")?.GetValue(eventObj)?.ToString();
                        var oldPrice = (decimal)eventType.GetProperty("OldPrice")?.GetValue(eventObj);
                        var newPrice = (decimal)eventType.GetProperty("NewPrice")?.GetValue(eventObj);
                        var timestamp = (DateTime)eventType.GetProperty("Timestamp")?.GetValue(eventObj);

                        changes.Add(new Change
                        {
                            Id = id,
                            TripId = trainId,
                            Type = "PRICE_CHANGE",
                            OldPrice = (int)oldPrice,
                            NewPrice = (int)newPrice,
                            Timestamp = timestamp,
                            Details = $"Price changed from {oldPrice} to {newPrice} PLN"
                        });
                    }
                    else if (eventTypeValue == "AvailabilityChangeDetected")
                    {
                        var id = (Guid)eventType.GetProperty("Id")?.GetValue(eventObj);
                        var trainId = eventType.GetProperty("TrainId")?.GetValue(eventObj)?.ToString();
                        var oldAvailability = (bool)eventType.GetProperty("OldAvailability")?.GetValue(eventObj);
                        var newAvailability = (bool)eventType.GetProperty("NewAvailability")?.GetValue(eventObj);
                        var timestamp = (DateTime)eventType.GetProperty("Timestamp")?.GetValue(eventObj);

                        changes.Add(new Change
                        {
                            Id = id,
                            TripId = trainId,
                            Type = "AVAILABILITY_CHANGE",
                            OldAvailability = oldAvailability,
                            NewAvailability = newAvailability,
                            Timestamp = timestamp,
                            Details = $"Availability changed to {(newAvailability ? "available" : "unavailable")}"
                        });
                    }
                }

                var result = changes.OrderByDescending(c => c.Timestamp).Take(count).ToList();
                
                Console.WriteLine($"Returning {result.Count} changes from event store");
                return Ok(result);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error getting changes: {ex.Message}");
                return Ok(new List<Change>());
            }
        }

        [HttpPost("active-trains")]
        public async Task<IActionResult> SetActiveTrains([FromBody] List<string> trainIds)
        {
            _currentSessionId = Guid.NewGuid().ToString();
            _lastChangeTime = DateTime.UtcNow.AddSeconds(-9); // Allow immediate first change
            
            var command = new StartMonitoringCommand
            {
                TrainIds = trainIds,
                SessionId = _currentSessionId,
                UserId = "system"
            };

            await _startMonitoringHandler.HandleAsync(command);
            
            // Get the event and trigger saga
            var events = await _eventStore.GetEventsAsync($"monitoring-{_currentSessionId}");
            foreach (var @event in events)
            {
                await _saga.HandleAsync(@event);
            }

            _monitoredTrains = trainIds;
            
            Console.WriteLine($"CQRS: Started monitoring session {_currentSessionId} with {trainIds.Count} trains");
            
            return Ok(new { SessionId = _currentSessionId, TrainsCount = trainIds.Count });
        }

        [HttpGet("events")]
        public async Task<IActionResult> GetEvents([FromQuery] int skip = 0, [FromQuery] int take = 20)
        {
            var events = await _eventStore.GetAllEventsAsync(skip, take);
            return Ok(events);
        }

        [HttpGet("events/{eventType}")]
        public async Task<IActionResult> GetEventsByType(string eventType, [FromQuery] int skip = 0, [FromQuery] int take = 20)
        {
            var events = await _eventStore.GetEventsByTypeAsync(eventType, skip, take);
            return Ok(events);
        }

        private async Task GenerateRandomChange()
        {
            if (_monitoredTrains.Count == 0) return;

            var selectedTrain = _monitoredTrains[_random.Next(_monitoredTrains.Count)];
            var changeType = _random.Next(2);

            Console.WriteLine($"Generating change for train {selectedTrain}, type: {(changeType == 0 ? "PRICE" : "AVAILABILITY")}");

            if (changeType == 0) // Price change
            {
                var command = new DetectPriceChangeCommand
                {
                    TrainId = selectedTrain,
                    NewPrice = _random.Next(15, 55),
                    SessionId = _currentSessionId
                };

                await _priceChangeHandler.HandleAsync(command);
                
                // Trigger saga
                var events = await _eventStore.GetEventsAsync(selectedTrain);
                var latestEvent = events.OrderByDescending(e => e.Timestamp).FirstOrDefault();
                if (latestEvent != null)
                {
                    await _saga.HandleAsync(latestEvent);
                }
            }
            else // Availability change
            {
                var command = new DetectAvailabilityChangeCommand
                {
                    TrainId = selectedTrain,
                    NewAvailability = _random.Next(2) == 0,
                    Reason = "Capacity or schedule change",
                    SessionId = _currentSessionId
                };

                await _availabilityChangeHandler.HandleAsync(command);
                
                // Trigger saga
                var events = await _eventStore.GetEventsAsync(selectedTrain);
                var latestEvent = events.OrderByDescending(e => e.Timestamp).FirstOrDefault();
                if (latestEvent != null)
                {
                    await _saga.HandleAsync(latestEvent);
                }
            }
        }
    }
}