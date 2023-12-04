from bs4 import BeautifulSoup
import requests
import folium

def add_user_to(users_list: list) -> None:
    """
    add object to list
    :param users_list: list - users list
    :return: None
    """
    name = input('podaj imię ?')
    posts = input('podaj liczbę postów ?')
    city = input('podaj miasto?')
    users_list.append({'name': name, 'posts': posts, "city": city})


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


def show_users_from(users_list: list) -> None:
    for user in users_list:
        print(f'Twoj znajomy {user["name"]} {user['nick']} dodał {user["posts"]}')


def update_user(users_list: list[dict, dict]) -> None:
    nick_of_user = input('podaj nick użytkownika do modyfikacji')
    print(nick_of_user)
    for user in users_list:
        if user['nick'] == nick_of_user:
            print('Znaleziono')
            user['name'] = input('podaj nowe imię: ')
            user['nick'] = input('podaj nowy nick: ')
            user['posts'] = int(input('podaj liczbę postów: '))
            user['city'] = input('podaj miasto')


def gui(users_list: list) -> None:
    while True:
        print(f'MENU: \n'
              f'0: Zakończ program \n'
              f'1: Wyświetl użytkowników \n'
              f'2: Dodaj użytkownika \n'
              f'3: Usuń użytkownika \n'
              f'4: Modyfikuj użytkownika \n'
              f'5: Wygeneruj mapę z użytkownkiem \n'
              f'6: Wygeneruj mapę z wszystkimi użytkownikami'
              )
        menu_option = input('Podaj funkcję do wywołania')
        print(f'Wybrano funkcję {menu_option}')

        match menu_option:
            case '0':
                print('Kończę pracę')
                break
            case '1':
                print('Wyświetlenie listy użytkowników')
                show_users_from(users_list)
            case '2':
                print('Dodawanie użytkownika')
                add_user_to(users_list)
            case '3':
                print("Usuwanie użytkownika")
                remove_user_from(users_list)
            case '4':
                print('Modyfikuję użytkownika')
                update_user(users_list)
            case '5':
                print('Rysuję mapę z użytkownikiem')
                user = input('Poda nazwę użytkownika do modyfikacji')
                for item in users_list:
                    if item['nick'] == user:
                        get_map_one_user(item)
            case '6':
                print('Rysuję mapę z wszystkimi użytkownikami')
                get_map_of(users_list)


# ==================MAPA==============


nazwy_miejscowości = ['Opoczno', 'Lublin', 'Gdańsk']


def get_coordinates_of(city: str) -> list[float, float]:
    # pobranie strony internetowej

    adres_URL = f'https://pl.wikipedia.org/wiki/{city}'
    response = requests.get(url=adres_URL)
    response_html = BeautifulSoup(response.text, 'html.parser')

    # pobranie współrzędnych z tresci strony internetowej
    response_html_latitude = response_html.select('.latitude')[1].text  # kropka ponieważ ona oznacza class
    response_html_latitude = float(response_html_latitude.replace(',', '.'))
    response_html_longitude = response_html.select('.longitude')[1].text  # kropka ponieważ ona oznacza class
    response_html_longitude = float(response_html_longitude.replace(',', '.'))

    return [response_html_latitude, response_html_longitude]


# zwróci mape z pinezka odnoszaca się do uzytkownika podanego z klawiatury
def get_map_one_user(user: str) -> None:
    city = get_coordinates_of(user["city"])
    map = folium.Map(
        location=city,
        tiles="OpenStreetMap",
        zoom_start=7
    )
    folium.Marker(
        location=city,
        popup=f'Tu rządzi {user["name"]},'
              f'postów: {user["posts"]}'
    ).add_to(map)
    map.save(f'mapka{user["name"]}.html')


# zwróci mapę z wszystkimi użytkownikai z danej listy (znajomymi)
def get_map_of(users: list) -> None:
    map = folium.Map(
        location=[52.3, 21.0],  # gdzie mapa ma byc wycentrowana
        tiles="OpenStreetMap",
        zoom_start=13
    )
    for user in users:
        folium.Marker(
            location=get_coordinates_of(city=user['city']),
            popup=f'Użytkownik: {user["name"]} \n'
                  f'Liczba postów {user["posts"]}'
        ).add_to(map)
    map.save('mapkaaa.html')

def pogoda_z(miasto: str):
    url = f"https://danepubliczne.imgw.pl/api/data/synop/station/{miasto}"
    return requests.get(url).json()

