from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit,
    QComboBox, QSlider, QCheckBox, QTableWidget, QTableWidgetItem, QMenuBar,
    QStatusBar, QVBoxLayout, QHBoxLayout, QGraphicsView, QGraphicsScene, QMessageBox,
    QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsSimpleTextItem)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QFont
from models import Player, Report
from game import Game


class MyButton(QPushButton):

    def __init__(self, text):
        super().__init__(text)
        self.setMinimumHeight(42)

    def enterEvent(self, event):
        self.setStyleSheet("background-color: #aaccee")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet("")
        super().leaveEvent(event)

    def sizeHint(self):
        size = super().sizeHint()
        size.setWidth(max(size.width(), 150))
        return size


class MyLabel(QLabel):

    def __init__(self, text):
        super().__init__(text)

    def sizeHint(self):
        size = super().sizeHint()
        size.setHeight(size.height() + 6)
        return size


class MyLineEdit(QLineEdit):

    def __init__(self):
        super().__init__()
        self.setMinimumHeight(34)

    def sizeHint(self):
        size = super().sizeHint()
        size.setWidth(max(size.width(), 220))
        return size

    def focusInEvent(self, event):
        self.setStyleSheet("background-color: #eef6ff")
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.setStyleSheet("")
        super().focusOutEvent(event)


class MyComboBox(QComboBox):

    def __init__(self):
        super().__init__()
        self.setMinimumHeight(32)

    def sizeHint(self):
        size = super().sizeHint()
        size.setWidth(max(size.width(), 160))
        return size

    def wheelEvent(self, event):
        event.ignore()


class MySlider(QSlider):

    def __init__(self):
        super().__init__(Qt.Horizontal)
        self.setMinimum(1)
        self.setMaximum(10)
        self.setValue(5)
        self.setMinimumWidth(200)

    def sizeHint(self):
        size = super().sizeHint()
        size.setHeight(size.height() + 10)
        return size


class MyCheckBox(QCheckBox):

    def __init__(self, text):
        super().__init__(text)
        self.setChecked(True)

    def sizeHint(self):
        size = super().sizeHint()
        size.setWidth(size.width() + 10)
        return size

class MyTable(QTableWidget):

    def __init__(self, rows, cols):
        super().__init__(rows, cols)

    def sizeHint(self):
        size = super().sizeHint()
        size.setHeight(380)
        return size


class MyMenuBar(QMenuBar):

    def __init__(self):
        super().__init__()

    def sizeHint(self):
        size = super().sizeHint()
        size.setHeight(size.height() + 6)
        return size


class MyStatusBar(QStatusBar):

    def __init__(self):
        super().__init__()

    def sizeHint(self):
        size = super().sizeHint()
        size.setHeight(size.height() + 8)
        return size


class MyVBoxLayout(QVBoxLayout):

    def __init__(self):
        super().__init__()
        self.setSpacing(12)
        self.setContentsMargins(24, 24, 24, 24)

    def sizeHint(self):
        size = super().sizeHint()
        size.setWidth(size.width() + 20)
        return size


class MyGraphicsView(QGraphicsView):

    def __init__(self, scene):
        super().__init__(scene)
        self.game_window = None
        self.setMinimumSize(620, 520)
        self.setRenderHint(QPainter.Antialiasing)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFocusPolicy(Qt.StrongFocus)

    def sizeHint(self):
        size = super().sizeHint()
        size.setWidth(max(size.width(), 640))
        size.setHeight(max(size.height(), 540))
        return size

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)

    def keyPressEvent(self, event):
        if self.game_window is not None:
            self.game_window.handle_key_press(event.key())
        else:
            super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if self.game_window is not None:
            self.game_window.handle_key_release(event.key())
        else:
            super().keyReleaseEvent(event)


