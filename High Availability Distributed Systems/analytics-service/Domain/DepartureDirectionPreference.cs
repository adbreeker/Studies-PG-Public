namespace analytics_service.Domain
{    public class DepartureDirectionPreference
    {
        public string DepartureStation { get; set; }
        public string ArrivalStation { get; set; }
        public int ReservationCount { get; set; }
        public DateTime LastUpdated { get; set; }
        public double Percentage { get; set; }
        
        // Period information for frontend
        public DateTime? PeriodStart { get; set; }
        public DateTime? PeriodEnd { get; set; }

        public DepartureDirectionPreference()
        {
            DepartureStation = string.Empty;
            ArrivalStation = string.Empty;
            LastUpdated = DateTime.UtcNow;
        }

        public DepartureDirectionPreference(string departureStation, string arrivalStation, 
            int reservationCount, double percentage)
        {
            DepartureStation = departureStation;
            ArrivalStation = arrivalStation;
            ReservationCount = reservationCount;
            Percentage = percentage;
            LastUpdated = DateTime.UtcNow;
        }
    }
}
