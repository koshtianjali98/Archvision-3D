import cv2
import numpy as np
import plotly.graph_objects as go

def process_eye_photo(uploaded_eye_image):
    # --- ORIGINAL LOGO (No Changes) ---
    file_bytes = np.asarray(bytearray(uploaded_eye_image.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (128, 128))

    nb_pts = 100
    theta = np.linspace(0, 2*np.pi, nb_pts)
    phi = np.linspace(0, np.pi, nb_pts)
    
    x = 10 * np.outer(np.cos(theta), np.sin(phi))
    y = 10 * np.outer(np.sin(theta), np.sin(phi))
    z = 10 * np.outer(np.ones(np.size(theta)), np.cos(phi))

    z[z > 8.5] += (z[z > 8.5] - 8.5) * 0.8
    mask_back = z < -9.5
    z[mask_back] -= 15
    x[mask_back] *= 0.3; y[mask_back] *= 0.3

    fig = go.Figure()

    # --- LAYER 1: OUTER SHELL ---
    fig.add_trace(go.Surface(
        x=x, y=y, z=z,
        colorscale=[[0, 'white'], [1, 'white']],
        opacity=0.3, showscale=False, name="Outer Shell"
    ))

    # --- LAYER 2: THE IRIS ---
    fig.add_trace(go.Surface(
        x=x*0.6, y=y*0.6, z=z*0.1 + 8.2,
        surfacecolor=img[:,:,0],
        colorscale='balance', showscale=False, name="Iris Detail"
    ))

    # --- LAYER 3: INTERNAL RETINA & VEINS ---
    fig.add_trace(go.Surface(
        x=x*0.95, y=y*0.95, z=z*0.95,
        colorscale=[[0, 'red'], [1, 'white']],
        surfacecolor=np.random.rand(nb_pts, nb_pts),
        opacity=0.6, showscale=False, name="Internal Anatomy"
    ))

    # --- 🏷️ ADDING ARROWS & LABELS (New Part) ---
    # Hum specific 3D points par text aur lines add kar rahe hain
    labels = [
        {"pos": [0, 0, 13], "text": "Cornea", "color": "cyan"},
        {"pos": [5, 5, 9], "text": "Iris", "color": "yellow"},
        {"pos": [0, -7, -5], "text": "Retina", "color": "red"},
        {"pos": [0, 0, -22], "text": "Optic Nerve", "color": "orange"}
    ]

    for lbl in labels:
        # Arrow line
        fig.add_trace(go.Scatter3d(
            x=[lbl["pos"][0], lbl["pos"][0] * 1.5],
            y=[lbl["pos"][1], lbl["pos"][1] * 1.5],
            z=[lbl["pos"][2], lbl["pos"][2]],
            mode='lines+text',
            text=["", f"<b>{lbl['text']}</b>"], # Bold text at the end of the line
            textfont=dict(color="white", size=14),
            line=dict(color=lbl["color"], width=6),
            showlegend=False
        ))

    # --- SCENE & CAMERA (No Changes) ---
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            bgcolor='black',
            camera=dict(eye=dict(x=1.5, y=1.5, z=0.8)) # Slightly adjusted for better label view
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        template="plotly_dark"
    )
    return fig