using transaction_manager.Application.Commands;
using transaction_manager.Infrastructure;
using Microsoft.EntityFrameworkCore;

namespace transaction_manager.Application.Handlers
{
    public class DeleteReservationCommandHandler
    {
        private readonly ReservationDbContext _dbContext;

        public DeleteReservationCommandHandler(ReservationDbContext dbContext)
        {
            _dbContext = dbContext;
        }

        public async Task<string> Handle(DeleteReservationCommand command)
        {
            var reservation = await _dbContext.Reservations.FirstOrDefaultAsync(a => a.Id == command.ReservationId);

            if (reservation == null)
            {
                return "Reservation not found.";
            }

            _dbContext.Reservations.Remove(reservation);
            await _dbContext.SaveChangesAsync();

            return "Reservation deleted successfully.";
        }
    }
}
