using account_manager.Application.Commands;
using account_manager.Infrastructure;

namespace account_manager.Application.Handlers
{
    public class DeleteAllAccountsCommandHandler
    {
        private readonly AccountDbContext _dbContext;

        public DeleteAllAccountsCommandHandler(AccountDbContext dbContext)
        {
            _dbContext = dbContext;
        }

        public async Task<string> Handle(DeleteAllAccountsCommand command)
        {
            _dbContext.Accounts.RemoveRange(_dbContext.Accounts);
            await _dbContext.SaveChangesAsync();

            return "All accounts deleted successfully.";
        }
    }
}
