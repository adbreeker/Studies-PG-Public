using Microsoft.EntityFrameworkCore;
using analytics_service.Domain;
using System.Text.Json;

namespace analytics_service.Infrastructure
{
    public class AnalyticsDbContext : DbContext
    {
        public AnalyticsDbContext(DbContextOptions<AnalyticsDbContext> options) : base(options)
        {
        }

        public DbSet<ReservationAnalytics> ReservationAnalytics { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Configure ReservationAnalytics entity
            modelBuilder.Entity<ReservationAnalytics>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.AccountId).IsRequired();
                entity.Property(e => e.TrainId).IsRequired();
                entity.Property(e => e.DepartureStation).IsRequired();
                entity.Property(e => e.ArrivalStation).IsRequired();
                entity.Property(e => e.DepartureDate).IsRequired();
                entity.Property(e => e.ArrivalDate).IsRequired();
                entity.Property(e => e.CreatedAt).IsRequired();
                
                // Configure TrainCars as JSON column
                entity.Property(e => e.TrainCars)
                    .HasConversion(
                        v => JsonSerializer.Serialize(v, (JsonSerializerOptions?)null),
                        v => JsonSerializer.Deserialize<List<int>>(v, (JsonSerializerOptions?)null) ?? new List<int>())
                    .HasColumnType("jsonb");

                // Add indexes for better query performance
                entity.HasIndex(e => e.DepartureStation);
                entity.HasIndex(e => e.ArrivalStation);
                entity.HasIndex(e => e.DepartureDate);
                entity.HasIndex(e => e.CreatedAt);
                entity.HasIndex(e => new { e.DepartureStation, e.ArrivalStation });
            });
        }
    }
}
