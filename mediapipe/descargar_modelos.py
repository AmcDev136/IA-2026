from pathlib import Path
import urllib.request

MODELOS = {
    "hand_landmarker.task": (
        "https://storage.googleapis.com/mediapipe-models/"
        "hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
    ),
    "face_landmarker.task": (
        "https://storage.googleapis.com/mediapipe-models/"
        "face_landmarker/face_landmarker/float16/1/face_landmarker.task"
    ),
}

def main():
    out = Path("modelos")
    out.mkdir(parents=True, exist_ok=True)
    for nombre, url in MODELOS.items():
        destino = out / nombre
        if destino.exists() and destino.stat().st_size > 1000:
            print("Ya existe:", destino)
            continue
        print("Descargando", nombre, "...")
        urllib.request.urlretrieve(url, destino)
        print("OK →", destino)

if __name__ == "__main__":
    main()