"""
Ejemplo 1 — Manos en vivo (OpenCV + MediaPipe).
Ejecutar en TERMINAL, no con Babel/C-c C-c.
"""
import argparse
import sys
import time
from pathlib import Path

import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (0, 9), (9, 10), (10, 11), (11, 12),
    (0, 13), (13, 14), (14, 15), (15, 16),
    (0, 17), (17, 18), (18, 19), (19, 20),
    (5, 9), (9, 13), (13, 17),
]


def bgr_a_mp(frame_bgr):
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    return mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)


def dibujar_mano(frame, landmarks):
    h, w = frame.shape[:2]
    pts = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]
    for a, b in HAND_CONNECTIONS:
        cv2.line(frame, pts[a], pts[b], (0, 255, 0), 2)
    for p in pts:
        cv2.circle(frame, p, 3, (0, 0, 255), -1)


def abrir_camara(indice):
    if sys.platform.startswith("linux"):
        cap = cv2.VideoCapture(indice, cv2.CAP_V4L2)
    elif sys.platform == "win32":
        cap = cv2.VideoCapture(indice, cv2.CAP_DSHOW)
    else:
        cap = cv2.VideoCapture(indice)
    if not cap.isOpened():
        cap = cv2.VideoCapture(indice)
    if not cap.isOpened():
        return None
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    try:
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    except Exception:
        pass
    # Vaciar buffer / calentar
    for _ in range(20):
        ok, frame = cap.read()
        if ok and frame is not None and float(frame.mean()) > 5:
            break
        time.sleep(0.03)
    return cap


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--camara", type=int, default=0)
    ap.add_argument(
        "--modelo",
        default=str(Path(__file__).resolve().parent / "modelos" / "hand_landmarker.task"),
    )
    ap.add_argument("--max-manos", type=int, default=2)
    args = ap.parse_args()

    modelo = Path(args.modelo)
    if not modelo.exists():
        # rutas frecuentes del laboratorio
        candidatos = [
            Path("modelos/hand_landmarker.task"),
            Path("/home/likcos/Scripts/modelos/hand_landmarker.task"),
        ]
        for c in candidatos:
            if c.exists():
                modelo = c
                break
        else:
            raise SystemExit(
                f"No esta el modelo en {args.modelo}. Ejecute descargar_modelos.py"
            )

    print("Cargando modelo (puede tardar unos segundos)...", modelo)
    options = vision.HandLandmarkerOptions(
        base_options=mp_python.BaseOptions(model_asset_path=str(modelo)),
        running_mode=vision.RunningMode.VIDEO,
        num_hands=args.max_manos,
        min_hand_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    # IMPORTANTE: crear el landmarker ANTES de abrir la camara
    with vision.HandLandmarker.create_from_options(options) as landmarker:
        print("Modelo listo. Abriendo camara", args.camara, "...")
        cap = abrir_camara(args.camara)
        if cap is None:
            raise SystemExit(f"No se abrio la camara {args.camara}")

        cv2.namedWindow("manos", cv2.WINDOW_NORMAL)
        t0 = time.time()
        n = 0
        print("Ventana abierta. Pulse q para salir.")

        while True:
            ok, frame = cap.read()
            if not ok:
                print("cap.read() fallo")
                break

            brillo = float(frame.mean())
            frame = cv2.flip(frame, 1)
            ts = int((time.time() - t0) * 1000)
            result = landmarker.detect_for_video(bgr_a_mp(frame), ts)

            etiquetas = []
            for lms, handed in zip(result.hand_landmarks, result.handedness):
                dibujar_mano(frame, lms)
                etiquetas.append(
                    f"{handed[0].category_name}:{handed[0].score:.2f}"
                )

            texto = " | ".join(etiquetas) if etiquetas else "Sin manos"
            cv2.putText(frame, texto, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.putText(frame, f"brillo={brillo:.0f}  q=salir", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

            # Cada ~30 frames guarda una foto de diagnostico
            if n % 30 == 0:
                cv2.imwrite("debug_mano.jpg", frame)
                print(f"frame {n} brillo={brillo:.1f} manos={len(result.hand_landmarks)}")

            cv2.imshow("manos", frame)
            n += 1
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
        print("Fin. Revise debug_mano.jpg si la ventana se veia negra.")


if __name__ == "__main__":
    main()