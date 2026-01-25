// Initialize QWebChannel
// The backend object will be available as 'backend'

var backend = null;

window.onload = function () {
    if (typeof qt != 'undefined') {
        new QWebChannel(qt.webChannelTransport, function (channel) {
            backend = channel.objects.backend;
            console.log("Connected to backend: SUCCESS");
        });
    } else {
        console.error("qt is undefined - QWebChannel transport failed");
    }

    const input = document.getElementById('quick-input');

    // Focus management is partly handled by Python injection, but good to have here too
    input.focus();

    input.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            if (backend) {
                backend.close_window();
            } else {
                console.log("Backend not connected yet");
            }
        }
    });

    // Optional: Log on enter
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const text = input.value;
            console.log("Capturing:", text);
            input.value = ""; // Clear
            if (backend) {
                backend.save_content(text); // Save to inbox
            }
        }
    });
}
