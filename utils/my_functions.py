from bs4 import BeautifulSoup
import psycopg2 as ps
import requests
import folium

db_params = ps.connect(
    database='postgres',
    user='postgres',
    password='psip2023',
    host='localhost',
    port=5432
)

cursor=db_params.cursor()
def add_user_to() -> None:
    """
    add object to list
    :param users_list: list - users list
    :return: None
    """
    name = input('podaj imię ?')
    posts = input('podaj liczbę opublikowanych postów ?')
    nick = input('podaj nick ?')
    city = input('podaj miasto?')
    sql_query_1 = f"INSERT INTO public.psip_zad(city, name, nick, posts) VALUES ('{city}', '{name}', '{nick}', '{posts}');"
    cursor.execute(sql_query_1)
    db_params.commit()


def remove_user_from() -> None:
    """
    remove object from list
    :param users_list: list - users list
    :return: None
    """
    name = input('Podaj imię użytkownika którego trzeba usunąć: ')
    sql_query_1 = f"SELECT * FROM public.psip_zad WHERE name='{name}';"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    print('Znaleziono uzytkownikow :')
    print('0: usun wszystkich znalezionych uzytkownikow')
    for numerek, user_to_be_removed in enumerate(query_result):
        print(f'{numerek + 1}, {user_to_be_removed}')
    numer = int(input(f'Wybierz numer uzytkownika do usuniecia: '))
    if numer == 0:
        sql_query_2 = f"DELETE * FROM public.psip_zad;"
        cursor.execute(sql_query_2)
        db_params.commit()
    else:
        sql_query_2 = f"DELETE FROM public.psip_zad WHERE id='{query_result[numer - 1][0]}';"
        cursor.execute(sql_query_2)
        db_params.commit()


def show_users_from() -> None:
    sql_query_1 = f"SELECT * FROM public.psip_zad;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    for row in query_result:
        print(f'Twoj znajomy {row[2]} opublikowal na tablicy {row[4]} postow')


def update_user() -> None:
    nick_of_user = input('podaj nick użytkownika do modyfikacji')
    sql_query_1 = f"SELECT * FROM public.psip_zad WHERE nick='{nick_of_user}';"
    cursor.execute(sql_query_1)
    print('Znaleziono pomyslnie')
    name = input('podaj nowe imie dla uzytkownika: ')
    nick = input('podaj nowe ksywe dla uzytkownika: ')
    posts = int(input('podaj liczbw postów uzytkownika: '))
    city = input('podaj miasto dla uzytkownika: ')
    sql_query_2 = f"UPDATE public.psip_zad SET name='{name}',nick='{nick}', posts='{posts}', city='{city}' WHERE nick='{nick_of_user}';"
    cursor.execute(sql_query_2)
    db_params.commit()


def gui() -> None:
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
                print('Kończę pracę na dziś')
                break
            case '1':
                print('Wyświetlenie listy użytkowników')
                show_users_from()
            case '2':
                print('Dodawanie użytkownika')
                add_user_to()
            case '3':
                print("Usuwanie użytkownika")
                remove_user_from()
            case '4':
                print('Modyfikuję użytkownika')
                update_user()
            case '5':
                print('Rysuję mapę z użytkownikiem')
                get_map_one_user()
            case '6':
                print('Rysuję mapę z wszystkimi użytkownikami')
                get_map_of()


# ==================MAPA==============

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
def get_map_one_user() -> None:
    city = input('Podajj miasto uzytwkonika: ')
    sql_query_1 = f"SELECT * FROM public.psip_zad WHERE city='{city}';"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    city = get_coordinates(city)
    map = folium.Map(
        location=city,
        tiles="OpenStreetMap",
        zoom_start=10
    )
    for user in query_result:
        folium.Marker(location=city,
                      popup=f'Użytkownik: {user[2]}\n'
                      f'Liczba postow: {user[4]}'
                      ).add_to(map)
    map.save(f'mapa{query_result[0][1]}.html')


# zwróci mapę z wszystkimi użytkownikai z danej listy (znajomymi)
def get_map_of() -> None:
    map = folium.Map(
        location=[52.3, 21.0],  # gdzie mapa ma byc wycentrowana
        tiles="OpenStreetMap",
        zoom_start=13
    )
    sql_query_1 = f"SELECT * FROM public.psip_zad;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    for user in query_result:
        folium.Marker(location=get_coordinates(city=user[1]),
                      popup=f'Użytkownik: {user[2]}\n'
                            f'Liczba postow: {user[4]}'
                      ).add_to(map)
        map.save('mapaa.html')


#======koniec mapy
def pogoda_z(miasto: str):
    url = f"https://danepubliczne.imgw.pl/api/data/synop/station/{miasto}"
    return requests.get(url).json()

class User:
    def __init__(self, city, name, nick, posts):
        self.city = city
        self.name = name
        self.nick = nick
        self.posts = posts
    def pogoda_z(self,miasto: str):
        url = f'https://danepubliczne.imgw.pl/api/data/synop/station/{miasto}'
        return requests.get(url).json()

npc_1=User(city='warszawa', name='Iza', nick='Izazmatiza', posts=76)
npc_2=User(city='krakow',  name='Marcin', nick='Marcinos', posts=932)
print(npc_1.city)
print(npc_2.city)

print(npc_1.pogoda_z(npc_1.city))
print(npc_2.pogoda_z(npc_2.city))