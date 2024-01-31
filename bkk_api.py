import requests

API_KEY = "ae30f36c-de78-4461-b533-fbde2b76ed91"
BASE_URL = "https://go.bkk.hu/api/query/v1/ws/gtfs-rt/full/"


def get_vehicle_positions(route_id=None):
    if route_id:
        url = f"{BASE_URL}VehiclePositions.pb?key={API_KEY}&routeId={route_id}"
    else:
        url = f"{BASE_URL}VehiclePositions.pb?key={API_KEY}"

    response = requests.get(url)

    if response.status_code == 200:
        return response.content
    else:
        return f'Hiba a BKK API hívás során: {response.status_code}'

# További BKK API függvények...
