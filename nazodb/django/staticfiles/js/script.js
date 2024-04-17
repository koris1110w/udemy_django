const swiper = new Swiper(".swiper", {
      loop: true, //繰り返しをする
      centeredSlides: true, //アクティブなスライドを中央に表示
      slidesPerView: 5, //スライダーコンテナにスライドを3枚同時表示
      spaceBetween: 16, //スライド間の距離を16pxに
      speed: 600, //スライドの推移時間を600msに
    });