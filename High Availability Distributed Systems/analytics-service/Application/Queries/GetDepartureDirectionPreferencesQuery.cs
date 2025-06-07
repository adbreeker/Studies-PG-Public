namespace analytics_service.Application.Queries
{
    public class GetDepartureDirectionPreferencesQuery
    {
        public DateTime? StartDate { get; set; }
        public DateTime? EndDate { get; set; }
        public int? Limit { get; set; }
        public string? DepartureStation { get; set; }
        public string? Period { get; set; } // "daily", "weekly", "monthly"

        public GetDepartureDirectionPreferencesQuery()
        {
            Limit = 10;
            StartDate = DateTime.UtcNow.AddDays(-30); // Default to last 30 days
            EndDate = DateTime.UtcNow;
            Period = "monthly"; // Default to monthly grouping
        }
    }
}
