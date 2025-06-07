using account_manager.Application.Commands;
using account_manager.Infrastructure;
using Microsoft.EntityFrameworkCore;

namespace account_manager.Application.Handlers
{
    public class DeleteAccountCommandHandler
    {
        private readonly AccountDbContext _dbContext;

        public DeleteAccountCommandHandler(AccountDbContext dbContext)
        {
            _dbContext = dbContext;
        }

        public async Task<string> Handle(DeleteAccountCommand command)
        {
            var account = await _dbContext.Accounts.FirstOrDefaultAsync(a => a.Id == command.AccountId);

            if (account == null)
            {
                return "Account not found.";
            }

            _dbContext.Accounts.Remove(account);
            await _dbContext.SaveChangesAsync();

            return "Account deleted successfully.";
        }
    }
}
