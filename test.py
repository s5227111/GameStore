import requests
from datetime import datetime
from random import random, choice

# edit_url = "http://localhost:8080/apis/catalogApi/editProduct"

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

game_id = 0
while True:
    game_id += 1

    game_name = input("Digite  o nome do jogo: ")

    if game_name == "exit":
        break

    image_1 = "https://cdn.akamai.steamstatic.com/steam/apps/427520/ss_36e4d8e5540805f5ed492d24d784ed9ba661752b.1920x1080.jpg?t=1664264081"
    image_2 = "https://cdn.akamai.steamstatic.com/steam/apps/427520/ss_0bf814493f247b6baa093511b46c352cf9e98435.1920x1080.jpg?t=1664264081"
    image_3 = "https://cdn.akamai.steamstatic.com/steam/apps/427520/ss_0e6d3c0d1af06fcde28ef1f1703e142f416ace44.1920x1080.jpg?t=1664264081"
    image_main = (
        "https://cdn.akamai.steamstatic.com/steam/apps/427520/header.jpg?t=1664264081"
    )

    description = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
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
        "details": {
            "long_description": description,
            "download_size": "40GB",
        },
        "reviews": dict(stars=stars),
        "tags": [t for t in tag],
        "images": {
            "thumb_image": image,
            "details-image-main": image_main,
            "details-image1": image_1,
            "details-image2": image_2,
            "details-image3": image_3,
        },
    }

    response = requests.post(url, json=inserted_data)
    print(response.json())
