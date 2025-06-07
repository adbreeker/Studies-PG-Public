// Application/Commands/ChangeCommands.cs
using System;
using System.Collections.Generic;

namespace changes_manager.Application.Commands
{
    public interface ICommand
    {
        Guid Id { get; }
    }

    public class StartMonitoringCommand : ICommand
    {
        public Guid Id { get; } = Guid.NewGuid();
        public List<string> TrainIds { get; set; }
        public string UserId { get; set; }
        public string SessionId { get; set; }
    }

    public class DetectPriceChangeCommand : ICommand
    {
        public Guid Id { get; } = Guid.NewGuid();
        public string TrainId { get; set; }
        public decimal NewPrice { get; set; }
        public string SessionId { get; set; }
    }

    public class DetectAvailabilityChangeCommand : ICommand
    {
        public Guid Id { get; } = Guid.NewGuid();
        public string TrainId { get; set; }
        public bool NewAvailability { get; set; }
        public string Reason { get; set; }
        public string SessionId { get; set; }
    }

    public class StopMonitoringCommand : ICommand
    {
        public Guid Id { get; } = Guid.NewGuid();
        public string SessionId { get; set; }
        public string Reason { get; set; }
    }
}