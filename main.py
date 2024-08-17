import os
import random
import winreg as reg
import atexit

def set_system_proxy(proxy):
    proxy_key = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
    reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, proxy_key, 0, reg.KEY_SET_VALUE)

    # Включаем прокси и устанавливаем адрес
    reg.SetValueEx(reg_key, "ProxyEnable", 0, reg.REG_DWORD, 1)
    reg.SetValueEx(reg_key, "ProxyServer", 0, reg.REG_SZ, proxy)

    # Обновляем настройки
    reg.SetValueEx(reg_key, "ProxyOverride", 0, reg.REG_SZ, "<local>")

    reg.CloseKey(reg_key)

def disable_system_proxy():
    proxy_key = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
    reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, proxy_key, 0, reg.KEY_SET_VALUE)

    # Отключаем прокси
    reg.SetValueEx(reg_key, "ProxyEnable", 0, reg.REG_DWORD, 0)
    reg.CloseKey(reg_key)

def get_random_proxy(proxy_file):
    with open(proxy_file, 'r') as f:
        proxies = f.readlines()
    return random.choice(proxies).strip()

if __name__ == "__main__":
    proxy_file = "proxy.txt"
    random_proxy = get_random_proxy(proxy_file)
    set_system_proxy(random_proxy)
    print(f"Системный прокси установлен: {random_proxy}")

    # Зарегистрировать функцию для отключения прокси при выходе
    atexit.register(disable_system_proxy)

    try:
        # Включение и выключение.
        input("Программа запущена. Нажмите Enter для выхода.\n")
    finally:
        print("Отключение системного прокси...")
        disable_system_proxy()
