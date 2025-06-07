using System.Collections.Concurrent;

namespace account_manager.Infrastructure
{
    public class InMemoryEventStore : IEventStore
    {
        private readonly ConcurrentDictionary<Guid, object> _store = new();

        public Task SaveAsync<T>(T aggregate) where T : class
        {
            var id = (Guid)aggregate.GetType().GetProperty("Id")!.GetValue(aggregate)!;
            _store[id] = aggregate;
            return Task.CompletedTask;
        }

        public Task<T?> LoadAsync<T>(Guid id) where T : class
        {
            _store.TryGetValue(id, out var aggregate);
            return Task.FromResult(aggregate as T);
        }
    }
}
