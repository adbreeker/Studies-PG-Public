namespace account_manager.Domain
{
    public class Account
    {
        public Guid Id { get; private set; }
        public string Email { get; private set; }
        public string Password { get; private set; }
        public bool IsActive { get; private set; }

        private Account()
        {
            Email = string.Empty;
            Password = string.Empty;
        }

        public Account(Guid id, string email, string password)
        {
            Id = id;
            Email = email;
            Password = password;
            IsActive = true;
        }

        public void Deactivate()
        {
            IsActive = false;
        }
    }
}
