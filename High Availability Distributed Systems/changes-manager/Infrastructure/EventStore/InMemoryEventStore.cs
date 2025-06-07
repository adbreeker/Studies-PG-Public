using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Text.Json;
using changes_manager.Domain.Events;
using Microsoft.Extensions.Logging;

namespace changes_manager.Infrastructure.EventStore
{
    public class InMemoryEventStore : IEventStore
    {
        private readonly List<StoredEvent> _events = new();
        private readonly ILogger<InMemoryEventStore> _logger;
        private readonly JsonSerializerOptions _jsonOptions;

        public InMemoryEventStore(ILogger<InMemoryEventStore> logger)
        {
            _logger = logger;
            _jsonOptions = new JsonSerializerOptions
            {
                PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
                WriteIndented = true
            };
        }

        public Task SaveEventAsync(IEvent @event)
        {
            var storedEvent = new StoredEvent
            {
                Id = @event.Id,
                AggregateId = @event.AggregateId,
                EventType = @event.EventType,
                EventData = JsonSerializer.Serialize(@event, @event.GetType(), _jsonOptions),
                Timestamp = @event.Timestamp,
                Version = @event.Version
            };

            _events.Add(storedEvent);
            _logger.LogInformation($"Event stored: {@event.EventType} - {@event.Id}");
            
            return Task.CompletedTask;
        }

        public Task<IEnumerable<IEvent>> GetEventsAsync(string aggregateId)
        {
            var events = _events
                .Where(e => e.AggregateId == aggregateId)
                .OrderBy(e => e.Timestamp)
                .Select(DeserializeEvent)
                .Where(e => e != null)
                .ToList();

            return Task.FromResult<IEnumerable<IEvent>>(events);
        }

        public Task<IEnumerable<IEvent>> GetEventsByTypeAsync(string eventType, int skip = 0, int take = 100)
        {
            var events = _events
                .Where(e => e.EventType == eventType)
                .OrderByDescending(e => e.Timestamp)
                .Skip(skip)
                .Take(take)
                .Select(DeserializeEvent)
                .Where(e => e != null)
                .ToList();

            return Task.FromResult<IEnumerable<IEvent>>(events);
        }

        public Task<IEnumerable<IEvent>> GetAllEventsAsync(int skip = 0, int take = 100)
        {
            var events = _events
                .OrderByDescending(e => e.Timestamp)
                .Skip(skip)
                .Take(take)
                .Select(DeserializeEvent)
                .Where(e => e != null)
                .ToList();

            return Task.FromResult<IEnumerable<IEvent>>(events);
        }

        private IEvent? DeserializeEvent(StoredEvent storedEvent)
        {
            try
            {
                var eventType = Type.GetType($"changes_manager.Domain.Events.{storedEvent.EventType}");
                if (eventType == null)
                {
                    _logger.LogWarning($"Unknown event type: {storedEvent.EventType}");
                    return null;
                }
                
                return (IEvent?)JsonSerializer.Deserialize(storedEvent.EventData, eventType, _jsonOptions);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Failed to deserialize event {storedEvent.Id}");
                return null;
            }
        }
    }

    public class StoredEvent
    {
        public Guid Id { get; set; }
        public string AggregateId { get; set; } = string.Empty;
        public string EventType { get; set; } = string.Empty;
        public string EventData { get; set; } = string.Empty;
        public DateTime Timestamp { get; set; }
        public int Version { get; set; }
    }
}