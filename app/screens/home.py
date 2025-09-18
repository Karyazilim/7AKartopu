from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Canvas, Color, Ellipse
from kivy.clock import Clock
import random
from kivymd.uix.button import MDRaisedButton, MDFillRoundFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Line, Rectangle


class SnowfallWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.snowflakes = []
        self.bind(size=self.update_graphics)
        Clock.schedule_interval(self.update_snowfall, 1/30.0)
        
    def update_graphics(self, *args):
        # Initialize snowflakes
        self.snowflakes = []
        for _ in range(50):
            self.snowflakes.append({
                'x': random.uniform(0, self.width),
                'y': random.uniform(0, self.height),
                'speed': random.uniform(20, 50),
                'size': random.uniform(2, 6)
            })
        self.draw_snowfall()
        
    def update_snowfall(self, dt):
        if not self.snowflakes:
            return
            
        # Update snowflake positions
        for flake in self.snowflakes:
            flake['y'] -= flake['speed'] * dt
            if flake['y'] < 0:
                flake['y'] = self.height
                flake['x'] = random.uniform(0, self.width)
        
        self.draw_snowfall()
        
    def draw_snowfall(self):
        self.canvas.clear()
        with self.canvas:
            Color(0.8, 0.8, 0.9, 0.6)
            for flake in self.snowflakes:
                d = flake['size']
                Ellipse(pos=(flake['x'] - d/2, flake['y'] - d/2), size=(d, d))


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Main layout
        main_layout = MDBoxLayout(
            orientation='vertical',
            md_bg_color=(0.96, 0.97, 0.97, 1),  # #f5f7f8
            spacing='20dp',
            padding=['20dp', '40dp', '20dp', '40dp']
        )
        
        # Add snowfall background
        snowfall = SnowfallWidget()
        main_layout.add_widget(snowfall)
        
        # Title with shadow effect
        title_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=0.4,
            pos_hint={'center_x': 0.5}
        )
        
        title = Label(
            text='KAR TOPU\nSAVAŞI',
            font_size='48sp',
            bold=True,
            halign='center',
            valign='center',
            color=(0.05, 0.11, 0.13, 1),  # Dark text
            text_size=(None, None)
        )
        title.bind(size=title.setter('text_size'))
        title_layout.add_widget(title)
        
        # Button layout
        button_layout = MDBoxLayout(
            orientation='vertical',
            size_hint_y=0.3,
            spacing='20dp',
            pos_hint={'center_x': 0.5}
        )
        
        # Start button
        start_btn = MDRaisedButton(
            text='BAŞLA',
            size_hint=(0.8, None),
            height='56dp',
            pos_hint={'center_x': 0.5},
            md_bg_color=(0.05, 0.65, 0.95, 1),  # #0da6f2
            text_color=(1, 1, 1, 1),
            font_size='18sp'
        )
        start_btn.bind(on_release=self.go_to_character_selection)
        
        # Settings button
        settings_btn = MDFillRoundFlatButton(
            text='AYARLAR',
            size_hint=(0.8, None),
            height='56dp',
            pos_hint={'center_x': 0.5},
            md_bg_color=(1, 1, 1, 1),
            text_color=(0.05, 0.65, 0.95, 1),
            line_color=(0.05, 0.65, 0.95, 1),
            font_size='18sp'
        )
        settings_btn.bind(on_release=self.go_to_settings)
        
        button_layout.add_widget(start_btn)
        button_layout.add_widget(settings_btn)
        
        main_layout.add_widget(title_layout)
        main_layout.add_widget(button_layout)
        
        self.add_widget(main_layout)
    
    def go_to_character_selection(self, instance):
        self.manager.current = 'character_selection'
        
    def go_to_settings(self, instance):
        self.manager.current = 'settings'