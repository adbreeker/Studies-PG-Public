namespace transaction_manager.Domain
{
    public class Reservation
    {
        public Guid Id { get; set; }
        public string AccountId { get; set; }
        public string TrainId { get; set; }
        public DateTime DepartureDate { get; set; }
        public string DepartureStation { get; set; }
        public DateTime ArrivalDate { get; set; }
        public string ArrivalStation { get; set; }
        public List<int> TrainCars { get; set; }

        public Reservation(Guid id, string accountId, string trainId, DateTime departureDate, string departureStation, DateTime arrivalDate, string arrivalStation, List<int> trainCars)
        {
            Id = id;
            AccountId = accountId;
            TrainId = trainId;
            DepartureDate = departureDate;
            DepartureStation = departureStation;
            ArrivalDate = arrivalDate;
            ArrivalStation = arrivalStation;
            TrainCars = trainCars;
        }
    }
}
