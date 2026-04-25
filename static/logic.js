const chatBox = document.getElementById('chat-box');
const status = document.getElementById('status');
const pdfInput = document.getElementById('pdf-input');
const uploadBtn = document.getElementById('upload-btn');
const sendBtn = document.getElementById('send-btn');
const queryInput = document.getElementById('query-input');

function appendMessage(role, text) {
    const msgDiv = document.createElement('div');

    msgDiv.className = `message ${role}`;
    msgDiv.innerText = text;

    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

uploadBtn.addEventListener('click', async () => {
    if (pdfInput.files.length === 0) {
        return alert("Select files first!");
    }

    status.innerText = "Indexing documents...";
    uploadBtn.disabled = true;

    const formData = new FormData();

    for (let file of pdfInput.files) {
        formData.append("files", file);
    }

    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();

    status.innerText = "Documents indexed";
    uploadBtn.classList.add("indexed");
    uploadBtn.innerText = "Indexed";

    appendMessage('bot', data.message);
});

async function handleQuery() {
    const query = queryInput.value.trim();

    if (!query) return;

    appendMessage('user', query);
    queryInput.value = "";

    const formData = new FormData();
    formData.append("query", query);

    const response = await fetch('/ask', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();

    appendMessage('bot', data.answer);
}

sendBtn.addEventListener('click', handleQuery);

queryInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleQuery();
    }
});