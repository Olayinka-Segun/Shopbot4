document.addEventListener('DOMContentLoaded', function () {
    const chatForm = document.getElementById('chat-form');
    const chatBox = document.getElementById('chat-box');
    const messageInput = document.getElementById('message');

    chatForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const userMessage = messageInput.value;

        // Display user message
        chatBox.innerHTML += `<div class="message user-message"><p>${userMessage}</p></div>`;
        messageInput.value = '';

        // Submit form via AJAX
        fetch(chatForm.action, {
            method: 'POST',
            body: new URLSearchParams(new FormData(chatForm)),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        })
        .then(response => response.text())
        .then(data => {
            // Update chat box with response
            chatBox.innerHTML += `<div class="message bot-message"><p>${data}</p></div>`;
            chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
        });
    });
});
