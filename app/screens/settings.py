from kivy.uix.screen import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import MDList, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.widget import Widget


class SettingsListItem(OneLineAvatarIconListItem):
    def __init__(self, text, switch_active=False, on_switch_change=None, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        
        # Add switch
        switch = MDSwitch(
            active=switch_active,
            pos_hint={'center_y': 0.5},
            size_hint_x=None,
            width='48dp'
        )
        if on_switch_change:
            switch.bind(active=on_switch_change)
        
        self.add_widget(switch)


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Main layout
        main_layout = MDBoxLayout(
            orientation='vertical',
            md_bg_color=(0.96, 0.97, 0.97, 1)
        )
        
        # Top app bar
        toolbar = MDTopAppBar(
            title='Ayarlar',
            md_bg_color=(0.05, 0.65, 0.95, 1),
            specific_text_color=(1, 1, 1, 1),
            left_action_items=[['arrow-left', lambda x: self.go_back()]]
        )
        
        # Settings content
        content_layout = MDBoxLayout(
            orientation='vertical',
            padding='20dp',
            spacing='20dp'
        )
        
        # Settings list
        settings_list = MDList()
        
        # Sound setting
        sound_item = SettingsListItem(
            text='Ses Efektleri',
            switch_active=True,
            on_switch_change=self.on_sound_change
        )
        
        # Music setting
        music_item = SettingsListItem(
            text='Müzik',
            switch_active=True,
            on_switch_change=self.on_music_change
        )
        
        # Dark mode setting
        dark_mode_item = SettingsListItem(
            text='Karanlık Mod',
            switch_active=False,
            on_switch_change=self.on_dark_mode_change
        )
        
        settings_list.add_widget(sound_item)
        settings_list.add_widget(music_item)
        settings_list.add_widget(dark_mode_item)
        
        # Difficulty section
        difficulty_label = MDLabel(
            text='Zorluk Seviyesi',
            theme_text_color='Primary',
            font_style='H6',
            size_hint_y=None,
            height='48dp'
        )
        
        difficulty_layout = MDBoxLayout(
            orientation='horizontal',
            spacing='10dp',
            size_hint_y=None,
            height='48dp'
        )
        
        easy_btn = MDRaisedButton(
            text='Kolay',
            size_hint_x=1,
            md_bg_color=(0.05, 0.65, 0.95, 1),
            text_color=(1, 1, 1, 1)
        )
        easy_btn.bind(on_release=lambda x: self.set_difficulty('easy'))
        
        normal_btn = MDRaisedButton(
            text='Normal',
            size_hint_x=1,
            md_bg_color=(1, 1, 1, 1),
            text_color=(0.05, 0.65, 0.95, 1),
            line_color=(0.05, 0.65, 0.95, 1)
        )
        normal_btn.bind(on_release=lambda x: self.set_difficulty('normal'))
        
        hard_btn = MDRaisedButton(
            text='Zor',
            size_hint_x=1,
            md_bg_color=(1, 1, 1, 1),
            text_color=(0.05, 0.65, 0.95, 1),
            line_color=(0.05, 0.65, 0.95, 1)
        )
        hard_btn.bind(on_release=lambda x: self.set_difficulty('hard'))
        
        difficulty_layout.add_widget(easy_btn)
        difficulty_layout.add_widget(normal_btn)
        difficulty_layout.add_widget(hard_btn)
        
        content_layout.add_widget(settings_list)
        content_layout.add_widget(Widget(size_hint_y=0.2))  # Spacer
        content_layout.add_widget(difficulty_label)
        content_layout.add_widget(difficulty_layout)
        content_layout.add_widget(Widget())  # Spacer
        
        main_layout.add_widget(toolbar)
        main_layout.add_widget(content_layout)
        
        self.add_widget(main_layout)
        
        # Store current settings
        self.settings = {
            'sound': True,
            'music': True,
            'dark_mode': False,
            'difficulty': 'easy'
        }
    
    def on_sound_change(self, instance, value):
        self.settings['sound'] = value
        print(f"Sound effects: {'ON' if value else 'OFF'}")
    
    def on_music_change(self, instance, value):
        self.settings['music'] = value
        print(f"Music: {'ON' if value else 'OFF'}")
    
    def on_dark_mode_change(self, instance, value):
        self.settings['dark_mode'] = value
        if value:
            # Switch to dark theme
            self.parent.md_bg_color = (0.06, 0.11, 0.13, 1)  # #101c22
        else:
            # Switch to light theme
            self.parent.md_bg_color = (0.96, 0.97, 0.97, 1)  # #f5f7f8
        print(f"Dark mode: {'ON' if value else 'OFF'}")
    
    def set_difficulty(self, difficulty):
        self.settings['difficulty'] = difficulty
        print(f"Difficulty set to: {difficulty}")
        
        # Update button colors to show selection
        # This is a simplified version - in a real app you'd properly manage button states
    
    def go_back(self):
        self.manager.current = 'home'