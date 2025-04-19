// public/src/utils/main.js

document.addEventListener('DOMContentLoaded', () => {
  // ✅ Dynamically load header and footer
  fetch('/src/header.html')
    .then((res) => res.text())
    .then((html) => {
      document.querySelector('.header').innerHTML = html;
    });

  fetch('/src/footer.html')
    .then((res) => res.text())
    .then((html) => {
      document.querySelector('.footer').innerHTML = html;
    });

  // ✅ Handle Contact Form
  const contactForm = document.querySelector('.contact-form');
  if (!contactForm) return; // Exit if not on a page with the form

  const responseMessage = document.createElement('div');
  contactForm.parentNode.insertBefore(responseMessage, contactForm.nextSibling);

  contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Ensure all fields are available
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone')?.value; // Optional field
    const message = document.getElementById('message').value;

    // Check for missing required fields
    if (!name || !email || !message) {
      responseMessage.className = 'error-message';
      responseMessage.textContent = 'Please fill out all required fields.';
      return;
    }

    const submitBtn = contactForm.querySelector('.submit-btn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Sending...';
    responseMessage.textContent = ''; // Clear any previous message

    try {
      const res = await fetch('/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, email, phone, message })
      });

      const data = await res.json();

      if (res.ok) {
        responseMessage.className = 'success-message';
        responseMessage.textContent = data.message || 'Message sent!';
        contactForm.reset(); // Clear the form
      } else {
        responseMessage.className = 'error-message';
        responseMessage.textContent = data.error || 'Something went wrong.';
      }
    } catch (err) {
      console.error('Submission error:', err);
      responseMessage.className = 'error-message';
      responseMessage.textContent = 'An error occurred while submitting the form.';
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Send Message'; // Reset button text
    }
  });
});
