import requests
import subprocess
import time
import pygetwindow

# disable warnings related to insecure requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

lockfile_path = "C:/Riot Games/League of Legends/lockfile"
username = 'riot'
champions = {
    '266': "Aatrox", '103': "Ahri", '84': "Akali", '166': "Akshan", '12': "Alistar", '32': "Amumu", '34': "Anivia",
    '1': "Annie", '523': "Aphelios", '22': "Ashe", '136': "AurelionSol", '268': "Azir", '432': "Bard", '200': "BelVeth",
    '53': "Blitzcrank", '63': "Brand", '201': "Braum", '233': "Briar", '51': "Caitlyn", '164': "Camille", '69': "Cassiopeia",
    '31': "ChoGath", '42': "Corki", '122': "Darius", '131': "Diana", '119': "Draven", '36': "DrMundo", '245': "Ekko",
    '60': "Elise", '28': "Evelynn", '81': "Ezreal", '9': "Fiddlesticks", '114': "Fiora", '105': "Fizz", '3': "Galio",
    '41': "Gangplank", '86': "Garen", '150': "Gnar", '79': "Gragas", '104': "Graves", '887': "Gwen", '120': "Hecarim",
    '74': "Heimerdinger", '910': "Hwei", '420': "Illaoi", '39': "Irelia", '427': "Ivern", '40': "Janna", '59': "JarvanIV",
    '24': "Jax", '126': "Jayce", '202': "Jhin", '222': "Jinx", '145': "KaiSa", '429': "Kalista", '43': "Karma",
    '30': "Karthus", '38': "Kassadin", '55': "Katarina", '10': "Kayle", '141': "Kayn", '85': "Kennen", '121': "KhaZix",
    '203': "Kindred", '240': "Kled", '96': "KogMaw", '897': "KSante", '7': "LeBlanc", '64': "LeeSin", '89': "Leona",
    '876': "Lillia", '127': "Lissandra", '236': "Lucian", '117': "Lulu", '99': "Lux", '54': "Malphite", '90': "Malzahar",
    '57': "Maokai", '11': "MasterYi", '902': "Milio", '21': "MissFortune", '62': "Wukong", '82': "Mordekaiser",
    '25': "Morgana", '950': "Naafiri", '267': "Nami", '75': "Nasus", '111': "Nautilus", '518': "Neeko", '76': "Nidalee",
    '895': "Nilah", '56': "Nocturne", '20': "Nunu", '2': "Olaf", '61': "Orianna", '516': "Ornn", '80': "Pantheon",
    '78': "Poppy", '555': "Pyke", '246': "Qiyana", '133': "Quinn", '497': "Rakan", '33': "Rammus", '421': "RekSai",
    '526': "Rell", '888': "RenataGlasc", '58': "Renekton", '107': "Rengar", '92': "Riven", '68': "Rumble", '13': "Ryze",
    '360': "Samira", '113': "Sejuani", '235': "Senna", '147': "Seraphine", '875': "Sett", '35': "Shaco", '98': "Shen",
    '102': "Shyvana", '27': "Singed", '14': "Sion", '15': "Sivir", '72': "Skarner", '901': "Smolder", '37': "Sona",
    '16': "Soraka", '50': "Swain", '517': "Sylas", '134': "Syndra", '223': "TahmKench", '163': "Taliyah", '91': "Talon",
    '44': "Taric", '17': "Teemo", '412': "Thresh", '18': "Tristana", '48': "Trundle", '23': "Tryndamere",
    '4': "TwistedFate", '29': "Twitch", '77': "Udyr", '6': "Urgot", '110': "Varus", '67': "Vayne", '45': "Veigar",
    '161': "VelKoz", '711': "Vex", '254': "Vi", '234': "Viego", '112': "Viktor", '8': "Vladimir", '106': "Volibear",
    '19': "Warwick", '498': "Xayah", '101': "Xerath", '5': "XinZhao", '157': "Yasuo", '777': "Yone", '83': "Yorick",
    '350': "Yuumi", '154': "Zac", '238': "Zed", '221': "Zeri", '115': "Ziggs", '26': "Zilean", '142': "Zoe", '143': "Zyra",
}


def make_array_from_lockfile():
    with open(lockfile_path, 'r') as file:
        contents = file.read()
        lockfile_array = contents.split(":")
    return lockfile_array


def get_champion():
    lockfile_array = make_array_from_lockfile()
    port = lockfile_array[2]
    password = lockfile_array[3]
    lol_client_url = f"https://127.0.0.1:{port}/lol-champ-select/v1/current-champion"
    authentication_login = {
        'url': lol_client_url,
        'headers': {'content-type': 'application/json'},
        'auth': (username, password),
        'verify': False
    }
    response = requests.get(**authentication_login)
    champion_id = response.text
    return champions.get(champion_id, "Unknown Champion")


def open_champion_page(champion_name):
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    subprocess.Popen([chrome_path, f'https://op.gg/champion/{champion_name}'])
    subprocess.Popen([chrome_path, f'https://lolalytics.com/lol/{champion_name}/build/'])

def check_window(window_title):
    window = pygetwindow.getWindowsWithTitle(window_title)
    if window:
        return True
    else:
        return False

if __name__ == "__main__":
    specific_window_title = "League of Legends (TM) Client"
    while True:
        if not check_window(specific_window_title):
            champion_name = get_champion()
            if champion_name != "Unknown Champion":
                print(f"Opening op.gg page for {champion_name}...")
                open_champion_page(champion_name.lower()) # lolalytics is case sensitive
                try:
                    time.sleep(120)
                except KeyboardInterrupt:
                    print("Sleep interrupted by KeyboardInterrupt.")
            else:
                print("No Champion locked.")
        time.sleep(10)

            
