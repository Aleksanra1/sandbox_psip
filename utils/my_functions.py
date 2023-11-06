def add_user_to(users_list:list) -> None:
    """
    add object to list
    :param users_list: list - users list
    :return: None
    """
    name = input('podaj imię ?')
    posts = input('podaj liczbę postów ?')
    users_list.append({'name': name, 'posts': posts})

def remove_user_from(users_list: list) -> None:
        """
        remove object from list
        :param users_list: list - users list
        :return: None
        """

        tmp_list = []
        name = input('Podaj imię użytkownika do usunięcia: ')
        for user in users_list:
            if user["name"] == name:
                print(f'Znaleziono użytkownika {user}')
                tmp_list.append(user)
        print('Znaleziono uzytkownikow :')
        print('0: usun wszystkich znalezionych uzytkownikow')
        for numerek, user_to_be_removed in enumerate(tmp_list):
            print(f'{numerek + 1}, {user_to_be_removed}')
        numer = int(input(f'Wybierz numer uzytkownika do usuniecia: '))
        if numer == 0:
            for user in tmp_list:
                users_list.remove(user)
        else:
            users_list.remove(tmp_list[numer - 1])

def show_users_from(users_list:list) ->None:
   for user in users_list:
      print(f'Twoj znajomy {user["name"]} dodał {user["posts"]}')

def gui(users_list) -> None:
    while True:
        print(f'Menu: \n'
              f'0: Zakończ program \n'
              f'1: Wyświetl użytkowników \n'
              f'2: Dodaj użytkownika \n'
              f'3: Usuń użytkownika \n'
              f'4: Modyfikuj użytkownika \n'
              )
        menu_option = input('Podaj funkcje do wywolania')
        print(f'Wybrano funkcje {menu_option}')

        match menu_option:
            case '0':
                print('Kończę pracę')
                break
            case '1':
                print('WYswietlanie listy uzytkownikow')
                show_users_from(users_list)
            case '2':
                print('Dodaję uzytkownika')
                add_user_to(users_list)
            case '3':
                print('Usuwanie użytkownika')
                remove_user_from(users_list)
            case '4':
                print('Modyfikuj uzytkownika')
                print('to bedzie zrobione')  # TODO add this function to my_functions


