from flask import Flask, render_template, jsonify, request, json
application = app = Flask(__name__)
import requests
from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.3wu806l.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsprata
# import certifi

# ca = certifi.where()

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/review')
def review():
    return render_template('review.html')

@app.route('/list_p')
def list_p():
    return render_template('list.html')

@app.route('/information')
def information():
    return render_template('information.html')



books = []

# def search_book(keyword, page):
#     url = 'https://www.aladin.co.kr/ttb/api/ItemSearch.aspx'
#     params = {
#         'ttbkey': 'ttbjjd03241934001',
#         'Query': keyword,
#         'start': (page-1) * 10 + 1,
#         'SearchTarget':'Book',
#         'maxResults': 10,
#         'output': 'js',
#         'Version': '20131101'
#     }
#     res = requests.get(url, params=params)
#     result = res.json()
#     return result['item'], result['totalCount']

@app.route('/search')
def search():
    query = request.args.get('query')
    page = request.args.get('page', type=int, default=1)
    print(request.headers['Referer'].find('index'))

    # 알라딘 검색 API에서 검색어에 대한 검색 결과를 받아옴
    api_key = 'ttbjjd03241934001'
    book_id = ''
    url = f'http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey={api_key}&Query={query}&MaxResults=10&SearchTarget=Book&start={(page)}&output=js&Version=20131101'

    # detail_url = f'http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx?ttbkey={api_key}&itemIdType=ISBN&ItemId={book_id}&output=xml&Version=20131101&OptResult=ebookList,usedList,reviewList'
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
        'book_id' : book_id,
        }
        books.append(book)
    
    # print(data)
    return jsonify({'data': books})


@app.route('/list')
def list_j():
    return render_template('list.html')


## API 역할을 하는 부분
@app.route('/htry', methods=['POST'])
def write_review():
    title_receive = request.form['title_give']
    review_receive = request.form['review_give']
    doc = {
        'title' : title_receive,
        'review' : review_receive
    }
    db.bookreview.insert_one(doc)
    return jsonify({'msg': '저장완료'})

@app.route('/htry', methods=['GET'])
def get_review():
    all_comments = list(db.bookreview.find({}, {'_id':False}))
    return jsonify({'htry': all_comments})


if __name__ == '__main__':
    app.run()