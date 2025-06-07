using Microsoft.AspNetCore.Mvc;
using transaction_manager.Application.Commands;
using transaction_manager.Application.Handlers;
using transaction_manager.Saga;

namespace transaction_manager.Controllers
{
    [ApiController]
    [Route("api/reservation/commands")]
    public class ReservationCommandsController : ControllerBase
    {
        private readonly ReservationCreationSaga _reservationCreationSaga;
        private readonly DeleteReservationCommandHandler _deleteReservationCommandHandler;
        private readonly DeleteAllReservationsCommandHandler _deleteAllReservationsCommandHandler;

        public ReservationCommandsController(
            ReservationCreationSaga reservationCreationSaga,
            DeleteReservationCommandHandler deleteReservationCommandHandler,
            DeleteAllReservationsCommandHandler deleteAllReservationsCommandHandler)
        {
            _reservationCreationSaga = reservationCreationSaga;
            _deleteReservationCommandHandler = deleteReservationCommandHandler;
            _deleteAllReservationsCommandHandler = deleteAllReservationsCommandHandler;
        }

        [HttpPost("create")]
        public async Task<IActionResult> CreateReservation([FromBody] CreateReservationCommand command, [FromHeader(Name = "X-SignalR-ConnectionId")] string connectionId = null)
        {
            var result = await _reservationCreationSaga.Start(command, connectionId);

            if (result == "Reservation created successfully.")
            {
                return Ok(result);
            }

            return BadRequest(result);
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteReservation(Guid id)
        {
            var result = await _deleteReservationCommandHandler.Handle(new DeleteReservationCommand { ReservationId = id });

            if (result == "Reservation deleted successfully.")
            {
                return Ok(result);
            }

            return NotFound(result);
        }

        [HttpDelete("all")]
        public async Task<IActionResult> DeleteAllReservations()
        {
            var result = await _deleteAllReservationsCommandHandler.Handle(new DeleteAllReservationsCommand());
            return Ok(result);
        }
    }
}
