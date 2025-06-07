using account_manager.Application.Commands;
using account_manager.Application.Handlers;
using account_manager.Sagas;
using Microsoft.AspNetCore.Mvc;

namespace account_manager.Controllers
{
    [ApiController]
    [Route("api/account/commands")]
    public class AccountCommandsController : ControllerBase
    {
        private readonly AccountCreationSaga _accountCreationSaga;
        private readonly DeleteAccountCommandHandler _deleteAccountCommandHandler;
        private readonly DeleteAllAccountsCommandHandler _deleteAllAccountsCommandHandler;
        private readonly LoginCommandHandler _loginCommandHandler;

        public AccountCommandsController(
            AccountCreationSaga accountCreationSaga,
            DeleteAccountCommandHandler deleteAccountCommandHandler,
            DeleteAllAccountsCommandHandler deleteAllAccountsCommandHandler,
            LoginCommandHandler loginCommandHandler)
        {
            _accountCreationSaga = accountCreationSaga;
            _deleteAccountCommandHandler = deleteAccountCommandHandler;
            _deleteAllAccountsCommandHandler = deleteAllAccountsCommandHandler;
            _loginCommandHandler = loginCommandHandler;
        }

        [HttpPost("create")]
        public async Task<IActionResult> CreateAccount([FromBody] CreateAccountCommand command)
        {
            var result = await _accountCreationSaga.Start(command);

            if (result == "Account created successfully.")
            {
                return Ok(result);
            }

            return BadRequest(result);
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteAccount(Guid id)
        {
            var result = await _deleteAccountCommandHandler.Handle(new DeleteAccountCommand { AccountId = id });

            if (result == "Account deleted successfully.")
            {
                return Ok(result);
            }

            return NotFound(result);
        }

        [HttpDelete("all")]
        public async Task<IActionResult> DeleteAllAccounts()
        {
            var result = await _deleteAllAccountsCommandHandler.Handle(new DeleteAllAccountsCommand());
            return Ok(result);
        }

        [HttpPost("login")]
        public async Task<IActionResult> Login([FromBody] LoginCommand command)
        {
            var (success, message, accountId) = await _loginCommandHandler.Handle(command);

            if (success)
            {
                return Ok(new { Message = message, AccountId = accountId });
            }

            return Unauthorized(new { Message = message });
        }
    }
}
