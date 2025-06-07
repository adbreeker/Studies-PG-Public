# Analytics Service - Train Reservation Analytics

## Overview

The Analytics Service is a real-time microservice component that provides insights into customer reservation preferences regarding departure directions in the train reservation system. It offers both REST API endpoints and real-time SignalR updates for live analytics dashboards.

## Features

### Core Functionality
- **Real-time Analytics**: Live updates via SignalR for departure direction preferences
- **Historical Data Analysis**: Query historical reservation patterns by time periods
- **Direction-based Insights**: Analyze customer preferences for travel directions (North, South, East, West, etc.)
- **Flexible Filtering**: Filter analytics by date ranges, departure stations, and aggregation periods
- **Background Data Sync**: Automatic synchronization with transaction-manager for up-to-date analytics

### Architecture
- **Domain-Driven Design**: Clean architecture with separate Domain, Application, and Infrastructure layers
- **Event-Driven**: SignalR hubs for real-time updates
- **Microservice Ready**: Containerized with Docker and ready for orchestration
- **Database Integration**: PostgreSQL with Entity Framework Core and JSONB support

## API Endpoints

### Health Check
```
GET /api/analytics/health
```
Returns service health status.

### Departure Direction Preferences
```
GET /api/analytics/departure-direction-preferences
```
Query parameters:
- `startDate` (optional): Filter from this date
- `endDate` (optional): Filter to this date  
- `limit` (optional): Limit number of results
- `departureStation` (optional): Filter by departure station

Returns aggregated data showing:
- Total reservations per direction
- Average price per direction
- Most popular routes
- Time period information

### Real-time Analytics
```
GET /api/analytics/real-time
```
Query parameters:
- `from` (optional): Start date for real-time data
- `to` (optional): End date for real-time data
- `groupBy` (optional): Grouping strategy

Returns current analytics state including:
- Total reservations count
- Active analytics sessions
- Last update timestamp

## SignalR Hub

### Analytics Hub
**Endpoint**: `/analyticsHub`

**Events**:
- `AnalyticsUpdated`: Broadcasts when new analytics data is available
- `DeparturePreferencesUpdated`: Broadcasts when departure preferences change

**Usage**: Connect to receive real-time updates for dashboard applications.

## Database Schema

### ReservationAnalytics Table
```sql
CREATE TABLE ReservationAnalytics (
    Id SERIAL PRIMARY KEY,
    AccountId INT NOT NULL,
    TrainId INT NOT NULL,
    DepartureStation VARCHAR NOT NULL,
    ArrivalStation VARCHAR NOT NULL,
    DepartureDirection VARCHAR,
    DepartureDate TIMESTAMP NOT NULL,
    ArrivalDate TIMESTAMP NOT NULL,
    Price DECIMAL,
    TrainCars JSONB,
    CreatedAt TIMESTAMP NOT NULL
);
```

**Indexes**:
- `IX_ReservationAnalytics_DepartureStation`
- `IX_ReservationAnalytics_ArrivalStation` 
- `IX_ReservationAnalytics_DepartureDate`
- `IX_ReservationAnalytics_CreatedAt`
- `IX_ReservationAnalytics_DepartureStation_ArrivalStation`

## Configuration

### Environment Variables
- `ASPNETCORE_ENVIRONMENT`: Development/Production
- `ASPNETCORE_HTTP_PORTS`: Port to listen on (default: 5223)
- `ConnectionStrings__DefaultConnection`: PostgreSQL connection string
- `TransactionManagerApiUrl`: URL of the transaction manager service

### appsettings.json
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*",
  "TransactionManagerApiUrl": "http://localhost:5221"
}
```

## Development Setup

### Prerequisites
- .NET 8.0 SDK
- PostgreSQL 15+
- Docker (for containerization)

### Local Development
1. **Setup Database**:
   ```bash
   # Update connection string in appsettings.Development.json
   dotnet ef database update
   ```

2. **Run Service**:
   ```bash
   dotnet run --urls "http://localhost:5223"
   ```

3. **Test Endpoints**:
   ```bash
   # Health check
   curl http://localhost:5223/api/analytics/health
   
   # Get departure preferences
   curl http://localhost:5223/api/analytics/departure-direction-preferences
   
   # Get real-time analytics
   curl http://localhost:5223/api/analytics/real-time
   ```

### Docker Deployment
```bash
# Build image
docker build -t analytics-service .

