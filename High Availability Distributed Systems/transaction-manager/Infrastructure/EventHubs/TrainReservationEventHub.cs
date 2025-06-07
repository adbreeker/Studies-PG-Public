using System.Threading.Tasks;
using Microsoft.AspNetCore.SignalR;

namespace transaction_manager.Infrastructure.EventHubs
{
    public class TrainReservationEventHub : Hub
    {
        public async Task JoinTrainGroup(string trainId)
        {
            await Groups.AddToGroupAsync(Context.ConnectionId, $"Train_{trainId}");
            Console.WriteLine($"Client {Context.ConnectionId} joined group Train_{trainId}");
        }

        public async Task LeaveTrainGroup(string trainId)
        {
            await Groups.RemoveFromGroupAsync(Context.ConnectionId, $"Train_{trainId}");
            Console.WriteLine($"Client {Context.ConnectionId} left group Train_{trainId}");
        }

        public async Task SendReservationNotificationToTrain(string trainId, string message, string excludeConnectionId = null)
        {
            var group = Clients.Group($"Train_{trainId}");
            
            if (!string.IsNullOrEmpty(excludeConnectionId))
            {
                // Send to all in group except the specified connection
                await Clients.GroupExcept($"Train_{trainId}", excludeConnectionId)
                    .SendAsync("ReceiveReservationNotification", message);
            }
            else
            {
                // Send to all in group
                await group.SendAsync("ReceiveReservationNotification", message);
            }
        }

        public override async Task OnDisconnectedAsync(Exception exception)
        {
            // Groups are automatically cleaned up when connection is lost
            await base.OnDisconnectedAsync(exception);
        }
    }
}
