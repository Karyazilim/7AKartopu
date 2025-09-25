from kivy.uix.screen import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDRaisedButton, MDFloatingActionButton
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Canvas, Color, Rectangle, Ellipse, Line
import random
from game.engine import GameEngine


class GameStatsCard(MDCard):
    def __init__(self, title, value="0", **kwargs):
        super().__init__(**kwargs)
        self.elevation = 2
        self.radius = [12]
        self.size_hint = (None, None)
        self.size = ('120dp', '80dp')
        self.md_bg_color = (1, 1, 1, 1)
        self.padding = '12dp'
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing='4dp'
        )
        
        self.title_label = MDLabel(
            text=title,
            theme_text_color='Secondary',
            font_style='Caption',
            halign='center',
            size_hint_y=None,
            height='16dp'
        )
        
        self.value_label = MDLabel(
            text=str(value),
            theme_text_color='Primary',
            font_style='H5',
            halign='center',
            bold=True
        )
        
        layout.add_widget(self.title_label)
        layout.add_widget(self.value_label)
        self.add_widget(layout)
    
    def update_value(self, value):
        self.value_label.text = str(value)


class GameCanvas(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_engine = None
        self.bind(size=self.update_graphics)
        
    def set_game_engine(self, engine):
        self.game_engine = engine
        
    def update_graphics(self, *args):
        if not self.game_engine:
            return
            
        self.canvas.clear()
        with self.canvas:
            # Background color
            Color(0.7, 0.85, 0.95, 1)  # Light blue sky
            Rectangle(pos=self.pos, size=self.size)
            
            # Ground
            Color(0.9, 0.9, 0.9, 1)  # Light gray ground
            Rectangle(pos=(self.x, self.y), size=(self.width, 100))
            
            # Draw snowfall
            Color(1, 1, 1, 0.8)
            for particle in self.game_engine.snow_particles:
                d = particle['size']
                Ellipse(pos=(particle['x'] - d/2, particle['y'] - d/2), size=(d, d))
            
            # Draw player
            if self.game_engine.player:
                player = self.game_engine.player
                Color(0.2, 0.6, 1, 1)  # Blue player
                Rectangle(pos=(player.x - player.width/2, player.y), 
                         size=(player.width, player.height))
            
            # Draw enemies
            Color(1, 0.3, 0.3, 1)  # Red enemies
            for enemy in self.game_engine.enemies:
                Rectangle(pos=(enemy.x - enemy.width/2, enemy.y), 
                         size=(enemy.width, enemy.height))
            
            # Draw snowballs
            Color(1, 1, 1, 1)  # White snowballs
            for snowball in self.game_engine.snowballs:
                d = snowball.radius * 2
                Ellipse(pos=(snowball.x - snowball.radius, snowball.y - snowball.radius), 
                       size=(d, d))


class ControlButton(MDRaisedButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = ('64dp', '64dp')
        self.md_bg_color = (0.05, 0.65, 0.95, 0.8)


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_character = None
        self.game_engine = GameEngine()
        self.game_running = False
        self.setup_ui()
        
        # Bind keyboard events
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)
        
    def setup_ui(self):
        # Main layout
        main_layout = MDBoxLayout(
            orientation='vertical',
            md_bg_color=(0.96, 0.97, 0.97, 1)
        )
        
        # Top app bar
        toolbar = MDTopAppBar(
            title='Oyun',
            md_bg_color=(0.05, 0.65, 0.95, 1),
            specific_text_color=(1, 1, 1, 1),
            left_action_items=[['arrow-left', lambda x: self.go_back()]],
            right_action_items=[['pause', lambda x: self.toggle_pause()]]
        )
        
        # Stats section
        stats_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='100dp',
            spacing='20dp',
            padding='16dp',
            pos_hint={'center_x': 0.5}
        )
        
        self.score_card = GameStatsCard('SKOR', '0')
        self.time_card = GameStatsCard('SÜRE', '60')
        
        stats_layout.add_widget(self.score_card)
        stats_layout.add_widget(Widget())  # Spacer
        stats_layout.add_widget(self.time_card)
        
        # Game canvas
        self.game_canvas = GameCanvas()
        self.game_canvas.set_game_engine(self.game_engine)
        
        # Controls layout
        controls_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='80dp',
            spacing='20dp',
            padding='16dp',
            pos_hint={'center_x': 0.5}
        )
        
        # Movement controls
        self.left_btn = ControlButton(icon='arrow-left')
        self.right_btn = ControlButton(icon='arrow-right')
        self.jump_btn = ControlButton(icon='arrow-up')
        
        # Throw button (larger)
        self.throw_btn = MDRaisedButton(
            text='ATI!',
            size_hint=(None, None),
            size=('120dp', '64dp'),
            md_bg_color=(0.05, 0.65, 0.95, 1),
            text_color=(1, 1, 1, 1),
            font_size='16sp'
        )
        
        # Bind control events
        self.left_btn.bind(on_press=lambda x: self.game_engine.set_player_input('left', True))
        self.left_btn.bind(on_release=lambda x: self.game_engine.set_player_input('left', False))
        self.right_btn.bind(on_press=lambda x: self.game_engine.set_player_input('right', True))
        self.right_btn.bind(on_release=lambda x: self.game_engine.set_player_input('right', False))
        self.jump_btn.bind(on_press=lambda x: self.game_engine.set_player_input('jump', True))
        self.throw_btn.bind(on_press=lambda x: self.game_engine.set_player_input('throw', True))
        
        controls_layout.add_widget(self.left_btn)
        controls_layout.add_widget(self.right_btn)
        controls_layout.add_widget(self.jump_btn)
        controls_layout.add_widget(Widget())  # Spacer
        controls_layout.add_widget(self.throw_btn)
        
        # Floating action button
        fab_layout = MDBoxLayout(
            size_hint_y=None,
            height='80dp',
            pos_hint={'center_x': 0.5}
        )
        
        fab = MDFloatingActionButton(
            icon='plus',
            pos_hint={'center_x': 0.5},
            md_bg_color=(0.05, 0.65, 0.95, 1)
        )
        
        fab_layout.add_widget(fab)
        
        # Add all layouts
        main_layout.add_widget(toolbar)
        main_layout.add_widget(stats_layout)
        main_layout.add_widget(self.game_canvas)
        main_layout.add_widget(controls_layout)
        main_layout.add_widget(fab_layout)
        
        self.add_widget(main_layout)
    
    def set_character(self, character_data):
        self.selected_character = character_data
        if self.game_engine:
            self.game_engine.set_character(character_data)
    
    def on_enter(self):
        """Called when screen becomes active"""
        self.start_game()
    
    def on_leave(self):
        """Called when screen becomes inactive"""
        self.stop_game()
    
    def start_game(self):
        if not self.game_running:
            self.game_running = True
            self.game_engine.reset_game()
            Clock.schedule_interval(self.update_game, 1/60.0)  # 60 FPS
    
    def stop_game(self):
        if self.game_running:
            self.game_running = False
            Clock.unschedule(self.update_game)
    
    def update_game(self, dt):
        if not self.game_running:
            return
            
        # Update game engine
        self.game_engine.update(dt)
        
        # Update UI
        self.score_card.update_value(self.game_engine.score)
        self.time_card.update_value(int(self.game_engine.time_remaining))
        
        # Update canvas
        self.game_canvas.update_graphics()
        
        # Check game over
        if self.game_engine.time_remaining <= 0:
            self.game_over()
    
    def game_over(self):
        self.stop_game()
        # TODO: Show game over dialog
        print(f"Game Over! Final Score: {self.game_engine.score}")
    
    def toggle_pause(self):
        if self.game_running:
            self.stop_game()
        else:
            self.start_game()
    
    def go_back(self):
        self.stop_game()
        self.manager.current = 'character_selection'
    
    def on_key_down(self, window, key, *args):
        # Desktop keyboard controls
        if key == 97 or key == 276:  # A or Left arrow
            self.game_engine.set_player_input('left', True)
        elif key == 100 or key == 275:  # D or Right arrow
            self.game_engine.set_player_input('right', True)
        elif key == 119 or key == 32:  # W or Space
            self.game_engine.set_player_input('jump', True)
        elif key == 102:  # F
            self.game_engine.set_player_input('throw', True)
        return True
    
    def on_key_up(self, window, key, *args):
        if key == 97 or key == 276:  # A or Left arrow
            self.game_engine.set_player_input('left', False)
        elif key == 100 or key == 275:  # D or Right arrow
            self.game_engine.set_player_input('right', False)
        elif key == 119 or key == 32:  # W or Space
            self.game_engine.set_player_input('jump', False)
        return True