class LoginWindow(QWidget):

    login_ok = pyqtSignal(object)

    def __init__(self, players):
        super().__init__()
        self.players = players
        self.player = None
        self.setWindowTitle("Вход")
        self.resize(380, 300)

        self.login_label = MyLabel("Логин")
        self.login_input = MyLineEdit()
        self.login_input.setPlaceholderText("player1")

        self.password_label = MyLabel("Пароль")
        self.password_input = MyLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("1234")

        self.info_label = MyLabel("")

        self.login_button = MyButton("Войти")
        self.exit_button = MyButton("Выход")
        self.login_button.clicked.connect(self.try_login)
        self.exit_button.clicked.connect(QApplication.instance().quit)

        login_row = QHBoxLayout()
        login_row.addWidget(self.login_label)
        login_row.addWidget(self.login_input)

        password_row = QHBoxLayout()
        password_row.addWidget(self.password_label)
        password_row.addWidget(self.password_input)

        button_row = QHBoxLayout()
        button_row.addWidget(self.login_button)
        button_row.addWidget(self.exit_button)

        layout = MyVBoxLayout()
        layout.addLayout(login_row)
        layout.addLayout(password_row)
        layout.addWidget(self.info_label)
        layout.addLayout(button_row)
        self.setLayout(layout)

    def try_login(self):
        login = self.login_input.text().strip()
        password = self.password_input.text()
        found = None
        i = 0
        while i < len(self.players):
            if self.players[i].login == login:
                found = self.players[i]
                break
            i = i + 1
        if found is None:
            self.info_label.setText("Нет такого игрока")
            return
        if not found.check_password(password):
            self.info_label.setText("Неверный пароль")
            return
        found.time_in = Report.now()
        self.player = found
        self.login_ok.emit(found)


class MainWindow(QWidget):

    def __init__(self, player, players, report, level_map):
        super().__init__()
        self.player = player
        self.players = players
        self.report = report
        self.level_map = level_map
        self.game_window = None
        self.records_window = None
        self.setWindowTitle("Арканоид - " + player.login)
        self.resize(420, 520)

        menu_bar = MyMenuBar()
        game_menu = menu_bar.addMenu("Игра")
        play_action = game_menu.addAction("Играть")
        records_action = game_menu.addAction("Рекорды")
        quit_action = game_menu.addAction("Выход")
        play_action.triggered.connect(self.start_game)
        records_action.triggered.connect(self.open_records)
        quit_action.triggered.connect(self.close)

        status_bar = MyStatusBar()
        status_bar.showMessage("Очки: " + str(player.score))

        title_label = MyLabel("Главное меню")

        self.play_button = MyButton("Играть")
        self.records_button = MyButton("Рекорды")
        self.exit_button = MyButton("Выход")
        self.play_button.clicked.connect(self.start_game)
        self.records_button.clicked.connect(self.open_records)
        self.exit_button.clicked.connect(self.close)

        level_label = MyLabel("Уровень")
        self.level_combo = MyComboBox()
        self.level_combo.addItem("1")
        self.level_combo.addItem("2")
        self.level_combo.addItem("3")

        difficulty_label = MyLabel("Сложность")
        self.difficulty_slider = MySlider()
        self.difficulty_value = MyLabel(str(self.difficulty_slider.value()))
        self.difficulty_slider.valueChanged.connect(self.change_difficulty)

        self.sound_checkbox = MyCheckBox("Звук")

        level_row = QHBoxLayout()
        level_row.addWidget(level_label)
        level_row.addWidget(self.level_combo)

        difficulty_row = QHBoxLayout()
        difficulty_row.addWidget(difficulty_label)
        difficulty_row.addWidget(self.difficulty_slider)
        difficulty_row.addWidget(self.difficulty_value)

        layout = MyVBoxLayout()
        layout.addWidget(menu_bar)
        layout.addWidget(title_label)
        layout.addWidget(self.play_button)
        layout.addWidget(self.records_button)
        layout.addWidget(self.exit_button)
        layout.addLayout(level_row)
        layout.addLayout(difficulty_row)
        layout.addWidget(self.sound_checkbox)
        layout.addStretch()
        layout.addWidget(status_bar)
        self.setLayout(layout)

    def change_difficulty(self, value):
        self.difficulty_value.setText(str(value))

    def start_game(self):
        level = int(self.level_combo.currentText())
        difficulty = self.difficulty_slider.value()
        sound = self.sound_checkbox.isChecked()
        self.game_window = GameWindow(self.player, self.level_map, level, difficulty, sound)
        self.game_window.show()

    def open_records(self):
        self.records_window = RecordsWindow(self.players)
        self.records_window.show()

    def closeEvent(self, event):
        self.player.time_out = Report.now()
        self.report.add_session(self.player.login, self.player.time_in, self.player.time_out)
        self.report.save("report.txt")
        event.accept()


