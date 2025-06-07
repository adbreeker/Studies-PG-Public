using analytics_service.Infrastructure;
using analytics_service.Controllers;
using analytics_service.Application.Handlers;
using analytics_service.Hubs;
using analytics_service.Services;
using Microsoft.EntityFrameworkCore;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace analytics_service
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);            // Add services to the container.
            builder.Services.AddControllers()
                .AddJsonOptions(options =>
                {
                    options.JsonSerializerOptions.PropertyNamingPolicy = JsonNamingPolicy.CamelCase;
                    options.JsonSerializerOptions.WriteIndented = false;
                    // Configure DateTime serialization to use ISO format
                    options.JsonSerializerOptions.Converters.Add(new JsonStringEnumConverter());
                });
            builder.Services.AddEndpointsApiExplorer();
            builder.Services.AddSwaggerGen();

            // Configure PostgreSQL
            var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");
            builder.Services.AddDbContext<AnalyticsDbContext>(options =>
                options.UseNpgsql(connectionString));

            // Register query handlers
            builder.Services.AddTransient<GetDepartureDirectionPreferencesQueryHandler>();
            builder.Services.AddTransient<GetRealTimeAnalyticsQueryHandler>();            // Add HTTP Client for transaction-manager integration
            builder.Services.AddHttpClient("TransactionManager", client =>
            {
                var transactionManagerUrl = builder.Configuration.GetValue<string>("TransactionManagerUrl") ?? "http://localhost:5221";
                client.BaseAddress = new Uri(transactionManagerUrl);
                client.Timeout = TimeSpan.FromSeconds(30);
            });

            // Register controllers
            builder.Services.AddTransient<AnalyticsQueriesController>();

            // Register background services
            builder.Services.AddHostedService<ReservationSyncService>();            // Add SignalR for real-time updates
            builder.Services.AddSignalR()
                .AddJsonProtocol(options =>
                {
                    options.PayloadSerializerOptions.PropertyNamingPolicy = JsonNamingPolicy.CamelCase;
                    options.PayloadSerializerOptions.WriteIndented = false;
                    options.PayloadSerializerOptions.Converters.Add(new JsonStringEnumConverter());
                });// Configure CORS
            var allowedOrigins = builder.Configuration.GetValue<string>("CORS_ALLOWED_ORIGINS") ?? 
                    "http://localhost:18942,http://localhost:3000";

            builder.Services.AddCors(options =>
            {
                options.AddPolicy("AllowSignalR", policy =>
                {
                    policy.WithOrigins(allowedOrigins.Split(',', StringSplitOptions.RemoveEmptyEntries))
                          .AllowAnyMethod()
                          .AllowAnyHeader()
                          .AllowCredentials();
                });
            });

            var app = builder.Build();

            // Configure the HTTP request pipeline.
            if (app.Environment.IsDevelopment())
            {
                app.UseSwagger();
                app.UseSwaggerUI();
                app.ApplyMigrations();
            }

            app.UseHttpsRedirection();            // Use CORS
            app.UseCors("AllowSignalR");

            app.UseAuthorization();
            app.MapControllers();
            
            // Map SignalR Hub with CORS
            app.MapHub<AnalyticsHub>("/analyticsHub");
            
            app.Run();
        }
    }

    // Extension method for applying migrations
    public static class ApplicationBuilderExtensions
    {
        public static void ApplyMigrations(this WebApplication app)
        {
            using var scope = app.Services.CreateScope();
            var context = scope.ServiceProvider.GetRequiredService<AnalyticsDbContext>();
            context.Database.Migrate();
        }
    }
}
