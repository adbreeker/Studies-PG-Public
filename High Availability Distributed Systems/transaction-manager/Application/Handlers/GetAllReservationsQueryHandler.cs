using transaction_manager.Domain;
using transaction_manager.Infrastructure;
using Microsoft.EntityFrameworkCore;

namespace transaction_manager.Application.Handlers
{
    public class GetAllReservationsQueryHandler
    {
        private readonly ReservationDbContext _dbContext;

        public GetAllReservationsQueryHandler(ReservationDbContext dbContext)
        {
            _dbContext = dbContext;
        }

        public async Task<List<Reservation>> Handle()
        {
            return await _dbContext.Reservations.ToListAsync();
        }
    }
}
