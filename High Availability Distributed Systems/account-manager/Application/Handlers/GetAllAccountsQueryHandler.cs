using account_manager.Domain;
using account_manager.Infrastructure;
using Microsoft.EntityFrameworkCore;

namespace account_manager.Application.Handlers
{
    public class GetAllAccountsQueryHandler
    {
        private readonly AccountDbContext _dbContext;

        public GetAllAccountsQueryHandler(AccountDbContext dbContext)
        {
            _dbContext = dbContext;
        }

        public async Task<List<Account>> Handle()
        {
            return await _dbContext.Accounts.ToListAsync();
        }
    }
}
