using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace analytics_service.Migrations
{
    /// <inheritdoc />
    public partial class InitialCreate : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "ReservationAnalytics",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "uuid", nullable: false),
                    AccountId = table.Column<string>(type: "text", nullable: false),
                    TrainId = table.Column<string>(type: "text", nullable: false),
                    DepartureDate = table.Column<DateTime>(type: "timestamp with time zone", nullable: false),
                    DepartureStation = table.Column<string>(type: "text", nullable: false),
                    ArrivalDate = table.Column<DateTime>(type: "timestamp with time zone", nullable: false),
                    ArrivalStation = table.Column<string>(type: "text", nullable: false),
                    TrainCars = table.Column<string>(type: "jsonb", nullable: false),
                    CreatedAt = table.Column<DateTime>(type: "timestamp with time zone", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_ReservationAnalytics", x => x.Id);
                });

            migrationBuilder.CreateIndex(
                name: "IX_ReservationAnalytics_ArrivalStation",
                table: "ReservationAnalytics",
                column: "ArrivalStation");

            migrationBuilder.CreateIndex(
                name: "IX_ReservationAnalytics_CreatedAt",
                table: "ReservationAnalytics",
                column: "CreatedAt");

            migrationBuilder.CreateIndex(
                name: "IX_ReservationAnalytics_DepartureDate",
                table: "ReservationAnalytics",
                column: "DepartureDate");

            migrationBuilder.CreateIndex(
                name: "IX_ReservationAnalytics_DepartureStation",
                table: "ReservationAnalytics",
                column: "DepartureStation");

            migrationBuilder.CreateIndex(
                name: "IX_ReservationAnalytics_DepartureStation_ArrivalStation",
                table: "ReservationAnalytics",
                columns: new[] { "DepartureStation", "ArrivalStation" });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "ReservationAnalytics");
        }
    }
}
