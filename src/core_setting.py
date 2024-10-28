from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Signal

from src.gui.components.Toast import Toast
from src.gui.settingwindow import SettingWindow

from src.module.api.openai import OpenAI
from src.module.config import openFolder, posterFolder, checkNameFormat, readConfig, writeConfig


class MySettingWindow(QDialog, SettingWindow):
    config_saved = Signal(str)

    def __init__(self):
        super().__init__()
        self.setupUI(self)
        self.initConnect()
        self.loadConfig()
        self.toast = Toast(parent=self)

    def initConnect(self):
        self.general_setting.open_poster_folder.clicked.connect(lambda: openFolder(posterFolder()))
        self.ai_setting.test.clicked.connect(self.testConnection)
        self.applyButton.clicked.connect(self.saveConfig)
        self.cancelButton.clicked.connect(lambda: self.close())

    def loadConfig(self):
        """
        在UI中加载保存的配置项
        """
        self.general_setting.name_variable.setText(readConfig("Format", "rename_format"))
        self.general_setting.date_variable.setText(readConfig("Format", "date_format"))

        self.ai_setting.usage.setCurrentIndex(int(readConfig("AI", "usage")))
        self.ai_setting.url.setText(readConfig("AI", "url"))
        self.ai_setting.token.setText(readConfig("AI", "token"))
        self.ai_setting.model.setText(readConfig("AI", "model"))

    def saveConfig(self):
        """
        保存配置项
        """
        error = checkNameFormat(self.general_setting.name_variable.currentText())  # 检查"命名格式"的合法性
        if error:
            self.toast.show("error", "命名格式错误", error)
        else:
            writeConfig("Format", "rename_format", self.general_setting.name_variable.currentText())
            writeConfig("Format", "date_format", self.general_setting.date_variable.currentText())

            writeConfig("AI", "usage", str(self.ai_setting.usage.currentIndex()))
            writeConfig("AI", "url", self.ai_setting.url.text())
            writeConfig("AI", "token", self.ai_setting.token.text())
            writeConfig("AI", "model", self.ai_setting.model.text())

            self.config_saved.emit("配置已保存")
            self.close()

    def testConnection(self):
        url = self.ai_setting.url.text()
        token = self.ai_setting.token.text()
        model = self.ai_setting.model.text()

        if not url or not token or not model:
            self.toast.show("warning", "", "请完整填写服务器信息")
        elif not (url.startswith("http://") or url.startswith("https://")):
            self.toast.show("warning", "", "服务器地址需以 http:// 或 https:// 开头")
        else:
            OpenAI().test(self.toast, url, token, model)
