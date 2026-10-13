import math
import time
from abc import ABC, abstractmethod


class AbstractEntity(ABC):

    @abstractmethod
    def show(self):
        pass


class Player(AbstractEntity):

    def __init__(self, login, password, score=0):
        self._login = login
        self._password = password
        self._score = score
        self._time_in = ""
        self._time_out = ""

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        self._login = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

    @property
    def time_in(self):
        return self._time_in

    @time_in.setter
    def time_in(self, value):
        self._time_in = value

    @property
    def time_out(self):
        return self._time_out

    @time_out.setter
    def time_out(self, value):
        self._time_out = value

    def add_score(self, points):
        self._score = self._score + points

    def check_password(self, password):
        return self._password == password

    def show(self):
        return "Player " + self._login + " score " + str(self._score)

    def __str__(self):
        return "Player(" + self._login + ")"

    def __repr__(self):
        return "Player('" + self._login + "', score=" + str(self._score) + ")"

    def __eq__(self, other):
        return self._login == other.login

    def __lt__(self, other):
        return self._score < other.score

    def __hash__(self):
        return hash(self._login)

    def __len__(self):
        return len(self._login)

    @staticmethod
    def create_default_players():
        result = []
        result.append(Player("player1", "1234", 120))
        result.append(Player("player2", "qwerty", 340))
        result.append(Player("player3", "1111", 90))
        result.append(Player("player4", "abcd", 560))
        result.append(Player("player5", "pass5", 210))
        result.append(Player("player6", "zebra", 480))
        result.append(Player("player7", "7777", 75))
        result.append(Player("player8", "hello", 390))
        result.append(Player("player9", "test9", 150))
        result.append(Player("player10", "0000", 620))
        result.append(Player("player11", "sun12", 45))
        result.append(Player("player12", "moon34", 275))
        return result

class Ball(AbstractEntity):

    def __init__(self, x, y, dx, dy, radius):
        self._x = x
        self._y = y
        self._dx = dx
        self._dy = dy
        self._radius = radius

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def dx(self):
        return self._dx

    @dx.setter
    def dx(self, value):
        self._dx = value

    @property
    def dy(self):
        return self._dy

    @dy.setter
    def dy(self, value):
        self._dy = value

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value

    def speed(self):
        return math.sqrt(self._dx * self._dx + self._dy * self._dy)

    def move(self):
        self._x = self._x + self._dx
        self._y = self._y + self._dy

    def bounce_x(self):
        self._dx = -self._dx

    def bounce_y(self):
        self._dy = -self._dy

    def set_position(self, x, y):
        self._x = x
        self._y = y

    def set_speed(self, dx, dy):
        self._dx = dx
        self._dy = dy

    def show(self):
        return "Ball at " + str(self._x) + " " + str(self._y) + " speed " + str(self.speed())

    def __str__(self):
        return "Ball(" + str(self._x) + ", " + str(self._y) + ")"

    def __repr__(self):
        return "Ball(x=" + str(self._x) + ", y=" + str(self._y) + ", r=" + str(self._radius) + ")"

    def __eq__(self, other):
        return self._x == other.x and self._y == other.y and self._radius == other.radius

    def __lt__(self, other):
        return self.speed() < other.speed()

    def __hash__(self):
        return hash((self._x, self._y, self._radius))

    def __len__(self):
        return self._radius


class Paddle(AbstractEntity):

    def __init__(self, x, y, width, height, speed):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._speed = speed

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value

    def move_left(self):
        self._x = self._x - self._speed

    def move_right(self):
        self._x = self._x + self._speed

    def clamp(self, min_x, max_x):
        if self._x < min_x:
            self._x = min_x
        if self._x + self._width > max_x:
            self._x = max_x - self._width

    def show(self):
        return "Paddle at " + str(self._x) + " width " + str(self._width)

    def __str__(self):
        return "Paddle(" + str(self._x) + ", " + str(self._y) + ")"

    def __repr__(self):
        return "Paddle(x=" + str(self._x) + ", w=" + str(self._width) + ")"

    def __eq__(self, other):
        return self._x == other.x and self._y == other.y and self._width == other.width

    def __lt__(self, other):
        return self._speed < other.speed

    def __hash__(self):
        return hash((self._x, self._y))

    def __len__(self):
        return self._width


