window.addEventListener('load', () => {
  const form = document.querySelector('#pokemon-form');

  form.addEventListener('change', (e) => {
    e.preventDefault();

    if (e.target.type === 'checkbox') {
      const container = e.target.closest('.pokemon-container');

      if (e.target.checked) {
        container.classList.add('grayscale');
      } else {
        container.classList.remove('grayscale');
      };
    };
  });
});