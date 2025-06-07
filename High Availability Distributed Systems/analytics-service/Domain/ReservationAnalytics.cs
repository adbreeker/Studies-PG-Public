namespace analytics_service.Domain
{    public class ReservationAnalytics
    {
        public Guid Id { get; set; }
        public string AccountId { get; set; } = string.Empty;
        public string TrainId { get; set; } = string.Empty;
        public DateTime DepartureDate { get; set; }
        public string DepartureStation { get; set; } = string.Empty;
        public DateTime ArrivalDate { get; set; }
        public string ArrivalStation { get; set; } = string.Empty;
        public List<int> TrainCars { get; set; } = new List<int>();
        public DateTime CreatedAt { get; set; }

        public ReservationAnalytics()
        {
            TrainCars = new List<int>();
        }

        public ReservationAnalytics(Guid id, string accountId, string trainId, DateTime departureDate, 
            string departureStation, DateTime arrivalDate, string arrivalStation, List<int> trainCars)
        {
            Id = id;
            AccountId = accountId;
            TrainId = trainId;
            DepartureDate = departureDate;
            DepartureStation = departureStation;
            ArrivalDate = arrivalDate;
            ArrivalStation = arrivalStation;
            TrainCars = trainCars ?? new List<int>();
            CreatedAt = DateTime.UtcNow;
        }
    }
}
