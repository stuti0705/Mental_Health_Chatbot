let token = "";

// LOGIN
async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const res = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ email, password })
    });

    const data = await res.json();
    console.log(data);
    token = data.access_token;

    document.getElementById("login").style.display = "none";
    document.getElementById("chat").style.display = "block";
}

// SEND MESSAGE
async function sendMessage() {
    const input = document.getElementById("messageInput");
    const message = input.value;

    addMessage(message, "user");

    const res = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({ message })
    });

    const data = await res.json();

    addMessage(data.response, "bot");

    document.getElementById("result").innerHTML = `
        <p><b>Condition:</b> ${data.symptoms_detected.predicted_condition}</p>
        <p><b>Confidence:</b> ${data.symptoms_detected.confidence_score}</p>
        <p class="${data.risk_level === 'HIGH' ? 'high-risk' : ''}">
            <b>Risk:</b> ${data.risk_level}
        </p>
        ${data.crisis_alert ? `<p class="high-risk">${data.emergency_message}</p>` : ""}
    `;

    input.value = "";
}

// ADD MESSAGE
function addMessage(text, type) {
    const msgDiv = document.getElementById("messages");
    const msg = document.createElement("p");
    msg.className = type;
    msg.innerText = text;
    msgDiv.appendChild(msg);
}