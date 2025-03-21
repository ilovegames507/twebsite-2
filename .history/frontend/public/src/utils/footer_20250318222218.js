const footer_import = () => {
    document.addEventListener('DOMContentLoaded', function() {
        const footerPlaceholder = document.querySelector('footer.footer');
        if (footerPlaceholder) {
            footerPlaceholder.innerHTML = `
                <div class="footer__container">
      <div class="footer__content">
        <div class="footer__section">
          <h3 class="footer__heading">Contact Us</h3>
          <p class="footer__text">123 Auto Repair Street</p>
          <p class="footer__text">Cityville, ST 12345</p>
          <p class="footer__text">Phone: (555) 123-4567</p>
          <p class="footer__text">Email: contact@marcelinsauto.com</p>
        </div>

        <div class="footer__section">
          <h3 class="footer__heading">Hours</h3>
          <p class="footer__text">Mon-Fri: 8am - 6pm</p>
          <p class="footer__text">Saturday: 9am - 4pm</p>
          <p class="footer__text">Sunday: Closed</p>
        </div>

        <div class="footer__section">
          <h3 class="footer__heading">Quick Links</h3>
          <a href="#services" class="footer__link">Services</a>
          <a href="#policy" class="footer__link">Policy</a>
          <a href="/contact" class="footer__link">Contact</a>
          <a href="/about" class="footer__link">About Us</a>
        </div>

        <div class="footer__section">
          <h3 class="footer__heading">Follow Us</h3>
          <div class="footer__socials">
            <a href="#" class="footer__social-link" aria-label="TicTok">
              <img src="src/Images/tictok.svg" alt="TicTok">
            </a>
            <a href="#" class="footer__social-link" aria-label="Instagram">
              <img src="src/Images/instagram.svg" alt="Instagram">
            </a>
            <a href="#" class="footer__social-link" aria-label="YouTube">
              <img src="src/Images/youtube.svg" alt="YouTube">
            </a>
          </div>
        </div>
      </div>

      <div class="footer__bottom">
        <p class="footer__copy">&copy; 2024 Marcelins Auto Repair. All rights reserved.</p>
      </div>
    </div>
            `;
        }
    });
};

export default footer_import;