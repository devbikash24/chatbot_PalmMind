// Handles form submission for user details
function submitForm() {
    const name = document.getElementById("name").value;
    const phone = document.getElementById("phone").value;
    const email = document.getElementById("email").value;

    // Submit the form data to the backend
    fetch("/submit-form", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: name, phone: phone, email: email })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Details saved successfully!");
            showChatInterface(data.user_info);  // Show the chat interface with user info
        } else {
            alert("Invalid data. Please correct the errors and try again.");
        }
    });
}

// Skips the form and moves to the chat functionality
function skipForm() {
    fetch("/skip_form", {
        method: "POST",
        headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(data => {
        alert("Skipping form. You can still chat with the bot.");
        showChatInterface(data.user_info);  // Show the chat interface with anonymous info
    });
}

// Show the chat interface after form submission or skipping
function showChatInterface(userInfo) {
    console.log("Showing chat interface with user info:", userInfo);  // Debugging statement

    // Hide the form
    document.getElementById("chat-form").style.display = "none";

    // Show the chat interface
    document.getElementById("chat-window").style.display = "block";
    document.getElementById("custome_message").style.display = "block";
    document.getElementById("chat-input-containing").style.display = "flex";
    console.log("Showing chat interfac")
    // Display welcome message with user details
    const welcomeMessage = `Welcome ${userInfo.name}! ${userInfo.phone !== 'N/A' ? 'Your phone: ' + userInfo.phone + '. ' : ''}${userInfo.email !== 'N/A' ? 'Your email: ' + userInfo.email + '.' : ''}`;
    console.log("Welcome message:", welcomeMessage);  // Debugging statement
    addMessage("Palm Bot", welcomeMessage, "bot-message");
}

// Function to add messages to the chat window
function addInitialMessage(sender, message, cssClass) {
    const chatWindow = document.getElementById("chat-window");
    const newMessage = document.createElement("div");
    newMessage.classList.add(cssClass);
    newMessage.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatWindow.appendChild(newMessage);
    chatWindow.scrollTop = chatWindow.scrollHeight; // Auto-scroll to the bottom
}



function sendMessage() {
    const userInput = document.getElementById("userInput").value;
    if (userInput.trim() === "") return;

    addInitialMessage("You", userInput, "user-message");
    // document.getElementById("userInput").value = "";

    // Send the message to the Flask backend
    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        addMessage("Palm Bot", data.response, "bot-message");
    });
}

function addMessage(sender, message, cssClass) {
    const chatWindow = document.getElementById("chat-window");
    const newMessage = document.createElement("div");
    newMessage.classList.add(cssClass);
    newMessage.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatWindow.appendChild(newMessage);
    chatWindow.scrollTop = chatWindow.scrollHeight; // Auto-scroll to the bottom
}
let conversationId = null; // To track the conversation state

// function sendPredefinedMessage(message) {
//     addMessage("You", message, "user-message");

//     fetch("/chat", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ message: message })
//     })
//     .then(response => response.json())
//     .then(data => {
//         addMessage("Palm Bot", data.response, "bot-message");
//     });
// }

// function addMessagenew(author, message, type) {
//     const messageBox = document.createElement("div");
//     messageBox.className = type;
//     // Check if the message is an object and convert it to a string appropriately
//     if (typeof message === 'object' && message !== null) {
//         // Assuming the object is simple and not nested
//         const messageString = Object.entries(message).map(([key, value]) => `${key}: ${value}`).join(", ");
//         messageBox.textContent = `${author}: ${messageString}`;
//     } else {
//         messageBox.textContent = `${author}: ${message}`;
//     }
//     document.getElementById("chat-window").appendChild(messageBox);
// }
// Ensuring DOMContentLoaded to run scripts after the DOM is fully loaded

// Define the function inside a DOMContentLoaded listener to ensure DOM is fully loaded

// document.addEventListener('DOMContentLoaded', function() {
//     // Tracking if forms have been submitted
//     const formSubmitted = {
//         callMeForm: false,
//         appointmentForm: false
//     };

//     // Function to add messages to the chat
//     function addMessage(author, message, type) {
//         const messageBox = document.createElement("div");
//         messageBox.className = type;
//         messageBox.textContent = `${author}: ${message}`;
//         document.getElementById("chat-window").appendChild(messageBox);
//     }

//     // Function to show forms
//     function showForm(formId, message) {
//         if (formSubmitted[formId]) {
//             addMessage("Palm Bot", "You have already submitted this form.", "bot-message");
//             return;
//         }

//         // Hide any previously shown forms first
//         document.getElementById("callMeForm").style.display = "none";
//         document.getElementById("appointmentForm").style.display = "none";

//         // Add a message above the form
//         addMessage("Palm Bot", message, "bot-message");

//         // Show the form
//         var form = document.getElementById(formId);
//         form.style.display = "block";
//         document.getElementById("chat-window").appendChild(form);
//     }

