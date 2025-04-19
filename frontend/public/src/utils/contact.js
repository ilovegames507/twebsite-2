document.addEventListener('DOMContentLoaded', function () {
  const form = document.querySelector('.contact-form');

  form.addEventListener('submit', async function (e) {
    e.preventDefault();

    const name = form.querySelector('input[name="name"]').value;
    const email = form.querySelector('input[name="email"]').value;
    const phone = form.querySelector('input[name="phone"]').value;
    const message = form.querySelector('textarea[name="message"]').value;

    try {
      const response = await fetch('/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, email, phone, message }),
      });

      const result = await response.json();

      if (response.ok) {
        alert(result.message); // Success!
        form.reset();
      } else {
        alert(result.error || 'Something went wrong.');
      }
    } catch (error) {
      console.error('Submit error:', error);
      alert('Failed to submit. Try again later.');
    }
  });
});