# Run container
docker run -p 5223:5223 -e ConnectionStrings__DefaultConnection="Host=postgres;Port=5432;Database=mydb;Username=admin;Password=adminpass" analytics-service
```

## Integration with Frontend

The service integrates with a React frontend that provides:

### Analytics Dashboard Features
- **Real-time Statistics**: Live counters for total reservations and active sessions
- **Interactive Filters**: Date ranges, time periods (daily/weekly/monthly)
- **Visual Direction Cards**: Each direction displayed with icons and statistics
- **Progress Indicators**: Visual representation of preference distribution
- **Connection Status**: Real-time connection indicator

### Frontend Components
- `AnalyticsPage.jsx`: Main analytics dashboard
- SignalR integration for real-time updates
- Responsive CSS with modern design
- Error handling and loading states

## Background Services

### ReservationSyncService
- **Purpose**: Synchronizes reservation data from transaction-manager
- **Frequency**: Configurable interval (default: every 30 seconds)
- **Data Processing**: Converts reservation data to analytics format
- **Direction Calculation**: Determines travel direction based on station coordinates

### Current Implementation
The service currently includes simulated data generation for demonstration purposes. In production, it would:
1. Fetch actual reservation data from transaction-manager API
2. Process and analyze the data for direction preferences
3. Store analytics in the database
4. Broadcast updates via SignalR

## Docker Compose Integration

The service is integrated into the main docker-compose.yml:

```yaml
analytics-service:
  container_name: analytics-service
  build:
    context: ./analytics-service
  ports:
    - "5223:5223"
  environment:
    - ASPNETCORE_ENVIRONMENT=Development
    - ASPNETCORE_HTTP_PORTS=5223
    - ConnectionStrings__DefaultConnection=Host=postgres;Port=5432;Database=mydb;Username=admin;Password=adminpass
    - TransactionManagerApiUrl=http://transaction-manager:5221
  depends_on:
    - postgres
    - transaction-manager
  networks:
    - app-network
  restart: unless-stopped
```

## Monitoring and Health

### Health Check Endpoint
The service provides a health check endpoint that returns:
```json
{
  "Status": "Healthy",
  "Service": "Analytics Service", 
  "Timestamp": "2025-06-02T21:00:00.000Z"
}
```

### Logging
- **Application Logs**: Structured logging with different log levels
- **Entity Framework Logs**: Database query logging in development
- **SignalR Logs**: Connection and hub activity logs
- **Background Service Logs**: Sync service activity logs

## Future Enhancements

### Planned Features
1. **Advanced Analytics**: More sophisticated statistical analysis
2. **Caching Layer**: Redis integration for improved performance
3. **Machine Learning**: Predictive analytics for demand forecasting
4. **Export Capabilities**: CSV/Excel export of analytics data
5. **Advanced Filtering**: More granular filtering options
6. **Real-time Alerts**: Configurable alerts for unusual patterns

### Performance Optimizations
1. **Database Indexing**: Additional indexes for complex queries
2. **Query Optimization**: Materialized views for common analytics
3. **Connection Pooling**: Optimized database connections
4. **SignalR Scaling**: Redis backplane for multi-instance deployments

## Security Considerations

- **CORS Configuration**: Proper cross-origin resource sharing setup
- **Input Validation**: Parameter validation for all endpoints
- **Connection Security**: Secure SignalR connections
- **Database Security**: Parameterized queries to prevent SQL injection

## Testing

### Unit Tests
- Domain model tests
- Handler logic tests
- Service behavior tests

### Integration Tests
- API endpoint tests
- Database integration tests
- SignalR hub tests

### Performance Tests
- Load testing for high-volume scenarios
- SignalR connection scaling tests

## Troubleshooting

### Common Issues
1. **Database Connection**: Verify PostgreSQL is running and connection string is correct
2. **Port Conflicts**: Ensure port 5223 is available
3. **CORS Errors**: Check frontend URL is in allowed origins
4. **SignalR Connection**: Verify WebSocket support and proxy configuration

### Debug Commands
```bash
# Check service status
curl http://localhost:5223/api/analytics/health

# View logs
docker logs analytics-service

# Database connection test
dotnet ef database update --verbose
```

## Contributing

1. Follow .NET coding standards
2. Add unit tests for new features
3. Update API documentation
4. Test SignalR integration
5. Verify Docker build works

## License

This project is part of the train reservation system microservices architecture.
