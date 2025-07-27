import pygame
import random
import json
import os
import time
from datetime import datetime

# 初始化 Pygame
pygame.init()

# 游戏设置
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (64, 128, 255)
DARK_BLUE = (0, 64, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
BROWN = (139, 69, 19)

# 鱼类数据
FISH_TYPES = {
    "小鲫鱼": {"weight_range": (0.1, 0.5), "rarity": 0.4, "color": (255, 215, 0), "points": 10},
    "草鱼": {"weight_range": (0.5, 2.0), "rarity": 0.3, "color": (0, 128, 0), "points": 25},
    "鲤鱼": {"weight_range": (1.0, 5.0), "rarity": 0.2, "color": (255, 140, 0), "points": 50},
    "黑鱼": {"weight_range": (2.0, 8.0), "rarity": 0.08, "color": (64, 64, 64), "points": 100},
    "鲈鱼": {"weight_range": (1.5, 6.0), "rarity": 0.15, "color": (128, 128, 255), "points": 75},
    "金龙鱼": {"weight_range": (5.0, 15.0), "rarity": 0.02, "color": (255, 215, 0), "points": 300},
    "巨型鲸鱼": {"weight_range": (50.0, 200.0), "rarity": 0.001, "color": (0, 0, 139), "points": 1000}
}

class FishingGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("钓鱼游戏 - Fishing Game")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # 游戏状态
        self.state = "menu"  # menu, fishing, leaderboard, records
        self.fishing_line_y = 300
        self.fishing_hook_x = 600
        self.fishing_hook_y = 300
        self.is_casting = False
        self.cast_power = 0
        self.cast_direction = 1
        self.fish_on_hook = None
        self.reeling_in = False
        self.player_name = ""
        self.input_active = False
        
        # 数据文件
        self.leaderboard_file = "leaderboard.json"
        self.records_file = "fish_records.json"
        
        # 加载数据
        self.leaderboard = self.load_leaderboard()
        self.fish_records = self.load_records()
        
        # 统计信息
        self.total_fish_caught = 0
        self.total_weight = 0
        self.session_score = 0
        
    def load_leaderboard(self):
        if os.path.exists(self.leaderboard_file):
            try:
                with open(self.leaderboard_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_leaderboard(self):
        with open(self.leaderboard_file, 'w', encoding='utf-8') as f:
            json.dump(self.leaderboard, f, ensure_ascii=False, indent=2)
    
    def load_records(self):
        if os.path.exists(self.records_file):
            try:
                with open(self.records_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_records(self):
        with open(self.records_file, 'w', encoding='utf-8') as f:
            json.dump(self.fish_records, f, ensure_ascii=False, indent=2)
    
    def add_to_leaderboard(self, name, score, fish_count, total_weight):
        entry = {
            "name": name,
            "score": score,
            "fish_count": fish_count,
            "total_weight": round(total_weight, 2),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.leaderboard.append(entry)
        self.leaderboard.sort(key=lambda x: x["score"], reverse=True)
        self.leaderboard = self.leaderboard[:10]  # 只保留前10名
        self.save_leaderboard()
    
    def add_fish_record(self, fish_type, weight, player_name):
        record = {
            "fish_type": fish_type,
            "weight": round(weight, 2),
            "player": player_name,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.fish_records.append(record)
        self.fish_records.sort(key=lambda x: x["weight"], reverse=True)
        self.save_records()
    
    def catch_fish(self):
        # 随机选择鱼类
        rand = random.random()
        cumulative_prob = 0
        
        for fish_type, data in FISH_TYPES.items():
            cumulative_prob += data["rarity"]
            if rand <= cumulative_prob:
                weight = random.uniform(data["weight_range"][0], data["weight_range"][1])
                return fish_type, weight, data
        
        # 默认返回小鲫鱼
        fish_type = "小鲫鱼"
        data = FISH_TYPES[fish_type]
        weight = random.uniform(data["weight_range"][0], data["weight_range"][1])
        return fish_type, weight, data
    
    def draw_water(self):
        # 绘制水面
        pygame.draw.rect(self.screen, BLUE, (0, 400, WINDOW_WIDTH, WINDOW_HEIGHT - 400))
        
        # 绘制波浪效果
        for i in range(0, WINDOW_WIDTH, 20):
            wave_height = 10 * (1 + 0.5 * pygame.math.Vector2(i/50, time.time()).length())
            pygame.draw.circle(self.screen, DARK_BLUE, (i, 400 + int(wave_height)), 5)
    
    def draw_fishing_rod(self):
        # 绘制钓鱼竿
        rod_start = (100, 200)
        rod_end = (self.fishing_hook_x, self.fishing_hook_y)
        pygame.draw.line(self.screen, BROWN, rod_start, rod_end, 3)
        
        # 绘制钓鱼线
        pygame.draw.line(self.screen, BLACK, rod_end, (self.fishing_hook_x, self.fishing_line_y), 2)
        
        # 绘制鱼钩
        pygame.draw.circle(self.screen, YELLOW, (self.fishing_hook_x, self.fishing_line_y), 5)
    
    def draw_fish(self, x, y, fish_type, size=1):
        data = FISH_TYPES[fish_type]
        color = data["color"]
        
        # 绘制鱼身
        fish_width = int(30 * size)
        fish_height = int(20 * size)
        pygame.draw.ellipse(self.screen, color, (x - fish_width//2, y - fish_height//2, fish_width, fish_height))
        
        # 绘制鱼尾
        tail_points = [
            (x - fish_width//2, y),
            (x - fish_width//2 - 10, y - 8),
            (x - fish_width//2 - 10, y + 8)
        ]
        pygame.draw.polygon(self.screen, color, tail_points)
        
        # 绘制眼睛
        pygame.draw.circle(self.screen, WHITE, (x + fish_width//4, y - fish_height//4), 3)
        pygame.draw.circle(self.screen, BLACK, (x + fish_width//4, y - fish_height//4), 2)
    
    def draw_menu(self):
        self.screen.fill(WHITE)
        
        # 标题
        title = self.font_large.render("钓鱼游戏", True, BLACK)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 150))
        self.screen.blit(title, title_rect)
        
        # 输入框
        input_label = self.font_medium.render("请输入您的姓名:", True, BLACK)
        input_rect = input_label.get_rect(center=(WINDOW_WIDTH//2, 250))
        self.screen.blit(input_label, input_rect)
        
        # 名字输入框
        input_box = pygame.Rect(WINDOW_WIDTH//2 - 150, 280, 300, 40)
        color = BLUE if self.input_active else GRAY
        pygame.draw.rect(self.screen, color, input_box, 2)
        
        name_surface = self.font_medium.render(self.player_name, True, BLACK)
        self.screen.blit(name_surface, (input_box.x + 10, input_box.y + 10))
        
        # 按钮
        buttons = [
            ("开始钓鱼", 350),
            ("排行榜", 420),
            ("鱼类记录", 490)
        ]
        
        for text, y in buttons:
            button_rect = pygame.Rect(WINDOW_WIDTH//2 - 100, y, 200, 50)
            pygame.draw.rect(self.screen, GREEN, button_rect)
            pygame.draw.rect(self.screen, BLACK, button_rect, 2)
            
            button_text = self.font_medium.render(text, True, BLACK)
            text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, text_rect)
    
    def draw_fishing_scene(self):
        self.screen.fill(WHITE)
        
        # 绘制天空
        pygame.draw.rect(self.screen, (135, 206, 235), (0, 0, WINDOW_WIDTH, 400))
        
        # 绘制水面
        self.draw_water()
        
        # 绘制钓鱼竿
        self.draw_fishing_rod()
        
        # 如果有鱼上钩，绘制鱼
        if self.fish_on_hook:
            fish_type, weight, _ = self.fish_on_hook
            self.draw_fish(self.fishing_hook_x, self.fishing_line_y - 20, fish_type, weight/5 + 0.5)
        
        # 绘制力量条（抛竿时）
        if self.is_casting and not self.reeling_in:
            power_rect = pygame.Rect(50, 50, 200, 20)
            pygame.draw.rect(self.screen, GRAY, power_rect)
            power_fill = pygame.Rect(50, 50, int(200 * self.cast_power / 100), 20)
            pygame.draw.rect(self.screen, GREEN if self.cast_power < 80 else RED, power_fill)
            
            power_text = self.font_small.render(f"力量: {int(self.cast_power)}%", True, BLACK)
            self.screen.blit(power_text, (50, 25))
        
        # 绘制统计信息
        stats_y = 50
        stats = [
            f"钓鱼者: {self.player_name}",
            f"本次钓鱼: {self.total_fish_caught} 条",
            f"总重量: {self.total_weight:.2f} kg",
            f"得分: {self.session_score}"
        ]
        
        for i, stat in enumerate(stats):
            text = self.font_small.render(stat, True, BLACK)
            self.screen.blit(text, (WINDOW_WIDTH - 250, stats_y + i * 25))
        
        # 操作提示
        if not self.is_casting and not self.reeling_in:
            hint = self.font_small.render("按空格键抛竿", True, BLACK)
            self.screen.blit(hint, (50, WINDOW_HEIGHT - 100))
        elif self.is_casting and not self.fish_on_hook:
            hint = self.font_small.render("再按空格键确定力量", True, BLACK)
            self.screen.blit(hint, (50, WINDOW_HEIGHT - 100))
        elif self.fish_on_hook and not self.reeling_in:
            hint = self.font_small.render("有鱼上钩了！按回车收线", True, BLACK)
            self.screen.blit(hint, (50, WINDOW_HEIGHT - 100))
        elif self.reeling_in:
            hint = self.font_small.render("正在收线...", True, BLACK)
            self.screen.blit(hint, (50, WINDOW_HEIGHT - 100))
        
        # 返回按钮
        back_button = pygame.Rect(50, WINDOW_HEIGHT - 50, 100, 30)
        pygame.draw.rect(self.screen, YELLOW, back_button)
        pygame.draw.rect(self.screen, BLACK, back_button, 2)
        back_text = self.font_small.render("返回菜单", True, BLACK)
        text_rect = back_text.get_rect(center=back_button.center)
        self.screen.blit(back_text, text_rect)
    
    def draw_leaderboard(self):
        self.screen.fill(WHITE)
        
        title = self.font_large.render("排行榜", True, BLACK)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 50))
        self.screen.blit(title, title_rect)
        
        headers = ["排名", "姓名", "得分", "鱼数", "总重量(kg)", "日期"]
        header_y = 120
        col_widths = [80, 150, 100, 80, 120, 200]
        col_x = [50, 130, 280, 380, 460, 580]
        
        # 绘制表头
        for i, header in enumerate(headers):
            text = self.font_medium.render(header, True, BLACK)
            self.screen.blit(text, (col_x[i], header_y))
        
        # 绘制分割线
        pygame.draw.line(self.screen, BLACK, (50, header_y + 35), (WINDOW_WIDTH - 50, header_y + 35), 2)
        
        # 绘制排行榜数据
        for i, entry in enumerate(self.leaderboard[:10]):
            y = header_y + 60 + i * 40
            data = [
                str(i + 1),
                entry["name"],
                str(entry["score"]),
                str(entry["fish_count"]),
                str(entry["total_weight"]),
                entry["date"]
            ]
            
            for j, item in enumerate(data):
                color = RED if i == 0 else (BLUE if i < 3 else BLACK)
                text = self.font_small.render(item, True, color)
                self.screen.blit(text, (col_x[j], y))
        
        # 返回按钮
        back_button = pygame.Rect(WINDOW_WIDTH//2 - 50, WINDOW_HEIGHT - 80, 100, 40)
        pygame.draw.rect(self.screen, GREEN, back_button)
        pygame.draw.rect(self.screen, BLACK, back_button, 2)
        back_text = self.font_medium.render("返回", True, BLACK)
        text_rect = back_text.get_rect(center=back_button.center)
        self.screen.blit(back_text, text_rect)
    
    def draw_records(self):
        self.screen.fill(WHITE)
        
        title = self.font_large.render("鱼类记录", True, BLACK)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 50))
        self.screen.blit(title, title_rect)
        
        headers = ["鱼类", "重量(kg)", "钓鱼者", "日期"]
        header_y = 120
        col_widths = [150, 120, 150, 200]
        col_x = [200, 350, 470, 620]
        
        # 绘制表头
        for i, header in enumerate(headers):
            text = self.font_medium.render(header, True, BLACK)
            self.screen.blit(text, (col_x[i], header_y))
        
        # 绘制分割线
        pygame.draw.line(self.screen, BLACK, (200, header_y + 35), (WINDOW_WIDTH - 200, header_y + 35), 2)
        
        # 绘制记录数据
        for i, record in enumerate(self.fish_records[:15]):
            y = header_y + 60 + i * 35
            data = [
                record["fish_type"],
                str(record["weight"]),
                record["player"],
                record["date"]
            ]
            
            fish_data = FISH_TYPES.get(record["fish_type"], FISH_TYPES["小鲫鱼"])
            color = fish_data["color"] if record["weight"] > 5 else BLACK
            
            for j, item in enumerate(data):
                text = self.font_small.render(item, True, color)
                self.screen.blit(text, (col_x[j], y))
        
        # 返回按钮
        back_button = pygame.Rect(WINDOW_WIDTH//2 - 50, WINDOW_HEIGHT - 80, 100, 40)
        pygame.draw.rect(self.screen, GREEN, back_button)
        pygame.draw.rect(self.screen, BLACK, back_button, 2)
        back_text = self.font_medium.render("返回", True, BLACK)
        text_rect = back_text.get_rect(center=back_button.center)
        self.screen.blit(back_text, text_rect)
    
    def handle_menu_click(self, pos):
        x, y = pos
        
        # 检查输入框点击
        input_box = pygame.Rect(WINDOW_WIDTH//2 - 150, 280, 300, 40)
        if input_box.collidepoint(pos):
            self.input_active = True
        else:
            self.input_active = False
        
        # 检查按钮点击
        buttons = [
            ("fishing", pygame.Rect(WINDOW_WIDTH//2 - 100, 350, 200, 50)),
            ("leaderboard", pygame.Rect(WINDOW_WIDTH//2 - 100, 420, 200, 50)),
            ("records", pygame.Rect(WINDOW_WIDTH//2 - 100, 490, 200, 50))
        ]
        
        for state, rect in buttons:
            if rect.collidepoint(pos):
                if state == "fishing" and self.player_name.strip():
                    self.state = state
                    self.reset_fishing()
                elif state in ["leaderboard", "records"]:
                    self.state = state
    
    def handle_fishing_click(self, pos):
        # 检查返回按钮
        back_button = pygame.Rect(50, WINDOW_HEIGHT - 50, 100, 30)
        if back_button.collidepoint(pos):
            self.state = "menu"
    
    def handle_other_click(self, pos):
        # 检查返回按钮
        back_button = pygame.Rect(WINDOW_WIDTH//2 - 50, WINDOW_HEIGHT - 80, 100, 40)
        if back_button.collidepoint(pos):
            self.state = "menu"
    
    def reset_fishing(self):
        self.fishing_line_y = 300
        self.fishing_hook_x = 600
        self.fishing_hook_y = 300
        self.is_casting = False
        self.cast_power = 0
        self.cast_direction = 1
        self.fish_on_hook = None
        self.reeling_in = False
        self.total_fish_caught = 0
        self.total_weight = 0
        self.session_score = 0
    
    def update_fishing(self):
        if self.is_casting and not self.fish_on_hook and not self.reeling_in:
            # 更新抛竿力量
            self.cast_power += self.cast_direction * 2
            if self.cast_power >= 100:
                self.cast_power = 100
                self.cast_direction = -1
            elif self.cast_power <= 0:
                self.cast_power = 0
                self.cast_direction = 1
        
        # 随机生成鱼上钩
        if (self.fishing_line_y > 400 and not self.fish_on_hook and 
            not self.is_casting and not self.reeling_in and random.random() < 0.01):
            self.fish_on_hook = self.catch_fish()
        
        # 收线动画
        if self.reeling_in:
            if self.fishing_line_y > 300:
                self.fishing_line_y -= 5
            else:
                self.reeling_in = False
                if self.fish_on_hook:
                    fish_type, weight, fish_data = self.fish_on_hook
                    points = fish_data["points"]
                    weight_bonus = int(weight * 10)
                    total_points = points + weight_bonus
                    
                    # 更新统计
                    self.total_fish_caught += 1
                    self.total_weight += weight
                    self.session_score += total_points
                    
                    # 添加到记录
                    self.add_fish_record(fish_type, weight, self.player_name)
                    
                    # 显示捕获信息
                    print(f"捕获了 {fish_type}，重量: {weight:.2f}kg，得分: {total_points}")
                    
                    self.fish_on_hook = None
    
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # 保存最终成绩到排行榜
                    if self.state == "fishing" and self.player_name.strip() and self.total_fish_caught > 0:
                        self.add_to_leaderboard(
                            self.player_name, 
                            self.session_score, 
                            self.total_fish_caught, 
                            self.total_weight
                        )
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == "menu":
                        self.handle_menu_click(event.pos)
                    elif self.state == "fishing":
                        self.handle_fishing_click(event.pos)
                    else:
                        self.handle_other_click(event.pos)
                
                elif event.type == pygame.KEYDOWN:
                    if self.state == "menu" and self.input_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.player_name = self.player_name[:-1]
                        elif event.unicode.isprintable():
                            self.player_name += event.unicode
                    
                    elif self.state == "fishing":
                        if event.key == pygame.K_SPACE:
                            if not self.is_casting and not self.fish_on_hook and not self.reeling_in:
                                self.is_casting = True
                                self.cast_power = 0
                                self.cast_direction = 1
                            elif self.is_casting and not self.fish_on_hook:
                                # 确定抛竿
                                distance = self.cast_power * 8  # 最远800像素
                                self.fishing_hook_x = min(600 + distance, WINDOW_WIDTH - 50)
                                self.fishing_line_y = 420 + self.cast_power * 2  # 最深620
                                self.is_casting = False
                        
                        elif event.key == pygame.K_RETURN:
                            if self.fish_on_hook and not self.reeling_in:
                                self.reeling_in = True
                        
                        elif event.key == pygame.K_ESCAPE:
                            # 保存成绩并返回菜单
                            if self.player_name.strip() and self.total_fish_caught > 0:
                                self.add_to_leaderboard(
                                    self.player_name, 
                                    self.session_score, 
                                    self.total_fish_caught, 
                                    self.total_weight
                                )
                            self.state = "menu"
            
            # 更新游戏状态
            if self.state == "fishing":
                self.update_fishing()
            
            # 绘制界面
            if self.state == "menu":
                self.draw_menu()
            elif self.state == "fishing":
                self.draw_fishing_scene()
            elif self.state == "leaderboard":
                self.draw_leaderboard()
            elif self.state == "records":
                self.draw_records()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = FishingGame()
    game.run()