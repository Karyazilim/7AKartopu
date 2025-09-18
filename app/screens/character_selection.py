from kivy.uix.screen import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivy.uix.image import Image
from kivy.uix.widget import Widget


class CharacterCard(MDCard):
    def __init__(self, character_data, on_select=None, **kwargs):
        super().__init__(**kwargs)
        self.character_data = character_data
        self.on_select_callback = on_select
        self.selected = False
        
        # Card styling
        self.elevation = 3
        self.radius = [16]
        self.size_hint = (None, None)
        self.size = ('200dp', '280dp')
        self.md_bg_color = (1, 1, 1, 1)
        self.line_color = (0.9, 0.9, 0.9, 1)
        self.line_width = 1
        
        # Card content layout
        layout = MDBoxLayout(
            orientation='vertical',
            padding='16dp',
            spacing='12dp'
        )
        
        # Character image placeholder
        img_container = Widget(size_hint_y=0.6)
        # For now, using a colored rectangle as placeholder
        # In production, you would load actual character images
        
        # Character name
        name_label = MDLabel(
            text=character_data['name'],
            theme_text_color='Primary',
            font_style='H6',
            halign='center',
            size_hint_y=None,
            height='32dp'
        )
        
        # Character description
        desc_label = MDLabel(
            text=character_data['description'],
            theme_text_color='Secondary',
            font_style='Caption',
            halign='center',
            text_size=(None, None),
            size_hint_y=None,
            height='48dp'
        )
        
        layout.add_widget(img_container)
        layout.add_widget(name_label)
        layout.add_widget(desc_label)
        
        self.add_widget(layout)
        self.bind(on_release=self.on_card_press)
    
    def on_card_press(self, *args):
        if self.on_select_callback:
            self.on_select_callback(self)
    
    def set_selected(self, selected):
        self.selected = selected
        if selected:
            self.md_bg_color = (0.85, 0.95, 1, 1)  # Light blue
            self.line_color = (0.05, 0.65, 0.95, 1)  # Primary blue
            self.line_width = 3
        else:
            self.md_bg_color = (1, 1, 1, 1)
            self.line_color = (0.9, 0.9, 0.9, 1)
            self.line_width = 1


class CharacterSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_character = None
        self.character_cards = []
        
        # Character data
        self.characters = [
            {
                'name': 'Arda',
                'description': 'Hızlı hareket\nkabiliyeti',
                'speed': 1.5,
                'throw_cooldown': 1.0,
                'jump_power': 1.0,
                'snowball_power': 1.0
            },
            {
                'name': 'Elif',
                'description': 'Hızlı atış\nkabiliyeti',
                'speed': 1.0,
                'throw_cooldown': 0.6,
                'jump_power': 1.0,
                'snowball_power': 1.0
            },
            {
                'name': 'Can',
                'description': 'Güçlü kar topu\natışları',
                'speed': 1.0,
                'throw_cooldown': 1.0,
                'jump_power': 1.0,
                'snowball_power': 1.5
            },
            {
                'name': 'Ayşe',
                'description': 'Yüksek zıplama\nkabiliyeti',
                'speed': 1.0,
                'throw_cooldown': 1.0,
                'jump_power': 1.4,
                'snowball_power': 1.0
            }
        ]
        
        # Main layout
        main_layout = MDBoxLayout(
            orientation='vertical',
            md_bg_color=(0.96, 0.97, 0.97, 1)
        )
        
        # Top app bar
        toolbar = MDTopAppBar(
            title='Karakter Seçimi',
            md_bg_color=(0.05, 0.65, 0.95, 1),
            specific_text_color=(1, 1, 1, 1),
            left_action_items=[['arrow-left', lambda x: self.go_back()]]
        )
        
        # Character selection area
        content_layout = MDBoxLayout(
            orientation='vertical',
            padding='20dp',
            spacing='20dp'
        )
        
        # Characters scroll view
        scroll = ScrollView(
            size_hint_y=0.7
        )
        
        characters_layout = MDBoxLayout(
            orientation='horizontal',
            spacing='16dp',
            adaptive_width=True,
            padding='10dp'
        )
        
        # Create character cards
        for char_data in self.characters:
            card = CharacterCard(
                character_data=char_data,
                on_select=self.on_character_select
            )
            self.character_cards.append(card)
            characters_layout.add_widget(card)
        
        scroll.add_widget(characters_layout)
        content_layout.add_widget(scroll)
        
        # Bottom navigation
        bottom_nav = MDBottomNavigation(
            panel_color=(1, 1, 1, 1),
            selected_color_background=(0.05, 0.65, 0.95, 1),
            text_color_active=(0.05, 0.65, 0.95, 1)
        )
        
        # Characters tab (active)
        char_item = MDBottomNavigationItem(
            name='characters',
            text='Karakterler',
            icon='account-group'
        )
        
        # Game tab
        game_item = MDBottomNavigationItem(
            name='game',
            text='Oyun',
            icon='gamepad-variant'
        )
        game_item.bind(on_tab_press=self.start_game)
        
        # Settings tab
        settings_item = MDBottomNavigationItem(
            name='settings',
            text='Ayarlar',
            icon='cog'
        )
        settings_item.bind(on_tab_press=self.go_to_settings)
        
        bottom_nav.add_widget(char_item)
        bottom_nav.add_widget(game_item)
        bottom_nav.add_widget(settings_item)
        
        main_layout.add_widget(toolbar)
        main_layout.add_widget(content_layout)
        main_layout.add_widget(bottom_nav)
        
        self.add_widget(main_layout)
        
        # Select first character by default
        if self.character_cards:
            self.on_character_select(self.character_cards[0])
    
    def on_character_select(self, card):
        # Deselect all cards
        for c in self.character_cards:
            c.set_selected(False)
        
        # Select the clicked card
        card.set_selected(True)
        self.selected_character = card.character_data
        
        # Store selection globally (you might want to use a proper state manager)
        if hasattr(self.manager.get_screen('game'), 'set_character'):
            self.manager.get_screen('game').set_character(self.selected_character)
    
    def start_game(self, instance):
        if self.selected_character:
            self.manager.current = 'game'
    
    def go_to_settings(self, instance):
        self.manager.current = 'settings'
    
    def go_back(self):
        self.manager.current = 'home'