using Microsoft.EntityFrameworkCore;
using transaction_manager.Infrastructure;
using transaction_manager.Application.Handlers;
using transaction_manager.Saga;
using transaction_manager.Controllers;
using transaction_manager.Infrastructure.EventHubs;

namespace transaction_manager
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);

            // Add services to the container.
            builder.Services.AddControllers();
            builder.Services.AddEndpointsApiExplorer();
            builder.Services.AddSwaggerGen();
            builder.Services.AddSignalR();

            // Configure PostgreSQL
            var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");
            builder.Services.AddDbContext<ReservationDbContext>(options =>
                options.UseNpgsql(connectionString));

            // Register query handlers
            builder.Services.AddTransient<GetAllReservationsQueryHandler>();
            builder.Services.AddTransient<GetReservationByIdQueryHandler>();
            builder.Services.AddTransient<GetReservationsByAccountQueryHandler>();
            builder.Services.AddTransient<GetReservedTrainCarsQueryHandler>();

            // Register command handlers
            builder.Services.AddTransient<CreateReservationCommandHandler>();
            builder.Services.AddTransient<DeleteReservationCommandHandler>();
            builder.Services.AddTransient<DeleteAllReservationsCommandHandler>();

            // Register sagas
            builder.Services.AddTransient<ReservationCreationSaga>();

            // Register controllers
            builder.Services.AddTransient<ReservationCommandsController>();
            builder.Services.AddTransient<ReservationQueriesController>();

            // Configure CORS for SignalR
            var allowedOrigins = builder.Configuration.GetValue<string>("CORS_ALLOWED_ORIGINS");
            Console.WriteLine($"CORS_ALLOWED_ORIGINS: {allowedOrigins}");
            
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

            app.UseHttpsRedirection();

            // Use CORS before mapping hubs
            app.UseCors("AllowSignalR");

            app.UseAuthorization();
            app.MapControllers();

            // Map SignalR hub
            app.MapHub<TrainReservationEventHub>("api/trainReservationEventHub");

            app.Run();
        }
    }
}
