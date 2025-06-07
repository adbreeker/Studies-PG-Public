using Microsoft.EntityFrameworkCore;
using transaction_manager.Domain;
using System.Runtime.CompilerServices;

namespace transaction_manager.Infrastructure
{
    public class ReservationDbContext : DbContext
    {
        public DbSet<Reservation> Reservations { get; set; }

        public ReservationDbContext(DbContextOptions<ReservationDbContext> options) : base(options) { }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {

        }
    }

    public static class MigrationsExtensions
    {
        public static void ApplyMigrations(this IApplicationBuilder app)
        {
            using (var scope = app.ApplicationServices.CreateScope())
            {
                var dbContext = scope.ServiceProvider.GetRequiredService<ReservationDbContext>();
                dbContext.Database.Migrate();
            }
        }
    }
}
