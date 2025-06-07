using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace changes_manager.Domain.Models
{
    public class Change
    {
        [Key]
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        public Guid Id { get; set; }
        public required string Type { get; set; }
        public string TripId { get; set; } = string.Empty;
        public required string Details { get; set; }
        public DateTime Timestamp { get; set; }
        public decimal? OldPrice { get; set; }
        public decimal? NewPrice { get; set; }
        public bool? OldAvailability { get; set; }
        public bool? NewAvailability { get; set; }
    }
}