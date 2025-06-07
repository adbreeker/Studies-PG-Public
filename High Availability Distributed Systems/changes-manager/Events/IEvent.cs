// IEvent.cs
using System;

namespace changes_manager.Domain.Events
{
    public interface IEvent
    {
        Guid Id { get; }
        DateTime Timestamp { get; }
        string EventType { get; }
        string AggregateId { get; }
        int Version { get; }
    }

    public abstract class BaseEvent : IEvent
    {
        public Guid Id { get; protected set; } = Guid.NewGuid();
        public DateTime Timestamp { get; protected set; } = DateTime.UtcNow;
        public abstract string EventType { get; }
        public abstract string AggregateId { get; }
        public int Version { get; protected set; } = 1;
    }
}