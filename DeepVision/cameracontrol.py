import cameraprofiles as profiles
import requests

base_url = "http://10.50.24.2:1182/?action=command&"

def setVisionMode():
    for setting in profiles.vision_profile:
        print(f"{setting}={profiles.vision_profile[setting]}")
        requests.get(f"{base_url}{setting}={profiles.vision_profile[setting]}")