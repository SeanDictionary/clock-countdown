'''
制作人：SeanDictionary
联系方式：sean.dictionary@qq.com
版本V1.3，随缘更新。
'''




import sys
import time
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QDialog, QVBoxLayout, QLineEdit, QPushButton, QShortcut, QCheckBox,QSystemTrayIcon, QMenu
from PyQt5.QtGui import QFont, QColor, QPainter, QBrush, QKeySequence, QIcon
from PyQt5.QtCore import Qt, QTimer, QCoreApplication,QEvent
import json
from markdown2 import markdown_path

class FloatingWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口样式
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 初始化界面
        self.initUI()

        # 更新时间和倒计时
        self.updateDateTime()
        self.updateCountdown()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.timeout.connect(self.updateCountdown)
        self.timer.timeout.connect(self.updateFontColor)
        self.timer.start(1000)  # 每秒更新一次

        # 创建快捷键    设置，关闭
        self.shortcut = QShortcut(QKeySequence(Qt.SHIFT + Qt.Key_S), self)
        self.shortcut.activated.connect(self.showSettingsWindow)
        self.escapeShortcut = QShortcut(QKeySequence(Qt.Key_Escape + Qt.SHIFT), self)
        self.escapeShortcut.activated.connect(self.close)
        
        # 创建快捷键    移动
        self.leftShortcut = QShortcut(QKeySequence(Qt.Key_Left), self)
        self.leftShortcut.activated.connect(self.moveLeft)
        self.rightShortcut = QShortcut(QKeySequence(Qt.Key_Right), self)
        self.rightShortcut.activated.connect(self.moveRight)
        self.upShortcut = QShortcut(QKeySequence(Qt.Key_Up), self)
        self.upShortcut.activated.connect(self.moveUp)
        self.downShortcut = QShortcut(QKeySequence(Qt.Key_Down), self)
        self.downShortcut.activated.connect(self.moveDown)


        # 加载字体大小和显示设置
        self.loadSettings()

        # 创建系统托盘图标
        self.createSystemTrayIcon()

        # 新增实例变量
        self.window_position = (0, 0)


    def createSystemTrayIcon(self):
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon("icon.png"))  # 替换为你自己的图标路径
        self.trayIcon.setToolTip("悬浮时钟V1.3 by.SL")
        self.trayIcon.activated.connect(self.toggleWindow)
        self.trayIcon.show()

        # 创建托盘图标菜单
        self.trayMenu = QMenu(self)
        self.showSettingsAction = self.trayMenu.addAction("设置")
        self.showSettingsAction.triggered.connect(self.showSettingsWindow)
        self.quitAction = self.trayMenu.addAction("退出")
        self.quitAction.triggered.connect(self.close)
        self.trayIcon.setContextMenu(self.trayMenu)

    def showSettingsWindow(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.exec_()


    def toggleWindow(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            if self.isHidden():
                self.showNormal()
            else:
                self.hide()

    def initUI(self):
        self.setGeometry(-900, -900, -900, -900)  # 设置窗口位置和大小
        self.setStyleSheet("color: black;")  # 设置文字颜色为黑色

        # 添加标签显示时间
        self.timeLabel = QLabel(self)
        self.timeLabel.setFont(QFont("Arial", 35))
        self.timeLabel.setAlignment(Qt.AlignCenter)

        # 添加标签显示秒钟
        self.secondLabel = QLabel(self)
        self.secondLabel.setFont(QFont("Arial", 35))
        self.secondLabel.setAlignment(Qt.AlignCenter)

        # 添加标签显示倒计时
        self.countdownLabel = QLabel(self)
        self.countdownLabel.setFont(QFont("Arial", 30))
        self.countdownLabel.setAlignment(Qt.AlignCenter)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 设置背景透明
        painter.setOpacity(0)
        painter.setBrush(QBrush(QColor(0, 0, 0)))  # 设置背景颜色为黑色
        painter.drawRect(self.rect())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.offset)

    def updateDateTime(self):
        current_time = time.strftime("%H:%M:%S", time.localtime())
        hour_minute = current_time[:-3]  # 截取小时和分钟部分
        second = current_time[-2:]  # 截取秒钟部分
        self.timeLabel.setText(hour_minute)
        self.secondLabel.setText(second)

    def updateCountdown(self):
        current_datetime = datetime.now()
        current_date = current_datetime.date()

        # 判断高考日期的年份
        if current_datetime.month < 6 or (current_datetime.month == 6 and current_datetime.day < 7):
            exam_year = current_datetime.year
        else:
            exam_year = current_datetime.year + 1

        # 计算下一次高考日期
        exam_datetime = datetime(exam_year, 6, 7, 9, 0, 0)
        exam_date = exam_datetime.date()
        remaining_time = (exam_date - current_date).days
        self.countdownLabel.setText(f"离高考还有 {remaining_time} 天")

        # 窗口自适应大小
        width = max(self.timeLabel.sizeHint().width(), self.countdownLabel.sizeHint().width()) + self.secondLabel.sizeHint().width()+ 20
        height = self.timeLabel.sizeHint().height() + self.countdownLabel.sizeHint().height() + 10
        self.resize(width, height)
        self.timeLabel.setGeometry(0, 0, width - self.secondLabel.sizeHint().width(), height // 2)
        self.secondLabel.setGeometry(width - self.secondLabel.sizeHint().width(), 0, self.secondLabel.sizeHint().width(), self.secondLabel.sizeHint().height())
        self.countdownLabel.setGeometry(0, height // 2, width - self.secondLabel.sizeHint().width(), height // 2)

    def updateFontColor(self):
        # 获取窗口下层画面
        screen = QApplication.primaryScreen()
        pixmap = screen.grabWindow(0, self.geometry().topLeft().x(), self.geometry().topLeft().y(),
                                   self.geometry().width(), self.geometry().height())

        # 获取背景颜色
        color = pixmap.toImage().pixelColor(0, 0)

        # 根据亮度计算对比明显的文字颜色
        brightness = color.red() * 0.299 + color.green() * 0.587 + color.blue() * 0.114
        contrast_color = "white" if brightness < 128 else "black"

        # 设置文字颜色
        self.secondLabel.setStyleSheet(f"color: {contrast_color};")
        self.timeLabel.setStyleSheet(f"color: {contrast_color};")
        self.countdownLabel.setStyleSheet(f"color: {contrast_color};")

    def showSettingsWindow(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.exec_()

    def updateTimeFontSize(self, fontsize):
        self.timeLabel.setFont(QFont("Arial", fontsize))
        self.secondLabel.setFont(QFont("Arial", fontsize*0.35))

    def updateCountdownFontSize(self, fontsize):
        self.countdownLabel.setFont(QFont("Arial", fontsize))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and event.modifiers() == Qt.ShiftModifier:
            self.close()

    def closeEvent(self, event):
        # 保存窗口的位置信息
        self.window_position = (self.x(), self.y())
        self.saveSettings(self.countdownLabel.isVisible())
        self.saveSettings(self.secondLabel.isVisible())
        event.accept()
        QCoreApplication.quit()


    def saveSettings(self, show_second_line, show_second):
        settings = {
            'show_second_line': show_second_line,
            'show_second': show_second,
            'time_fontsize': self.timeLabel.font().pointSize(),
            'countdown_fontsize': self.countdownLabel.font().pointSize(),
            'window_position_x': self.window_position[0],  # 保存窗口位置的 X 坐标
            'window_position_y': self.window_position[1]   # 保存窗口位置的 Y 坐标
        }

        with open('setting.json', 'w') as file:
            json.dump(settings, file, indent=4)  # 指定缩进为4个空格


    def loadSettings(self):
        try:
            with open('setting.json', 'r') as file:
                settings = json.load(file)
                show_second_line = settings.get('show_second_line', True)
                show_second = settings.get('show_second', True)
                time_fontsize = settings.get('time_fontsize')
                countdown_fontsize = settings.get('countdown_fontsize')
                window_position_x = settings.get('window_position_x')
                window_position_y = settings.get('window_position_y')

                self.countdownLabel.setVisible(show_second_line)
                self.secondLabel.setVisible(show_second)

                if time_fontsize:
                    self.updateTimeFontSize(time_fontsize)
                if countdown_fontsize:
                    self.updateCountdownFontSize(countdown_fontsize)
                
                if window_position_x and window_position_y:
                    self.window_position = (window_position_x, window_position_y)
                    self.move(self.window_position[0], self.window_position[1])
                else:
                    # 获取屏幕的大小
                    screen_geometry = QApplication.desktop().screenGeometry()
                    screen_width = screen_geometry.width()
                    screen_height = screen_geometry.height()

                    # 计算窗口的位置
                    window_width = self.width()
                    window_height = self.height()
                    x = (screen_width - window_width) // 2
                    y = (screen_height - window_height) // 2

                    # 将窗口移动到屏幕的正中央
                    self.move(x, y)

        except FileNotFoundError:
            pass


    def moveLeft(self):
        self.move(self.x() - 10, self.y())

    def moveRight(self):
        self.move(self.x() + 10, self.y())

    def moveUp(self):
        self.move(self.x(), self.y() - 10)

    def moveDown(self):
        self.move(self.x(), self.y() + 10)


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("设置")
        self.setLayout(QVBoxLayout())

        # 第二行显示设置复选框
        self.showSecondLineCheckBox = QCheckBox("显示第二行", self)
        self.layout().addWidget(self.showSecondLineCheckBox)

        # 秒显示设置复选框
        self.showSecond = QCheckBox("显示秒", self)
        self.layout().addWidget(self.showSecond)

        # 字体大小输入框
        self.timeFontsizeInput = QLineEdit(self)
        self.layout().addWidget(QLabel("第一行字体大小:"))
        self.layout().addWidget(self.timeFontsizeInput)

        self.countdownFontsizeInput = QLineEdit(self)
        self.layout().addWidget(QLabel("第二行字体大小:"))
        self.layout().addWidget(self.countdownFontsizeInput)

        # 保存按钮
        save_button = QPushButton("保存", self)
        save_button.clicked.connect(self.saveSettings)
        self.layout().addWidget(save_button)

        # 加载设置
        self.loadSettings()

    def saveSettings(self):
        show_second_line = self.showSecondLineCheckBox.isChecked()
        show_second = self.showSecond.isChecked()
        time_fontsize = self.timeFontsizeInput.text()
        countdown_fontsize = self.countdownFontsizeInput.text()

        try:
            time_fontsize = int(time_fontsize)
            countdown_fontsize = int(countdown_fontsize)

            self.parent().countdownLabel.setVisible(show_second_line)
            self.parent().secondLabel.setVisible(show_second)
            self.parent().updateTimeFontSize(time_fontsize)
            self.parent().updateCountdownFontSize(countdown_fontsize)
            self.parent().saveSettings(show_second_line,show_second)
            self.close()
        except ValueError:
            pass


    def loadSettings(self):
        try:
            with open('setting.json', 'r') as file:
                settings = json.load(file)
                show_second_line = settings.get('show_second_line', True)
                show_second = settings.get('show_second', True)
                time_fontsize = settings.get('time_fontsize')
                countdown_fontsize = settings.get('countdown_fontsize')

                self.showSecondLineCheckBox.setChecked(show_second_line)
                self.showSecond.setChecked(show_second)
                self.timeFontsizeInput.setText(str(time_fontsize))
                self.countdownFontsizeInput.setText(str(countdown_fontsize))
        except FileNotFoundError:
            pass

    def event(self, event):
        if event.type()==QEvent.EnterWhatsThisMode:
            self.showHelpWindow()
        return QDialog.event(self,event)
    
    def showHelpWindow(self):
       self.settings_window = HelpWindow(self.parent())
       self.settings_window.exec_()


class HelpWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('帮助')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # 读取 readme.md 文件的内容并转换为 HTML
        readme_html = markdown_path('readme.md')

        # 创建 QLabel 显示 HTML 内容
        label = QLabel()
        label.setOpenExternalLinks(True)
        label.setText(readme_html)
        layout.addWidget(label)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = FloatingWindow()
    window.show()

    sys.exit(app.exec_())
