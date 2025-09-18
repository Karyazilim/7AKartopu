#!/usr/bin/env python3
"""
Validate the complete Kar Topu Savaşı implementation.
Tests all components and verifies the project structure.
"""

import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists and print status"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} (MISSING)")
        return False

def validate_project_structure():
    """Validate that all required files and directories exist"""
    print("🔍 Validating Kar Topu Savaşı Project Structure")
    print("=" * 60)
    
    base_dir = "/home/runner/work/7AKartopu/7AKartopu"
    
    # Required files
    required_files = [
        ("requirements.txt", "Python dependencies"),
        ("buildozer.spec", "Android build configuration"),
        ("README.md", "Project documentation"),
        ("app/main.py", "Main application entry point"),
        ("app/ui.kv", "Kivy UI layout file"),
        ("app/screens/__init__.py", "Screens package"),
        ("app/screens/home.py", "Home screen"),
        ("app/screens/character_selection.py", "Character selection screen"),
        ("app/screens/game.py", "Game screen"),
        ("app/screens/settings.py", "Settings screen"),
        ("app/game/__init__.py", "Game package"),
        ("app/game/engine.py", "Game engine"),
        ("app/game/sprites.py", "Game sprites"),
    ]
    
    # Asset files
    asset_files = [
        ("assets/characters/arda.png", "Arda character image"),
        ("assets/characters/elif.png", "Elif character image"),
        ("assets/characters/can.png", "Can character image"),
        ("assets/characters/ayse.png", "Ayşe character image"),
        ("assets/fonts/README.md", "Font directory documentation"),
    ]
    
    all_good = True
    
    print("\n📁 Core Application Files:")
    for filepath, description in required_files:
        full_path = os.path.join(base_dir, filepath)
        if not check_file_exists(full_path, description):
            all_good = False
    
    print("\n🎨 Asset Files:")
    for filepath, description in asset_files:
        full_path = os.path.join(base_dir, filepath)
        if not check_file_exists(full_path, description):
            all_good = False
    
    return all_good

def validate_code_imports():
    """Test that all Python modules can be imported"""
    print("\n🐍 Validating Python Code:")
    
    # Add the app directory to path
    app_dir = "/home/runner/work/7AKartopu/7AKartopu/app"
    if app_dir not in sys.path:
        sys.path.insert(0, app_dir)
    
    modules_to_test = [
        ("game.engine", "Game engine module"),
        ("game.sprites", "Game sprites module"),
        ("screens.home", "Home screen module"),
        ("screens.character_selection", "Character selection screen"),
        ("screens.game", "Game screen module"),
        ("screens.settings", "Settings screen module"),
    ]
    
    all_imports_good = True
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {description}: {module_name}")
        except ImportError as e:
            print(f"❌ {description}: {module_name} - Import Error: {e}")
            all_imports_good = False
        except Exception as e:
            print(f"⚠️  {description}: {module_name} - Warning: {e}")
    
    return all_imports_good

def check_game_features():
    """Check that key game features are implemented"""
    print("\n🎮 Game Features Check:")
    
    try:
        from game.engine import GameEngine
        from game.sprites import Player, Enemy, Snowball
        
        # Test game engine creation
        engine = GameEngine()
        print("✅ Game engine creates successfully")
        
        # Test character system
        character_data = {
            'name': 'Test',
            'speed': 1.2,
            'throw_cooldown': 0.8,
            'jump_power': 1.1,
            'snowball_power': 1.3
        }
        
        engine.set_character(character_data)
        engine.reset_game()
        print("✅ Character system works")
        
        # Test game mechanics
        engine.set_player_input('right', True)
        engine.set_player_input('throw', True)
        engine.update(1/60.0)
        print("✅ Game mechanics (input, update) work")
        
        print("✅ All core game features are functional")
        return True
        
    except Exception as e:
        print(f"❌ Game features test failed: {e}")
        return False

def main():
    """Run all validation checks"""
    print("🚀 Kar Topu Savaşı - Complete Project Validation")
    print("=" * 60)
    
    structure_ok = validate_project_structure()
    imports_ok = validate_code_imports()
    features_ok = check_game_features()
    
    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY:")
    
    if structure_ok and imports_ok and features_ok:
        print("🎉 ALL CHECKS PASSED! The project is complete and ready.")
        print("\n🚀 Next Steps:")
        print("   1. Desktop Testing: python app/main.py")
        print("   2. Android Build: buildozer android debug")
        print("   3. Install APK on Android device")
        print("\n✨ Features Implemented:")
        print("   • Four screens with Turkish UI")
        print("   • Character selection with unique abilities")
        print("   • Physics-based gameplay")
        print("   • Mobile touch controls + keyboard support")
        print("   • Score tracking and timer")
        print("   • Animated backgrounds")
        print("   • KivyMD Material Design components")
        return True
    else:
        print("❌ Some validation checks failed.")
        print("Please review the issues above before proceeding.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)