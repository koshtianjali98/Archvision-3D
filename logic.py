import cv2
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from sklearn.linear_model import LinearRegression

# --- MODULE A: IMAGE TO 3D ---
def process_floorplan(image_file):
    # Read image from streamlit upload
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Canny Edge Detection
    edges = cv2.Canny(gray, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=50, maxLineGap=10)
    
    return lines, img.shape

def generate_3d_plot(lines, img_shape):
    fig = go.Figure()
    wall_height = 40  # Height thodi badha di hai real look ke liye
    thickness = 4     # Isse walls solid (moti) dikhengi

    if lines is not None:
        # 1. Background Ground Plane (Dark Navy/Gray)
        # Isse wo "Floor" wali feel aayegi jo image mein hai
        fig.add_trace(go.Mesh3d(
            x=[0, img_shape[1], img_shape[1], 0],
            y=[0, 0, img_shape[0], img_shape[0]],
            z=[-1, -1, -1, -1],
            color='#1a2433', opacity=1.0, showlegend=False
        ))

        for line in lines:
            x1, y1, x2, y2 = line[0]
            
            # --- TEAL SOLID WALLS (Extrusion) ---
            fig.add_trace(go.Mesh3d(
                # 8 points for a solid 3D Box
                x=[x1, x2, x2, x1, x1, x2, x2, x1],
                y=[y1, y2, y2+thickness, y1+thickness, y1, y2, y2+thickness, y1+thickness],
                z=[0, 0, 0, 0, wall_height, wall_height, wall_height, wall_height],
                
                # Face indices to make it a solid block
                i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
                j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
                k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
                
                color='#008080', # Teal Color
                opacity=0.7,    # Translucent look
                flatshading=True,
                name="Wall"
            ))

            # --- WHITE WIREFRAME HIGHLIGHTS ---
            # Isse wo "Vector Line" wala effect aayega
            fig.add_trace(go.Scatter3d(
                x=[x1, x2], y=[y1, y2], z=[wall_height, wall_height],
                mode='lines',
                line=dict(color='white', width=5),
                showlegend=False
            ))

    # Dark Theme Setup matching the screenshot
    fig.update_layout(
        template="plotly_dark",
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=True, range=[0, wall_height+20], title=""),
            bgcolor='black', # Pure black background
            aspectmode='data'
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        title="Archvision 3D: Neural Layout Conversion"
    )
    return fig

# --- MODULE B: ML PRICE PREDICTION ---
def train_price_model(csv_path):
    try:
        df = pd.read_csv(csv_path)
        # Assuming CSV has 'SquareFeet', 'Bedrooms', and 'Price' columns
        X = df[['SquareFeet', 'Bedrooms']]
        y = df['Price']
        model = LinearRegression().fit(X, y)
        return model
    except Exception as e:
        print(f"Error training model: {e}")
        return None

def predict_price(model, area, bhk):
    """
    This function was missing in your logic.py which caused the AttributeError.
    It takes the trained model and returns the prediction.
    """
    if model is not None:
        prediction = model.predict([[area, bhk]])
        return prediction[0]
    else:
        # Fallback calculation if model fails to train (e.g., 5000 per sqft)
        return area * 5000 + (bhk * 200000)
    
def add_door_or_window(fig, x, y, z_start, z_end, type="window"):
    # Window ke liye Blue Glass look
    if type == "window":
        color = "lightblue"
        opacity = 0.3
    # Door ke liye Brown Wood look
    else:
        color = "#8B4513" # Brown
        opacity = 1.0

    fig.add_trace(go.Mesh3d(
        x=[x, x+2, x+2, x], y=[y, y, y+2, y+2],
        z=[z_start, z_start, z_end, z_end],
        color=color, opacity=opacity
    ))

    def generate_3d_eye(image_file):
    # 1. Circle Detection (Iris dhundna)
    # Maan lo humne iris ka center (cx, cy) aur radius (r) nikal liya
     cx, cy, r = 100, 100, 50 
    
    # 2. 3D Sphere Data Banana
    phi = np.linspace(0, 2*np.pi, 50)
    theta = np.linspace(0, np.pi, 50)
    
    # Sphere ke coordinates
    x = r * np.outer(np.cos(phi), np.sin(theta))
    y = r * np.outer(np.sin(phi), np.sin(theta))
    z = r * np.outer(np.ones(np.size(phi)), np.cos(theta))

    # 3. Plotly par 3D Eye dikhana
    fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, 
                                     colorscale='tealrose', # Iris ka color
                                     showscale=False)])
    
    fig.update_layout(title="2D Image to 3D Eye Reconstruction",
                      scene=dict(bgcolor='black'),
                      template="plotly_dark")
    return fig