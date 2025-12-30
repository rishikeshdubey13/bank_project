# class FakeDB:
#     def __init__(self):
#         self.users = []
    
#     def check_user(self, email):
#         for user in self.users:
#             if user['email'] == email:
#                 return user
#         return None
    
#     def create_user(self, email, password_hash):
#         user_id = len(self.users) + 1
#         new_user = {
#             'id': user_id,
#             'email': email,
#             'password_hash': password_hash,
#             'is_active': True,
#             'role': 'user'
#         }
#         self.users.append(new_user)
    
#     def commit(self):
#         pass
    
#     def rollback(self):
#         pass