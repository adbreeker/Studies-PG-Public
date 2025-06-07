using account_manager.Application.Commands;
using account_manager.Infrastructure;
using Microsoft.EntityFrameworkCore;

namespace account_manager.Application.Handlers
{
    public class LoginCommandHandler
    {
        private readonly AccountDbContext _dbContext;

        public LoginCommandHandler(AccountDbContext dbContext)
        {
            _dbContext = dbContext;
        }

        public async Task<(bool Success, string Message, Guid? AccountId)> Handle(LoginCommand command)
        {
            // Check if the account exists
            var account = await _dbContext.Accounts
                .FirstOrDefaultAsync(a => a.Email == command.Email);

            if (account == null)
            {
                return (false, "Invalid email or password.", null);
            }

            // Validate the password (for simplicity, assuming plain text comparison)
            if (account.Password != command.Password)
            {
                return (false, "Invalid email or password.", null);
            }

            // Return success with the account ID
            return (true, "Login successful.", account.Id);
        }
    }
}
