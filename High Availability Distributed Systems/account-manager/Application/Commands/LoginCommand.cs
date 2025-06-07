namespace account_manager.Application.Commands
{
    public class LoginCommand
    {
        public required string Email { get; set; }
        public required string Password { get; set; }
    }
}
