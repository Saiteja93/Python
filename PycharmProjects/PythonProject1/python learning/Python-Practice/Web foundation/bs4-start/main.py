from bs4 import BeautifulSoup
import requests

response = requests.get("https://news.ycombinator.com/news")
ycb_live = response.text

soup = BeautifulSoup(ycb_live, "html.parser")
print(soup.title)
tags_title = []
tags_links = []
tags = soup.find_all(class_ = "titleline")
for i,tag in enumerate(tags, start =1):
    a_tag = tag.find("a")
    text = tag.get_text()
    link = a_tag.get('href')
    print(f"{i}. {text} ")
    print(f"Link ---> {link}")









#import lxml

# with open("website.html") as file:
#     content = file.read()
#


# soup = BeautifulSoup(content,"html.parser" )
# title = soup.title
# print(title)
#
# class_is_heading = soup.find_all(class_= "heading")
# print(class_is_heading)
#
# tag_names = soup.find_all(name="a")
# print(tag_names)
# for tag in tag_names:
#     Anchor_tag = tag
#     print(f"Anchor tag = {Anchor_tag}")
