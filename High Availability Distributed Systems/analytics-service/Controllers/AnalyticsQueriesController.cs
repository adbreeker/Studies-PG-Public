using Microsoft.AspNetCore.Mvc;
using analytics_service.Application.Handlers;
using analytics_service.Application.Queries;

namespace analytics_service.Controllers
{    [ApiController]
    [Route("api/analytics")]
    public class AnalyticsQueriesController : ControllerBase
    {
        private readonly GetDepartureDirectionPreferencesQueryHandler _departureDirectionPreferencesHandler;
        private readonly GetRealTimeAnalyticsQueryHandler _realTimeAnalyticsHandler;

        public AnalyticsQueriesController(
            GetDepartureDirectionPreferencesQueryHandler departureDirectionPreferencesHandler,
            GetRealTimeAnalyticsQueryHandler realTimeAnalyticsHandler)
        {
            _departureDirectionPreferencesHandler = departureDirectionPreferencesHandler;
            _realTimeAnalyticsHandler = realTimeAnalyticsHandler;
        }        [HttpGet("departure-direction-preferences")]
        public async Task<IActionResult> GetDepartureDirectionPreferences(
            [FromQuery] DateTime? startDate,
            [FromQuery] DateTime? endDate,
            [FromQuery] int? limit,
            [FromQuery] string? departureStation,
            [FromQuery] string? period)
        {
            var query = new GetDepartureDirectionPreferencesQuery
            {
                StartDate = startDate,
                EndDate = endDate,
                Limit = limit,
                DepartureStation = departureStation,
                Period = period
            };

            var result = await _departureDirectionPreferencesHandler.Handle(query);
            return Ok(result);
        }[HttpGet("real-time")]
        public async Task<IActionResult> GetRealTimeAnalytics(
            [FromQuery] DateTime? from,
            [FromQuery] DateTime? to,
            [FromQuery] string? groupBy)
        {
            var query = new GetRealTimeAnalyticsQuery
            {
                From = from,
                To = to,
                GroupBy = groupBy
            };

            var result = await _realTimeAnalyticsHandler.Handle(query);
            return Ok(result);
        }

        [HttpGet("health")]
        public IActionResult HealthCheck()
        {
            return Ok(new { Status = "Healthy", Service = "Analytics Service", Timestamp = DateTime.UtcNow });
        }
    }
}
