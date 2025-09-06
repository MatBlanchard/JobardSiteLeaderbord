import threading
import time
import requests
from .models import Car, Class, Track, Layout

URL = "https://raw.githubusercontent.com/sector3studios/r3e-spectator-overlay/master/r3e-data.json"

def update_data():
    try:
        resp = requests.get(URL)
        if resp.status_code == 200:
            data = resp.json()

            # --- Classes ---
            for class_id, class_info in data.get("classes", {}).items():
                Class.objects.update_or_create(
                    id=class_id,
                    defaults={
                        "name": class_info.get("Name", "Unkown")
                    }
                )
            # --- Cars ---
            for car_id, car_info in data.get("cars", {}).items():
                class_car = Class.objects.get(id=car_info.get("Class"))
                Car.objects.update_or_create(
                    id=car_id,
                    defaults={
                        "name": car_info.get("Name", "Unkown"),
                        "carClass": class_car
                    }
                )
            # --- Tracks ---
            for track_id, track_info in data.get("tracks", {}).items():
                Track.objects.update_or_create(
                    id=track_id,
                    defaults={
                        "name": track_info.get("Name", "Unknown")
                    }
                )
            # --- Layouts ---
            for layout_id, layout_info in data.get("layouts", {}).items():
                track = Track.objects.get(id=layout_info.get("Track"))
                Layout.objects.update_or_create(
                    id=layout_id,
                    defaults={
                        "name": layout_info.get("Name", "Unknown"),
                        "track": track
                    }
                )

            print("✅ Données mises à jour depuis R3E JSON")
        else:
            print(f"❌ Erreur {resp.status_code} en téléchargeant les données")

    except Exception as e:
        print(f"⚠️ Erreur pendant update_data: {e}")


def background_updater():
    while True:
        update_data()
        time.sleep(24 * 3600)


def start_background_updater():
    thread = threading.Thread(target=background_updater, daemon=True)
    thread.start()
