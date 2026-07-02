import pygame
import random
import sys
import time

# 初始化 Pygame
pygame.init()

# 窗口尺寸
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

# 网格设置（每个格子 20x20 像素）
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
GRAY = (40, 40, 40)
LIGHT_GRAY = (80, 80, 80)

# 设置窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("贪吃蛇小游戏 - 奖励加速版")
clock = pygame.time.Clock()

# 字体（用于显示分数和提示）
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)


class Snake:
    """蛇类"""
    def __init__(self):
        # 蛇的初始位置：在屏幕中央，长度为3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2),
                          (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
                          (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # 初始向右移动
        self.grow = False
        self.base_speed = 10  # 基础速度

    def move(self):
        """移动蛇"""
        head = self.positions[0]
        x, y = head
        dx, dy = self.direction
        new_head = (x + dx, y + dy)

        # 插入新头部
        self.positions.insert(0, new_head)

        # 如果不需要增长，删除尾部
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False

    def change_direction(self, direction):
        """改变方向（不能反向）"""
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def check_collision(self):
        """检测是否撞墙或撞自己"""
        head = self.positions[0]
        x, y = head

        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
            return True

        if head in self.positions[1:]:
            return True

        return False

    def eat_food(self, food_pos):
        """检测是否吃到食物"""
        if self.positions[0] == food_pos:
            self.grow = True
            return True
        return False

    def grow_snake(self, amount=1):
        """让蛇增长指定的长度"""
        for _ in range(amount):
            self.grow = True
            # 立即执行一次增长（不移动，直接加长尾部）
            if self.grow:
                tail = self.positions[-1]
                self.positions.append(tail)
                self.grow = False

    def get_speed(self, is_boosting):
        """获取当前速度"""
        if is_boosting:
            return self.base_speed * 2
        return self.base_speed


class Food:
    """红色普通食物类"""
    def __init__(self, snake_positions):
        self.position = self.generate(snake_positions)

    def generate(self, snake_positions):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in snake_positions:
                return (x, y)


class GoldenFood:
    """金色奖励食物类"""
    def __init__(self, snake_positions):
        self.position = None
        self.active = False
        self.appear_time = 0
        self.duration = 0  # 持续时间（秒）
        self.size = 2  # 占2x2格（4格大小）
        self.generate(snake_positions)

    def generate(self, snake_positions):
        """生成黄苹果"""
        # 占2x2格，需要检查所有格子都不在蛇身上
        attempts = 0
        while attempts < 1000:
            x = random.randint(0, GRID_WIDTH - self.size)
            y = random.randint(0, GRID_HEIGHT - self.size)
            # 检查2x2区域是否都被蛇占据
            occupied = False
            for i in range(self.size):
                for j in range(self.size):
                    if (x + i, y + j) in snake_positions:
                        occupied = True
                        break
                if occupied:
                    break
            if not occupied:
                self.position = (x, y)
                self.active = True
                self.appear_time = time.time()
                self.duration = random.randint(10, 15)  # 10~15秒消失
                return
            attempts += 1
        # 如果找不到位置，暂时不生成
        self.active = False
        self.position = None

    def update(self, snake_positions):
        """更新黄苹果状态"""
        if self.active:
            # 检查是否超时
            if time.time() - self.appear_time > self.duration:
                self.active = False
                self.position = None

    def check_eaten(self, snake_positions):
        """检查蛇头是否碰到了黄苹果的2x2区域"""
        if not self.active or self.position is None:
            return False

        head = snake_positions[0]
        hx, hy = head
        px, py = self.position

        # 检查蛇头是否在2x2区域内
        if px <= hx < px + self.size and py <= hy < py + self.size:
            return True
        return False


def draw_grid():
    """绘制网格线"""
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WINDOW_WIDTH, y))


def draw_snake(snake):
    """绘制蛇"""
    for i, pos in enumerate(snake.positions):
        rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE,
                           GRID_SIZE, GRID_SIZE)
        if i == 0:
            pygame.draw.rect(screen, GREEN, rect)
            pygame.draw.rect(screen, WHITE, rect, 2)
        else:
            pygame.draw.rect(screen, DARK_GREEN, rect)
            pygame.draw.rect(screen, WHITE, rect, 1)


def draw_food(food_pos):
    """绘制红色普通食物"""
    rect = pygame.Rect(food_pos[0] * GRID_SIZE, food_pos[1] * GRID_SIZE,
                       GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, RED, rect)
    pygame.draw.rect(screen, WHITE, rect, 2)


