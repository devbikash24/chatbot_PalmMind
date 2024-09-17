document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const callMeForm = document.getElementById("call-me-form");
    const uploadForm = document.getElementById("upload-form");
    const appointmentForm = document.getElementById("appointment-form");
    const queryForm = document.getElementById("query-form");
    const userMessageInput = document.getElementById("user-message");
    const sendMessageButton = document.getElementById("send-message");

    // Handle Call Me form submission
    document.getElementById("call-me-info-form").addEventListener("submit", function (event) {
        event.preventDefault();

        const name = document.getElementById("call-me-name").value;
        const phone = document.getElementById("call-me-phone").value;
        const email = document.getElementById("call-me-email").value;

        // Send Call Me form data to Flask server
        fetch("/submit-call-me-form", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ name: name, phone: phone, email: email }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Call Me request submitted successfully!");
                callMeForm.style.display = "none";
                chatBox.innerHTML += `<div><strong>Chatbot:</strong> ${data.message}</div>`;
            } else {
                alert(data.message);
            }
        });
    });

    // Handle Appointment form submission
    document.getElementById("appointment-info-form").addEventListener("submit", function (event) {
        event.preventDefault();

        const name = document.getElementById("appointment-name").value;
        const phone = document.getElementById("appointment-phone").value;
        const email = document.getElementById("appointment-email").value;
        const date = document.getElementById("appointment-date").value;

        // Send Appointment form data to Flask server
        fetch("/submit-appointment-form", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ name: name, phone: phone, email: email, date: date }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Appointment booked successfully!");
                appointmentForm.style.display = "none";
                chatBox.innerHTML += `<div><strong>Chatbot:</strong> ${data.message}</div>`;
            } else {
                alert(data.message);
            }
        });
    });

    // Handle Document Upload
    document.getElementById("upload-document-form").addEventListener("submit", function (event) {
        event.preventDefault();

        const documentInput = document.getElementById("document").files[0];
        
        const formData = new FormData();
        formData.append('document', documentInput);

        // Send document to Flask server for vectorizing and storing in FAISS
        fetch("/upload-document", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Document uploaded and vectorized successfully!");
                uploadForm.style.display = "none";
                queryForm.style.display = "block";  // Enable querying after upload
                chatBox.innerHTML += `<div><strong>Chatbot:</strong> Document uploaded. You can now query it.</div>`;
            } else {
                alert(data.message);
            }
        });
    });

    // document.getElementById("upload-document-form").addEventListener("submit", function (event) {
    //     event.preventDefault();
    //     const formData = new FormData();
    //     formData.append('document', document.getElementById('document').files[0]);
    
    //     fetch("/upload-document", {
    //         method: "POST",
    //         body: formData  // ensure no Content-Type header is set here
    //     })
    //     .then(response => response.json())
    //     .then(data => {
    //         if (data.success) {
    //             console.log("Upload successful");
    //         } else {
    //             console.error("Upload failed:", data.message);
    //         }
    //     });
    // });
    

    // Handle Document Querying
    document.getElementById("query-document-form").addEventListener("submit", function (event) {
        event.preventDefault();

        const query = document.getElementById("query").value;


        // Send query to Flask server to search in FAISS and get the response
        fetch("/query-document", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ query: query }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                chatBox.innerHTML += `<div><strong>Chatbot:</strong>hhhhhhhhhhhhhhhhhhhhh ${data.message}</div>`;
            } else {
                alert(data.message);
            }
        });
    });

    // Handle message sending
    sendMessageButton.addEventListener("click", function () {
        const message = userMessageInput.value;
        if (message.trim() === "") return;

        // Display user message in chat
        chatBox.innerHTML += `<div><strong>You:</strong> ${message}</div>`;
        userMessageInput.value = ""; // Clear input

        // Send message to Flask backend
        fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: message }),
        })
        .then(response => response.json())
        .then(data => {
            // Handle chatbot response
            if (data.action === "showCallMeForm") {
                chatBox.innerHTML += `<div><strong>Chatbot:</strong> I need your contact information. Please fill in the form.</div>`;
                callMeForm.style.display = "block";  // Show "Call Me" form
                appointmentForm.style.display = "none";  // Hide "Appointment" form
            } else if (data.action === "showAppointmentForm") {
                chatBox.innerHTML += `<div><strong>Chatbot:</strong> Let's book an appointment. Please provide your name, phone, email, and date.</div>`;
                appointmentForm.style.display = "block";  // Show "Appointment" form
                callMeForm.style.display = "none";  // Hide "Call Me" form
            } else if (data.action === "showUploadForm") {
                chatBox.innerHTML += `<div><strong>Chatbot:</strong> Please upload a document to begin.</div>`;
                uploadForm.style.display = "block";  // Show document upload form
                queryForm.style.display = "none";  // Hide query form
            }
             else if (data.response) {
                chatBox.innerHTML += `<div><strong>Chatbot:</strong> ${data.response}</div>`;
            }
        });
    });
});
