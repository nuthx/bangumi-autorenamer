import sys
from PySide6.QtWidgets import QApplication

from src.core_home import MyHomeWindow
from src.function import log
from src.module.version import currentVersion


if __name__ == "__main__":
    log("=============================")
    log("BangumiRenamer启动")
    log(f"当前版本：{currentVersion()}")

    app = QApplication(sys.argv)
    window = MyHomeWindow()
    window.show()
    app.exec()
