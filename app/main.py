from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior

from screens.home import HomeScreen
from screens.character_selection import CharacterSelectionScreen
from screens.game import GameScreen
from screens.settings import SettingsScreen


class KarTopuApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Kar Topu Savaşı"
        
    def build(self):
        # Set app theme
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "400"
        self.theme_cls.accent_palette = "LightBlue"
        self.theme_cls.theme_style = "Light"
        
        # Create screen manager
        sm = ScreenManager()
        
        # Add screens
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(CharacterSelectionScreen(name='character_selection'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(SettingsScreen(name='settings'))
        
        return sm


if __name__ == '__main__':
    KarTopuApp().run()