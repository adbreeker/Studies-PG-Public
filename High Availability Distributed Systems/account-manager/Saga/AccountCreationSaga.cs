using account_manager.Application.Commands;
using account_manager.Application.Handlers;

namespace account_manager.Sagas
{
    public class AccountCreationSaga
    {
        private readonly CreateAccountCommandHandler _commandHandler;

        public AccountCreationSaga(CreateAccountCommandHandler commandHandler)
        {
            _commandHandler = commandHandler;
        }

        public async Task<string> Start(CreateAccountCommand command)
        {
            // Saga step 1: Create account
            return await _commandHandler.Handle(command);
        }
    }
}

