import os
import json
import secrets
from bank import Account

DATA_FILE = "bank_data.json"


class Storage:
    def _load_data(self):
            if not os.path.exists(DATA_FILE):
                return {}
            try:
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f) 
                    return {int(acc): Account.from_dict(acc_data)
                        for acc, acc_data in data.items()}
            except (json.JSONDecodeError):
                return {}


    def _save_data(self, accounts:dict):
        data_to_save = {str(acc): obj.to_dict() for acc, obj in accounts.items()}
        with open(DATA_FILE, 'w') as f:
            json.dump(data_to_save,f, indent=4)


    def generate_account_number(self, accounts: dict):
            while True:
                new_num = secrets.randbelow(90_000_000) + 10_000_000
                if new_num not in accounts:
                    return new_num