from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np
import torch
from torchvision import transforms
import io
import base64

input_size = 28 * 28

# Cargar el modelo en modo CPU
model = torch.load("mnist_model.pth", map_location=torch.device('cpu'))
model.eval()
model.to("cpu")

# Transformación de la imagen
transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),
    transforms.Resize((28, 28)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

def crop_to_content(image):
            # Convert to numpy array
            img_array = np.array(image)
            
            # Ensure grayscale
            if len(img_array.shape) == 3 and img_array.shape[2] > 1:
                gray = np.array(image.convert('L'))
            else:
                gray = img_array
            
            # Find non-white pixels
            non_white = np.where(gray < 240)
            
            # If no content, return original
            if len(non_white[0]) == 0:
                return image
            
            # Find bounds
            min_y, max_y = np.min(non_white[0]), np.max(non_white[0])
            min_x, max_x = np.min(non_white[1]), np.max(non_white[1])
            
            # Calculate content dimensions
            height = max_y - min_y + 1
            width = max_x - min_x + 1
            
            # Use larger dimension for square
            size = max(height, width)
            
            # Add padding (20% of size)
            padding = int(size * 0.2)
            size += padding * 2
            
            # Find content center
            center_y = (min_y + max_y) // 2
            center_x = (min_x + max_x) // 2
            
            # Calculate square crop coordinates
            left = max(0, center_x - size // 2)
            top = max(0, center_y - size // 2)
            right = min(gray.shape[1], left + size)
            bottom = min(gray.shape[0], top + size)
            
            # Adjust if hitting boundaries
            if right - left < size:
                left = max(0, right - size)
            if bottom - top < size:
                top = max(0, bottom - size)
            
            # Crop and return
            cropped_img = image.crop((left, top, right, bottom))
            return cropped_img

app = FastAPI()

# Habilitar CORS para todas las solicitudes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las URLs
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/predict/")
async def predict(request: Request):
    try:
        data = await request.json()
        image_data = data.get("image")
        if not image_data:
            return {"error": "No image data received"}

        # Decodificar la imagen de Base64
        image_data = image_data.split(",")[1]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))

        # Crop the image to focus on the content
        image = crop_to_content(image)

        # Aplicar las transformaciones
        image = transform(image).unsqueeze(0)
        with torch.no_grad():
            output = model(image)
            _, predicted = torch.max(output, 1)
            prediction = predicted.item()
        return {"prediction": prediction}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=3000)
