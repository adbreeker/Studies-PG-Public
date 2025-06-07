// Infrastructure/EventStore/IEventStore.cs
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using changes_manager.Domain.Events;

namespace changes_manager.Infrastructure.EventStore
{
    public interface IEventStore
    {
        Task SaveEventAsync(IEvent @event);
        Task<IEnumerable<IEvent>> GetEventsAsync(string aggregateId);
        Task<IEnumerable<IEvent>> GetEventsByTypeAsync(string eventType, int skip = 0, int take = 100);
        Task<IEnumerable<IEvent>> GetAllEventsAsync(int skip = 0, int take = 100);
    }
}