class RecordsWindow(QWidget):

    def __init__(self, players):
        super().__init__()
        self.setWindowTitle("Рекорды")
        self.resize(420, 460)

        sorted_players = sorted(players, reverse=True)

        self.table = MyTable(len(sorted_players), 3)
        self.table.setHorizontalHeaderLabels(["Игрок", "Очки", "Время входа"])

        row = 0
        i = 0
        while i < len(sorted_players):
            player = sorted_players[i]
            self.table.setItem(row, 0, QTableWidgetItem(player.login))
            self.table.setItem(row, 1, QTableWidgetItem(str(player.score)))
            self.table.setItem(row, 2, QTableWidgetItem(player.time_in))
            row = row + 1
            i = i + 1

        close_button = MyButton("Закрыть")
        close_button.clicked.connect(self.close)

        layout = MyVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(close_button)
        self.setLayout(layout)


class GameWindow(QWidget):

    def __init__(self, player, level_map, level, difficulty, sound):
        super().__init__()
        self.player = player
        self.level_map = level_map
        self.level = level
        self.difficulty = difficulty
        self.sound = sound
        self.setWindowTitle("Игра - уровень " + str(level))
        self.resize(680, 640)
        self.setStyleSheet("background-color: #16213e;")
        self.keys_pressed = set()

        self.game = Game(level_map, level, difficulty, 600, 500)

        self.scene = QGraphicsScene(0, 0, 600, 500)
        self.scene.setBackgroundBrush(QBrush(QColor("#1a1a2e")))
        self.view = MyGraphicsView(self.scene)
        self.view.game_window = self

        self.info_label = MyLabel("Жизни: " + str(self.game.lives) + "  Очки: " + str(self.game.score))
        self.info_label.setStyleSheet("color: #00e5ff; font-size: 16px; font-weight: bold;")

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(16)

        layout = MyVBoxLayout()
        layout.addWidget(self.info_label)
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.bonus_items = []
        self.build_scene()

    def build_scene(self):
        frame = self.scene.addRect(0, 0, 600, 500, QPen(QColor("#00e5ff"), 3), QBrush(Qt.NoBrush))
        frame.setZValue(20)
        ball = self.game.ball
        r = ball.radius
        self.ball_item = QGraphicsEllipseItem(-r, -r, 2 * r, 2 * r)
        self.ball_item.setBrush(QBrush(QColor("#ff1744")))
        self.ball_item.setPen(QPen(Qt.NoPen))
        self.ball_item.setZValue(10)
        self.ball_item.setVisible(True)
        self.scene.addItem(self.ball_item)

        paddle = self.game.paddle
        self.paddle_item = QGraphicsRectItem(0, 0, paddle.width, paddle.height)
        self.paddle_item.setBrush(QBrush(QColor("#00e5ff")))
        self.paddle_item.setPen(QPen(QColor("#00b8d4"), 2))
        self.paddle_item.setZValue(2)
        self.paddle_item.setVisible(True)
        self.scene.addItem(self.paddle_item)

        self.brick_items = []
        i = 0
        while i < len(self.game.bricks):
            brick = self.game.bricks[i]
            item = QGraphicsRectItem(0, 0, brick.width, brick.height)
            item.setBrush(QBrush(QColor(brick.color)))
            item.setPen(QPen(Qt.NoPen))
            item.setZValue(1)
            self.scene.addItem(item)
            self.brick_items.append(item)
            i = i + 1
        self.sync_scene()

    def sync_scene(self):
        ball = self.game.ball
        self.ball_item.setPos(ball.x, ball.y)
        self.ball_item.setVisible(True)
        paddle = self.game.paddle
        self.paddle_item.setRect(0, 0, paddle.width, paddle.height)
        self.paddle_item.setPos(paddle.x, paddle.y)
        self.paddle_item.setVisible(True)
        i = 0
        while i < len(self.brick_items):
            brick = self.game.bricks[i]
            item = self.brick_items[i]
            if brick.is_alive():
                item.setVisible(True)
                item.setPos(brick.x, brick.y)
                item.setBrush(QBrush(QColor(Game.color_for_hp(brick.hp))))
            else:
                item.setVisible(False)
            i = i + 1

    def sync_bonuses(self):
        i = 0
        while i < len(self.bonus_items):
            self.scene.removeItem(self.bonus_items[i])
            i = i + 1
        self.bonus_items = []
        i = 0
        while i < len(self.game.bonuses):
            bonus = self.game.bonuses[i]
            color = Game.bonus_color(bonus.bonus_type)
            item = QGraphicsEllipseItem(-10, -10, 20, 20)
            item.setBrush(QBrush(QColor(color)))
            item.setPen(QPen(Qt.black, 1))
            item.setZValue(5)
            item.setPos(bonus.x, bonus.y)
            self.scene.addItem(item)
            text = QGraphicsSimpleTextItem(Game.bonus_letter(bonus.bonus_type))
            font = QFont()
            font.setPointSize(12)
            font.setBold(True)
            text.setFont(font)
            text.setBrush(QBrush(QColor("black")))
            text.setParentItem(item)
            text_rect = text.boundingRect()
            text.setPos(-text_rect.width() / 2, -text_rect.height() / 2)
            self.bonus_items.append(item)
            i = i + 1

    def tick(self):
        if self.game.game_over or self.game.win:
            self.finish()
            return
        if Qt.Key_Left in self.keys_pressed:
            self.game.move_paddle_left()
        if Qt.Key_Right in self.keys_pressed:
            self.game.move_paddle_right()
        old_score = self.game.score
        self.game.update()
        self.sync_scene()
        self.sync_bonuses()
        if self.sound and self.game.score > old_score:
            QApplication.instance().beep()
        if not self.game.started:
            self.info_label.setStyleSheet("color: #ffea00; font-size: 16px; font-weight: bold;")
            self.info_label.setText("Жизни: " + str(self.game.lives) + "  Очки: " + str(self.game.score) + "  Нажмите пробел")
        else:
            self.info_label.setStyleSheet("color: #00e5ff; font-size: 16px; font-weight: bold;")
            self.info_label.setText("Жизни: " + str(self.game.lives) + "  Очки: " + str(self.game.score))

    def finish(self):
        self.timer.stop()
        if self.game.win:
            self.player.add_score(self.game.score)
            QMessageBox.information(self, "Победа", "Вы набрали " + str(self.game.score) + " очков")
        else:
            QMessageBox.information(self, "Поражение", "Игра окончена. Очки: " + str(self.game.score))
        self.close()

    def handle_key_press(self, key):
        if key == Qt.Key_Left or key == Qt.Key_Right:
            self.keys_pressed.add(key)
        elif key == Qt.Key_Space:
            self.game.start()
            self.sync_scene()

    def handle_key_release(self, key):
        if key in self.keys_pressed:
            self.keys_pressed.discard(key)

    def showEvent(self, event):
        super().showEvent(event)
        self.view.setFocus()

