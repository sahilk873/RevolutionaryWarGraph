// Get references to HTML elements
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const chatLog = document.getElementById('chat-log');
const contextSlider = document.getElementById('context-slider');
const sliderValueDisplay = document.getElementById('slider-value');

// Update the displayed slider value in real-time
contextSlider.addEventListener('input', function() {
    sliderValueDisplay.textContent = contextSlider.value;
});

// Event listener for 'Send' button click
sendBtn.addEventListener('click', sendMessage);

// Event listener for pressing 'Enter' key in the input field
userInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const message = userInput.value.trim();
    if (message === '') return;

    // Display the user's message
    addMessage('You', message, 'user-message');
    userInput.value = ''; // Clear the input field

    // Show typing indicator
    showTypingIndicator();

    // Get the number of query vectors from the slider
    const numMatches = parseInt(contextSlider.value, 10);

    // Send the message to the backend with the number of query vectors
    fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: message, num_matches: numMatches })
    })
    .then(response => response.json())
    .then(data => {
        hideTypingIndicator(); // Hide typing indicator after receiving response
        addMessage('RevolutionaryWarChat', data.answer, 'bot-message', data.context);
    })
    .catch(error => {
        hideTypingIndicator();
        addMessage('RevolutionaryWarChat', 'Sorry, an error occurred.', 'bot-message');
        console.error('Error:', error);
    });
}

function addMessage(sender, text, className, contextArray = []) {
    const messageElem = document.createElement('div');
    messageElem.className = `${className} message`;

    // Add the main response text
    messageElem.innerHTML = `<strong>${sender}:</strong> ${text}`;

    // Add context dropdown if contextArray has items
    if (contextArray.length > 0) {
        const contextButton = document.createElement('button');
        contextButton.className = 'context-button';
        contextButton.innerText = 'Show Context Vectors';
        
        // Create the context container
        const contextElem = document.createElement('div');
        contextElem.className = 'context-message';
        contextElem.innerHTML = contextArray.join('<br>');

        // Toggle context visibility on button click
        contextButton.addEventListener('click', () => {
            if (contextElem.style.display === 'none' || contextElem.style.display === '') {
                contextElem.style.display = 'block';
                contextButton.innerText = 'Hide Context Vectors';
            } else {
                contextElem.style.display = 'none';
                contextButton.innerText = 'Show Context Vectors';
            }
        });

        // Append the button and context container to the message
        messageElem.appendChild(contextButton);
        messageElem.appendChild(contextElem);
    }

    chatLog.appendChild(messageElem);
    chatLog.scrollTop = chatLog.scrollHeight; // Scroll to the bottom
}

// Show typing indicator
function showTypingIndicator() {
    const typingIndicator = document.createElement('div');
    typingIndicator.id = 'typing-indicator';
    typingIndicator.className = 'bot-message message';
    typingIndicator.innerHTML = `
        <strong>ChatGPT:</strong> 
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
    `;
    chatLog.appendChild(typingIndicator);
}

// Hide typing indicator
function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}
