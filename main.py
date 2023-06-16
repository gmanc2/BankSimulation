class BankAccount:
    def __init__(self, account_number, balance=0):
        self.account_number = account_number  # initialize accouont number
        self.balance = balance  # initalize balance

    def deposit(self, amount):  # deposit function (add money)
        self.balance += amount  # balance =  balance plus amount to add

    def withdraw(self, amount):  # withdraw function with overdraft check
        if self.balance >= amount:  # if balance is > amount to withdrawal continue
            self.balance -= amount  # subtract money from balance
        else:  # else insufficient funds
            raise ValueError("Insufficient funds.")

    def transfer(self, amount, account):  # transfer function
        self.withdraw(amount)  # withdraw the amount from the chosen account number
        account.deposit(amount)  # deposit those funds into the chosen account number

    def get_balance(self):  # simply return the balance for the selected account number
        return self.balance


class Checking(BankAccount):  # checking account class
    def __init__(self, account_number, balance=0, overdraft_limit=0):  # init params for the checking account
        super().__init__(account_number, balance)  # inherit the properties of BankAccount
        self.overdraft_limit = overdraft_limit  # set the overdraft limit of the account

    def withdraw(self, amount):  # withdraw function
        if self.balance + self.overdraft_limit >= amount:  # check if balance is > the overdraft limit + the amount
            self.balance -= amount  # set the new balance
        else:  # else handle insufficient funds
            raise ValueError("Insufficient funds.")

    def set_overdraft_limit(self, overdraft_limit):  # function to set the new overdraft limit
        self.overdraft_limit = overdraft_limit


class Savings(BankAccount):  # savings account class
    def __init__(self, account_number, balance=0, interest_rate=0.01):  # init the params for the savings account
        super().__init__(account_number, balance)  # init the properties of BankAccount
        self.interest_rate = interest_rate  # set the interest rate

    def add_interest(self):  # function to add interest over time (doesn't do anything in this case as time is not
        # taken into account for now)
        interest = self.balance * self.interest_rate  # interest rerun = balance * interest rate
        self.balance += interest


class Bank:  # bank class
    def __init__(self, name):  # intialize bank
        self.name = name  # set name
        self.accounts = {}  # set accounts dict

    def create_account(self, account_type, account_number, balance=0, **kwargs):  # create account with addition args
        try:
            if account_number in self.accounts:  # check if account exists
                raise ValueError("Account already exists.")
            if account_type == "checking":
                account = Checking(account_number, balance, **kwargs)  # add checking account to dict
            elif account_type == "savings":
                account = Savings(account_number, balance, **kwargs)  # add savings account to dict
            else:  # handle errors
                raise ValueError("Invalid account type.")
            self.accounts[account_number] = account
        except ValueError as e:
            print(e)

    def get_account(self, account_number):  # get the specified account
        try:
            return self.accounts[account_number]
        except KeyError:
            print("Account not found.")

    def get_all_accounts(self):  # get all the accounts
        return self.accounts.values()


class Admin:
    def __init__(self, username, password, bank):  # intialize the admin with the parameters
        self.username = username  # set the username
        self.password = password  # set the password
        self.bank = bank  # set the bank

    def create_account(self, account_type, account_number, balance, interest_rate=None,
                       overdraft_limit=None):  # create an account with the associated parameters
        try:
            if account_type.lower() == "checking":
                account = Checking(account_number, balance, overdraft_limit=overdraft_limit)
                self.bank.create_account(account_type, account_number, balance, overdraft_limit=overdraft_limit)
            elif account_type.lower() == "savings":
                account = Savings(account_number, balance, interest_rate=interest_rate)
                if interest_rate is not None and not (
                        0.0 <= interest_rate <= 1.0):  # check to ensure interest rate make sense (today it should be more like 0 to 0.0001)
                    raise ValueError("Interest rate must be between 0.0 and 1.0.")
                self.bank.create_account(account_type, account_number, balance, interest_rate=interest_rate)
            else:
                raise ValueError("Invalid account type.")  # handle errors
        except ValueError as e:
            print(e)

    def set_overdraft_limit(self, account_number, overdraft_limit):  # set the over draft limit
        account = self.bank.get_account(account_number)
        try:
            if account:
                if isinstance(account, Checking):
                    account.set_overdraft_limit(overdraft_limit)
                else:  # handle invalid accounts
                    raise ValueError("Invalid account type.")
            else:  # handle no accounts found
                raise ValueError("Account not found.")
        except ValueError as e:
            print(e)


