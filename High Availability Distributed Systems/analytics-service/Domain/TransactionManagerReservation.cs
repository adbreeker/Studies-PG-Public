namespace analytics_service.Domain
{
    /// <summary>
    /// DTO model representing reservation data from transaction-manager API
    /// </summary>
    public class TransactionManagerReservation
    {
        public Guid Id { get; set; }
        public string AccountId { get; set; } = string.Empty;
        public string TrainId { get; set; } = string.Empty;
        public DateTime DepartureDate { get; set; }
        public string DepartureStation { get; set; } = string.Empty;
        public DateTime ArrivalDate { get; set; }
        public string ArrivalStation { get; set; } = string.Empty;
        public List<int> TrainCars { get; set; } = new List<int>();
    }
}
