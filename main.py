from dane import users_list



def add_user_to(users_list:list) -> None:
    """
    add object to list
    :param users_list: list - users list
    :return: None
    """

    name = input('podaj imię ?')
    posts = input('podaj liczbę postów ?')
    users_list.append({'name': name, 'posts': posts})

add_user_to(users_list)
add_user_to(users_list)
add_user_to(users_list)


for user in users_list:
    print(f'Twoj znajomy {user["name"]} dodał {user["posts"]}')