def draw_golden_food(golden_food):
    """绘制金色奖励食物（2x2大小）"""
    if not golden_food.active or golden_food.position is None:
        return

    px, py = golden_food.position
    size = golden_food.size * GRID_SIZE
    rect = pygame.Rect(px * GRID_SIZE, py * GRID_SIZE, size, size)

    # 金色渐变效果（用旋转的圆环模拟）
    pygame.draw.rect(screen, GOLD, rect)
    pygame.draw.rect(screen, YELLOW, rect, 3)

    # 绘制星标✨
    center_x = px * GRID_SIZE + size // 2
    center_y = py * GRID_SIZE + size // 2
    star_text = small_font.render("⭐", True, WHITE)
    screen.blit(star_text, (center_x - 10, center_y - 10))

    # 显示剩余时间（在食物上方）
    remaining = int(golden_food.duration - (time.time() - golden_food.appear_time))
    if remaining >= 0:
        time_text = small_font.render(f"{remaining}s", True, YELLOW)
        screen.blit(time_text, (px * GRID_SIZE, py * GRID_SIZE - 20))


def show_score(score, length, is_boosting):
    """显示分数、长度和加速状态"""
    score_text = font.render(f"分数: {score}", True, WHITE)
    length_text = font.render(f"长度: {length}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(length_text, (10, 50))

    # 显示加速状态
    if is_boosting:
        boost_text = font.render("🚀 加速中!", True, YELLOW)
        screen.blit(boost_text, (WINDOW_WIDTH - 150, 10))


def show_game_over(score, length):
    """显示游戏结束画面"""
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    game_over_text = font.render("游戏结束!", True, RED)
    score_text = font.render(f"最终得分: {score}", True, WHITE)
    length_text = font.render(f"最终长度: {length}", True, WHITE)
    restart_text = font.render("按 R 重新开始  按 ESC 退出", True, WHITE)

    screen.blit(game_over_text,
                (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2,
                 WINDOW_HEIGHT // 2 - 80))
    screen.blit(score_text,
                (WINDOW_WIDTH // 2 - score_text.get_width() // 2,
                 WINDOW_HEIGHT // 2 - 30))
    screen.blit(length_text,
                (WINDOW_WIDTH // 2 - length_text.get_width() // 2,
                 WINDOW_HEIGHT // 2 + 10))
    screen.blit(restart_text,
                (WINDOW_WIDTH // 2 - restart_text.get_width() // 2,
                 WINDOW_HEIGHT // 2 + 60))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    return True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def main():
    """主游戏循环"""
    snake = Snake()
    food = Food(snake.positions)
    golden_food = GoldenFood(snake.positions)
    score = 0
    game_over = False
    is_boosting = False  # 是否正在加速

    # 黄苹果出现计时器
    golden_timer = 0  # 距离上次出现的时间（秒）
    golden_interval = random.randint(30, 60)  # 30~60秒出现一次
    last_time = time.time()

    while True:
        current_time = time.time()
        delta_time = current_time - last_time
        last_time = current_time

        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        snake.change_direction((1, 0))
                    elif event.key == pygame.K_SPACE:
                        is_boosting = True  # 按下空格加速

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    is_boosting = False  # 松开空格停止加速

        if not game_over:
            # 移动蛇
            snake.move()

            # 检测是否吃到普通食物
            if snake.eat_food(food.position):
                score += 10
                food = Food(snake.positions)

            # 检测是否吃到黄苹果（奖励）
            if golden_food.check_eaten(snake.positions):
                score *= 2  # 积分翻倍
                # 长度翻倍（增加当前长度-1的长度，因为蛇头已经算一个）
                current_length = len(snake.positions)
                for _ in range(current_length - 1):
                    snake.grow = True
                    # 立即增长
                    if snake.grow:
                        tail = snake.positions[-1]
                        snake.positions.append(tail)
                        snake.grow = False
                golden_food.active = False
                golden_food.position = None
                golden_timer = 0  # 重置计时器
                golden_interval = random.randint(30, 60)  # 重新设定间隔

            # 检测碰撞
            if snake.check_collision():
                game_over = True

            # 更新黄苹果状态（超时消失）
            golden_food.update(snake.positions)

            # 黄苹果生成逻辑
            golden_timer += delta_time
            if not golden_food.active and golden_timer >= golden_interval:
                # 尝试生成黄苹果
                golden_food.generate(snake.positions)
                if golden_food.active:
                    golden_timer = 0
                    golden_interval = random.randint(30, 60)

        # 绘制画面
        screen.fill(BLACK)
        draw_grid()
        draw_snake(snake)
        draw_food(food.position)
        draw_golden_food(golden_food)
        show_score(score, len(snake.positions), is_boosting)

        if game_over:
            if show_game_over(score, len(snake.positions)):
                # 重新开始
                snake = Snake()
                food = Food(snake.positions)
                golden_food = GoldenFood(snake.positions)
                score = 0
                game_over = False
                is_boosting = False
                golden_timer = 0
                golden_interval = random.randint(30, 60)
                last_time = time.time()

        pygame.display.flip()

        # 控制帧率（速度）
        speed = snake.get_speed(is_boosting)
        clock.tick(speed)


if __name__ == "__main__":
    main()