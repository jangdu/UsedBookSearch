const toggleBtn = document.querySelector('.navbar__toggleBtn');
const menu = document.querySelector('.navbar__menu');
const icons = document.querySelector('.navbar__icons');
const searcher = document.querySelector('.topnav');
toggleBtn.addEventListener('click', () => {
  menu.classList.toggle('active');
  icons.classList.toggle('acitve');
  searcher.classList.toggle('active');
});

const swiper = new Swiper('.swiper', {
  // Optional parameters
  autoplay: {     //자동슬라이드 (false-비활성화)
    delay: 1500, // 시간 설정
  },

  loop: true,

  // Navigation arrows
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },

  // And if we need scrollbar
  scrollbar: {
    el: '.swiper-scrollbar',
  },
});


