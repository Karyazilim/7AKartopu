#!/usr/bin/env python3
"""
Headless demo of Kar Topu Savaşı game.
Shows the game state without opening a window.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Simulate the game for a few seconds and show what's happening
from game.engine import GameEngine
import time

def run_headless_demo():
    print("🎮 Kar Topu Savaşı - Headless Demo")
    print("=" * 50)
    
    # Initialize game
    engine = GameEngine()
    
    # Set up Arda character
    arda_data = {
        'name': 'Arda',
        'speed': 1.5,
        'throw_cooldown': 1.0,
        'jump_power': 1.0,
        'snowball_power': 1.0
    }
    
    engine.set_character(arda_data)
    engine.reset_game()
    
    print(f"🎯 Game started with {arda_data['name']}")
    print(f"📍 Player at position ({engine.player.x:.0f}, {engine.player.y:.0f})")
    
    # Simulate 10 seconds of gameplay
    frame_time = 1/60.0  # 60 FPS
    total_time = 0
    
    # Set some inputs
    engine.set_player_input('right', True)
    
    while total_time < 10.0 and engine.time_remaining > 0:
        # Occasionally throw snowballs
        if int(total_time * 2) % 3 == 0:
            engine.set_player_input('throw', True)
        
        # Update game
        engine.update(frame_time)
        total_time += frame_time
        
        # Print status every second
        if int(total_time) != int(total_time - frame_time):
            print(f"⏱️  Time: {int(total_time)}s | "
                  f"Score: {engine.score} | "
                  f"Player: ({engine.player.x:.0f}, {engine.player.y:.0f}) | "
                  f"Enemies: {len(engine.enemies)} | "
                  f"Snowballs: {len(engine.snowballs)}")
    
    print("\n✅ Demo completed!")
    print(f"📊 Final Statistics:")
    print(f"   • Final Score: {engine.score}")
    print(f"   • Enemies Spawned: Total enemies that appeared")
    print(f"   • Snowballs Thrown: Total snowballs created")
    print(f"   • Game Time: {60 - engine.time_remaining:.1f} seconds")
    
    print(f"\n🎮 The full game features:")
    print(f"   • Beautiful UI with KivyMD components")
    print(f"   • Touch controls for mobile devices") 
    print(f"   • 4 unique characters with different abilities")
    print(f"   • Animated snowfall background")
    print(f"   • Sound effects and music (when implemented)")
    print(f"   • Settings for difficulty and preferences")
    
    print(f"\n🚀 To run the complete game:")
    print(f"   Desktop: python app/main.py")
    print(f"   Android: buildozer android debug")

if __name__ == '__main__':
    run_headless_demo()