import time


class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = True
        
        # Character attributes (defaults)
        self.speed = 200  # pixels per second
        self.jump_power = 400
        self.throw_cooldown = 1.0  # seconds
        self.snowball_power = 1.0
        
        # State
        self.last_throw_time = 0
        self.gravity = 800  # pixels per second squared
    
    def set_character_attributes(self, character_data):
        """Apply character-specific attributes"""
        base_speed = 200
        base_jump = 400
        base_cooldown = 1.0
        base_power = 1.0
        
        self.speed = base_speed * character_data.get('speed', 1.0)
        self.jump_power = base_jump * character_data.get('jump_power', 1.0)
        self.throw_cooldown = base_cooldown * character_data.get('throw_cooldown', 1.0)
        self.snowball_power = base_power * character_data.get('snowball_power', 1.0)
    
    def move_left(self, dt):
        """Move player left"""
        self.velocity_x = -self.speed
    
    def move_right(self, dt):
        """Move player right"""
        self.velocity_x = self.speed
    
    def jump(self):
        """Make player jump"""
        if self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False
    
    def throw_snowball(self):
        """Throw a snowball if cooldown allows"""
        current_time = time.time()
        if current_time - self.last_throw_time >= self.throw_cooldown:
            self.last_throw_time = current_time
            
            # Create snowball
            snowball = Snowball(
                x=self.x + self.width/2,
                y=self.y + self.height/2,
                velocity_x=300 * self.snowball_power,
                velocity_y=50
            )
            return snowball
        return None
    
    def update(self, dt):
        """Update player physics"""
        # Apply gravity
        self.velocity_y -= self.gravity * dt
        
        # Update position
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        
        # Apply friction to horizontal movement
        self.velocity_x *= 0.8


class Enemy:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity_x = -80  # Move left
        self.velocity_y = 0
        self.on_ground = True
        self.gravity = 800
    
    def update(self, dt):
        """Update enemy physics"""
        # Apply gravity
        self.velocity_y -= self.gravity * dt
        
        # Update position
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        
        # Ground collision (simplified)
        if self.y <= 100:  # Ground level
            self.y = 100
            self.velocity_y = 0
            self.on_ground = True


class Snowball:
    def __init__(self, x, y, velocity_x, velocity_y, radius=8):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.radius = radius
        self.gravity = 400  # Less gravity for snowballs
    
    def update(self, dt):
        """Update snowball physics"""
        # Apply gravity
        self.velocity_y -= self.gravity * dt
        
        # Update position
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt