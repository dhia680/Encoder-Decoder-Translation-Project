const promptForm = document.getElementById("prompt-form");
const submitButton = document.getElementById("submit-button");
const questionButton = document.getElementById("question-button");
const messagesContainer = document.getElementById("messages-container");
const darkmodeButton = document.getElementById("darkmode-button");
const historyButton = document.getElementById("history-button");
const chatButton = document.getElementById("chat-button");
const body = document.getElementById("body")
const form = document.getElementById("form");
mode = "light";

const appendHumanMessage = (message) => {
  const humanMessageElement = document.createElement("div");
  humanMessageElement.classList.add("message", "message-human");
  humanMessageElement.innerHTML = message;
  messagesContainer.appendChild(humanMessageElement);
};

const appendAIMessage = async (messagePromise) => {
  // Add a loader to the interface
  const loaderElement = document.createElement("div");
  loaderElement.classList.add("message");
  loaderElement.innerHTML =
    "<div class='loader'><div></div><div></div><div></div>";
  messagesContainer.appendChild(loaderElement);

  // Await the answer from the server
  const messageToAppend = await messagePromise();

  // Replace the loader with the answer
  loaderElement.classList.remove("loader");
  loaderElement.innerHTML = messageToAppend;
};

const handlePrompt = async (event) => {
  event.preventDefault();
  // Parse form data in a structured object
  const data = new FormData(event.target);
  promptForm.reset();

  let url = "/prompt";
  if (questionButton.dataset.question !== undefined) {
    url = "/answer";
    data.append("question", questionButton.dataset.question);
    delete questionButton.dataset.question;
    questionButton.classList.remove("hidden");
    submitButton.innerHTML = "Message";
  }

  appendHumanMessage(data.get("prompt"));

  await appendAIMessage(async () => {
    const response = await fetch(url, {
      method: "POST",
      body: data,
    });
    const result = await response.json();
    return result.answer;
  });
};

promptForm.addEventListener("submit", handlePrompt);

const handleQuestionClick = async (event) => {
  appendAIMessage(async () => {
    const response = await fetch("/question", {
      method: "GET",
    });
    const result = await response.json();
    const question = result.answer;

    questionButton.dataset.question = question;
    questionButton.classList.add("hidden");
    submitButton.innerHTML = "Répondre à la question";
    return question;
  });
};

const handleDarkmodeClick = async (event) => {
  if (mode == "light") {
    body.classList.remove("lightmode");
    body.classList.add("darkmode");
    mode = "dark";
  }
  else {
    body.classList.remove("darkmode");
    body.classList.add("lightmode");
    mode = "light"
  }
  return;
}

const currentPath = window.location.pathname;

const handleHistoryClick = () => {
  if (currentPath !== '/chat-history') {
    window.location.href = '/chat-history'; // Redirige vers l'URL '/chat-history'
  }
};

const handleChatClick = () => {
  window.location.href = '/'; // Redirige vers l'URL '/'
};

questionButton.addEventListener("click", handleQuestionClick);
darkmodeButton.addEventListener("click", handleDarkmodeClick);
historyButton.addEventListener("click", handleHistoryClick);
chatButton.addEventListener("click", handleChatClick);

form.addEventListener("submit", async function (e) {
  e.preventDefault();
  const formData = new FormData(e.target);
  await fetch("/upload", {
    method: "POST",
    body: formData,
  });
  // On réinitialise le formulaire
  form.reset();
});
