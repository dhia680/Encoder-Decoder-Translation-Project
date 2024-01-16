// static/script.js
function translate() {
  const inputText = document.getElementById('inputText').value;

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
}
