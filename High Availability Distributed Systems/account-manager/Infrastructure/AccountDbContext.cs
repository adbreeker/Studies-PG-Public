using System.Runtime.CompilerServices;
using account_manager.Domain;
using Microsoft.EntityFrameworkCore;

namespace account_manager.Infrastructure
{
    public class AccountDbContext : DbContext
    {
        public DbSet<Account> Accounts { get; set; }

        public AccountDbContext(DbContextOptions<AccountDbContext> options) : base(options) { }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Account>()
                .HasIndex(a => a.Email)
                .IsUnique(); // Ensure unique emails
        }
    }

    public static class MigrationsExtensions
    {
        public static void ApplyMigrations(this IApplicationBuilder app)
        {
            using (var scope = app.ApplicationServices.CreateScope())
            {
                var dbContext = scope.ServiceProvider.GetRequiredService<AccountDbContext>();
                dbContext.Database.Migrate();
            }
        }
    }
}
