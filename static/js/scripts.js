document.addEventListener('DOMContentLoaded', function() {
    const humanCircle = document.querySelector('.human');
    const aiCircle = document.querySelector('.ai');
    const humanMessage = document.getElementById('humanMessage');
    const aiMessage = document.getElementById('aiMessage');
    const humanTerminal = document.getElementById('humanTerminal');
    const aiTerminal = document.getElementById('aiTerminal');
    const audio = document.getElementById('aiAudio');
    let mediaRecorder;
    let audioChunks = [];
    let silenceCounter = 0;
    let analyser;
    let audioContext;

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };
            mediaRecorder.onstop = sendAudioToServer;

            audioContext = new (window.AudioContext || window.webkitAudioContext)();
            analyser = audioContext.createAnalyser();
            analyser.fftSize = 2048;
            const source = audioContext.createMediaStreamSource(stream);
            source.connect(analyser);
        })
        .catch(error => console.error('Error accessing microphone:', error));

    humanCircle.addEventListener('click', startRecording);

    function startRecording() {
        humanCircle.classList.add('speaking');
        audioChunks = [];
        silenceCounter = 0;
        mediaRecorder.start();
        checkSilence();
    }
    function checkSilence() {
        const bufferLength = analyser.fftSize;
        const dataArray = new Float32Array(bufferLength);
        analyser.getFloatTimeDomainData(dataArray);

        fetch('/check-silence', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ audio_chunk: Array.from(dataArray) })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Is silent:', data.is_silent, 'Silence counter:', silenceCounter);

            if (data.is_silent=="true") {
                silenceCounter += 0.2;
                if (silenceCounter >= 1.0) { 
                    console.log('Stopping recording due to silence');
                    mediaRecorder.stop();
                    humanCircle.classList.remove('speaking');
                    return;
                }
            } else {
                silenceCounter = 0;
            }
            
            if (mediaRecorder.state === 'recording') {
                setTimeout(checkSilence, 200);
            }else{
                console.log('Recording Stopped');
            }
        })
        .catch(error => console.error('Error checking silence:', error));
    }
    function sendAudioToServer() {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.wav');

        fetch('/process-audio', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const transcription = data.transcription.trim();
            updateUI('Human', transcription, humanMessage, humanTerminal);
            return fetch('/generate-response', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ transcription })
            });
        })
        .then(response => response.json())
        .then(data => {
            const aiResponse = data.response;
            if (!aiResponse) return;

            updateUI('Jarvis', aiResponse, aiMessage, aiTerminal);
            aiCircle.classList.add('speaking');

            audio.src = data.audio_file;
            audio.play().catch(e => console.error("Audio playback failed:", e));
            audio.onended = () => {
                aiMessage.classList.remove('show-message');
                aiCircle.classList.remove('speaking');
            };
        })
        .catch(error => console.error('Error:', error));
    }

    function updateUI(prefix, message, messageElement, terminalElement) {
        messageElement.textContent = truncateText(message, 25);
        messageElement.classList.add('show-message');
        setTimeout(() => messageElement.classList.remove('show-message'), 3500);

        const newMessage = `<p><span class="prefix">${prefix}: </span>${message}</p>`;
        terminalElement.innerHTML += newMessage;
        terminalElement.scrollTop = terminalElement.scrollHeight;
    }
    function truncateText(text, maxLength) {
        if (text.length <= maxLength) return text;
        return text.substr(0, maxLength - 3) + '...';
    }
    const particlesContainer = document.querySelector('.particles');
    for (let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.animationDelay = `${Math.random() * 15}s`;
        particlesContainer.appendChild(particle);
    }
});