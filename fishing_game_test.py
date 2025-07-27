#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
钓鱼游戏 - 命令行测试版本
用于验证游戏逻辑和数据存储功能
"""

import random
import json
import os
import time
from datetime import datetime

# 鱼类数据
FISH_TYPES = {
    "小鲫鱼": {"weight_range": (0.1, 0.5), "rarity": 0.4, "color": "金黄色", "points": 10},
    "草鱼": {"weight_range": (0.5, 2.0), "rarity": 0.3, "color": "绿色", "points": 25},
    "鲤鱼": {"weight_range": (1.0, 5.0), "rarity": 0.2, "color": "橙色", "points": 50},
    "黑鱼": {"weight_range": (2.0, 8.0), "rarity": 0.08, "color": "黑色", "points": 100},
    "鲈鱼": {"weight_range": (1.5, 6.0), "rarity": 0.15, "color": "银蓝色", "points": 75},
    "金龙鱼": {"weight_range": (5.0, 15.0), "rarity": 0.02, "color": "金色", "points": 300},
    "巨型鲸鱼": {"weight_range": (50.0, 200.0), "rarity": 0.001, "color": "深蓝色", "points": 1000}
}

class FishingGameCLI:
    def __init__(self):
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
        self.player_name = ""
        
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
    
    def print_banner(self):
        print("=" * 60)
        print("🎣 欢迎来到钓鱼游戏 🎣")
        print("=" * 60)
        print()
    
    def get_player_name(self):
        while True:
            name = input("请输入您的姓名: ").strip()
            if name:
                self.player_name = name
                break
            print("姓名不能为空，请重新输入！")
    
    def show_menu(self):
        print("\n📋 主菜单")
        print("1. 开始钓鱼")
        print("2. 查看排行榜")
        print("3. 查看鱼类记录")
        print("4. 退出游戏")
        print("-" * 30)
    
    def fishing_session(self):
        print(f"\n🎣 {self.player_name}，开始钓鱼！")
        print("=" * 40)
        
        # 重置会话统计
        self.total_fish_caught = 0
        self.total_weight = 0
        self.session_score = 0
        
        while True:
            print("\n选择操作:")
            print("1. 抛竿钓鱼")
            print("2. 查看当前统计")
            print("3. 返回主菜单")
            
            choice = input("请选择 (1-3): ").strip()
            
            if choice == "1":
                self.cast_line()
            elif choice == "2":
                self.show_session_stats()
            elif choice == "3":
                if self.total_fish_caught > 0:
                    self.add_to_leaderboard(
                        self.player_name, 
                        self.session_score, 
                        self.total_fish_caught, 
                        self.total_weight
                    )
                    print(f"\n✅ 成绩已保存到排行榜！")
                break
            else:
                print("❌ 无效选择，请重新输入！")
    
    def cast_line(self):
        print("\n🎣 正在抛竿...")
        time.sleep(1)
        
        # 模拟抛竿力量
        power = random.randint(20, 100)
        print(f"抛竿力量: {power}%")
        
        # 等待鱼上钩 (模拟)
        wait_time = random.randint(1, 5)
        print(f"等待鱼上钩... (等待 {wait_time} 秒)")
        time.sleep(wait_time)
        
        # 随机决定是否有鱼上钩
        if random.random() < 0.7:  # 70% 概率有鱼
            fish_type, weight, fish_data = self.catch_fish()
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
            print(f"\n🐟 恭喜！钓到了一条 {fish_type}！")
            print(f"   颜色: {fish_data['color']}")
            print(f"   重量: {weight:.2f} kg")
            print(f"   得分: {total_points} 分")
            
            # 特殊鱼类提示
            if fish_data["rarity"] <= 0.05:
                print("🌟 哇！这是一条稀有鱼类！")
        else:
            print("😔 很遗憾，这次没有鱼上钩...")
    
    def show_session_stats(self):
        print(f"\n📊 当前钓鱼统计")
        print("=" * 30)
        print(f"钓鱼者: {self.player_name}")
        print(f"钓鱼总数: {self.total_fish_caught} 条")
        print(f"总重量: {self.total_weight:.2f} kg")
        print(f"总得分: {self.session_score} 分")
        
        if self.total_fish_caught > 0:
            avg_weight = self.total_weight / self.total_fish_caught
            print(f"平均重量: {avg_weight:.2f} kg")
    
    def show_leaderboard(self):
        print("\n🏆 排行榜 (前10名)")
        print("=" * 60)
        
        if not self.leaderboard:
            print("暂无排行榜记录")
            return
        
        print(f"{'排名':<4} {'姓名':<10} {'得分':<8} {'鱼数':<6} {'总重量(kg)':<10} {'日期':<16}")
        print("-" * 60)
        
        for i, entry in enumerate(self.leaderboard[:10]):
            rank_symbol = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"{i+1:2d}"
            print(f"{rank_symbol:<4} {entry['name']:<10} {entry['score']:<8} "
                  f"{entry['fish_count']:<6} {entry['total_weight']:<10} {entry['date']:<16}")
    
    def show_fish_records(self):
        print("\n🐟 鱼类记录 (按重量排序)")
        print("=" * 60)
        
        if not self.fish_records:
            print("暂无鱼类记录")
            return
        
        print(f"{'鱼类':<12} {'重量(kg)':<10} {'钓鱼者':<12} {'日期':<16}")
        print("-" * 60)
        
        for i, record in enumerate(self.fish_records[:15]):
            weight_symbol = "🐋" if record["weight"] > 10 else "🐟"
            print(f"{weight_symbol} {record['fish_type']:<10} {record['weight']:<10} "
                  f"{record['player']:<12} {record['date']:<16}")
    
    def show_fish_guide(self):
        print("\n📖 鱼类图鉴")
        print("=" * 50)
        
        for fish_type, data in FISH_TYPES.items():
            rarity_desc = ("极其稀有" if data["rarity"] <= 0.01 else
                          "稀有" if data["rarity"] <= 0.1 else
                          "普通" if data["rarity"] <= 0.3 else
                          "常见")
            
            print(f"\n🐟 {fish_type}")
            print(f"   重量范围: {data['weight_range'][0]:.1f} - {data['weight_range'][1]:.1f} kg")
            print(f"   稀有度: {rarity_desc} ({data['rarity']*100:.1f}%)")
            print(f"   基础分数: {data['points']} 分")
            print(f"   颜色: {data['color']}")
    
    def run(self):
        self.print_banner()
        self.get_player_name()
        
        while True:
            self.show_menu()
            choice = input("请选择 (1-4): ").strip()
            
            if choice == "1":
                self.fishing_session()
            elif choice == "2":
                self.show_leaderboard()
            elif choice == "3":
                self.show_fish_records()
            elif choice == "4":
                print("\n👋 感谢游玩钓鱼游戏！再见！")
                break
            else:
                print("❌ 无效选择，请重新输入！")

def main():
    """主函数"""
    try:
        game = FishingGameCLI()
        game.run()
    except KeyboardInterrupt:
        print("\n\n👋 游戏被中断，再见！")
    except Exception as e:
        print(f"\n❌ 游戏运行出错: {e}")

if __name__ == "__main__":
    main()