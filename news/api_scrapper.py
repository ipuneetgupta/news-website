from .models import News
import requests
import json
from .utils import randomNumGen
from cat.models import Cat
from .models import HeadLine


def api_news(url_):
    url = (url_)
    response = requests.get(url)
    return response.json()

def scrap_news_list(x):
    url = 'http://newsapi.org/v2/top-headlines?country=in&category='+str(x)+'&apiKey=d639a4c944084985ba9e8adb4f3b888c'
    news = api_news(url)
    if news['status'] == 'ok':
        c = Cat.objects.get(catName=x)
        for a in news['articles']:
            if a['urlToImage'] == None or a['content'] == None or a['content'].startswith('Subscribe'):
                b = HeadLine()
                b.title = a['title']
                if len(HeadLine.objects.filter(title=a['title'])) != 0:
                    b.newsUrl = a['url']
                    b.publishDate = a['publishedAt'].split('T')[0]
                    b.writerName = a['author']
                    b.ocatId = Cat.objects.get(catName=x).pk
                    b.act = 1
                    b.time = a['publishedAt'].split('T')[1]
                    b.publisherName = 'admin'
                    c.headlineCount+=1
                    c.save()
                    b.save()
            else:
                b = HeadLine()
                b.title = a['title']
                if len(HeadLine.objects.filter(title=a['title'])) == 0:

                    b.newsUrl = a['url']
                    b.publishDate = a['publishedAt'].split('T')[0]
                    b.writerName = a['author']
                    b.ocatId = Cat.objects.get(catName=x).pk
                    b.act = 1
                    b.time = a['publishedAt'].split('T')[1]
                    b.publisherName = 'admin'
                    c.headlineCount+=1
                    b.save()
                
                b = News()
                b.title = a['title']
                if len(News.objects.filter(title=a['title'])) == 0:
                    b.newsSummary = a['description']
                    b.newsContent = a['content']
                    b.image_url = a['urlToImage']
                    b.publishDate = a['publishedAt'].split('T')[0]
                    b.time = a['publishedAt'].split('T')[1]
                    b.writerName = a['author']
                    b.ocatId = Cat.objects.get(catName=x).pk
                    b.tag = 'News,' + str(x)
                    b.newsUrl = a['url']
                    b.publisherName = 'admin'
                    b.rand = randomNumGen()
                    b.source_name = a['source']['name'] 
                    b.act = 1
                    c.newsCount+=1
                    c.save()
                    b.save()