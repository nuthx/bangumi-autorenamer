from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QFrame
from qfluentwidgets import (PushButton, FluentIcon, PrimaryPushButton, EditableComboBox, GroupHeaderCardWidget,
                            ComboBox, InfoBarIcon, LineEdit)

from src.module.utils import getResource
from src.module.config import posterFolder


class SettingWindow(object):
    def setupUI(self, this_window):
        # 加载 QSS
        with open(getResource("src/style/style_light.qss"), "r", encoding="UTF-8") as file:
            style_sheet = file.read()
        this_window.setStyleSheet(style_sheet)

        this_window.setWindowTitle("设置")
        this_window.setWindowIcon(QIcon(getResource("src/image/icon_win.png")))
        this_window.resize(850, -1)
        this_window.setFixedSize(self.size())  # 禁止拉伸窗口

        # 按钮
        self.applyButton = PrimaryPushButton("保存", self)
        self.applyButton.setFixedWidth(120)
        self.cancelButton = PushButton("取消", self)
        self.cancelButton.setFixedWidth(120)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setSpacing(12)
        self.buttonLayout.addStretch(0)
        self.buttonLayout.addWidget(self.applyButton)
        self.buttonLayout.addWidget(self.cancelButton)
        self.buttonLayout.addStretch(0)

        # 叠叠乐
        layout = QVBoxLayout()
        layout.setSpacing(14)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.addWidget(self.name_variable_card())
        self.general_setting = GeneralSetting()
        layout.addWidget(self.general_setting)
        self.ai_setting = AISetting()
        layout.addWidget(self.ai_setting)
        layout.addLayout(self.buttonLayout)

        this_window.setLayout(layout)

    def name_variable_card(self):
        self.t1 = self.name_variable_block("name_jp", "日文名")
        self.t2 = self.name_variable_block("name_cn", "中文名")
        self.t3 = self.name_variable_block("fs_name_cn", "首季中文名")
        self.t4 = self.name_variable_block("bangumi_id", "Bangumi ID")

        self.f1 = QHBoxLayout()
        self.f1.setSpacing(12)
        self.f1.setContentsMargins(0, 0, 0, 0)
        self.f1.addWidget(self.t1)
        self.f1.addWidget(self.t2)
        self.f1.addWidget(self.t3)
        self.f1.addWidget(self.t4)

        self.t5 = self.name_variable_block("type", "动画类型")
        self.t6 = self.name_variable_block("typecode", "类型编号")
        self.t7 = self.name_variable_block("episodes", "当前评分")
        self.t8 = self.name_variable_block("score", "章节数量")

        self.f2 = QHBoxLayout()
        self.f2.setSpacing(12)
        self.f2.setContentsMargins(0, 0, 0, 0)
        self.f2.addWidget(self.t5)
        self.f2.addWidget(self.t6)
        self.f2.addWidget(self.t7)
        self.f2.addWidget(self.t8)

        self.t9 = self.name_variable_block("release", "放送开始日期")
        self.t10 = self.name_variable_block("release_end", "放送结束日期")
        self.t11 = self.name_variable_block("release_week", "放送星期")
        self.t12 = self.name_variable_block("release_week", "放送星期")

        self.f3 = QHBoxLayout()
        self.f3.setSpacing(12)
        self.f3.setContentsMargins(0, 0, 0, 0)
        self.f3.addWidget(self.t9)
        self.f3.addWidget(self.t10)
        self.f3.addWidget(self.t11)
        # self.f3.addWidget(self.t12)
        self.f3.addStretch(0)

        self.renameTutorialLayout = QVBoxLayout()
        self.renameTutorialLayout.setSpacing(12)
        self.renameTutorialLayout.setContentsMargins(20, 16, 20, 16)
        self.renameTutorialLayout.addLayout(self.f1)
        self.renameTutorialLayout.addLayout(self.f2)
        self.renameTutorialLayout.addLayout(self.f3)

        self.renameTutorialCard = QFrame()
        self.renameTutorialCard.setObjectName("cardFrameFull")
        self.renameTutorialCard.setLayout(self.renameTutorialLayout)

        return self.renameTutorialCard

    def name_variable_block(self, card_token, card_explain):
        self.tokenLabel = QLabel(card_token)
        self.tokenLabel.setObjectName("lightLabel")
        self.explainLabel = QLabel(card_explain)
        self.explainLabel.setObjectName("lightLabel")

        self.tutorialLayout = QHBoxLayout()
        self.tutorialLayout.setContentsMargins(12, 8, 12, 8)
        self.tutorialLayout.addWidget(self.tokenLabel)
        self.tutorialLayout.addStretch(0)
        self.tutorialLayout.addWidget(self.explainLabel)

        self.card = QFrame()
        self.card.setMinimumWidth(181)
        self.card.setMaximumWidth(181)
        self.card.setObjectName("cardFrameTutorial")
        self.card.setLayout(self.tutorialLayout)

        return self.card


