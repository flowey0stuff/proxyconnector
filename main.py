import os
import random
import requests
import winreg as reg
import atexit

def set_system_proxy(proxy):
    proxy_key = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
    reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, proxy_key, 0, reg.KEY_SET_VALUE)

    # Включаем прокси и устанавливаем HTTP адрес
    reg.SetValueEx(reg_key, "ProxyEnable", 0, reg.REG_DWORD, 1)
    reg.SetValueEx(reg_key, "ProxyServer", 0, reg.REG_SZ, f"http={proxy}")

    # Обновляем настройки
    reg.SetValueEx(reg_key, "ProxyOverride", 0, reg.REG_SZ, "<local>")

    reg.CloseKey(reg_key)

def disable_system_proxy():
    proxy_key = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
    reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, proxy_key, 0, reg.KEY_SET_VALUE)

    # Отключаем прокси
    reg.SetValueEx(reg_key, "ProxyEnable", 0, reg.REG_DWORD, 0)
    reg.CloseKey(reg_key)

def get_random_proxy_from_file(file):
    with open(file, 'r') as f:
        proxies = f.readlines()
    return random.choice(proxies).strip()

def get_random_proxy_from_link(link):
    try:
        response = requests.get(link)
        proxy_list = response.text.splitlines()
        return random.choice(proxy_list).strip()
    except Exception as e:
        print(f"Ошибка при получении прокси из ссылки: {e}")
        return None

def check_proxy(proxy):
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
    try:
        response = requests.get("http://ipinfo.io/ip", proxies=proxies, timeout=5)
        if response.status_code == 200:
            print(f"Прокси работает: {proxy}")
            return True
        else:
            print(f"Прокси не отвечает: {proxy}")
            return False
    except Exception as e:
        print(f"Ошибка при проверке прокси: {e}")
        return False

if __name__ == "__main__":
    print("1) Подключиться к рандомному прокси из ссылок")
    print("2) Подключиться к рандомному прокси из файла")
    choice = input("Выберите опцию (1 или 2): ")

    proxy = None

    if choice == "1":
        link = get_random_proxy_from_file("links.txt")
        if link:
            proxy = get_random_proxy_from_link(link)
    elif choice == "2":
        proxy = get_random_proxy_from_file("proxys.txt")

    if proxy and check_proxy(proxy):
        set_system_proxy(proxy)
        print(f"Системный прокси установлен: {proxy}")
        atexit.register(disable_system_proxy)
    else:
        print("Не удалось установить прокси.")
