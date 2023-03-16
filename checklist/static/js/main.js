// Get a reference to the form element
const form = document.querySelector('#pokemon-form');

// Add an event listener to the form submit event
form.addEventListener('submit', event => {
  // Prevent the default form submission behavior
  event.preventDefault();

  // Serialize the form data into a URL-encoded string
  const formData = new URLSearchParams(new FormData(form));

  // Send a POST request to the server to update the "completed" attribute
  fetch(form.action, {
    method: form.method,
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: formData,
  })
  .then(response => response.json())
  .then(data => {
    // If the update was successful, remove the grayscale filter from the corresponding containers
    const containers = document.querySelectorAll('.pokemon-container');
    for (const container of containers) {
      const pk = container.querySelector('[name="pk"]').value;
      const completed = container.querySelector('[name="completed"]').checked;
      if (data[pk] === completed) {
        container.classList.remove('grayscale');
      } else {
        container.classList.add('grayscale');
      }
    }
  });
});

// Get the value of a cookie by name
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}