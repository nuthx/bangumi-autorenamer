import os
import re
import platform
import subprocess
import configparser


def openFolder(path):
    """
    在不同系统下，以不同方式打开指定文件夹
    :param path: 文件夹路径
    """
    if platform.system() == "Windows":
        subprocess.call(["explorer", path])
    elif platform.system() == "Darwin":
        subprocess.call(["open", path])
    elif platform.system() == "Linux":
        subprocess.call(["xdg-open", path])


def configPath():
    """
    输出当前系统下配置文件夹的路径
    :return: 配置文件夹的路径
    """
    if platform.system() == "Windows":
        sys_path = os.environ["APPDATA"]
    elif platform.system() == "Darwin":
        sys_path = os.path.expanduser("~/Library/Application Support")
    elif platform.system() == "Linux":
        sys_path = os.path.expanduser("~/.config")
    else:
        sys_path = "/"

    config_path = os.path.join(sys_path, "BangumiRenamer")
    if not os.path.exists(config_path):
        os.makedirs(config_path)

    return config_path


def configFile():
    """
    输出BangumiRenamer配置文件的路径
    :return: BangumiRenamer配置文件的路径
    """
    config_file = os.path.join(configPath(), "config.ini")
    if not os.path.exists(config_file):
        initConfig(config_file)  # 初始化配置文件

    return config_file


def posterFolder():
    """
    输出缓存海报文件夹的路径
    :return: 缓存海报文件夹的路径
    """
    poster_folder = os.path.join(configPath(), "poster")
    if not os.path.exists(poster_folder):
        os.makedirs(poster_folder)

    return poster_folder


def logFolder():
    """
    输出日志文件夹的路径
    :return: 日志文件夹的路径
    """
    log_folder = os.path.join(configPath(), "logs")
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    return log_folder


def readConfig(category, item):
    """
    读取配置项的值
    :param category: 配置类别
    :param item: 配置项目
    :return: 指定配置项的值
    """
    config = configparser.ConfigParser()
    config.read(configFile())
    return config.get(category, item)


def writeConfig(category, item, value):
    """
    写入配置项的值
    :param category: 配置类别
    :param item: 配置项目
    :param value: 待写入的值
    """
    config = configparser.ConfigParser()
    config.read(configFile())
    config.set(category, item, value)
    with open(configFile(), "w", encoding="utf-8") as content:
        config.write(content)


def initConfig(config_file):
    """
    初始化配置文件
    :param config_file: 配置文件路径
    """
    config = configparser.ConfigParser()

    config.add_section("Application")
    config.set("Application", "version", "2.1.1")

    config.add_section("Format")
    config.set("Format", "rename_format", "{fs_name_cn}/[{typecode}] [{release}] {name_jp}")
    config.set("Format", "date_format", "YYMMDD")

    config.add_section("AI")
    config.set("AI", "usage", "0")
    config.set("AI", "url", "")
    config.set("AI", "token", "")
    config.set("AI", "model", "")

    with open(config_file, "w", encoding="utf-8") as content:
        config.write(content)


def checkNameFormat(name_format):
    """
    检查配置文件中，"命名格式"项的合法性
    :return: 不合法则返回检查结果；若合法则无返回
    """
    available = ["name_jp", "name_cn", "fs_name_cn", "bangumi_id",
                 "type", "typecode", "episodes", "score",
                 "release", "release_end", "release_week"]
    pattern = r"\{(.*?)\}"
    matches = re.findall(pattern, name_format)
    invalid_vars = [match for match in matches if match not in available]
    if invalid_vars:
        return "检查花括号内的变量拼写"


def checkConfigVersion():
    """
    检测配置文件版本是否为最新，决定是否重置配置文件

    更新历史：

    2.1.1 加入AI选项
    """
    if readConfig("Application", "version") != "2.1.1":
        os.remove(configFile())
        initConfig(configFile())
