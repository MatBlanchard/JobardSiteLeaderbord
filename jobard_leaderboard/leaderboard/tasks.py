import threading
import time
from admin_app.models import Campaign
from .models import Driver, LapTime
import requests
import json
import re

COUNT = 1500
DRIVER_ID_RE = re.compile(r'/users/info/(\d+)(?:/|[?#]|$)')

def ms_from_laptime_str(s: str) -> int | None:
    if not s:
        return None
    main = s.split(',', 1)[0].strip()
    m = re.match(r'^\s*(?:(\d+)\s*m\s*)?(\d+)(?:\.(\d{1,3}))?\s*s\s*$', main)
    if not m:
        return None
    minutes = int(m.group(1) or 0)
    seconds = int(m.group(2))
    ms = int((m.group(3) or '0').ljust(3, '0'))
    return minutes * 60_000 + seconds * 1_000 + ms

def get_json(layout_id, car_id):
    url = 'https://game.raceroom.com/leaderboard/listing/0?start=0&count=' + \
          str(COUNT) + '&track=' + str(layout_id) + '&car_class=' + str(car_id)
    page = requests.get(url, headers={'X-Requested-With': 'XMLHttpRequest'})
    if page.ok:
        return json.loads(page.text)
    else:
        return ""

def update_data():
    campaigns = Campaign.objects.all()
    for campaign in campaigns:
        layouts = campaign.layouts.all()
        cars = campaign.cars.all()
        for layout in layouts:
            for car in cars:
                file = get_json(layout.id, car.id)
                results = file['context']['c']['results']
                for r in results:
                    driver = r["driver"]
                    driver_id = int(DRIVER_ID_RE.search(driver["path"]).group(1))
                    driver_name = driver["name"]
                    driver_obj, _created = Driver.objects.update_or_create(
                        id=driver_id,
                        defaults={
                            "name":driver_name
                        }
                    )
                    laptime_obj, _created= LapTime.objects.update_or_create(
                        driver=driver_obj,
                        layout=layout,
                        car=car,
                        defaults={
                            "lap_time_ms": ms_from_laptime_str(r["laptime"])
                        }
                    )
                    laptime_obj.campaigns.add(campaign)
    print("✅ Données mises à jour laptimes et drivers")

def background_updater():
    while True:
        try:
            update_data()
        except Exception as e:
            print(f"⚠️ Erreur pendant leaderboard.update_data: {e}")
        time.sleep(900)


def start_background_updater():
    thread = threading.Thread(target=background_updater, daemon=True)
    thread.start()