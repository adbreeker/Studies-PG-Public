# Use the official .NET 8 SDK image to build the application
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /app

# Copy the project file and restore dependencies
COPY analytics-service.csproj ./
RUN dotnet restore

# Copy the rest of the application files and build the project
COPY . ./
RUN dotnet publish -c Release -o out

# Use the official .NET 8 runtime image to run the application
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app
COPY --from=build /app/out ./

# Expose the ports the application will run on
EXPOSE 5223

# Set the entry point for the container
ENTRYPOINT ["dotnet", "analytics-service.dll"]
