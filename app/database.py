import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import OperationalError
from app.config import settings





class Database:
    def __init__(self):
        self.conn =None
        psycopg2.extras.register_uuid()
        try:
            self.conn = psycopg2.connect(
                dbname = settings.DB_NAME,
                user =settings.DB_USER,
                password = settings.DB_PASSWORD,
                host = settings.DB_HOST,
                port = settings.DB_PORT
            )
            self.conn.autocommit = False
            print("Databse connection is succesfull")
        except OperationalError as e:
            print(f"Connection failed: {e}")
            raise e
    
    def close(self):
        if self.conn:
            self.conn.close()

    def execute(self, query, params=None, fetch=False, return_rowcount=False):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            if fetch:
                return cur.fetchall()
            if return_rowcount:
                return cur.rowcount
            return None
    
    def commit(self):
        self.conn.commit()
    
    def rollback(self):
        self.conn.rollback()

    #------Accounts operations------

    
    def create_account(self, acc_num, name, user_id):
        query = """
        INSERT INTO accounts (account_number, name, user_id, balance)
        VALUES (%s, %s, %s, %s)
        """
        self.execute(query, (acc_num, name, user_id, 0))

    def get_account(self, acc_num):
        query = "SELECT * from accounts WHERE account_number = %s"
        result = self.execute(query, (int(acc_num),), fetch=True)
        return result[0] if result else None
    
    def delete_account(self, acc_num):
        query = "DELETE FROM accounts WHERE account_number = %s"
        row_count = self.execute(query, (acc_num,), return_rowcount=True)
        return row_count > 0
        
    def update_balance(self, acc_num, new_balance):
        query = "UPDATE accounts SET balance = %s WHERE account_number = %s"
        self.execute(query, (new_balance, acc_num))

    #------Transactions------

    def record_transaction(self, acc_num, amount, type):
        query = "INSERT INTO transactions (account_number, amount, type) VALUES (%s, %s, %s)"
        self.execute(query, (acc_num, amount, type))
    
    def get_transactions(self, acc_num):
        query = "SELECT * from transactions WHERE account_number = %s ORDER by time DESC"
        result = self.execute(query, (acc_num,), fetch=True)
        return result

    def delete_transacations(self, acc_num):
        query = "DELETE FROM transactions WHERE account_number= %s"
        row_count = self.execute(query, (acc_num,), return_rowcount=True)
        return row_count >0
    
 #------Users------
    

    def create_user(self, email, password_hash, role='user'):
        query = """
        INSERT INTO users(email, password_hash, role)
        VALUES (%s, %s, %s)
        RETURNING id; 
        """
        #RETURNING id; because this allows python to return the value immediately
        try: 
            result = self.execute(query, (email, password_hash, role))
            return result
        except psycopg2.IntegrityError as e:
            print(f"Error: User with email {email} already exists.")
            raise e


    def check_user(self, email):
        query = "SELECT * FROM users WHERE email= %s"
        result = self.execute(query, (email,), fetch =True)
        return result[0] if result else None
    
        
    def delete_user(self, email):
        query =  "DELETE FROM users WHERE emial = %s"
        row_count = self.execute(query,  (email,), return_rowcount=True)
        return row_count > 0



    def create_refresh_token(self, user_id, token_hash, expires_at):
        query = """
        INSERT INTO refresh_tokens(user_id, token_hash, expires_at)
        VALUES (%s, %s, %s)
        RETURNING id; 
        """
        result = self.execute(query, (user_id, token_hash, expires_at))
        return result

    def get_refresh_token_by_hash(self, token_hash):
        query = "SELECT * FROM refresh_tokens WHERE token_hash = %s"
        result = self.execute(query, (token_hash,), fetch= True)
        return result[0] if result else None
    
    def delete_refresh_token(self, token_hash):
        query =  "DELETE FROM refresh_token WHERE token_hash = %s"
        row_count= self.execute(query, (token_hash,), return_rowcount=True)
        return row_count > 0

    # def begin(self):
    #     self.conn.cursor().execute('BEGIN')
    
  

    
   
