using account_manager.Domain;
using account_manager.Application.Commands;
using account_manager.Infrastructure;
using Microsoft.EntityFrameworkCore;

namespace account_manager.Application.Handlers
{
    public class CreateAccountCommandHandler
    {
        private readonly AccountDbContext _dbContext;

        public CreateAccountCommandHandler(AccountDbContext dbContext)
        {
            _dbContext = dbContext;
        }

        public async Task<string> Handle(CreateAccountCommand command)
        {
            // Check if the account already exists
            var existingAccount = await _dbContext.Accounts
                .FirstOrDefaultAsync(a => a.Email == command.Email);

            if (existingAccount != null)
            {
                return "Account with the same email already exists.";
            }

            // Create a new account
            var account = new Account(Guid.NewGuid(), command.Email, command.Password);
            _dbContext.Accounts.Add(account);
            await _dbContext.SaveChangesAsync();

            return "Account created successfully.";
        }
    }
}

