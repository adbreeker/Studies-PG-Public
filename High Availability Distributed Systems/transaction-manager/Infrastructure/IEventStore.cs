namespace transaction_manager.Infrastructure
{
    public interface IEventStore
    {
        Task SaveAsync<T>(T aggregate) where T : class;
        Task<T?> LoadAsync<T>(Guid id) where T : class;
    }
}
