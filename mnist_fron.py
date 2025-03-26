import streamlit as st
import requests
from PIL import Image
import io

API_ENDPOIMT = 'http://127.0.0.1:3000/predict'

def st_canvas(fill_color, stroke_width, stroke_color, background_color, height, width, drawing_mode,key):
    from streamlit_drawable_canvas import st_canvas as st_canvas_component
    return st_canvas_component(
        fill_color=fill_color,
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=background_color,
        height=height,
        width=width,
        drawing_mode=drawing_mode,
        key=key,
    )

        
st.title("MNIST Classifier")
canvas = st_canvas(
    fill_color='black',
    stroke_width=20,
    stroke_color='white',
    background_color='black',
    height=500,
    width=500,
    drawing_mode='freedraw',
    key='canvas'
)

if st.button("Predict"):
    if canvas.image_data is not None:
        image = Image.fromarray(canvas.image_data.astype('uint8'))
        image = image.convert('L')
        image = image.resize((28, 28))
        image_bytes = io.BytesIO() # BytesIO object to write image data
        image.save(image_bytes, format='PNG')
        image_bytes = image_bytes.getvalue()

        files = {'file': ('image.png', image_bytes, 'image/png')}
        response = requests.post(API_ENDPOIMT, files=files)

        if response.status_code == 200:
            prediction = response.json()['prediction']
            st.write(f"Prediction: {prediction}")
        else:
            st.error("Error making prediction")
    else:
        st.warning("Please draw a digit before making a prediction")
       