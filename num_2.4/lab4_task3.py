import sqlite3
import psutil
import os
from psutil._common import bytes2human

con = sqlite3.connect("task3.db")

create_table = """
create table if not exists PCInfo(
id integer primary key,
measurement_time datetime not null,
cpu_usage float(2) not null,
ram_usage float(2) not null,
disk_usage float(2) not null
);
"""

con.executescript(create_table)


def save_stats(cpu_usage, ram_usage, disk_usage):
    cursor = con.cursor()

    cursor.execute("insert into PCInfo values (null, datetime(), ?, ?, ?)", (cpu_usage, ram_usage, disk_usage))

    con.commit()


def get_stats():
    cursor = con.cursor()

    cursor.execute("select * from PCInfo")

    stats = cursor.fetchall()

    print_format = "{:<19}{:>5}{:>5}{:>5}"
    print(print_format.format("Дата", "ЦПУ", "ОЗУ", "ДИСК"))
    for x in stats:
        print(print_format.format(x[1], x[2], x[3], x[4]))


def measure_usage():
    cpu_usage = psutil.cpu_percent(interval=0.5)
    ram_usage = psutil.virtual_memory().percent

    templ = "{:<17} {:<8} {:>8} {:>8} {:>5}% {:>9} {}"
    print("Статистика дисков: ")
    print(templ.format("Устройство", "Размер", "Исп.", "Своб.", "Исп.", "Тип", "Точка монтирования"))
    all_storage = []
    devices = []
    used_storage = []
    for part in psutil.disk_partitions(all=False):
        if os.name == 'nt':
            if 'cdrom' in part.opts or part.fstype == '' or 'removable' in part.opts:
                continue
        if part.fstype in ('vfat', 'exfat', 'fat') or part.mountpoint.startswith("/run"):
            continue
        usage = psutil.disk_usage(part.mountpoint)

        if part.device in devices:
            if usage.total in all_storage:
                continue
        all_storage.append(usage.total)
        used_storage.append(usage.used)
        devices.append(part.device)

        print(templ.format(part.device, bytes2human(usage.total), bytes2human(usage.used), bytes2human(usage.free),
                           int(usage.percent), part.fstype, part.mountpoint))

    disk_usage = sum(used_storage) / sum(all_storage) * 100
    return cpu_usage, ram_usage, round(disk_usage, 1)

def monitor_usage():
    cpu, ram, disk = measure_usage()

    print(f"Расход ЦПУ: {cpu}%, ОЗУ: {ram}% Диска: {disk}%")
    save_stats(cpu, ram, disk)

while True:
    print("Меню:")
    print("1. Посмотреть и сохранить")
    print("2. Вывести всю статистику")
    print("0. Выйти из программы")

    try:
        choice = int(input("Введите номер действия:"))
    except:
        print("Введите номер!")
        continue

    if choice == 1:
        monitor_usage()
    elif choice == 2:
        get_stats()
    elif choice == 0:
        break
    else:
        print("Неверный выбор")
        continue

    input("Нажмите enter для продолжения...")
    print()