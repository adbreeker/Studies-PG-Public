using Microsoft.EntityFrameworkCore;
using transaction_manager.Application.Commands;
using transaction_manager.Domain;
using transaction_manager.Infrastructure;

public class CreateReservationCommandHandler
{
    private readonly ReservationDbContext _dbContext;

    public CreateReservationCommandHandler(ReservationDbContext dbContext)
    {
        _dbContext = dbContext;
    }

    public async Task<string> Handle(CreateReservationCommand command)
    {
        // Check for conflicts
        var conflictingReservations = await _dbContext.Reservations
            .Where(r => r.TrainId == command.TrainId &&
                        r.DepartureStation == command.DepartureStation &&
                        r.DepartureDate == command.DepartureDate &&
                        r.ArrivalStation == command.ArrivalStation &&
                        r.ArrivalDate == command.ArrivalDate &&
                        r.TrainCars.Any(car => command.TrainCars.Contains(car)))
            .ToListAsync();

        if (conflictingReservations.Any())
        {
            return "One or more train cars are already reserved for the specified train and time.";
        }

        // Create the reservation
        var reservation = new Reservation(
            Guid.NewGuid(),
            command.AccountId,
            command.TrainId,
            command.DepartureDate,
            command.DepartureStation,
            command.ArrivalDate,
            command.ArrivalStation,
            command.TrainCars
        );

        _dbContext.Reservations.Add(reservation);
        await _dbContext.SaveChangesAsync();

        return "Reservation created successfully.";
    }
}
