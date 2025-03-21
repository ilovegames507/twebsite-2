import header_import from "./utils/header.js";
import footer_import from "./utils/footer.js";

header_import();
footer_import();


document.getElementById('img-link').addEventListener('click', function () {
    window.location.href = '/';
  });
  document.querySelector('.header__bars').addEventListener('click', function () {
    document.querySelector('.header').classList.toggle('header--mobile-open');
  });
  document.getElementById('login-link').addEventListener('click', function () {
    window.location.href = '/login';
  });