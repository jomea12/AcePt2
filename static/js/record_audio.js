let chunks = [];
let recorder;
const recordButton = document.getElementById('recordButton');
const stopButton = document.getElementById('stopButton');
const audioPlayback = document.getElementById('audioPlayback');

recordButton.addEventListener('click', async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    recorder = new MediaRecorder(stream);
    recorder.ondataavailable = e => chunks.push(e.data);
    recorder.onstop = e => {
        const blob = new Blob(chunks, { type: 'audio/wav' });
        chunks = [];
        const url = URL.createObjectURL(blob);
        audioPlayback.src = url;
        const file = new File([blob], "recording.wav", { type: "audio/wav" });
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        document.querySelector('input[type="file"]').files = dataTransfer.files;
    };
    recorder.start();
    recordButton.disabled = true;
    stopButton.disabled = false;
});

stopButton.addEventListener('click', () => {
    recorder.stop();
    recordButton.disabled = false;
    stopButton.disabled = true;
});
