// document.addEventListener("DOMContentLoaded", function () {
//     const chatBox = document.getElementById("chat-box");
//     const userForm = document.getElementById("info-form");
//     const userMessageInput = document.getElementById("user-message");
//     const sendMessageButton = document.getElementById("send-message");
//     const formContainer = document.getElementById("user-form");

//     // Handle form submission
//     userForm.addEventListener("submit", function (event) {
//         event.preventDefault();

//         const name = document.getElementById("name").value;
//         const phone = document.getElementById("phone").value;
//         const email = document.getElementById("email").value;
//         const date = document.getElementById("date").value;

//         // Send form data to Flask server
//         fetch("/submit-conversational-form", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json",
//             },
//             body: JSON.stringify({ name: name, phone: phone, email: email, date: date }),
//         })
//         .then(response => response.json())
//         .then(data => {
//             if (data.success) {
//                 alert("Form submitted successfully!");
//                 formContainer.style.display = "none";
//                 chatBox.innerHTML += `<div><strong>Chatbot:</strong> ${data.message}</div>`;
//             } else {
//                 // Show error message when date or input validation fails
//                 alert(data.message);
//             }
//         });
//     });

//     // Handle message sending
//     sendMessageButton.addEventListener("click", function () {
//         const message = userMessageInput.value;
//         if (message.trim() === "") return;

//         // Display user message in chat
//         chatBox.innerHTML += `<div><strong>You:</strong> ${message}</div>`;
//         userMessageInput.value = ""; // Clear input

//         // Send message to Flask backend
//         fetch("/chat", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json",
//             },
//             body: JSON.stringify({ message: message }),
//         })
//         .then(response => response.json())
//         .then(data => {
//             // Handle chatbot response
//             if (data.action === "showCallMeForm") {
//                 chatBox.innerHTML += `<div><strong>Chatbot:</strong> I need your contact information. Please fill in the form.</div>`;
//                 formContainer.style.display = "block";  // Show form if required
//             } else if (data.action === "showAppointmentForm") {
//                 chatBox.innerHTML += `<div><strong>Chatbot:</strong> Let's book an appointment. Please provide your name, phone, email, and date.</div>`;
//                 formContainer.style.display = "block";  // Show form if required
//             } else if (data.response) {
//                 chatBox.innerHTML += `<div><strong>Chatbot:</strong> ${data.response}</div>`;
//             }
//         });
//     });
// });
