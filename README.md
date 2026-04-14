🏗️ Arch-Vision 3D: AI-Powered 2D to 3D Reconstruction
Arch-Vision 3D is an innovative tool designed to bridge the gap between 2D imagery and 3D visualization. By leveraging advanced image processing and mathematical mapping, the system converts flat 2D inputs—such as Architectural Blueprints and Anatomical Eye Scans—into interactive, high-fidelity 3D models.

🚀 Key Features
Architectural Extrusion: Automatically detects walls from 2D floor plans and extrudes them into 3D structures with customizable heights.
Medical Visualization: Maps 2D eye images onto spherical 3D models, allowing for detailed visualization of the Cornea and Iris.
Interactive Dashboard: A user-friendly Streamlit interface featuring sliders to control wall height, eye bulge intensity, and layer opacity.
Cloud Integration: Seamlessly saves and retrieves project data using MongoDB Atlas for metadata and AWS S3 for file storage.
Real-time Rendering: Utilizes Plotly and WebGL for smooth, 360-degree model rotation and zooming directly in the browser.

🛠️ Tech Stack
Language: Python 3.9+
Frontend Framework: Streamlit
Visualization Engine: Plotly (WebGL enabled)
Image Processing: OpenCV
Mathematical Computing: NumPy
Database: MongoDB Atlas (NoSQL)
Cloud Storage: Amazon Web Services (AWS S3)

📂 Project Structure
Plaintext
├── app.py              # Main application entry point
├── logic.py            # Core 3D transformation & NumPy algorithms
├── eye_logic.py        # Specialized module for anatomical mapping
├── database.py         # Cloud connectivity for MongoDB & AWS S3
├── requirements.txt    # List of project dependencies
└── samples/            # Folder containing test floor plans and eye scans

🔧 Installation & Setup
Clone the Repository:

Bash
git clone https://github.com/koshtianjali98/Archvision-3D.git
cd Archvision-3D

Install Dependencies:
Bash
pip install -r requirements.txt
Run the Application:

Bash
streamlit run app.py
