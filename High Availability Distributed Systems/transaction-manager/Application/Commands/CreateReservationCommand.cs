namespace transaction_manager.Application.Commands
{
    public class CreateReservationCommand
    {
        public required string AccountId { get; set; }
        public required string TrainId { get; set; }
        public required DateTime DepartureDate { get; set; }
        public required string DepartureStation { get; set; }
        public required DateTime ArrivalDate { get; set; }
        public required string ArrivalStation { get; set; }
        public required List<int> TrainCars { get; set; }
    }
}
