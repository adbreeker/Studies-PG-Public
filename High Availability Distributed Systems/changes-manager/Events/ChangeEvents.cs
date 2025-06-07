// ChangeEvents.cs
using System;

namespace changes_manager.Domain.Events
{
    public class TrainMonitoringStarted : BaseEvent
    {
        public override string EventType => "TrainMonitoringStarted";
        public override string AggregateId => $"monitoring-{SessionId}";
        
        public string SessionId { get; set; }
        public List<string> TrainIds { get; set; }
        public string UserId { get; set; }
        public DateTime StartedAt { get; set; }
    }

    public class PriceChangeDetected : BaseEvent
    {
        public override string EventType => "PriceChangeDetected";
        public override string AggregateId => TrainId;
        
        public string TrainId { get; set; }
        public decimal OldPrice { get; set; }
        public decimal NewPrice { get; set; }
        public string DetectionMethod { get; set; } = "Simulation";
        public string SessionId { get; set; }
    }

    public class AvailabilityChangeDetected : BaseEvent
    {
        public override string EventType => "AvailabilityChangeDetected";
        public override string AggregateId => TrainId;
        
        public string TrainId { get; set; }
        public bool OldAvailability { get; set; }
        public bool NewAvailability { get; set; }
        public string Reason { get; set; }
        public string SessionId { get; set; }
    }

    public class ChangeNotificationSent : BaseEvent
    {
        public override string EventType => "ChangeNotificationSent";
        public override string AggregateId => ChangeId.ToString();
        
        public Guid ChangeId { get; set; }
        public string TrainId { get; set; }
        public string NotificationType { get; set; }
        public string Channel { get; set; } = "WebSocket";
        public bool Success { get; set; }
    }

    public class MonitoringSessionEnded : BaseEvent
    {
        public override string EventType => "MonitoringSessionEnded";
        public override string AggregateId => $"monitoring-{SessionId}";
        
        public string SessionId { get; set; }
        public int TotalChangesDetected { get; set; }
        public DateTime EndedAt { get; set; }
        public string Reason { get; set; }
    }
}