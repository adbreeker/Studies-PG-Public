using changes_manager.Application.Handlers;
using changes_manager.Application.Commands;
using changes_manager.Application.Sagas;
using changes_manager.Infrastructure.EventStore;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Pattern-based services only
builder.Services.AddSingleton<IEventStore, InMemoryEventStore>();
builder.Services.AddScoped<ICommandHandler<StartMonitoringCommand>, StartMonitoringCommandHandler>();
builder.Services.AddScoped<ICommandHandler<DetectPriceChangeCommand>, DetectPriceChangeCommandHandler>();
builder.Services.AddScoped<ICommandHandler<DetectAvailabilityChangeCommand>, DetectAvailabilityChangeCommandHandler>();
builder.Services.AddScoped<ChangeProcessingSaga>();

// CORS
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowFrontend", policy =>
    {
        policy.WithOrigins("http://localhost:3000")
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseCors("AllowFrontend");
app.UseAuthorization();
app.MapControllers();

app.Run();