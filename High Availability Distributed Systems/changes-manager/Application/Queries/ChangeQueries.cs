// Application/Queries/ChangeQueries.cs
using System;

namespace changes_manager.Application.Queries
{
    public class GetRecentChangesQuery
    {
        public int Count { get; set; } = 10;
        public string TrainId { get; set; }
        public string EventType { get; set; }
    }

    public class GetMonitoringSessionQuery
    {
        public string SessionId { get; set; }
    }

    public class GetTrainChangeHistoryQuery
    {
        public string TrainId { get; set; }
        public int Skip { get; set; } = 0;
        public int Take { get; set; } = 50;
    }
}