import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import threading
from datetime import datetime
import json
import os

class FishingGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("钓鱼游戏 - Fishing Game")
        self.root.geometry("1000x700")
        self.root.configure(bg='lightblue')
        
        # 游戏数据
        self.fish_types = {
            "鲫鱼": {"weight_range": (0.1, 0.8), "rarity": 0.4, "color": "silver"},
            "鲤鱼": {"weight_range": (0.5, 2.5), "rarity": 0.3, "color": "gold"},
            "草鱼": {"weight_range": (1.0, 4.0), "rarity": 0.15, "color": "green"},
            "黑鱼": {"weight_range": (0.8, 3.5), "rarity": 0.1, "color": "black"},
            "鲈鱼": {"weight_range": (0.3, 1.5), "rarity": 0.04, "color": "gray"},
            "金鱼": {"weight_range": (0.1, 0.3), "rarity": 0.01, "color": "orange"}
        }
        
        self.caught_fish = []
        self.is_fishing = False
        self.fishing_line_y = 200
        
        # 加载历史记录
        self.load_records()
        
        # 创建界面
        self.create_widgets()
        
    def create_widgets(self):
        # 主框架
        main_frame = tk.Frame(self.root, bg='lightblue')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧游戏区域
        game_frame = tk.Frame(main_frame, bg='lightblue', width=600)
        game_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 画布 - 钓鱼场景
        self.canvas = tk.Canvas(game_frame, width=580, height=400, bg='skyblue')
        self.canvas.pack(pady=10)
        
        # 绘制池塘背景
        self.draw_scene()
        
        # 控制按钮
        control_frame = tk.Frame(game_frame, bg='lightblue')
        control_frame.pack(pady=10)
        
        self.fishing_btn = tk.Button(control_frame, text="开始钓鱼", 
                                   command=self.start_fishing, 
                                   font=('Arial', 12), 
                                   bg='green', fg='white',
                                   width=12, height=2)
        self.fishing_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(control_frame, text="停止钓鱼", 
                                command=self.stop_fishing, 
                                font=('Arial', 12), 
                                bg='red', fg='white',
                                width=12, height=2)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # 状态显示
        self.status_label = tk.Label(game_frame, text="准备钓鱼...", 
                                   font=('Arial', 10), bg='lightblue')
        self.status_label.pack(pady=5)
        
        # 右侧信息区域
        info_frame = tk.Frame(main_frame, bg='lightgray', width=350)
        info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        info_frame.pack_propagate(False)
        
        # 当前钓鱼记录
        current_label = tk.Label(info_frame, text="本次钓鱼记录", 
                               font=('Arial', 12, 'bold'), bg='lightgray')
        current_label.pack(pady=5)
        
        # 创建表格
        columns = ("鱼类", "重量(kg)", "时间")
        self.tree = ttk.Treeview(info_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        tree_frame = tk.Frame(info_frame, bg='lightgray')
        tree_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 统计信息
        stats_frame = tk.Frame(info_frame, bg='lightgray')
        stats_frame.pack(pady=10, fill=tk.X, padx=10)
        
        self.stats_label = tk.Label(stats_frame, text="统计信息:", 
                                  font=('Arial', 10, 'bold'), bg='lightgray')
        self.stats_label.pack()
        
        self.total_fish_label = tk.Label(stats_frame, text="总计: 0 条鱼", 
                                       font=('Arial', 9), bg='lightgray')
        self.total_fish_label.pack()
        
        self.total_weight_label = tk.Label(stats_frame, text="总重量: 0.0 kg", 
                                         font=('Arial', 9), bg='lightgray')
        self.total_weight_label.pack()
        
        # 排行榜按钮
        ranking_btn = tk.Button(info_frame, text="查看排行榜", 
                              command=self.show_ranking, 
                              font=('Arial', 10), 
                              bg='blue', fg='white')
        ranking_btn.pack(pady=10)
        
        # 清空记录按钮
        clear_btn = tk.Button(info_frame, text="清空本次记录", 
                            command=self.clear_current_records, 
                            font=('Arial', 10), 
                            bg='orange', fg='white')
        clear_btn.pack(pady=5)
        
    def draw_scene(self):
        # 清空画布
        self.canvas.delete("all")
        
        # 绘制池塘
        self.canvas.create_oval(50, 200, 530, 380, fill='blue', outline='darkblue', width=3)
        
        # 绘制岸边
        self.canvas.create_rectangle(0, 150, 580, 200, fill='brown', outline='')
        self.canvas.create_rectangle(0, 100, 580, 150, fill='green', outline='')
        
        # 绘制小人
        self.draw_person()
        
        # 绘制鱼竿
        self.draw_fishing_rod()
        
        # 绘制一些装饰
        self.canvas.create_text(290, 50, text="🌞", font=('Arial', 30))
        self.canvas.create_text(100, 70, text="🌲", font=('Arial', 25))
        self.canvas.create_text(480, 70, text="🌲", font=('Arial', 25))
        
    def draw_person(self):
        # 小人身体
        x, y = 150, 120
        
        # 头
        self.canvas.create_oval(x-10, y-20, x+10, y, fill='peachpuff', outline='black')
        
        # 身体
        self.canvas.create_rectangle(x-8, y, x+8, y+30, fill='blue', outline='black')
        
        # 手臂
        self.canvas.create_line(x-8, y+10, x-20, y+20, width=3, fill='peachpuff')
        self.canvas.create_line(x+8, y+10, x+30, y+5, width=3, fill='peachpuff')  # 持竿手臂
        
        # 腿
        self.canvas.create_line(x-5, y+30, x-10, y+50, width=3, fill='blue')
        self.canvas.create_line(x+5, y+30, x+10, y+50, width=3, fill='blue')
        
    def draw_fishing_rod(self):
        # 鱼竿
        self.canvas.create_line(180, 125, 250, 100, width=3, fill='brown', tags="rod")
        
        # 鱼线
        self.fishing_line = self.canvas.create_line(250, 100, 290, self.fishing_line_y, 
                                                  width=2, fill='gray', tags="line")
        
        # 鱼钩
        self.fish_hook = self.canvas.create_oval(288, self.fishing_line_y-2, 292, self.fishing_line_y+2, 
                                               fill='silver', tags="hook")
        
    def start_fishing(self):
        if not self.is_fishing:
            self.is_fishing = True
            self.fishing_btn.config(state='disabled')
            self.status_label.config(text="正在钓鱼...")
            
            # 开始钓鱼动画
            threading.Thread(target=self.fishing_animation, daemon=True).start()
            
    def stop_fishing(self):
        self.is_fishing = False
        self.fishing_btn.config(state='normal')
        self.status_label.config(text="准备钓鱼...")
        
    def fishing_animation(self):
        while self.is_fishing:
            # 鱼线摆动动画
            for i in range(20):
                if not self.is_fishing:
                    break
                self.fishing_line_y = 280 + random.randint(-10, 10)
                self.canvas.coords(self.fishing_line, 250, 100, 290, self.fishing_line_y)
                self.canvas.coords(self.fish_hook, 288, self.fishing_line_y-2, 292, self.fishing_line_y+2)
                time.sleep(0.1)
            
            # 随机决定是否钓到鱼
            if self.is_fishing and random.random() < 0.3:  # 30% 概率钓到鱼
                self.catch_fish()
                
            time.sleep(1)
            
    def catch_fish(self):
        # 选择鱼的种类
        fish_type = self.select_fish_type()
        fish_data = self.fish_types[fish_type]
        
        # 生成重量
        weight = round(random.uniform(*fish_data["weight_range"]), 2)
        
        # 记录钓到的鱼
        catch_time = datetime.now().strftime("%H:%M:%S")
        fish_record = {
            "type": fish_type,
            "weight": weight,
            "time": catch_time,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        
        self.caught_fish.append(fish_record)
        
        # 更新界面
        self.root.after(0, self.update_fish_display, fish_record)
        
        # 钓鱼成功动画
        self.root.after(0, self.fish_caught_animation, fish_type)
        
    def select_fish_type(self):
        # 根据稀有度选择鱼类
        rand = random.random()
        cumulative = 0
        
        for fish_type, data in self.fish_types.items():
            cumulative += data["rarity"]
            if rand <= cumulative:
                return fish_type
        
        return list(self.fish_types.keys())[0]
        
    def fish_caught_animation(self, fish_type):
        # 显示钓到鱼的提示
        self.status_label.config(text=f"钓到了 {fish_type}!")
        
        # 在池塘中显示鱼的图标
        fish_x = random.randint(100, 450)
        fish_y = random.randint(250, 350)
        
        fish_icon = self.canvas.create_text(fish_x, fish_y, text="🐟", 
                                          font=('Arial', 20), tags="caught_fish")
        
        # 1秒后移除鱼图标
        self.root.after(1000, lambda: self.canvas.delete(fish_icon))
        
    def update_fish_display(self, fish_record):
        # 添加到表格
        self.tree.insert("", "end", values=(
            fish_record["type"], 
            f"{fish_record['weight']}", 
            fish_record["time"]
        ))
        
        # 自动滚动到最新记录
        children = self.tree.get_children()
        if children:
            self.tree.see(children[-1])
        
        # 更新统计信息
        self.update_statistics()
        
    def update_statistics(self):
        total_fish = len(self.caught_fish)
        total_weight = sum(fish["weight"] for fish in self.caught_fish)
        
        self.total_fish_label.config(text=f"总计: {total_fish} 条鱼")
        self.total_weight_label.config(text=f"总重量: {total_weight:.2f} kg")
        
    def show_ranking(self):
        # 创建排行榜窗口
        ranking_window = tk.Toplevel(self.root)
        ranking_window.title("钓鱼排行榜")
        ranking_window.geometry("500x400")
        ranking_window.configure(bg='lightblue')
        
        # 标题
        title_label = tk.Label(ranking_window, text="🏆 钓鱼排行榜 🏆", 
                             font=('Arial', 16, 'bold'), bg='lightblue')
        title_label.pack(pady=10)
        
        # 创建排行榜表格
        columns = ("排名", "鱼类", "重量(kg)", "日期")
        ranking_tree = ttk.Treeview(ranking_window, columns=columns, show='headings', height=15)
        
        for col in columns:
            ranking_tree.heading(col, text=col)
            ranking_tree.column(col, width=120)
        
        # 按重量排序
        all_fish = sorted(self.caught_fish, key=lambda x: x["weight"], reverse=True)
        
        # 显示前20条记录
        for i, fish in enumerate(all_fish[:20], 1):
            ranking_tree.insert("", "end", values=(
                i, fish["type"], f"{fish['weight']}", fish["date"]
            ))
        
        ranking_tree.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # 滚动条
        ranking_scrollbar = ttk.Scrollbar(ranking_window, orient=tk.VERTICAL, command=ranking_tree.yview)
        ranking_tree.configure(yscrollcommand=ranking_scrollbar.set)
        ranking_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def clear_current_records(self):
        if messagebox.askyesno("确认", "确定要清空本次钓鱼记录吗？"):
            self.caught_fish.clear()
            
            # 清空表格
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # 重置统计
            self.update_statistics()
            
    def load_records(self):
        # 从文件加载历史记录
        try:
            if os.path.exists("fishing_records.json"):
                with open("fishing_records.json", "r", encoding="utf-8") as f:
                    self.caught_fish = json.load(f)
        except:
            self.caught_fish = []
            
    def save_records(self):
        # 保存记录到文件
        try:
            with open("fishing_records.json", "w", encoding="utf-8") as f:
                json.dump(self.caught_fish, f, ensure_ascii=False, indent=2)
        except:
            pass
            
    def on_closing(self):
        # 关闭程序时保存记录
        self.is_fishing = False
        self.save_records()
        self.root.destroy()
        
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

if __name__ == "__main__":
    game = FishingGame()
    game.run()