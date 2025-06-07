using transaction_manager.Application.Queries;
using transaction_manager.Domain;
using transaction_manager.Infrastructure;
using Microsoft.EntityFrameworkCore;

public class GetReservationsByAccountQueryHandler
{
    private readonly ReservationDbContext _dbContext;

    public GetReservationsByAccountQueryHandler(ReservationDbContext dbContext)
    {
        _dbContext = dbContext;
    }

    public async Task<List<Reservation>> Handle(GetReservationsByAccountQuery query)
    {
        return await _dbContext.Reservations
            .Where(r => r.AccountId == query.AccountId)
            .ToListAsync();
    }
}
