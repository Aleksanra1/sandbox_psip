
from bs4 import BeautifulSoup

import requests
import folium

nazwy_miejscowości = ['Opoczno', 'Lublin', 'Gdańsk']
def get_coordinates_of(city:str)->list[float,float]:
    # pobranie strony internetowej

    adres_URL = f'https://pl.wikipedia.org/wiki/{city}'
    response = requests.get(url=adres_URL)
    response_html = BeautifulSoup(response.text, 'html.parser')

    #pobranie współrzędnych z tresci strony internetowej
    response_html_latitude = response_html.select('.latitude')[1].text # kropka ponieważ ona oznacza class
    response_html_latitude = float(response_html_latitude.replace(',','.'))
    response_html_longitude = response_html.select('.longitude')[1].text # kropka ponieważ ona oznacza class
    response_html_longitude = float(response_html_longitude.replace(',','.'))

    return[response_html_latitude, response_html_longitude]

#for item in nazwy_miejscowości:
#   print(get_coordinates_of(item))

# zwróci mape z pinezka odnoszaca się do uzytkownika podanego z klawiatury

# zwróci mapę z wszystkimi użytkownikai z danej listy (znajomymi)
###RYSOWANIE MAPY
city= get_coordinates_of(city='Zamość')
map = folium.Map(
    location=[52.3, 21.0], #gdzie mapa ma byc wycentrowana
    tiles="OpenStreetMap",
    zoom_start=7
    )
for item in nazwy_miejscowości:
    folium.Marker(
        location=get_coordinates_of(city=item),
         popup='GEOINFORMATYKA RZĄDZI OU YEEEAH!'
    ).add_to(map)
map.save('mapka.html')







