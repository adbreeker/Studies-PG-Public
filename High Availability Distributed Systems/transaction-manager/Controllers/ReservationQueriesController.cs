using Microsoft.AspNetCore.Mvc;
using transaction_manager.Application.Handlers;
using transaction_manager.Application.Queries;

namespace transaction_manager.Controllers
{
    [ApiController]
    [Route("api/reservation/queries")]
    public class ReservationQueriesController : ControllerBase
    {
        private readonly GetAllReservationsQueryHandler _getAllReservationsQueryHandler;
        private readonly GetReservationByIdQueryHandler _getReservationByIdQueryHandler;
        private readonly GetReservationsByAccountQueryHandler _getReservationsByAccountQueryHandler;
        private readonly GetReservedTrainCarsQueryHandler _getReservedTrainCarsQueryHandler;

        public ReservationQueriesController(
            GetAllReservationsQueryHandler getAllReservationsQueryHandler,
            GetReservationByIdQueryHandler getReservationByIdQueryHandler,
            GetReservationsByAccountQueryHandler getReservationsByAccountQueryHandler,
            GetReservedTrainCarsQueryHandler getReservedTrainCarsQueryHandler)
        {
            _getAllReservationsQueryHandler = getAllReservationsQueryHandler;
            _getReservationByIdQueryHandler = getReservationByIdQueryHandler;
            _getReservationsByAccountQueryHandler = getReservationsByAccountQueryHandler;
            _getReservedTrainCarsQueryHandler = getReservedTrainCarsQueryHandler;
        }

        [HttpGet("all")]
        public async Task<IActionResult> GetAllReservations()
        {
            var reservations = await _getAllReservationsQueryHandler.Handle();
            return Ok(reservations);
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> GetReservationById(Guid id)
        {
            var reservation = await _getReservationByIdQueryHandler.Handle(new GetReservationByIdQuery { ReservationId = id });
            
            if (reservation == null)
            {
                return NotFound("Reservation not found.");
            }

            return Ok(reservation);
        }

        [HttpGet("account/{accountId}")]
        public async Task<IActionResult> GetReservationsByAccount(string accountId)
        {
            var reservations = await _getReservationsByAccountQueryHandler.Handle(new GetReservationsByAccountQuery { AccountId = accountId });
            return Ok(reservations);
        }

        [HttpGet("train-cars")]
        public async Task<IActionResult> GetReservedTrainCars([FromQuery] string trainId, [FromQuery] DateTime departureDate, [FromQuery] string departureStation, [FromQuery] DateTime arrivalDate, [FromQuery] string arrivalStation)
        {
            var query = new GetReservedTrainCarsQuery
            {
                TrainId = trainId,
                DepartureDate = departureDate,
                DepartureStation = departureStation,
                ArrivalDate = arrivalDate,
                ArrivalStation = arrivalStation
            };

            var reservedTrainCars = await _getReservedTrainCarsQueryHandler.Handle(query);
            return Ok(reservedTrainCars);
        }
    }
}
