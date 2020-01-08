import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from aviation_news.models import Headline

def scrape(request):
  session = requests.Session()
#   session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
  url = "https://www.ainonline.com/aviation-news/aircraft"
  content = session.get(url, verify=False).content
  soup = BSoup(content, "html.parser")
#   print(soup.prettify)
  print("Hello")
  News = soup.find_all('div', {"class":"views-row"})
  for artcile in News:
    for_link = artcile.find_all('a')[0]
    for_img = artcile.find_all('img')[0]
    for_text = artcile.find_all('a')[1]
    new_headline = Headline()
    new_headline.title = for_text.get_text()
    new_headline.url = for_link['href']
    new_headline.image = for_img['src']
    new_headline.save()
  return redirect("../")

def news_list(request):
    headlines = Headline.objects.all()[::-1]
    context = {
        'object_list': headlines,
    }
    return render(request, "aviation_news/home.html", context)