class Brick(AbstractEntity):

    def __init__(self, x, y, width, height, hp, color):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._hp = hp
        self._color = color

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    def hit(self):
        self._hp = self._hp - 1

    def is_alive(self):
        return self._hp > 0

    def show(self):
        return "Brick at " + str(self._x) + " hp " + str(self._hp) + " color " + self._color

    def __str__(self):
        return "Brick(" + self._color + ", hp=" + str(self._hp) + ")"

    def __repr__(self):
        return "Brick(x=" + str(self._x) + ", y=" + str(self._y) + ", hp=" + str(self._hp) + ")"

    def __eq__(self, other):
        return self._x == other.x and self._y == other.y and self._hp == other.hp

    def __lt__(self, other):
        return self._hp < other.hp

    def __hash__(self):
        return hash((self._x, self._y))

    def __len__(self):
        return self._hp


class Bonus(AbstractEntity):

    def __init__(self, x, y, bonus_type):
        self._x = x
        self._y = y
        self._bonus_type = bonus_type

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def bonus_type(self):
        return self._bonus_type

    @bonus_type.setter
    def bonus_type(self, value):
        self._bonus_type = value

    def move_down(self):
        self._y = self._y + 3

    def show(self):
        return "Bonus " + self._bonus_type + " at " + str(self._x) + " " + str(self._y)

    def __str__(self):
        return "Bonus(" + self._bonus_type + ")"

    def __repr__(self):
        return "Bonus(x=" + str(self._x) + ", y=" + str(self._y) + ", type=" + self._bonus_type + ")"

    def __eq__(self, other):
        return self._x == other.x and self._y == other.y and self._bonus_type == other.bonus_type

    def __lt__(self, other):
        return self._bonus_type < other.bonus_type

    def __hash__(self):
        return hash((self._x, self._y, self._bonus_type))

    def __len__(self):
        return len(self._bonus_type)


class LevelMap(AbstractEntity):

    def __init__(self):
        self._levels = []
        self._blocks = []

    @property
    def levels(self):
        return self._levels

    def add_level(self, level, blocks):
        self._levels.append(level)
        self._blocks.append(blocks)

    def find_index(self, level):
        index = -1
        i = 0
        while i < len(self._levels):
            if self._levels[i] == level:
                index = i
                break
            i = i + 1
        return index

    def has_level(self, level):
        return self.find_index(level) != -1

    def get_blocks(self, level):
        index = self.find_index(level)
        if index == -1:
            return []
        return self._blocks[index]

    def show(self):
        text = "LevelMap with levels: "
        i = 0
        while i < len(self._levels):
            text = text + str(self._levels[i]) + " "
            i = i + 1
        return text

    def __str__(self):
        return "LevelMap(" + str(self._levels) + ")"

    def __repr__(self):
        return "LevelMap(levels=" + str(len(self._levels)) + ")"

    def __eq__(self, other):
        return self._levels == other.levels and self._blocks == other._blocks

    def __lt__(self, other):
        return len(self._levels) < len(other.levels)

    def __hash__(self):
        return hash(tuple(self._levels))

    def __len__(self):
        return len(self._levels)


class Report(AbstractEntity):

    def __init__(self):
        self._sessions = []

    @property
    def sessions(self):
        return self._sessions

    def add_session(self, login, time_in, time_out):
        session = []
        session.append(login)
        session.append(time_in)
        session.append(time_out)
        self._sessions.append(session)

    def save(self, filename):
        file = open(filename, "w", encoding="utf-8")
        file.write("+--- | login | time_in | time_out |\n")
        i = 0
        while i < 4:
            file.write("|---|---|---|\n")
            i = i + 1
        i = 0
        while i < len(self._sessions):
            session = self._sessions[i]
            file.write("| " + session[0] + " | " + session[1] + " | " + session[2] + " |\n")
            i = i + 1
        file.write("+---\n")
        file.close()

    def show(self):
        return "Report with " + str(len(self._sessions)) + " sessions"

    def __str__(self):
        return "Report(" + str(len(self._sessions)) + " sessions)"

    def __repr__(self):
        return "Report(sessions=" + str(len(self._sessions)) + ")"

    def __eq__(self, other):
        return self._sessions == other.sessions

    def __lt__(self, other):
        return len(self._sessions) < len(other.sessions)

    def __hash__(self):
        return hash(len(self._sessions))

    def __len__(self):
        return len(self._sessions)

    @staticmethod
    def now():
        return time.strftime("%d.%m.%Y %H:%M:%S")

