#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
钓鱼游戏演示脚本
自动运行游戏的各种功能来展示完整的游戏体验
"""

import random
import json
import os
import time
from datetime import datetime
from fishing_game_test import FishingGameCLI, FISH_TYPES

class FishingGameDemo(FishingGameCLI):
    def __init__(self):
        super().__init__()
        self.demo_players = ["小明", "小红", "小李", "小王", "小张"]
        
    def demo_fishing_session(self, player_name, fish_count=5):
        """演示一个钓鱼会话"""
        print(f"\n🎣 演示玩家 {player_name} 的钓鱼会话")
        print("=" * 50)
        
        self.player_name = player_name
        self.total_fish_caught = 0
        self.total_weight = 0
        self.session_score = 0
        
        for i in range(fish_count):
            print(f"\n第 {i+1} 次抛竿:")
            
            # 模拟抛竿
            power = random.randint(30, 100)
            print(f"  抛竿力量: {power}%")
            
            # 模拟等待
            wait_time = random.uniform(0.5, 2.0)
            time.sleep(wait_time)
            
            # 决定是否有鱼 (演示模式提高概率)
            if random.random() < 0.8:  # 80% 概率有鱼
                fish_type, weight, fish_data = self.catch_fish()
                points = fish_data["points"]
                weight_bonus = int(weight * 10)
                total_points = points + weight_bonus
                
                # 更新统计
                self.total_fish_caught += 1
                self.total_weight += weight
                self.session_score += total_points
                
                # 添加到记录
                self.add_fish_record(fish_type, weight, player_name)
                
                # 显示结果
                print(f"  ✅ 钓到了 {fish_type} ({fish_data['color']}) - {weight:.2f}kg - {total_points}分")
                
                if fish_data["rarity"] <= 0.05:
                    print("  🌟 稀有鱼类！")
            else:
                print("  ❌ 没有鱼上钩")
        
        # 保存成绩
        if self.total_fish_caught > 0:
            self.add_to_leaderboard(
                player_name, 
                self.session_score, 
                self.total_fish_caught, 
                self.total_weight
            )
            
        # 显示会话总结
        print(f"\n📊 {player_name} 的钓鱼总结:")
        print(f"  钓鱼总数: {self.total_fish_caught} 条")
        print(f"  总重量: {self.total_weight:.2f} kg")
        print(f"  总得分: {self.session_score} 分")
        
        if self.total_fish_caught > 0:
            avg_weight = self.total_weight / self.total_fish_caught
            print(f"  平均重量: {avg_weight:.2f} kg")
    
    def demo_multiple_players(self):
        """演示多个玩家的游戏会话"""
        print("\n🎮 多玩家钓鱼演示")
        print("=" * 60)
        
        for player in self.demo_players:
            # 随机钓鱼次数
            fish_count = random.randint(3, 8)
            self.demo_fishing_session(player, fish_count)
            time.sleep(1)  # 短暂暂停
    
    def show_demo_leaderboard(self):
        """显示演示排行榜"""
        print("\n🏆 演示排行榜")
        print("=" * 60)
        
        if not self.leaderboard:
            print("暂无排行榜记录")
            return
        
        print(f"{'排名':<6} {'姓名':<8} {'得分':<8} {'鱼数':<6} {'总重量':<10} {'日期':<16}")
        print("-" * 60)
        
        for i, entry in enumerate(self.leaderboard):
            rank_icons = ["🥇", "🥈", "🥉"]
            rank_display = rank_icons[i] if i < 3 else f"{i+1:2d}."
            
            print(f"{rank_display:<6} {entry['name']:<8} {entry['score']:<8} "
                  f"{entry['fish_count']:<6} {entry['total_weight']:<10} {entry['date']:<16}")
    
    def show_demo_fish_records(self):
        """显示演示鱼类记录"""
        print("\n🐟 演示鱼类记录 (最重的前15条)")
        print("=" * 60)
        
        if not self.fish_records:
            print("暂无鱼类记录")
            return
        
        print(f"{'鱼类':<12} {'重量(kg)':<10} {'钓鱼者':<10} {'日期':<16}")
        print("-" * 60)
        
        for i, record in enumerate(self.fish_records[:15]):
            weight_icon = "🐋" if record["weight"] > 10 else "🐟"
            rarity_icon = "⭐" if record["weight"] > 5 else ""
            
            print(f"{weight_icon} {record['fish_type']:<10} {record['weight']:<10} "
                  f"{record['player']:<10} {record['date']:<16} {rarity_icon}")
    
    def show_fish_statistics(self):
        """显示鱼类统计信息"""
        print("\n📈 鱼类统计分析")
        print("=" * 50)
        
        if not self.fish_records:
            print("暂无数据可分析")
            return
        
        # 统计每种鱼的数量
        fish_count = {}
        total_weight_by_type = {}
        
        for record in self.fish_records:
            fish_type = record["fish_type"]
            weight = record["weight"]
            
            fish_count[fish_type] = fish_count.get(fish_type, 0) + 1
            total_weight_by_type[fish_type] = total_weight_by_type.get(fish_type, 0) + weight
        
        print("各类鱼的钓获统计:")
        print(f"{'鱼类':<12} {'数量':<6} {'总重量':<10} {'平均重量':<10}")
        print("-" * 45)
        
        for fish_type in FISH_TYPES.keys():
            if fish_type in fish_count:
                count = fish_count[fish_type]
                total_weight = total_weight_by_type[fish_type]
                avg_weight = total_weight / count
                print(f"{fish_type:<12} {count:<6} {total_weight:<10.2f} {avg_weight:<10.2f}")
            else:
                print(f"{fish_type:<12} 0     0.00       0.00")
        
        # 最重的鱼
        heaviest = max(self.fish_records, key=lambda x: x["weight"])
        print(f"\n🏆 最重的鱼: {heaviest['fish_type']} - {heaviest['weight']} kg")
        print(f"   钓鱼者: {heaviest['player']} ({heaviest['date']})")
        
        # 最多鱼的玩家
        player_count = {}
        for record in self.fish_records:
            player = record["player"]
            player_count[player] = player_count.get(player, 0) + 1
        
        if player_count:
            top_player = max(player_count.items(), key=lambda x: x[1])
            print(f"\n🎣 钓鱼大师: {top_player[0]} - 钓获 {top_player[1]} 条鱼")
    
    def run_demo(self):
        """运行完整的演示"""
        print("🎣 钓鱼游戏完整功能演示")
        print("=" * 60)
        print("本演示将展示:")
        print("1. 多玩家钓鱼会话")
        print("2. 排行榜系统")
        print("3. 鱼类记录系统")
        print("4. 数据统计分析")
        print("5. 数据持久化存储")
        print()
        
        input("按回车键开始演示...")
        
        # 清理之前的数据
        if os.path.exists(self.leaderboard_file):
            os.remove(self.leaderboard_file)
        if os.path.exists(self.records_file):
            os.remove(self.records_file)
        
        self.leaderboard = []
        self.fish_records = []
        
        # 1. 多玩家钓鱼演示
        self.demo_multiple_players()
        
        print("\n" + "="*60)
        input("按回车键查看排行榜...")
        
        # 2. 显示排行榜
        self.show_demo_leaderboard()
        
        print("\n" + "="*60)
        input("按回车键查看鱼类记录...")
        
        # 3. 显示鱼类记录
        self.show_demo_fish_records()
        
        print("\n" + "="*60)
        input("按回车键查看统计分析...")
        
        # 4. 显示统计分析
        self.show_fish_statistics()
        
        print("\n" + "="*60)
        input("按回车键查看鱼类图鉴...")
        
        # 5. 显示鱼类图鉴
        self.show_fish_guide()
        
        print("\n" + "="*60)
        print("📁 数据文件演示")
        print("游戏数据已保存到以下文件:")
        print(f"- {self.leaderboard_file} (排行榜数据)")
        print(f"- {self.records_file} (鱼类记录数据)")
        
        if os.path.exists(self.leaderboard_file):
            print(f"\n排行榜文件大小: {os.path.getsize(self.leaderboard_file)} 字节")
        if os.path.exists(self.records_file):
            print(f"记录文件大小: {os.path.getsize(self.records_file)} 字节")
        
        print("\n✅ 演示完成！")
        print("🎮 图形界面版本在有显示器的环境中可以运行 fishing_game.py")
        print("🖥️  命令行版本可以运行 fishing_game_test.py")
        print("📊 演示版本可以运行 demo_fishing_game.py")

def main():
    """主函数"""
    try:
        demo = FishingGameDemo()
        demo.run_demo()
    except KeyboardInterrupt:
        print("\n\n👋 演示被中断，再见！")
    except Exception as e:
        print(f"\n❌ 演示运行出错: {e}")

if __name__ == "__main__":
    main()