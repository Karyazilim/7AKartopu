import random
from .sprites import Player, Enemy, Snowball


class GameEngine:
    def __init__(self):
        self.player = None
        self.enemies = []
        self.snowballs = []
        self.snow_particles = []
        self.score = 0
        self.time_remaining = 60.0
        self.game_width = 800
        self.game_height = 600
        self.ground_level = 100
        self.character_data = None
        self.player_input = {
            'left': False,
            'right': False,
            'jump': False,
            'throw': False
        }
        self.enemy_spawn_timer = 0
        self.enemy_spawn_interval = 2.0
        
        self.init_snow_particles()
    
    def set_character(self, character_data):
        """Set the selected character data"""
        self.character_data = character_data
        if self.player:
            self.player.set_character_attributes(character_data)
    
    def reset_game(self):
        """Reset game state for a new game"""
        self.score = 0
        self.time_remaining = 60.0
        self.enemies.clear()
        self.snowballs.clear()
        self.enemy_spawn_timer = 0
        
        # Create player
        self.player = Player(
            x=100,
            y=self.ground_level,
            width=40,
            height=60
        )
        
        if self.character_data:
            self.player.set_character_attributes(self.character_data)
    
    def init_snow_particles(self):
        """Initialize background snow particles"""
        self.snow_particles = []
        for _ in range(30):
            self.snow_particles.append({
                'x': random.uniform(0, self.game_width),
                'y': random.uniform(0, self.game_height),
                'speed': random.uniform(20, 60),
                'size': random.uniform(2, 4)
            })
    
    def set_player_input(self, action, active):
        """Set player input state"""
        if action in self.player_input:
            self.player_input[action] = active
    
    def update(self, dt):
        """Main game update loop"""
        # Update timer
        self.time_remaining -= dt
        if self.time_remaining <= 0:
            self.time_remaining = 0
            return  # Game over
        
        # Update snow particles
        self.update_snow_particles(dt)
        
        # Update player
        if self.player:
            self.update_player(dt)
        
        # Update enemies
        self.update_enemies(dt)
        
        # Update snowballs
        self.update_snowballs(dt)
        
        # Spawn enemies
        self.update_enemy_spawning(dt)
        
        # Check collisions
        self.check_collisions()
    
    def update_snow_particles(self, dt):
        """Update background snow animation"""
        for particle in self.snow_particles:
            particle['y'] -= particle['speed'] * dt
            if particle['y'] < 0:
                particle['y'] = self.game_height
                particle['x'] = random.uniform(0, self.game_width)
    
    def update_player(self, dt):
        """Update player physics and input"""
        # Handle horizontal movement
        if self.player_input['left']:
            self.player.move_left(dt)
        if self.player_input['right']:
            self.player.move_right(dt)
        
        # Handle jumping
        if self.player_input['jump'] and self.player.on_ground:
            self.player.jump()
        
        # Handle throwing
        if self.player_input['throw']:
            self.player_input['throw'] = False  # Reset throw input
            snowball = self.player.throw_snowball()
            if snowball:
                self.snowballs.append(snowball)
        
        # Update player physics
        self.player.update(dt)
        
        # Keep player in bounds
        if self.player.x < 20:
            self.player.x = 20
        elif self.player.x > self.game_width - 20:
            self.player.x = self.game_width - 20
        
        # Ground collision
        if self.player.y <= self.ground_level:
            self.player.y = self.ground_level
            self.player.velocity_y = 0
            self.player.on_ground = True
        else:
            self.player.on_ground = False
    
    def update_enemies(self, dt):
        """Update all enemies"""
        enemies_to_remove = []
        
        for enemy in self.enemies:
            enemy.update(dt)
            
            # Remove enemies that have moved off screen
            if enemy.x < -enemy.width:
                enemies_to_remove.append(enemy)
        
        # Remove off-screen enemies
        for enemy in enemies_to_remove:
            self.enemies.remove(enemy)
    
    def update_snowballs(self, dt):
        """Update all snowballs"""
        snowballs_to_remove = []
        
        for snowball in self.snowballs:
            snowball.update(dt)
            
            # Remove snowballs that are off screen or hit ground
            if (snowball.x > self.game_width + 50 or 
                snowball.x < -50 or 
                snowball.y <= self.ground_level):
                snowballs_to_remove.append(snowball)
        
        # Remove off-screen snowballs
        for snowball in snowballs_to_remove:
            self.snowballs.remove(snowball)
    
    def update_enemy_spawning(self, dt):
        """Handle enemy spawning"""
        self.enemy_spawn_timer += dt
        
        if self.enemy_spawn_timer >= self.enemy_spawn_interval:
            self.enemy_spawn_timer = 0
            
            # Spawn new enemy
            enemy = Enemy(
                x=self.game_width + 50,
                y=self.ground_level,
                width=35,
                height=55
            )
            self.enemies.append(enemy)
            
            # Adjust spawn rate based on time
            if self.time_remaining < 30:
                self.enemy_spawn_interval = 1.5
            elif self.time_remaining < 45:
                self.enemy_spawn_interval = 1.8
    
    def check_collisions(self):
        """Check for collisions between game objects"""
        # Check snowball-enemy collisions
        snowballs_to_remove = []
        enemies_to_remove = []
        
        for snowball in self.snowballs:
            for enemy in self.enemies:
                if self.check_aabb_collision(snowball, enemy):
                    # Hit!
                    snowballs_to_remove.append(snowball)
                    enemies_to_remove.append(enemy)
                    self.score += 10
                    break
        
        # Remove hit snowballs and enemies
        for snowball in snowballs_to_remove:
            if snowball in self.snowballs:
                self.snowballs.remove(snowball)
        
        for enemy in enemies_to_remove:
            if enemy in self.enemies:
                self.enemies.remove(enemy)
        
        # Check player-enemy collisions (optional - could reduce score or end game)
        if self.player:
            for enemy in self.enemies:
                if self.check_aabb_collision(self.player, enemy):
                    # Player hit by enemy - could implement damage/game over logic here
                    pass
    
    def check_aabb_collision(self, obj1, obj2):
        """Check axis-aligned bounding box collision between two objects"""
        # Get bounding boxes
        obj1_left = obj1.x - getattr(obj1, 'width', getattr(obj1, 'radius', 10)) / 2
        obj1_right = obj1.x + getattr(obj1, 'width', getattr(obj1, 'radius', 10)) / 2
        obj1_top = obj1.y + getattr(obj1, 'height', getattr(obj1, 'radius', 10))
        obj1_bottom = obj1.y
        
        obj2_left = obj2.x - getattr(obj2, 'width', getattr(obj2, 'radius', 10)) / 2
        obj2_right = obj2.x + getattr(obj2, 'width', getattr(obj2, 'radius', 10)) / 2
        obj2_top = obj2.y + getattr(obj2, 'height', getattr(obj2, 'radius', 10))
        obj2_bottom = obj2.y
        
        # Check collision
        return (obj1_right > obj2_left and 
                obj1_left < obj2_right and 
                obj1_top > obj2_bottom and 
                obj1_bottom < obj2_top)