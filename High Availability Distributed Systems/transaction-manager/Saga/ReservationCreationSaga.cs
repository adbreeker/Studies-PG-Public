using Microsoft.AspNetCore.SignalR;
using transaction_manager.Application.Commands;
using transaction_manager.Application.Handlers;
using transaction_manager.Domain;
using transaction_manager.Infrastructure.EventHubs;

namespace transaction_manager.Saga
{
    public class ReservationCreationSaga
    {
        private readonly CreateReservationCommandHandler _commandHandler;
        private readonly IHubContext<TrainReservationEventHub> _trainReservationHubContext;

        public ReservationCreationSaga(CreateReservationCommandHandler commandHandler, IHubContext<TrainReservationEventHub> trainReservationHubContext)
        {
            _commandHandler = commandHandler;
            _trainReservationHubContext = trainReservationHubContext;
        }

        public async Task<string> Start(CreateReservationCommand command, string excludeConnectionId = null)
        {
            // Step 1: Create a reservation
            string commandResult = await _commandHandler.Handle(command);

            // Step 2: Notify the event hub about the reservation creation
            if (commandResult == "Reservation created successfully.")
            {
                string message = $"Train car(s) {string.Join(", ", command.TrainCars)} reserved by some other user";
                
                // Send notification only to clients viewing the same train, excluding the sender
                await _trainReservationHubContext.Clients.GroupExcept($"Train_{command.TrainId}", excludeConnectionId ?? "")
                    .SendAsync("ReceiveReservationNotification", message);
                
                Console.WriteLine($"Reservation notification sent to Train_{command.TrainId} group (excluding {excludeConnectionId})");
            }
            
            // Step 3: Return the result of the command
            return commandResult;
        }
    }
}
