import os
import platform
import subprocess
import logging
from datetime import datetime

from src.module.config import configFile, readConfig, logFolder


def log(content):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%Y-%m-%d %H:%M:%S")

    log_folder = logFolder()
    log_file = os.path.join(log_folder, f"{date}.log")

    logging.basicConfig(filename=log_file, level=logging.INFO, format="%(message)s")
    logging.info(f"[{time}] {content}")

    print(f"[{time}] {content}")


def initList(list_id, anime_list, raw_list):
    for raw_path in raw_list:
        # 转换为文件路径
        file_path = raw_path.toLocalFile()

        # Windows 下调整路径分隔符
        if platform.system() == 'Windows':
            file_path = file_path.replace('/', '\\')

        # 解决 macOS 下路径无法识别
        if file_path.endswith('/'):
            file_path = file_path[:-1]

        # 过滤非文件夹
        if not os.path.isdir(file_path):
            continue

        # 去重已存在的文件夹
        path_exist = any(item['file_path'] == file_path for item in anime_list)
        if path_exist:
            continue

        this_anime_dict = dict()
        this_anime_dict['list_id'] = list_id
        this_anime_dict['file_name'] = os.path.basename(file_path)
        this_anime_dict['file_path'] = file_path

        anime_list.append(this_anime_dict)
        list_id += 1

    return list_id, anime_list


def openFolder(path):
    if platform.system() == "Windows":
        subprocess.call(["explorer", path])
    elif platform.system() == "Darwin":
        subprocess.call(["open", path])
    elif platform.system() == "Linux":
        subprocess.call(["xdg-open", path])
