from bs4 import BeautifulSoup
import requests

response = requests.get("https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/")
movies_data = response.text

soup = BeautifulSoup(movies_data, "html.parser")
data = soup.find_all(name = "h3", class_="title")

# for i,movie in enumerate(data, start=1):
#     movie_name = movie.get_text().strip()
movies_list = [movie.getText().strip() for movie in data]
# for top in reversed(movies_list):
#     print(top)
ordered_list = movies_list[::-1]

with open("Movies.txt", mode='w') as file:
    for top in ordered_list:
        file.write(f"{top}\n")

