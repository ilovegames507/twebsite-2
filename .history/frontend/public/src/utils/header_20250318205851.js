const header_import = () => {
    document.addEventListener('DOMContentLoaded', function () {
        const headerPlaceholder = document.querySelector('header.header');
        if (headerPlaceholder) {
            headerPlaceholder.innerHTML = `
                    <div class="header__container">
      <div class="header__title-container"> <img src="https://picsum.photos/1080/1080?random" id="img-link"class="header__logo"
          alt="Marcelins Auto Repair Logo">
        <a href="/" class="header__title">Marcelins Auto Repair</a>
      </div>
      <nav class="header__nav">
        <a class="header__link" href="#pricing">Servies</a>
        <a class="header__link" href="#features">Policy</a>
        <a class="header__link" href="#contact">Contact</a>
        <div class="header__btn-container">
          <button class="header__btn" id="login-link">Login</button>
        </div>
      </nav>

      <button class="header__bars">
        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px">
          <path d="M120-240v-80h720v80H120Zm0-200v-80h720v80H120Zm0-200v-80h720v80H120Z" />
        </svg>
      </button>
    </div>
            `;
        }
    });
};

export default header_import;

document.getElementById('img-link').addEventListener('click', function () {
    window.location.href = '/';
  });
  document.querySelector('.header__bars').addEventListener('click', function () {
    document.querySelector('.header').classList.toggle('header--mobile-open');
  });
  document.getElementById('login-link').addEventListener('click', function () {
    window.location.href = '/login';
  });