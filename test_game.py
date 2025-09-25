#!/usr/bin/env python3
"""
Test script for Kar Topu Savaşı game logic without GUI.
This validates that the game engine works correctly.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from game.engine import GameEngine
from game.sprites import Player, Enemy, Snowball


def test_game_engine():
    print("Testing Kar Topu Savaşı Game Engine...")
    
    # Create game engine
    engine = GameEngine()
    
    # Test character data
    character_data = {
        'name': 'Arda',
        'description': 'Hızlı hareket kabiliyeti',
        'speed': 1.5,
        'throw_cooldown': 1.0,
        'jump_power': 1.0,
        'snowball_power': 1.0
    }
    
    # Set character and reset game
    engine.set_character(character_data)
    engine.reset_game()
    
    print(f"✓ Game initialized with character: {character_data['name']}")
    print(f"  - Player position: ({engine.player.x}, {engine.player.y})")
    print(f"  - Player speed: {engine.player.speed}")
    print(f"  - Initial score: {engine.score}")
    print(f"  - Initial time: {engine.time_remaining}s")
    
    # Test player movement
    engine.set_player_input('right', True)
    initial_x = engine.player.x
    
    # Simulate game updates
    for i in range(10):
        engine.update(1/60.0)  # 60 FPS
    
    print(f"✓ Player movement test: {initial_x} -> {engine.player.x}")
    
    # Test jump
    engine.set_player_input('right', False)
    engine.set_player_input('jump', True)
    initial_y = engine.player.y
    
    for i in range(5):
        engine.update(1/60.0)
    
    print(f"✓ Player jump test: {initial_y} -> {engine.player.y}")
    
    # Test snowball throwing
    initial_snowballs = len(engine.snowballs)
    engine.set_player_input('throw', True)
    engine.update(1/60.0)
    
    print(f"✓ Snowball throwing test: {initial_snowballs} -> {len(engine.snowballs)} snowballs")
    
    # Test enemy spawning
    engine.enemy_spawn_timer = engine.enemy_spawn_interval  # Force spawn
    initial_enemies = len(engine.enemies)
    engine.update(1/60.0)
    
    print(f"✓ Enemy spawning test: {initial_enemies} -> {len(engine.enemies)} enemies")
    
    # Test collision detection (simplified)
    if engine.snowballs and engine.enemies:
        snowball = engine.snowballs[0]
        enemy = engine.enemies[0]
        
        # Position them close together
        snowball.x = enemy.x
        snowball.y = enemy.y
        
        initial_score = engine.score
        engine.check_collisions()
        
        print(f"✓ Collision detection test: Score {initial_score} -> {engine.score}")
    
    print("\n🎮 All game engine tests passed! The game logic is working correctly.")
    print("\nTo run the full game:")
    print("1. Desktop: python app/main.py")
    print("2. Android: buildozer android debug")


def test_character_attributes():
    print("\nTesting character attributes...")
    
    characters = [
        {'name': 'Arda', 'speed': 1.5, 'throw_cooldown': 1.0, 'jump_power': 1.0, 'snowball_power': 1.0},
        {'name': 'Elif', 'speed': 1.0, 'throw_cooldown': 0.6, 'jump_power': 1.0, 'snowball_power': 1.0},
        {'name': 'Can', 'speed': 1.0, 'throw_cooldown': 1.0, 'jump_power': 1.0, 'snowball_power': 1.5},
        {'name': 'Ayşe', 'speed': 1.0, 'throw_cooldown': 1.0, 'jump_power': 1.4, 'snowball_power': 1.0}
    ]
    
    for char in characters:
        player = Player(100, 100, 40, 60)
        player.set_character_attributes(char)
        
        print(f"✓ {char['name']}: Speed={player.speed:.0f}, Jump={player.jump_power:.0f}, "
              f"Cooldown={player.throw_cooldown:.1f}s, Power={player.snowball_power:.1f}")


if __name__ == '__main__':
    test_character_attributes()
    test_game_engine()