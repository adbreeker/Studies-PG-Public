namespace transaction_manager.Application.Queries
{
    public class GetReservedTrainCarsQuery
    {
        public required string TrainId { get; set; }
        public required DateTime DepartureDate { get; set; }
        public required string DepartureStation { get; set; }
        public required DateTime ArrivalDate { get; set; }
        public required string ArrivalStation { get; set; }
    }
}
