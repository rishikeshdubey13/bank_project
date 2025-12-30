import secrets
import psycopg2
class Banking_system:
    def __init__(self, db):
        self.db = db

    def generate_account_number(self):
        new_num = secrets.randbelow(90_000_000) + 10_000_000
        return new_num
    
    def create_account(self, name, user_id):
        max_attemps = 10 #if there is a collison its the max_attempt to generate the unique number
        for attemps in range(max_attemps):      
            acc_num = self.generate_account_number()
            try:
                self.db.create_account(acc_num, name, user_id)
                self.db.commit()
                return acc_num
            except psycopg2.IntegrityError:
                self.db.conn.rollback()
                print(f"Rare collision occured retrying... attempt {attemps +1}")
                continue
        raise RuntimeError("Failed to generate unique account number after several attempts")
    
    def get_account(self, acc_num, user_id):
        return self.db.get_account(acc_num, user_id)
    
    def delete_account(self, acc_num):
        success = self.db.delete_account(acc_num)
        if not success:
            raise ValueError(f"Account {acc_num} does not exist or could not be deleted")
        return True
        
    def show_balance(self, acc_num, user_id):
        acc = self.db.get_account(acc_num)
        if not acc:
            return None
        if str(acc['user_id']) !=  str(user_id):
            return "UNAUTHORIZED"
        return {"account":acc_num, "balance": float(acc['balance'])}
         
    def deposit(self, acc_num, amount, user_id):
        if amount < 0:
            raise ValueError(f"Amount cannot be negative")
        acc = self.db.get_account(acc_num)
        if not acc:
            raise ValueError(f"No such account")
        if str(acc['user_id']) !=  str(user_id):
            raise PermissionError("UNAUTHORIZED")
        try:
            new_balance = acc['balance'] + amount
            self.db.update_balance(acc_num, new_balance)
            self.db.record_transaction(acc_num, amount, 'Deposit')
            self.db.commit()
            return new_balance
        except Exception as e:
            self.db.rollback()
            raise e
    
    def withdraw(self, acc_num, amount, user_id):
        if amount < 0:
            raise ValueError(f"Amount cannot be negative")
        acc = self.db.get_account(acc_num)
        if not acc:
            raise ValueError(f"No such account")
        if amount > acc['balance']:
            raise ValueError("Insuffecient Funds")
        if str(acc['user_id']) !=  str(user_id):
                return "UNAUTHORIZED"
        try:
            new_balance = acc['balance'] - amount
            self.db.update_balance(acc_num, new_balance)
            self.db.record_transaction(acc_num, amount, 'Withdraw')
            self.db.commit()
            
            return new_balance
        except Exception as e:
            self.db.rollback()
            raise e
 
    def transfer(self, source_acc_num, dest_acc_num, amount, user_id):
        if amount <=0:
            raise ValueError("Amount can not be negative")
        if source_acc_num == dest_acc_num:
            raise ValueError("Cannot tranfer to same account")
        source = self.db.get_account(source_acc_num)
        dest = self.db.get_account(dest_acc_num)
        if not source:
            raise ValueError(f"Source account: {source_acc_num} does not exist")
        if not dest:
            raise ValueError(f"Destination account: {dest_acc_num} does not exist")
        if amount > source['balance']:
            raise ValueError("Insufficient Funds")
        if str(source['user_id']) !=  str(user_id):
            return "UNAUTHORIZED"
        try:
            # Update balances
            self.db.update_balance(source_acc_num, source['balance'] - amount)
            self.db.update_balance(dest_acc_num, dest['balance'] + amount)

            # Record correct transaction amount (not balance)
            self.db.record_transaction(source_acc_num, amount, f"Transfer to {dest_acc_num}")
            self.db.record_transaction(dest_acc_num, amount, f"Transfer from {source_acc_num}")

            self.db.commit()
            
            return source['balance'], dest['balance']
        except psycopg2.errors.DeadlockDetected:
            self.db.rollback()
            raise RuntimeError("Temporary conflict, please retry")
        except Exception as e:
            self.db.rollback()
            raise e
        
    def get_transactions(self, acc_num):
        return self.db.get_transactions(acc_num)





