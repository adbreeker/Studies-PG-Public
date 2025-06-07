using transaction_manager.Application.Queries;
using transaction_manager.Infrastructure;
using Microsoft.EntityFrameworkCore;

public class GetReservedTrainCarsQueryHandler
{
    private readonly ReservationDbContext _dbContext;

    public GetReservedTrainCarsQueryHandler(ReservationDbContext dbContext)
    {
        _dbContext = dbContext;
    }

    public async Task<List<int>> Handle(GetReservedTrainCarsQuery query)
    {
        return await _dbContext.Reservations
            .Where(r => r.TrainId == query.TrainId &&
                        r.DepartureDate == query.DepartureDate &&
                        r.DepartureStation == query.DepartureStation &&
                        r.ArrivalDate == query.ArrivalDate &&
                        r.ArrivalStation == query.ArrivalStation)
            .SelectMany(r => r.TrainCars)
            .Distinct()
            .ToListAsync();
    }
}