//     // Handle form submission
//     function handleFormSubmit(event) {
//         event.preventDefault(); // Stop the form from submitting normally

//         const formId = event.target.id;
//         if (formSubmitted[formId]) {
//             addMessage("Palm Bot", "You have already submitted this form.", "bot-message");
//             return;
//         }

//         // Extract and serialize form data
//         const formData = new FormData(event.target);
//         const data = {};
//         formData.forEach((value, key) => {
//             data[key] = value;
//         });

//         // Build a meaningful sentence with the data
//         let detailsMessage = "";
//         if (formId === "callMeForm") {
//             detailsMessage = `You have registered your name as ${data.name}, phone number as ${data.phone}, and email as ${data.email}.`;
//         } else if (formId === "appointmentForm") {
//             detailsMessage = `You have booked an appointment under the name ${data.name}, phone number ${data.phone}, email ${data.email}, on ${data.date}.`;
//         }

//         addMessage("You", detailsMessage, "user-message");

//         // Mark the form as submitted
//         formSubmitted[formId] = true;

//         // Optionally, clear or hide the form after submission
//         event.target.style.display = "none";
//     }

//     // Attach submit event handlers to forms
//     document.getElementById("callMeForm").addEventListener("submit", handleFormSubmit);
//     document.getElementById("appointmentForm").addEventListener("submit", handleFormSubmit);

//     // Function to send a predefined message
//     window.sendPredefinedMessage = function(message) {
//         fetch("/chat", {
//             method: "POST",
//             headers: { "Content-Type": "application/json" },
//             body: JSON.stringify({ message: message })
//         })
//         .then(response => response.json())
//         .then(data => {
//             // Use showForm based on the action from the server
//             if (data.action === "showCallMeForm") {
//                 showForm("callMeForm", "Please submit the form to request a call.");
//             } else if (data.action === "showAppointmentForm") {
//                 showForm("appointmentForm", "Please submit the form to get an appointment.");
//             } else {
//                 addMessage("Palm Bot", data.response || "Unhandled response type", "bot-message");
//             }
//         }).catch(error => {
//             console.error("Error handling the response:", error);
//             addMessage("Palm Bot", "Error processing your request", "bot-message");
//         });
//     };
// });

document.addEventListener('DOMContentLoaded', function() {
    const formSubmitted = {
        callMeForm: false,
        appointmentForm: false
    };

    function addMessage(author, message, type) {
        const messageBox = document.createElement("div");
        messageBox.className = type;
        messageBox.textContent = `${author}: ${message}`;
        document.getElementById("chat-window").appendChild(messageBox);
    }

    function showForm(formId, message) {
        if (formSubmitted[formId]) {
            addMessage("Palm Bot", "You have already submitted this form.", "bot-message");
            return;
        }

        document.querySelectorAll('form').forEach(form => form.style.display = 'none');  // Hide all forms

        addMessage("Palm Bot", message, "bot-message");
        const form = document.getElementById(formId);
        form.style.display = "block";
        document.getElementById("chat-window").appendChild(form);
    }

    async function handleFormSubmit(event) {
        event.preventDefault();

        const formId = event.target.id;
        if (formSubmitted[formId]) {
            addMessage("Palm Bot", "You have already submitted this form.", "bot-message");
            return;
        }

        const formData = new FormData(event.target);
        const data = {};
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }

        // Process date if present in the appointment form
        if (formId === "appointmentForm" && data.date) {
            try {
                const response = await fetch('/parse_date', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ date: data.date })
                });
                const parsedData = await response.json();
                data.date = parsedData.date;  // Update the date with the parsed date
            } catch (error) {
                console.error('Error parsing date:', error);
            }
        }

        let detailsMessage = "";
        if (formId === "callMeForm") {
            detailsMessage = `You have registered your name as ${data.name}, phone number as ${data.phone}, and email as ${data.email}.`;
        } else if (formId === "appointmentForm") {
            detailsMessage = `You have booked an appointment under the name ${data.name}, phone number ${data.phone}, email ${data.email}, on ${data.date}.`;
        }

        addMessage("You", detailsMessage, "user-message");
        formSubmitted[formId] = true;
        event.target.style.display = "none";
    }

    document.querySelectorAll("form").forEach(form => {
        form.addEventListener("submit", handleFormSubmit);
    });

    window.sendPredefinedMessage = function(message) {
        fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            if (data.action === "showCallMeForm") {
                showForm("callMeForm", "Please submit the form to request a call.");
            } else if (data.action === "showAppointmentForm") {
                showForm("appointmentForm", "Please submit the form to get an appointment.");
            } else {
                addMessage("Palm Bot", data.response || "Unhandled response type", "bot-message");
            }
        }).catch(error => {
            console.error("Error handling the response:", error);
            addMessage("Palm Bot", "Error processing your request", "bot-message");
        });
    };
});
