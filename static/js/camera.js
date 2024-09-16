const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('captureButton');
const resultContainer = document.getElementById('emotion-result');
const context = canvas.getContext('2d');

// Access the camera
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
  })
  .catch(err => {
    console.error("Error accessing the camera: ", err);
  });

// Capture the frame and send it to the Flask backend
captureButton.addEventListener('click', () => {
    // Draw the video frame to the canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL('image/png');

    // Send the image to the Flask app for emotion detection
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: imageData })
    })
    .then(response => response.json())
    .then(data => {
        if (data.emotion) {
            // Display the detected emotion as a string
            resultContainer.innerText = data.emotion;
        } else {
            resultContainer.innerText = `Error: ${data.error}`;
        }
    })
    .catch(error => {
        console.error("Error:", error);
        resultContainer.innerText = "Error detecting emotion.";
    });
});
