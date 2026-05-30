import urllib.request
import bz2
import os

models_to_download = [
    {
        "url": "http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2",
        "compressed": "temp_resnet.bz2",
        "final": "dlib_face_recognition_resnet_model_v1.dat",
        "name": "Face Recognition Brain (ResNet, ~21MB)"
    },
    {
        "url": "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2",
        "compressed": "temp_landmarks.bz2",
        "final": "shape_predictor_68_face_landmarks.dat",
        "name": "Face Landmark Mapper (Shape Predictor, ~64MB)"
    }
]

print("Starting model download sequence...\n")

for model in models_to_download:
    # Check if the file is already there so we don't waste time re-downloading
    if os.path.exists(model["final"]):
        print(f"✅ {model['name']} already exists. Skipping...")
        continue
        
    print(f"⬇️ Downloading {model['name']}...")
    urllib.request.urlretrieve(model["url"], model["compressed"])
    
    print(f"📦 Extracting...")
    with bz2.BZ2File(model["compressed"], 'rb') as source, open(model["final"], 'wb') as dest:
        dest.write(source.read())
        
    os.remove(model["compressed"])
    print(f"✅ {model['name']} is ready!\n")

print("🎉 All models downloaded and extracted successfully! You are ready to start the server.")