class Customer:  # customer class
    def __init__(self, username, password, bank):  # intialize the customer with the parameters
        self.username = username  # inti username
        self.password = password  # inti password
        self.bank = bank  # inti bank
        self.account = None  # init account

    def create_account(self, account_type, account_number, balance=0, **kwargs):  # create account same as admin
        self.bank.create_account(account_type, account_number, balance, **kwargs)

    def access_account(self,
                       account_number):  # access the account number (does not handle if it's someone else's account)
        account = self.bank.get_account(account_number)
        if account:
            self.account = account
        else:  # handle not found error
            raise ValueError("Account not found.")

    def deposit(self, amount):  # simple deposit money
        if self.account:
            self.account.deposit(amount)
        else:  # handle if they haven't chosen access_account yet
            raise ValueError("No account selected.")

    def withdraw(self, amount):  # simple withdraw of money
        if self.account:
            self.account.withdraw(amount)
        else:  # handle if they haven't chosen access_account yet
            raise ValueError("No account selected.")

    def transfer(self, amount, account_number):  # handle the transfer of money between customer accounts
        if self.account:
            account = self.bank.get_account(account_number)
            if account:
                self.account.transfer(amount, account)
            else:  # handle if the chosen account is not found
                raise ValueError("Account not found.")
        else:  # handle if they haven't chosen access_account yet
            raise ValueError("No account selected.")

    def check_balance(self):
        if self.account:
            return self.account.get_balance()
        else:  # handle if they haven't chosen access_account yet
            raise ValueError("No account selected.")


class BankSystem:  # the main bank system
    def __init__(self):
        self.bank = Bank("Big Glenn's Bank")  # create the bank
        self.admin = Admin("glenn", "securepassword", self.bank)  # create the administrator account
        self.customers = {}  # create the customer dict

    def admin_login(self, username, password):  # handle the admins login
        if username == self.admin.username and password == self.admin.password:  # get input of username and password and check them agains the stored username and password
            return self.admin
        else:
            raise ValueError("Invalid credentials.")  # return invalid credentials

    def customer_login(self, username, password):  # handle the customer login
        if username in self.customers and self.customers[
            username].password == password:  # get input of username and password and check them agains the stored username and password
            return self.customers[username]
        else:
            raise ValueError("Invalid credentials.")  # return invalid credentials

    def create_customer(self, username, password):  # create customer function
        if username in self.customers:  # check if the username exists already
            raise ValueError("Username already exists.")
        self.customers[username] = Customer(username, password, self.bank)  # otherwise create the account


