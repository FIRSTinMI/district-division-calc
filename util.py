from base64 import b64encode
import requests

import models

def get_rankings(season: int, district: str, num_teams: int, api_key: str) -> list[models.DivisionTeam]:
    rankings = []
    current_page = 1
    total_pages = 99

    api_headers = {
        "Authorization": f"Basic {b64encode(api_key.encode()).decode()}",
        "Accept": "application/json"
    }

    while len(rankings) < 160 and current_page < total_pages:
        resp = requests.get(f"https://frc-api.firstinspires.org/v3.0/{season}/rankings/district?districtCode={district}&page={current_page}", headers=api_headers)
        if not resp.ok:
            raise Exception("Got a bad response from the FRC API: " + str(resp.status_code) + " - " + resp.text)
        resp = resp.json()
        if current_page == 1:
            total_pages =  resp["pageTotal"]
        rankings += [models.DivisionTeam(t["teamNumber"], t["totalPoints"]) for t in resp["districtRanks"]]
        current_page += 1
    
    return rankings[:num_teams]