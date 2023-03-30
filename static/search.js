let page = 1;
let firstGetBool = true;
let loading = true;
const urlParams = new URL(location.href).searchParams;

function handleSearchFormEnterKey(keyword) {
  firstGetBool = true;
  $("input[name=query]").attr("value", keyword);
  window.open("?" + "query=" + keyword, "_self");
  loadBooks(keyword);
  scroll();
}

function onClickBookTitle(e) {
  location.replace(`/information?id=${e}`);
}

$(document).ready(function (data) {
  event.preventDefault();
  firstGetBool = true;
  //console.log(urlParams.get('query'))

  $("input[name=query]").attr("value", urlParams.get("query"));
  loadBooks(urlParams.get("query"));
  scroll();
});

function scroll() {
  $(window).scroll(async function () {
    if ($(window).scrollTop() + $(window).height() >= $(document).height() - 300) {
      if (loading) {
        loading = false;
        firstGetBool = false;
        let html = `
          <div class="spinner-border mb-4" role="status">
            <span class="sr-only">Loading...</span>
          </div>`;
        $("#loading").append(html);
        await loadBooks();
        setTimeout(function () {
          loading = true;
          firstGetBool = false;
          $("#loading").empty();
        }, 3000); // 1초 지연시간 설정
      }
    }
  });
}
$("form").on("submit", function (event) {
  event.preventDefault();
  if ($('input[name="query"]').val()==''){
    const html = `
    <div class="alert alert-warning alert-dismissible fade show" role="alert">
      <strong>검색어를 입력해주세요!</strong>
    </div>
    `
    $("#none_key").append(html);
    setTimeout(() => {
      $("#none_key").empty();
    }, 3000);
  }else{
    firstGetBool = true;
    loadBooks();
    scroll();
  }
});

async function loadBooks(key) {
  if (firstGetBool) {
    page = 1;
    $("#search-result").empty();
  } else page += 1;
  $.ajax({
    data: {
      query: key === undefined ? $('input[name="query"]').val() : key,
      page: page,
    },
    type: "GET",
    url: "/search",
  }).done(function (data) {
    data = data.data;
    total = data.total;
    if (data.length > 0) {
      $.each(data, function (i, book) {
        //var html = '<li>' + book.title + ' / ' + book.author + '</li>'
        var image_url = book.cover_url.replace("coversum", "cover500");
        var html = `<div class="row cards list-wrap d-flex justify-content-center">
              <div class="col">
                <div class="banner" style="background-image: url('${image_url}'); width:150px; height:200px; background-size : contain; background-size: 100% 100%;">
                </div>
              </div>
              <div id="search-result" class="bg-transparent col-6" style="width: 600px; margin: 10px;">
                <div class="card bg-transparent">
                  <h3 class="card-header book_title" onClick='onClickBookTitle(${book.book_id})'>${book.title}</h3>
                  <div class="card-body book_detail">
                    <p class="card-text">${book.author}</p>
                    <p class="card-text">가격 : ${book.price}</p>
                  </div>
                </div>
              </div>
            </div>`;
        $("#search-result").append(html);
      });
    } else {
      var html = firstGetBool ? '<p class="mt-4">검색 결과가 없습니다.</p>' : '<p class="mt-4">더이상 검색 결과가 없습니다.</p>';
      $("#search-result").append(html);
      $("#loading").empty();
      $(window).off("scroll");
    }
  });
}
