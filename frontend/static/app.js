const canvas = document.getElementById('drawing-canvas');
const ctx = canvas.getContext('2d');
let drawing = false;

// Eventos de dibujo
canvas.addEventListener('mousedown', () => drawing = true);
canvas.addEventListener('mouseup', () => drawing = false);
canvas.addEventListener('mousemove', draw);

function draw(event) {
    if (!drawing) return;
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    ctx.fillStyle = 'white';
    ctx.fillRect(x, y, 20, 20);
}

function clearCanvas() {
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

// Inicializa el lienzo en negro
clearCanvas();

async function predict() {
    const imageData = canvas.toDataURL('image/png');
    try {
        const response = await fetch('http://127.0.0.1:3000/predict/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData })
        });
        const result = await response.json();
        document.getElementById('prediction-result').textContent = 'Predicción: ' + result.prediction;
    } catch (error) {
        console.error('Error:', error);
    }
}

// Asignación de eventos a los botones
document.getElementById('predict-btn').addEventListener('click', predict);
document.getElementById('clear-btn').addEventListener('click', clearCanvas);
