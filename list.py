from flask import Flask, render_template, request, jsonify
import json
import requests
import xml.etree.ElementTree as ET

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://sparta:test@cluster0.gm0wapr.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta
app = Flask(__name__)
books = []

def search_book(keyword, page):
    url = 'https://www.aladin.co.kr/ttb/api/ItemSearch.aspx'
    params = {
        'ttbkey': 'ttbjjd03241934001',
        'Query': keyword,
        'start': (page-1) * 10 + 1,
        'SearchTarget':'Book',
        'maxResults': 10,
        'output': 'js',
        'Version': '20131101'
    }
    res = requests.get(url, params=params)
    result = res.json()
    return result['item'], result['totalCount']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
  query = request.args.get('query')
  page = request.args.get('page', type=int, default=1)
  print(request.headers['Referer'].find('index'))

  # 알라딘 검색 API에서 검색어에 대한 검색 결과를 받아옴
  api_key = 'ttbjjd03241934001'
  book_id = ''
  url = f'http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey={api_key}&Query={query}&MaxResults=10&SearchTarget=Book&start={(page)}&output=js&Version=20131101'

  detail_url = f'http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx?ttbkey={api_key}&itemIdType=ISBN&ItemId={book_id}&output=xml&Version=20131101&OptResult=ebookList,usedList,reviewList'
  response = requests.get(url)
  

  data = json.loads(response.text)
  books.clear()
  for book in data['item']:
    #print(book['title'], book['author'], book['publisher'], book['priceStandard'])
    title = book['title']
    author = book['author']
    publisher = book['publisher']
    price = book['priceStandard']
    pubDate = book['pubDate']
    link = book['link']
    cover_url = book['cover']
    book_id = book['itemId']
    book = {
      'title' : title,
      'author' : author,
      'publisher' : publisher,
      'price' : price,
      'pubDate' : pubDate,
      'link' : link,
      'cover_url' : cover_url,
    }
    books.append(book)
  return jsonify({'data': books})


@app.route('/list')
def list():
  keyword = request.args.get('query')
  return render_template('list.html')


if __name__ == '__main__':
  app.run('0.0.0.0', port=5001, debug=True)