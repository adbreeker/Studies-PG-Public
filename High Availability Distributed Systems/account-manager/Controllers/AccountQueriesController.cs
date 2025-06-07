using account_manager.Application.Handlers;
using account_manager.Application.Queries;
using Microsoft.AspNetCore.Mvc;

namespace account_manager.Controllers
{
    [ApiController]
    [Route("api/account/queries")]
    public class AccountQueriesController : ControllerBase
    {
        private readonly GetAllAccountsQueryHandler _getAllAccountsQueryHandler;
        private readonly GetAccountQueryHandler _getAccountQueryHandler;

        public AccountQueriesController(
            GetAllAccountsQueryHandler getAllAccountsQueryHandler,
            GetAccountQueryHandler getAccountQueryHandler)
        {
            _getAllAccountsQueryHandler = getAllAccountsQueryHandler;
            _getAccountQueryHandler = getAccountQueryHandler;
        }

        [HttpGet("all")]
        public async Task<IActionResult> GetAllAccounts()
        {
            var accounts = await _getAllAccountsQueryHandler.Handle();
            return Ok(accounts);
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> GetAccount(Guid id)
        {
            var account = await _getAccountQueryHandler.Handle(new GetAccountQuery { AccountId = id });

            if (account == null)
            {
                return NotFound("Account not found.");
            }

            return Ok(account);
        }
    }
}
