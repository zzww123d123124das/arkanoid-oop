import sys
from PyQt5.QtWidgets import QApplication
from models import Player, Report
from game import Game
from ui import LoginWindow, MainWindow


def main():
    app = QApplication(sys.argv)
    players = Player.create_default_players()
    report = Report()
    level_map = Game.create_default_levels()

    login_window = LoginWindow(players)
    login_window.show()

    def open_menu(player):
        window = MainWindow(player, players, report, level_map)
        window.show()
        login_window.close()
        app.main_window = window

    login_window.login_ok.connect(open_menu)

    sys.exit(app.exec_())


main()
