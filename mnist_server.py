# pip install requests 
# VAMOS A CREAR API REST DONDE SIRVA EL MODELO ENTRENADO
# Despues interface web para subir imagenes y que el modelo las clasifique
# Por ulitmo, crear dockerfile y desplegarlo en la nube

from fastapi import FastAPI, File, UploadFile
from PIL import Image
import torch
from torchvision import transforms
from models import MLP
import io


input_size = 28*28

# model  = torch.load("mnist_model.pth")
model = torch.load("mnist_model.pth", map_location=torch.device('cpu'))
model.eval()
model.to("cpu")

## Canalizar la imagen de entrada
transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1), # Convertir a escala de grises
    transforms.Resize((28, 28)), # Cambppiar tamaño a 28x28
    transforms.ToTensor(), # Convertir a tensor 
    transforms.Normalize((0.5,), (0.5,)) # Normalizar
])

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))
    image = transform(image).unsqueeze(0) # Añadir dimensión de batch
    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)
        prediction = predicted.item()
        print(f"Prediction: {prediction}")
    return {"prediction": prediction}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3000)