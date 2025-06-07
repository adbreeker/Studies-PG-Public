using transaction_manager.Application.Commands;
using transaction_manager.Infrastructure;

namespace transaction_manager.Application.Handlers
{
    public class DeleteAllReservationsCommandHandler
    {
        private readonly ReservationDbContext _dbContext;

        public DeleteAllReservationsCommandHandler(ReservationDbContext dbContext)
        {
            _dbContext = dbContext;
        }

        public async Task<string> Handle(DeleteAllReservationsCommand command)
        {
            _dbContext.Reservations.RemoveRange(_dbContext.Reservations);
            await _dbContext.SaveChangesAsync();

            return "All reservations deleted successfully.";
        }
    }
}
