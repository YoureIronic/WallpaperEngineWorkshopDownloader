import tkinter as tk
from tkinter import scrolledtext, filedialog
import subprocess
import threading
import base64
import re
import os
import json
import sys

accounts = {
    'kuramaduellinks': 'ZGVtYWNpYW4xMjM=',
    'Phi_Kung00': 'cGVlaW53emEwMDc=',
    'adgjl1182': 'UUVUVU85OTk5OQ==',
    'heqxa1234567': 'QW5uZm9yZW1hbjkx',
    'ruiiixx': 'UzY3R0JUQjgzRDNZ'
}
passwords = {account: base64.b64decode(accounts[account]).decode('utf-8') for account in accounts}

def run_command(pubfileid):
    printlog(t("downloading", id=pubfileid))
    if 'save_location' not in globals():
        printlog(t("error_save_location_not_set"))
        return
    if not os.path.isdir(save_location):
        printlog(t("error_save_location_not_exist"))
        return
    target_directory = os.path.join(save_location, "projects", "myprojects")
    if not os.path.isdir(target_directory):
        printlog(t("invalid_save_location"))
        return
    dir_option = f"-dir \"{save_location}\\projects\\myprojects\\{pubfileid}\""
    command = f"DepotdownloaderMod\\DepotDownloadermod.exe -app 431960 -pubfile {pubfileid} -verify-all -username {username.get()} -password {passwords[username.get()]} {dir_option}"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,creationflags=subprocess.CREATE_NO_WINDOW)
    for line in process.stdout:
        printlog(line)
    process.stdout.close()
    process.wait()
    printlog(t("download_finished"))

def printlog(log):
    console.config(state=tk.NORMAL)
    console.insert(tk.END, log)
    console.yview(tk.END)
    console.config(state=tk.DISABLED)

def run_commands():
    run_button.config(state=tk.DISABLED)
    links = link_text.get("1.0", tk.END).splitlines()
    for link in links:
        if link:
            match = re.search(r'\b\d{8,10}\b', link.strip())
            if match:
                run_command(match.group(0))
            else:
                printlog(t("invalid_link", link=link))
    run_button.config(state=tk.NORMAL)

def start_thread():
    threading.Thread(target=run_commands).start()

def on_closing():
    subprocess.Popen("taskkill /f /im DepotDownloadermod.exe", creationflags=subprocess.CREATE_NO_WINDOW)
    os._exit(0)

def select_save_location():
    selected_directory = filedialog.askdirectory()
    target_directory = os.path.join(selected_directory, "projects", "myprojects")
    if not os.path.isdir(target_directory):
        printlog(t("invalid_save_location"))
    else:
        printlog(t("path_set", path=selected_directory))
        set_save_location(selected_directory)
        save_location_label.config(text=t("wallpaper_path", path=selected_directory))

def set_save_location(path):
    global save_location, config
    save_location = path
    config["save_location"] = save_location
    save_config(config)

def load_config():
    config_path = "config.cfg"
    config = {"save_location": "Not set", "lang": "en_us"}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        k, v = line.strip().split("=", 1)
                        config[k.strip()] = v.strip()
        except Exception:
            pass
    return config

def save_config(config):
    config_path = "config.cfg"
    with open(config_path, "w", encoding="utf-8") as f:
        for k, v in config.items():
            f.write(f"{k}={v}\n")

def resource_path(relative_path):
    if hasattr(sys, 'frozen'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

def load_language(lang_code):
    lang_path = resource_path(os.path.join("lang", f"{lang_code}.json"))
    try:
        with open(lang_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

config = load_config()
save_location = config.get("save_location", "Not set")
LANG_CODE = config.get("lang", "en_us")
lang = load_language(LANG_CODE)

def load_save_location():
    global save_location, config
    save_location = config.get("save_location", "Not set")

load_save_location()

def t(key, **kwargs):
    text = lang.get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text

def set_language(lang_code):
    global LANG_CODE, lang, config
    LANG_CODE = lang_code
    lang = load_language(LANG_CODE)
    config["lang"] = LANG_CODE
    save_config(config)
    refresh_labels()

def refresh_labels():
    root.title(t("app_title"))
    title_label.config(text=t("app_title"))
    username_label.config(text=t("select_account"))
    save_location_button.config(text=t("select_path"))
    save_location_label.config(text=t("wallpaper_path", path=save_location))
    link_label.config(text=t("enter_items"))
    console_label.config(text=t("console_output"))
    run_button.config(text=t("download"))
    lang_menu_label.config(text="Language:")

root = tk.Tk()

title_label = tk.Label(root, font=("Arial", 21))
title_label.grid(row=0, column=0)

username_label = tk.Label(root)
username_label.grid(row=1, column=0, sticky='w', padx=(130, 0))
username = tk.StringVar(root)
username.set(list(accounts.keys())[0])
username_menu = tk.OptionMenu(root, username, *accounts.keys())
username_menu.grid(row=1, column=0)

save_location_button = tk.Button(root, command=select_save_location)
save_location_button.grid(row=2, column=0)

save_location_label = tk.Label(root)
save_location_label.grid(row=3, column=0)

link_label = tk.Label(root)
link_text = scrolledtext.ScrolledText(root, height=10)
link_label.grid(row=4, column=0)
link_text.grid(row=5, column=0)

console_label = tk.Label(root)
console = scrolledtext.ScrolledText(root, height=10)
console_label.grid(row=6, column=0)
console.grid(row=7, column=0)
console.config(state=tk.DISABLED)

run_button = tk.Button(root, command=start_thread)
run_button.grid(row=8, column=0)

lang_menu_label = tk.Label(root)
lang_menu_label.grid(row=9, column=0, sticky='w', padx=(130, 0))
language_var = tk.StringVar(root)
language_var.set(LANG_CODE)
language_menu = tk.OptionMenu(root, language_var, "en_us", "zh_cn", command=set_language)
language_menu.grid(row=9, column=0)

refresh_labels()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()