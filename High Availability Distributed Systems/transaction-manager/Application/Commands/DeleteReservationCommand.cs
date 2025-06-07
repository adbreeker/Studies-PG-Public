namespace transaction_manager.Application.Commands
{
    public class DeleteReservationCommand
    {
        public required Guid ReservationId { get; set; }
    }
}
