// STATE MANAGEMENT

function getDemoPhoneNumber() {
    const prefix = "~"; // start with a tilde for demo numbers
    const phoneNumber = prefix + Math.floor(Math.random() * 100000000000).toString().padStart(11, '0');
    return phoneNumber;
}

function getState() {
    const number = localStorage.getItem('number');
    const messages = localStorage.getItem('messages');
    if (!number) {
        const newNumber = getDemoPhoneNumber();
        localStorage.setItem('number', newNumber);
        localStorage.setItem('messages', '');
        return { number: newNumber, messages: '' };
    }
    return { number, messages };
}

function addMessage(message, friend = true) {
    const chatbox = document.getElementById('chatbox');
    const sender = friend ? "Friend" : "You";
    chatbox.innerHTML += `<div><b>${sender}:</b> ${message}</div>`;
    chatbox.scrollTop = chatbox.scrollHeight; // Scroll to bottom
    localStorage.setItem('messages', chatbox.innerHTML);
}

// PAGE LOADING

function onLoad() {
    const { messages } = getState();
    const chatbox = document.getElementById('chatbox');
    chatbox.innerHTML = messages;
    console.log('loaded' + chatbox.innerHTML);
    chatbox.scrollTop = chatbox.scrollHeight;
}
document.addEventListener('DOMContentLoaded', onLoad);

// FUNCTIONS CALLED FROM UI

function sendMessage() {
    const { number } = getState();
    const userInput = document.getElementById('userInput').value;
    const chatbox = document.getElementById('chatbox');

    if (userInput.trim() === '') return;

    // Append user message to chatbox
    addMessage(userInput, false);

    // Clear input field
    document.getElementById('userInput').value = '';

    // Send message to Flask backend
    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userInput, number })
    })
    .then(response => response.json())
    .then(data => {
        // Append chatbot response to chatbox
        addMessage(data.response, true);
    });
}

function resetState() {
    localStorage.removeItem('number');
    localStorage.removeItem('messages');
    window.location.reload();
}