def main():
    bank_system = BankSystem()  # create an instance of BankSystem

    while True:  # simple main menu
        print(f"\nWelcome to {bank_system.bank.name}!")
        print("1. Admin Login")
        print("2. Customer Login")
        print("3. Create Customer Account")
        print("4. Exit")

        choice = int(input("Enter your choice: "))  # get input

        if choice == 1:
            username = input("Enter your username: ")  # get username
            password = input("Enter your password: ")  # get password

            try:  # try the login and check it
                admin = bank_system.admin_login(username, password)  # use admin_login to login with params
            except ValueError as e:
                print(e)
                continue

            while True:  # simple admin panel
                print("\nAdmin Options:")
                print("1. Create Account")
                print("2. Set Overdraft Limit")
                print("3. View All Accounts")
                print("4. Logout")

                admin_choice = int(input("Enter your choice: "))  # get choice

                if admin_choice == 1:  # create the new account
                    account_type = input("Enter the account type (checking/savings): ")
                    account_number = input("Enter the account number: ")
                    balance = float(input("Enter the starting balance: "))

                    if account_type == "checking":  # if checking create it
                        overdraft_limit = float(input("Enter the overdraft limit: "))  # set the overdraft on checking
                        admin.create_account(account_type, account_number, balance,
                                             overdraft_limit=overdraft_limit)  # use admin.create_account to create the account with the params
                    elif account_type == "savings":
                        interest_rate = float(
                            input("Enter the interest rate: "))  # set he interest rate errors handled earlier
                        admin.create_account(account_type, account_number, balance,
                                             interest_rate=interest_rate)  # use admin.create_account to create the account with the params
                    else:  # handle invalid account types
                        print("Invalid account type.")


                elif admin_choice == 2:  # set the overdraft limit
                    account_number = input("Enter the account number: ")
                    overdraft_limit = float(input("Enter the overdraft limit: "))
                    admin.set_overdraft_limit(account_number,
                                              overdraft_limit)  # use the admin.set_overdraft_limit to set the overdraft limit with the params

                elif admin_choice == 3:  # get all the current accounts
                    accounts = bank_system.bank.get_all_accounts()
                    for account in accounts:
                        if isinstance(account, Checking):
                            account_type = "Checking"
                            overdraft_limit = account.overdraft_limit  # set the overdraft limit for checking account
                        elif isinstance(account,
                                        Savings):  # set the overdraft limit to N/A since savings accounts dont have overdrafts
                            account_type = "Savings"
                            overdraft_limit = "N/A"
                        else:  # encase any other accounts were in the mix (I was gonna add a file)
                            account_type = "Unknown"
                            overdraft_limit = "N/A"
                        print(
                            f"Account Number: {account.account_number}, Balance: {account.get_balance()}, Type: {type(account).__name__}, Overdraft Limit: {overdraft_limit}")  # print all the accounts

                elif admin_choice == 4:  # return
                    break

        elif choice == 2:  # simple customer login
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            try:  # try the login and check it
                customer = bank_system.customer_login(username, password)  # use the customer_login to login with params

            except ValueError as e:
                print(e)
                continue

            while True:  # customer panel

                print("\nCustomer Options:")
                print("1. Create Account")
                print("2. Access Account")
                print("3. Deposit")
                print("4. Withdraw")
                print("5. Transfer")
                print("6. Check Balance")
                print("7. Logout")
                customer_choice = int(input("Enter your choice: "))

                if customer_choice == 1:  # create an account but do not allow them to set the interest rate
                    account_type = input("Enter the account type (checking/savings): ")
                    account_number = input("Enter the account number: ")
                    balance = float(input("Enter the starting balance: "))
                    customer.create_account(account_type, account_number,
                                            balance)  # use create_account to create the account with the params

                elif customer_choice == 2:  # access the account for the other functions
                    account_number = input("Enter the account number: ")
                    try:
                        customer.access_account(
                            account_number)  # use access_account to access the account with the params
                    except ValueError as e:
                        print(e)

                elif customer_choice == 3:  # deposit to account
                    amount = float(input("Enter the amount to deposit: "))
                    try:
                        customer.deposit(amount)  # use deposit to deposit the amount with params
                    except ValueError as e:
                        print(e)

                elif customer_choice == 4:  # withdraw the amount
                    amount = float(input("Enter the amount to withdraw: "))
                    try:
                        customer.withdraw(amount)  # use withdraw to withdraw the amount with params
                    except ValueError as e:
                        print(e)

                elif customer_choice == 5:  # transfer to chosen account
                    amount = float(input("Enter the amount to transfer: "))
                    account_number = input("Enter the account number to transfer to: ")
                    try:
                        customer.transfer(amount, account_number)  # use transfer to transfer the amount with params
                    except ValueError as e:
                        print(e)

                elif customer_choice == 6:  # return balance
                    try:
                        balance = customer.check_balance()  # use check_balance
                        print(f"Current Balance: {balance}")
                    except ValueError as e:  # handle value errors
                        print(e)

                elif customer_choice == 7:  # return
                    break

        elif choice == 3:  # create a customer account
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            try:
                bank_system.create_customer(username, password)  # use create_customer to create the account with params
            except ValueError as e:
                print(e)

        elif choice == 4:  # quit the program
            break


if __name__ == "__main__":
    main()
