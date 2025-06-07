using account_manager.Application.Handlers;
using account_manager.Infrastructure;
using account_manager.Sagas;
using account_manager.Controllers;
using Microsoft.EntityFrameworkCore;

namespace account_manager
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

            // Configure PostgreSQL
            var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");
            builder.Services.AddDbContext<AccountDbContext>(options =>
                options.UseNpgsql(connectionString));

            // Register query handlers
            builder.Services.AddTransient<GetAllAccountsQueryHandler>();
            builder.Services.AddTransient<GetAccountQueryHandler>();

            // Register command handlers
            builder.Services.AddTransient<CreateAccountCommandHandler>();
            builder.Services.AddTransient<LoginCommandHandler>();
            builder.Services.AddTransient<DeleteAccountCommandHandler>();
            builder.Services.AddTransient<DeleteAllAccountsCommandHandler>();

            // Register sagas
            builder.Services.AddTransient<AccountCreationSaga>();

            // Register controllers
            builder.Services.AddTransient<AccountQueriesController>();
            builder.Services.AddTransient<AccountCommandsController>();

            // Configure CORS
            builder.Services.AddCors(options =>
            {
                options.AddPolicy("AllowAll", policy =>
                {
                    policy.AllowAnyOrigin()
                          .AllowAnyMethod()
                          .AllowAnyHeader();
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

            // Use CORS
            app.UseCors("AllowAll");

            app.UseAuthorization();
            app.MapControllers(); // Automatically maps AccountCommandsController and AccountQueriesController
            app.Run();
        }
    }
}
