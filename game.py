import random
from models import Ball, Paddle, Brick, Bonus, LevelMap


class Game:

    def __init__(self, level_map, level, difficulty, width, height):
        self.width = width
        self.height = height
        self.level = level
        self.difficulty = difficulty
        self.score = 0
        self.lives = 5
        self.game_over = False
        self.win = False
        self.started = False

        factor = 0.5 + difficulty * 0.1
        self.paddle = Paddle(width / 2 - 50, height - 40, 100, 15, 8)
        self.ball = Ball(width / 2, height - 60, 0, 0, 12)
        self.ball_dx = 4 * factor * 0.6
        self.ball_dy = 4 * factor

        self.bricks = []
        self.bonuses = []
        blocks = level_map.get_blocks(level)
        i = 0
        while i < len(blocks):
            source = blocks[i]
            brick = Brick(source.x, source.y, source.width, source.height, source.hp, source.color)
            self.bricks.append(brick)
            i = i + 1

    def move_paddle_left(self):
        self.paddle.move_left()
        self.paddle.clamp(0, self.width)

    def move_paddle_right(self):
        self.paddle.move_right()
        self.paddle.clamp(0, self.width)

    def start(self):
        if self.started:
            return
        self.started = True
        self.ball.set_speed(self.ball_dx, -self.ball_dy)

    def update(self):
        if self.game_over or self.win:
            return
        if not self.started:
            self.ball.set_position(self.paddle.x + self.paddle.width / 2, self.paddle.y - 20)
            return
        self.ball.move()
        self.check_walls()
        self.hit_paddle()
        self.check_bricks()
        self.check_fall()
        self.check_win()
        self.update_bonuses()

    def check_walls(self):
        ball = self.ball
        if ball.x - ball.radius <= 0:
            ball.set_position(ball.radius, ball.y)
            ball.bounce_x()
        if ball.x + ball.radius >= self.width:
            ball.set_position(self.width - ball.radius, ball.y)
            ball.bounce_x()
        if ball.y - ball.radius <= 0:
            ball.set_position(ball.x, ball.radius)
            ball.bounce_y()

    def hit_paddle(self):
        ball = self.ball
        paddle = self.paddle
        prev_y = ball.y - ball.dy
        if ball.dy > 0 and prev_y + ball.radius <= paddle.y and ball.y + ball.radius >= paddle.y:
            if ball.x >= paddle.x and ball.x <= paddle.x + paddle.width:
                ball.y = paddle.y - ball.radius
                ball.dy = -abs(ball.dy)
                third = paddle.width / 3
                if ball.x < paddle.x + third:
                    ball.dx = -abs(ball.dx) - 1
                elif ball.x > paddle.x + 2 * third:
                    ball.dx = abs(ball.dx)

    def overlap(self, ball, brick):
        if ball.x + ball.radius <= brick.x:
            return False
        if ball.x - ball.radius >= brick.x + brick.width:
            return False
        if ball.y + ball.radius <= brick.y:
            return False
        if ball.y - ball.radius >= brick.y + brick.height:
            return False
        return True

    def check_bricks(self):
        ball = self.ball
        i = 0
        hit_index = -1
        while i < len(self.bricks):
            brick = self.bricks[i]
            if brick.is_alive() and self.overlap(ball, brick):
                hit_index = i
                break
            i = i + 1
        if hit_index == -1:
            return
        brick = self.bricks[hit_index]
        brick.hit()
        self.score = self.score + 10
        ball.bounce_y()
        if not brick.is_alive():
            self.drop_bonus(brick)

    def check_fall(self):
        if self.ball.y - self.ball.radius > self.height:
            self.lives = self.lives - 1
            if self.lives <= 0:
                self.game_over = True
            else:
                self.reset_ball()

    def reset_ball(self):
        self.ball.set_position(self.paddle.x + self.paddle.width / 2, self.paddle.y - 20)
        self.ball.set_speed(0, 0)
        self.started = False
        self.bonuses = []

    def check_win(self):
        i = 0
        while i < len(self.bricks):
            if self.bricks[i].is_alive():
                return
            i = i + 1
        self.win = True

    def drop_bonus(self, brick):
        if random.randint(0, 9) != 0:
            return
        number = random.randint(0, 3)
        if number == 0:
            bonus_type = "expand"
        elif number == 1:
            bonus_type = "shrink"
        elif number == 2:
            bonus_type = "slow"
        else:
            bonus_type = "life"
        bonus = Bonus(brick.x + brick.width / 2, brick.y, bonus_type)
        self.bonuses.append(bonus)

    def update_bonuses(self):
        i = 0
        while i < len(self.bonuses):
            bonus = self.bonuses[i]
            bonus.move_down()
            if self.apply_bonus(bonus):
                self.bonuses.pop(i)
                continue
            if bonus.y > self.height:
                self.bonuses.pop(i)
                continue
            i = i + 1

    def apply_bonus(self, bonus):
        paddle = self.paddle
        if bonus.y >= paddle.y and bonus.y <= paddle.y + paddle.height:
            if bonus.x >= paddle.x and bonus.x <= paddle.x + paddle.width:
                self.bonus_effect(bonus.bonus_type)
                return True
        return False

    def bonus_effect(self, bonus_type):
        if bonus_type == "expand":
            self.paddle.width = self.paddle.width + 30
        elif bonus_type == "shrink":
            self.paddle.width = self.paddle.width - 30
            if self.paddle.width < 40:
                self.paddle.width = 40
        elif bonus_type == "slow":
            self.ball.dx = self.ball.dx * 0.7
            self.ball.dy = self.ball.dy * 0.7
        elif bonus_type == "life":
            self.lives = self.lives + 1

    @staticmethod
    def color_for_hp(hp):
        if hp >= 4:
            return "#d500f9"
        if hp == 3:
            return "#ff5252"
        if hp == 2:
            return "#ffea00"
        return "#00e676"

    @staticmethod
    def bonus_color(bonus_type):
        if bonus_type == "expand":
            return "#00e676"
        if bonus_type == "shrink":
            return "#ff5252"
        if bonus_type == "slow":
            return "#40c4ff"
        return "#ffea00"

    @staticmethod
    def bonus_letter(bonus_type):
        if bonus_type == "expand":
            return "E"
        if bonus_type == "shrink":
            return "S"
        if bonus_type == "slow":
            return "L"
        return "H"

    @staticmethod
    def make_row(row, cols, start_x, brick_width, brick_height, gap, hp, top):
        result = []
        y = top + row * (brick_height + gap)
        col = 0
        while col < cols:
            x = start_x + col * (brick_width + gap)
            brick = Brick(x, y, brick_width, brick_height, hp, Game.color_for_hp(hp))
            result.append(brick)
            col = col + 1
        return result

    @staticmethod
    def create_default_levels():
        level_map = LevelMap()
        cols = 8
        brick_width = 60
        brick_height = 22
        gap = 6
        total_width = cols * (brick_width + gap) - gap
        start_x = (600 - total_width) / 2

        blocks1 = []
        row = 0
        while row < 3:
            blocks1.extend(Game.make_row(row, cols, start_x, brick_width, brick_height, gap, 1, 60))
            row = row + 1
        level_map.add_level(1, blocks1)

        blocks2 = []
        row = 0
        while row < 4:
            hp = 1
            if row >= 2:
                hp = 2
            blocks2.extend(Game.make_row(row, cols, start_x, brick_width, brick_height, gap, hp, 60))
            row = row + 1
        level_map.add_level(2, blocks2)

        blocks3 = []
        row = 0
        while row < 5:
            hp = 2
            if row >= 2:
                hp = 3
            blocks3.extend(Game.make_row(row, cols, start_x, brick_width, brick_height, gap, hp, 60))
            row = row + 1
        level_map.add_level(3, blocks3)

        return level_map

