// 알라딘에 신간 리스트 요청 하는 코드
let static_json =
    'http://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey=ttbliujjang1711001&QueryType=ItemNewAll&MaxResults=1&start=1&SearchTarget=Book&output=js&Version=20131101';


$.ajax({
    url: static_json,
    dataType: 'jsonp',
    jsonpCallback: 'myCallback',
    success: function (data) {
        let items = data['item'][0];
        let cover_p = items['cover'].replace('sum', '500');
        let b_link =`/information?id=`+items['itemId'];

        document.getElementById("new_img").src = cover_p;
        
        document.getElementById("newbook_name").innerHTML = items['title'];
        document.getElementById("newbook_author").innerHTML = items['author'].replace('(지은이)', '');
        document.getElementById("newbook_des").innerHTML = items['description'];
        document.getElementById("newbook_link").onclick= function(){window.open(b_link);};
    }
    


    }
);
