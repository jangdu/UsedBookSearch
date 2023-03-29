// 알라딘에 신간 리스트 
let static_json2 =
    'http://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey=ttbliujjang1711001&QueryType=Bestseller&MaxResults=1&start=1&SearchTarget=Book&output=js&Version=20131101';


$.ajax({
    url: static_json2,
    dataType: 'jsonp',
    jsonpCallback: 'myCallback',
    success: function (data) {
        let items = data['item'][0];
        let cover_p = items['cover'].replace('sum', '500')
        let title = items['title']
        let author = items['author']
        let b_link = items['link']

        document.getElementById("best_img").src = cover_p;
        document.getElementById("bestseller").innerHTML = " 도서 제목 : " + items['title'];

    }
});