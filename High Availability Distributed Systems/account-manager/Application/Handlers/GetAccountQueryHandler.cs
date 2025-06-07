using account_manager.Application.Queries;
using account_manager.Domain;
using account_manager.Infrastructure;
using Microsoft.EntityFrameworkCore;

namespace account_manager.Application.Handlers
{
    public class GetAccountQueryHandler
    {
        private readonly AccountDbContext _dbContext;

        public GetAccountQueryHandler(AccountDbContext dbContext)
        {
            _dbContext = dbContext;
        }

        public async Task<Account?> Handle(GetAccountQuery query)
        {
            return await _dbContext.Accounts
                .FirstOrDefaultAsync(a => a.Id == query.AccountId);
        }
    }
}
