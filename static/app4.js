document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const forms = {
        callMeForm: document.getElementById("call-me-form"),
        uploadForm: document.getElementById("upload-form"),
        appointmentForm: document.getElementById("appointment-form"),
        queryForm: document.getElementById("query-form"),
    };
    const userMessageInput = document.getElementById("user-message");
    const sendMessageButton = document.getElementById("send-message");

    // Action buttons
    const actionButtons = {
        callMeButton: document.getElementById("call-me-button"),
        bookAppointmentButton: document.getElementById("book-appointment-button"),
        queryDocumentButton: document.getElementById("query-document-button"),
    };

    // Utility function to display messages in the chat
    const displayMessage = (sender, message) => {
        const messageElement = document.createElement("div");
        messageElement.classList.add("chat-message");
        messageElement.innerHTML = `<div class="${sender === 'Chatbot' ? 'chatbot-message' : 'user-message'}"><strong>${sender}: </strong>${message}</div>`;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the bottom
    };

    // Display initial Chatbot message
    displayMessage("Chatbot", "I can help you with bookings, calling, or answering your queries.");

    // Function to toggle form visibility
    const showForm = (formToShow) => {
        Object.values(forms).forEach(form => form.style.display = "none");
        if (formToShow) formToShow.style.display = "block";
    };

    // Handle form submissions
    const handleSubmit = (formId, endpoint, formData) => {
        fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(`${formId.replace(/-/g, ' ')} submitted successfully!`);
                showForm(null);
                displayMessage("Chatbot", data.message);
            } else {
                alert(data.message);
            }
        });
    };

    // Button click handlers
    actionButtons.callMeButton.addEventListener("click", () => {
        displayMessage("You", "I want to be called back.");
        displayMessage("Chatbot", "Please provide your contact details below.");
        showForm(forms.callMeForm);
    });

    actionButtons.bookAppointmentButton.addEventListener("click", () => {
        displayMessage("You", "I want to book an appointment.");
        displayMessage("Chatbot", "Please provide your appointment details below.");
        showForm(forms.appointmentForm);
    });

    actionButtons.queryDocumentButton.addEventListener("click", () => {
        displayMessage("You", "I want to query a document.");
        displayMessage("Chatbot", "Please upload a document or ask your question below.");
        showForm(forms.uploadForm);
    });

    // Form submission handlers
    document.getElementById("call-me-info-form").addEventListener("submit", (event) => {
        event.preventDefault();
        const formData = {
            name: document.getElementById("call-me-name").value,
            phone: document.getElementById("call-me-phone").value,
            email: document.getElementById("call-me-email").value,
        };
        handleSubmit("call-me-info-form", "/submit-call-me-form", formData);
    });

    document.getElementById("appointment-info-form").addEventListener("submit", (event) => {
        event.preventDefault();
        const formData = {
            name: document.getElementById("appointment-name").value,
            phone: document.getElementById("appointment-phone").value,
            email: document.getElementById("appointment-email").value,
            date: document.getElementById("appointment-date").value,
        };
        handleSubmit("appointment-info-form", "/submit-appointment-form", formData);
    });

    document.getElementById("upload-document-form").addEventListener("submit", (event) => {
        event.preventDefault();
        const documentInput = document.getElementById("document").files[0];
        const formData = new FormData();
        formData.append('document', documentInput);

        fetch("/upload-document", { method: "POST", body: formData })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Document uploaded and vectorized successfully!");
                displayMessage("Chatbot", "Document uploaded. You can now query it.");
                showForm(forms.queryForm);
            } else {
                alert(data.message);
            }
        });
    });

    document.getElementById("query-document-form").addEventListener("submit", (event) => {
        event.preventDefault();
        const query = document.getElementById("query").value;
        displayMessage("You", query);

        fetch("/query-document", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayMessage("Chatbot", data.message);
            } else {
                alert(data.message);
            }
        });
    });

    // Handle generic message sending
    sendMessageButton.addEventListener("click", () => {
        const message = userMessageInput.value.trim();
        if (!message) return;

        displayMessage("You", message);

        fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.action) {
                const actionMap = {
                    showCallMeForm: forms.callMeForm,
                    showAppointmentForm: forms.appointmentForm,
                    showUploadForm: forms.uploadForm,
                };
                displayMessage("Chatbot", "Please fill in the form.");
                showForm(actionMap[data.action]);
            } else if (data.response) {
                displayMessage("Chatbot", data.response);
            }
        });
    });
});