class GeneralSetting(GroupHeaderCardWidget):
    def __init__(self):
        super().__init__()
        self.setTitle("一般设置")
        self.setBorderRadius(8)

        # 命名格式
        self.name_variable = EditableComboBox(self)
        self.name_variable.setMinimumWidth(480)
        self.name_variable.setMaximumWidth(400)
        self.name_variable.addItems(["{fs_name_cn}/[{typecode}] [{release}] {name_jp}",
                                     "{fs_name_cn}/[{score}] [{typecode}] [{release}] {name_jp}",
                                     "{type}/{name_cn} ({name_jp})",
                                     "[{release}] {name_cn} ({release_week})"])
        self.addGroup(FluentIcon.EDIT, "命名格式", "支持使用斜杠创建子文件夹", self.name_variable)

        # 日期格式
        self.date_variable = EditableComboBox(self)
        self.date_variable.setFixedWidth(320)
        self.date_variable.addItems(["YYMMDD", "YYYY-MM", "MMM YYYY"])
        # self.dateTypeUrl = QLabel("<a href='https://arrow.readthedocs.io/en/latest/guide.html#supported-tokens' "
        #                           "style='font-size:12px;color:#F09199;'>查看在线文档</a>")
        # self.dateTypeUrl.setOpenExternalLinks(True)
        self.addGroup(FluentIcon.EDIT, "日期格式", "指定 release_date 的显示格式", self.date_variable)

        # 动画海报
        self.open_poster_folder = PushButton("打开", self, FluentIcon.FOLDER)
        self.open_poster_folder.setFixedWidth(100)
        self.addGroup(FluentIcon.EDIT, "动画海报", posterFolder(), self.open_poster_folder)


class AISetting(GroupHeaderCardWidget):
    def __init__(self):
        super().__init__()
        # TODO: 重写边框样式、副标题尺寸(尝试大改)
        self.setTitle("AI 设置")
        self.setBorderRadius(8)

        self.usage = ComboBox()
        self.usage.setFixedWidth(320)
        self.usage.addItems(["不使用", "优先本地分析，失败时尝试 AI 分析", "优先 AI 分析，失败时尝试本地分析", "始终使用 AI 分析"])
        self.addGroup(FluentIcon.APPLICATION, "启用 AI", "使用 AI 提取动画罗马名，获取更准确（或更离谱）的结果", self.usage)

        self.url = LineEdit()
        self.url.setFixedWidth(320)
        # self.url.setPlaceholderText("https://")
        self.addGroup(FluentIcon.APPLICATION, "服务器地址", "输入 AI 服务器的域名地址", self.url)

        self.token = LineEdit()
        self.token.setFixedWidth(320)
        # self.token.setPlaceholderText("sk-")
        self.addGroup(FluentIcon.APPLICATION, "API Key", "输入用于连接 AI 服务器的授权 Token，通常以 sk 开头", self.token)

        self.model = EditableComboBox()
        self.model.setFixedWidth(320)
        self.model.addItems(["", "gpt-3.5-turbo", "gpt-4o", "gpt-4o-mini", "qwen2-1.5b-instruct", "hunyuan-lite"])
        self.addGroup(FluentIcon.APPLICATION, "AI 模型", "选择你想使用的 AI 模型", self.model)

        self.test = PushButton("开始测试", self)
        self.test.setFixedWidth(100)
        self.addGroup(FluentIcon.DEVELOPER_TOOLS, "连接测试", "通过发送简短的请求，测试填写的 AI 服务器是否可用", self.test)
