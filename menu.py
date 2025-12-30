from decimal import Decimal

def main_menu(bank):
    while True:
        print("\n Welcome to Main menu")
        print("1. Open new account")
        print("2. Check Balance")
        print("3. Deposit amount")
        print("4. Withdraw amount")
        print("5. View Account info")
        print("6. View Transaction info")
        print("7. Transfer amount")
        print("8. Delete Account")
        print("9. Exit")

        choice = int(input("Enter your choice: "))
    
        try:
            if choice == 1:
                name = input("Enter name: ")
                # account = bank.create_account(name)
                # print(f"Account created! Number: {account.acc_num}")
                print(f"Account created. Account number: {bank.create_account(name)}")

            elif choice ==2:
                # acc= bank.show_balance(int(input("Enter your 8-digit account number: ")))
                acc_num = int(input("Enter your 8-digit account number: "))
                balance = bank.show_balance(acc_num)
                if balance is not None:
                    print(f"Your current balance is: {balance:.2f}€")
                else:
                    print("Account not found")

                
            elif choice == 3:#deposit
                acc_num = int(input("Enter your 8-digit account number: "))
                amount = Decimal(input("Enter amount to deposit: "))
                bank.deposit(acc_num, amount)
                print("Deposit successfully")

            elif choice == 4:#withdraw
                acc_num = int(input("Enter your 8-digit account number: "))
                amount = Decimal(input("Enter amount to withdraw: "))
                bank.withdraw(acc_num, amount)
                print("Withdrawn successfully")
                            
            elif choice == 5:#account details
                acc = bank.get_account(int(input("Account number: ")))
                if acc:
                    print(f"Account Number: {acc['account_number']}")
                    print(f"Account Name: {acc['name']}")
                    print(f"Balance: {acc['balance']:.2f}€")
            
            elif choice == 6:#transactions history
                acc_num = int(input("Enter your 8 digit account number: "))
                transactions = bank.get_transactions(acc_num)
                if not transactions:
                    print("no Transactions found")
                else:
                    for t in transactions:
                        print(f"{t['time']} | {t['type']} | {t['amount']:.2f}£")

                
            elif choice == 7:#transfer
                source_acc = int(input("Enter your 8-digit Sender account number: "))
                dest_acc = int(input("Enter dest 8-digit Reciver account number: "))
                amount = Decimal(input("Enter amount to transfer: "))
                try:
                    success = bank.transfer(source_acc, dest_acc, amount)
                    if success:
                        print("Transfer successful!")
                except Exception as e:
                    print(f"Transfer failed: {e}")
                
            
            elif choice == 8: #Delete account
                acc = int(input("Enter your 8-digit account number: "))
                safety_check = input("If you want to permanently delete your account, type 'DELETE' (case sensitive): ")
                if safety_check == "DELETE":
                    print("\n--- Processing Deletion Request ---")
                    try:
                        bank.delete_account(acc)
                        print(f"Account {acc} has been permanently deleted.")
                        print("Thank you for using our bank. Goodbye!")
                    except ValueError as e:
                        print(f"Error: Account deletion failed: {e}")
                    except Exception as e:
                        print(f"Error account deleteion failed: {e}")
                else:
                    print("Account deletion cancelled. Returning to main menu.")

            elif choice == 9:
                print("Goodbye!")
                break
            else:
                print("Invalid Input. Choose again")
        except Exception as e:
            print(f"Error: {e}")
            