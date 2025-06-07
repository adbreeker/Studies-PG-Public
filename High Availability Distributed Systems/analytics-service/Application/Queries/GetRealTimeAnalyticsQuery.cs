namespace analytics_service.Application.Queries
{
    public class GetRealTimeAnalyticsQuery
    {
        public DateTime? From { get; set; }
        public DateTime? To { get; set; }
        public string? GroupBy { get; set; } // "hour", "day", "week"

        public GetRealTimeAnalyticsQuery()
        {
            From = DateTime.UtcNow.AddHours(-24); // Default to last 24 hours
            To = DateTime.UtcNow;
            GroupBy = "hour";
        }
    }
}
