import os
from datetime import datetime
from pprint import pprint
import time
from dotenv import load_dotenv
from requests import get
from bs4 import BeautifulSoup
from matrix_client.client import MatrixClient, Room

load_dotenv()

client = MatrixClient("https://d0.ee")
token = client.login(
    username=os.environ.get("ARK_USERNAME"),
    password=os.environ.get("ARK_PASSWORD")
)
client.start_listener_thread()

ROOM_ID = os.environ.get("ARK_ROOM")
if ROOM_ID not in client.rooms:
    client.join_room(ROOM_ID)
room: Room = client.rooms[ROOM_ID]



def get_times():
    r = get("https://eteenindus.mnt.ee/public/vabadSoidueksamiajad.xhtml")
    r.raise_for_status()
    #pyhton go hurr duurrr, java is superior
    soup = BeautifulSoup(r.content, features="html.parser")
    table = soup.find(id='eksami_ajad:kategooriaBEksamiAjad_data')
    trs = list(table.find_all('tr'))
    times = {}
    for tr in trs:
        td = [td.get_text() for td in tr.find_all('td') if td.get_text()]
        city = td[0]
        del td[0]
        times[city] = []
        for t in td:
            d = datetime.strptime(t.strip(), "%d.%m.%Y %H:%M")
            times[city].append(d)
    return times


def main():
    times = {}
    try:
        times = get_times()
    except Exception as e:
        room.send_text(f"Refresh failed, {e}")

    latest_times = sorted(times.get("Tallinn", []))
    latest_times_pretty=', '.join([t.strftime('%d.%m.%Y %H:%M') for t in latest_times])
    print(datetime.now(), "Slots:", latest_times_pretty)
    if latest_times and latest_times[0] < datetime(2021, 9, 7, 12, 30):
        room.send_text(f"Slot Free Tallinn {latest_times_pretty}")
        room.send_text("https://eteenindus.mnt.ee/main.jsf")


if __name__ == '__main__':
    while True:
        main()
        time.sleep(5)
    client.logout()
