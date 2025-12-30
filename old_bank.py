import secrets
import psycopg2
class Banking_system:
    def __init__(self, db):
        self.db = db

    def generate_account_number(self):
        new_num = secrets.randbelow(90_000_000) + 10_000_000
        return new_num
    
    def create_account(self, name):
        max_attemps = 10 #if there is a collison its the max_attempt to generate the unique number
        for attemps in range(max_attemps):      
            acc_num = self.generate_account_number()
            try:
                self.db.create_account(acc_num, name)
                return acc_num
            except psycopg2.IntegrityError:
                self.db.conn.rollback()
                print(f"Rare collision occured retrying... attempt {attemps +1}")
                continue
        raise RuntimeError("Failed to generate unique account number after several attempts")
    
    def get_account(self, acc_num):
        return self.db.get_account(acc_num)
    
    def delete_account(self, acc_num):
        success = self.db.delete_account(acc_num)
        if not success:
            raise ValueError(f"Account {acc_num} does not exist or could not be deleted")
        return True
        
    def show_balance(self, acc_num):
        acc = self.db.get_account(acc_num)
        if not acc:
            return None
        return float(acc['balance'])
         
    def deposit(self, acc_num, amount):
        try:
            # self.db.begin()
            acc = self.db.get_account(acc_num)
            if not acc:
                raise ValueError(f"No such account")
            if amount < 0:
                raise ValueError(f"Amount cannot be negative")
            new_balance = acc['balance'] + amount
            self.db.update_balance(acc_num, new_balance)
            self.db.record_transaction(acc_num, amount, 'Deposit')
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
    
    def withdraw(self, acc_num, amount):
        try:
            # self.db.begin()
            acc = self.db.get_account(acc_num)
            if not acc:
                raise ValueError(f"No such account")
            if amount < 0:
                raise ValueError(f"Amount cannot be negative")
            if amount > acc['balance']:
                raise ValueError("Insuffecient Funds")
            new_balance = acc['balance'] - amount
            self.db.update_balance(acc_num, new_balance)
            self.db.record_transaction(acc_num, amount, 'Withdraw')
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
 
    def transfer(self, source_acc_num, dest_acc_num, amount):
        try:
            # self.db.begin()
            if source_acc_num == dest_acc_num:
                raise ValueError("Cannot tranfer to same account")
            if amount <=0:
                raise ValueError("Amount can not be negative")
            
            source = self.db.get_account(source_acc_num)
            dest = self.db.get_account(dest_acc_num)

            if not source:
                raise ValueError(f"Source account: {source_acc_num} does not exist")
            if not dest:
                raise ValueError(f"Destination account: {dest_acc_num} does not exist")
            if amount > source['balance']:
                raise ValueError("Insufficient Funds")
            
            # Update balances
            self.db.update_balance(source_acc_num, source['balance'] - amount)
            self.db.update_balance(dest_acc_num, dest['balance'] + amount)

            # Record correct transaction amount (not balance)
            self.db.record_transaction(source_acc_num, amount, f"Transfer to {dest_acc_num}")
            self.db.record_transaction(dest_acc_num, amount, f"Transfer from {source_acc_num}")

            self.db.commit()
        except psycopg2.errors.DeadlockDetected:
            self.db.rollback()
            raise RuntimeError("Temporary conflict, please retry")
        except Exception as e:
            self.db.rollback()
            raise e
        
    def get_transactions(self, acc_num):
        return self.db.get_transactions(acc_num)





# class Account:
#     def __init__(self, account_number, name, balance = 0,transactions=None):
#         self.account_number = account_number
#         self.name = name
#         self.balance = balance
#         self.transactions = transactions if transactions else []

#     def deposit(self, amount):
#         if amount <=0:
#             print("Amount cannot be negative or zero")
#         else:
#             self.balance += amount
#             self.add_transactions(amount, "Deposit")

#     def withdraw(self, amount):
#         if amount <=0:
#             print("Amount cannot be negative or zero")
#         elif amount > self.balance:
#             print("Insuffcient amount")
#         else:
#             self.balance -= amount
#             self.add_transactions(amount, "Withdraw")

#     def transfer(self,dest_account, amount):
#         if amount <= 0:
#             print("Amount cannot be negative or zero")
#         elif amount > self.balance:
#             print("Insuffcient amount")
        
#         # Deduct from source
#         self.balance -= amount
#         self.add_transactions(amount, f"Transfer to {dest_account.account_number}")

#         dest_account.balance += amount
#         dest_account.add_transactions(amount, f"Transfer from {self.account_number}")



#     def add_transactions(self, amount: float, type: str):
#         self.transactions.append({
#             'amount': amount,
#             'type': type,
#             'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         })

#     def show_balance(self):
#         return self.balance
    
#     def display_transactions(self):
#         if not self.transactions:
#             print("No recorded transactions for this account")
#             return 
        
#         for transaction in self.transactions:
#             print(f"{transaction['amount']}")
#             print(f"{transaction['type']}")
#             print(f"{transaction['time']}")
    
#     def to_dict(self):
#         return {
#             "account_number": self.account_number,
#             "name": self.name,
#             "balance": self.balance,
#             'transactions': self.transactions
#         }
    
#     @classmethod
#     def from_dict(cls, data:dict):
#         return cls(
#             data['account_number'], 
#             data['name'], 
#             data['balance'],
#             data.get('transactions', []) 
#         )
    

# class Banking_system:
#     def __init__(self, storage):
#         self.storage = storage
#         self.accounts = self.storage._load_data()
        
#     def open_new_account(self, name: str):
#         account_number = self.storage.generate_account_number(self.accounts)
#         new_account = Account(account_number, name)
#         self.accounts[account_number] = new_account
#         self.storage._save_data(self.accounts)
#         return new_account
    
#     def get_account(self, account_number:int):
#         account = self.accounts.get(account_number)
#         if account is None:
#             print(f"Account number {account_number} does not exist")
#         return account
    
#     def save(self):
#         self.storage._save_data(self.accounts)
    
#     # def transfer_money(self, account_number, source, dest, amount):
#     def transfer_process(self, source_account_numer:int, dest_account_number:int, amount :float):
#         source  =  self.accounts.get(source_account_numer)
#         dest =  self.accounts.get(dest_account_number)
#         if not source:
#             print(f"Source account {source_account_numer} not found")
#             return False
    
#         if not dest:
#             print(f"Source account {dest_account_number} not found")
#             return False
        
#         if source_account_numer == dest_account_number:
#             print("Source and destination cannot be same")
#             return False

#         if source.transfer(dest, amount):
#             self.save()
#             print(f"Succesfully transfered from {source_account_numer} to {dest_account_number}")
#             return True
        
#         return False
#         # #begin_transaction()
#         # #commit_transaction()
#         # #rollback_transaction()