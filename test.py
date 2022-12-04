import requests
from datetime import datetime
from random import random, choice

# edit_url = "http://localhost:8080/apis/catalogApi/editProduct"
# game_id = 1


# data_to_edit = {
#     "game_id": 1,
#     "name": "The Witcher 3: Wild Hunt",
# }


# response = requests.put(edit_url, params={"game_id": game_id}, json=data_to_edit)

# print(response.json())

#  TEST DELETE
# delete_url = "http://localhost:8080/apis/catalogApi/deleteProduct"
# game_id = 1

# response = requests.delete(delete_url, params={"game_id": game_id})

# print(response.json())

url = "http://localhost:8080/apis/catalogApi/createProduct"

avaible_images = [
    "/catalog/static/catalog/images/popular-01.jpg",
    "/catalog/static/catalog/images/popular-02.jpg",
    "/catalog/static/catalog/images/popular-03.jpg",
    "/catalog/static/catalog/images/popular-04.jpg",
    "/catalog/static/catalog/images/popular-05.jpg",
    "/catalog/static/catalog/images/popular-06.jpg",
    "/catalog/static/catalog/images/popular-07.jpg",
    "/catalog/static/catalog/images/popular-08.jpg",
]

# Gera dados
game_id = 0
while True:
    game_id += 1

    game_name = input("Digite  o nome do jogo: ")

    if game_name == "exit":
        break

    added_at = datetime.today().date()
    added_at = datetime.today().date().strftime("%d/%m/%y")
    publisher = input("digite a editora do game: ")
    tag = input("digite categorias seperado por espaço").split(" ")
    downloads = 0
    image = choice(avaible_images)

    listed_price = round(random() * 200, 1)
    stars = round(random() * 5, 1)

    inserted_data = {
        "game_id": game_id,
        "name": game_name,
        "developer": publisher,
        "downloads": 0,
        "added_at": added_at,
        "pricing": listed_price,
        "details": {},
        "reviews": dict(stars=stars),
        "tags": [t for t in tag],
        "images": [image],
    }

    response = requests.post(url, json=inserted_data)
    print(response.json())
