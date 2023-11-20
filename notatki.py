from dane import users_list
from utils.my_functions import update_user


update_user(users_list)

for user in users_list:
    print(user)
