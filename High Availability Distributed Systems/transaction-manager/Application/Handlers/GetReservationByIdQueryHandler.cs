using transaction_manager.Application.Queries;
using transaction_manager.Domain;
using transaction_manager.Infrastructure;
using Microsoft.EntityFrameworkCore;

public class GetReservationByIdQueryHandler
{
    private readonly ReservationDbContext _dbContext;

    public GetReservationByIdQueryHandler(ReservationDbContext dbContext)
    {
        _dbContext = dbContext;
    }

    public async Task<Reservation?> Handle(GetReservationByIdQuery query)
    {
        return await _dbContext.Reservations.FirstOrDefaultAsync(r => r.Id == query.ReservationId);
    }
}
