// static/script.js
function translateForm() {
  const inputText = document.getElementById('input_text').value;

  fetch('/translate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `input_text=${encodeURIComponent(inputText)}`,
  })
    .then(response => response.json())
    .then(data => {
      document.getElementById('outputText').value = data.translated_text;
    })
    .catch(error => console.error('Error:', error));

  // Prevent the default form submission
  return false;
}

