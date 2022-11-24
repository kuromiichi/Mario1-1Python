import pyxel
from sprites import *


class Mario(Sprite):
    def __init__(
            self, x: int, y: int, image=0, u=0, v=0, w=13, h=16, orientation=1, jump=False,
            base_speed=3, momentum_x=0, momentum_y=0, powerup=0, star=False, spr_frame=0,
            frame_counter=0, hitbox_size=None, hitpoints=None, y_limit=192, no_movement=False,
            dead=False, invulnerable=0, score=0, star_time=0, coins=0):
        super().__init__(x, y, image, u, v, w, h, orientation, hitpoints)
        self.jump = jump
        self.base_speed = base_speed
        self.momentum_x = momentum_x
        self.momentum_y = momentum_y
        self.powerup = powerup
        self.star = star
        self.spr_frame = spr_frame
        self.frame_counter = frame_counter
        self.y_limit = y_limit
        self.no_movement = no_movement
        self.dead = dead
        self.invulnerable = invulnerable
        self.score = score
        self.star_time = star_time
        self.coins = coins
        if hitbox_size is None:
            self.hitbox_size = [14, 16]
        else:
            self.hitbox_size = hitbox_size

    def standing(self, other):
        # x check
        if self.hitpoints[0] < other.hitpoints[2] and self.hitpoints[2] > other.hitpoints[0]:
            # y check
            if other.hitpoints[1] + 8 >= self.hitpoints[3] >= other.hitpoints[1] and self.momentum_y >= 0:
                return True

    def block_collision_check(self, other: Block):
        if not self.dead:
            if self is not other:
                # Ground collision
                if self.standing(other):
                    if not other.hidden:
                        self.y_limit = other.hitpoints[1]
                        self.no_movement = False
                        if not self.jump:
                            self.y = other.hitpoints[1] - self.hitbox_size[1]
                # Hit from below
                # x check
                elif self.hitpoints[0] < other.hitpoints[2] and self.hitpoints[2] > other.hitpoints[0]:
                    # y check
                    if other.hitpoints[3] >= self.hitpoints[1] > other.hitpoints[3] - 4 and self.momentum_y < 0:
                        self.y = other.hitpoints[3]
                        self.momentum_y = 0
                        if isinstance(other, BreakableBrick):
                            if self.powerup >= 1:
                                other.brick_break()
                        elif isinstance(other, ItemBlock) or isinstance(other, ItemBrick):
                            if not other.is_hit:
                                other.hit()
                                if other.item == 0:
                                    self.coins += 1
                                    self.score += 200
                # Wall collision
                # y check
                if not self.standing(other):
                    if not other.hidden:
                        if self.hitpoints[1] < other.hitpoints[3] and self.hitpoints[3] > other.hitpoints[1]:
                            # From left
                            if self.hitpoints[2] >= other.hitpoints[0] > self.hitpoints[2] - 4:
                                self.x -= self.hitpoints[2] - other.hitpoints[0]
                                self.momentum_x = 0
                            # From right
                            if self.hitpoints[0] <= other.hitpoints[2] < self.hitpoints[0] + 4:
                                self.x += other.hitpoints[2] - self.hitpoints[0]
                                self.momentum_x = 0
                if isinstance(other, ItemBlock) or isinstance(other, ItemBrick):
                    if other.is_hit and not other.item_obj.spawned:
                        other.item_obj.spawned = True
                        return other.item_obj

    def enemy_collision_check(self, other: Enemy):
        if not self.dead and self is not other:
            on_enemy = self.standing(other)
            # Jump on enemy
            if on_enemy:
                self.no_movement = True
                if isinstance(other, Goomba):
                    if not other.stomped:
                        # Stomp
                        self.momentum_y = -3.5
                        other.stomped = True
                        self.score += 100
                elif isinstance(other, Koopa):
                    if not other.stomped:
                        self.momentum_y = -3.5
                        other.stomped = True
                        self.score += 100
                    else:
                        self.momentum_y = -3.5
                        if other.hit:
                            other.hit = False
                        else:
                            if self.hitpoints[0] <= other.hitpoints[0] + 8:
                                other.orientation = 1
                            else:
                                other.orientation = -1
                            other.hit = True

            # Bottom collision
            elif self.hitpoints[0] < other.hitpoints[2] and self.hitpoints[2] > other.hitpoints[0]:
                if other.hitpoints[3] >= self.hitpoints[1] > other.hitpoints[3] - 4:
                    if self.star:
                        other.dead = True
                    else:
                        if not other.stomped:
                            if self.invulnerable <= 0:
                                if self.powerup > 0:
                                    self.powerup -= 1
                                    self.invulnerable = 60
                                else:
                                    self.die()

            # Side collision
            if not on_enemy:
                if self.hitpoints[1] < other.hitpoints[3] and self.hitpoints[3] > other.hitpoints[1]:
                    if self.hitpoints[0] < other.hitpoints[2] and self.hitpoints[2] > other.hitpoints[0]:
                        if self.star:
                            other.dead = True
                        else:
                            if isinstance(other, Koopa) and other.stomped and not other.hit:
                                # From left
                                if self.hitpoints[2] >= other.hitpoints[0] > self.hitpoints[2] - 4:
                                    other.orientation = 1
                                # From right
                                if self.hitpoints[0] <= other.hitpoints[2] < self.hitpoints[0] + 4:
                                    other.orientation = -1
                                other.hit = True
                            else:
                                if not other.stomped or (isinstance(other, Koopa) and other.hit):
                                    if self.invulnerable <= 0:
                                        if self.powerup > 0:
                                            self.powerup -= 1
                                            self.invulnerable = 60
                                        else:
                                            self.die()

    def item_collision_check(self, other: Item):
        if not other.picked:
            # Ground collision
            if self.standing(other):
                if isinstance():
                    self.powerup += 1
                    other.pick_up()

            # Hit from below
            # x check
            elif self.hitpoints[0] < other.hitpoints[2] and self.hitpoints[2] > other.hitpoints[0]:
                # y check
                if other.hitpoints[3] >= self.hitpoints[1] > other.hitpoints[3] - 4 and self.momentum_y < 0:
                    if other.item <= 1:
                        self.powerup += 1
                        other.pick_up()
            # Wall collision
            # y check
            if not self.standing(other):
                if self.hitpoints[1] < other.hitpoints[3] and self.hitpoints[3] > other.hitpoints[1]:
                    if self.hitpoints[0] < other.hitpoints[2] and self.hitpoints[2] > other.hitpoints[0]:
                        if isinstance(other, Mushroom):
                            self.powerup = 1
                            self.score += 1000
                            other.pick_up()

    def collision_check(self, other):
        if isinstance(other, Block):
            return self.block_collision_check(other)
        elif isinstance(other, Enemy):
            self.enemy_collision_check(other)
        elif isinstance(other, Item):
            self.item_collision_check(other)

    def player_movement(self, gravity):
        self.player_movement_x()
        self.player_movement_y(gravity)

    # Left/Right movement
    def player_movement_x(self):
        speed_limit = self.base_speed
        speed_increment = 0.2
        # Aerial movement reduction
        if self.hitpoints[3] < self.y_limit:
            speed_increment *= 0.45

        # Walking/Running
        if not pyxel.btn(pyxel.KEY_Z):
            speed_limit = self.base_speed * 3 / 5
            speed_increment *= 3 / 5

        # Right
        if not self.no_movement:
            if not pyxel.btn(pyxel.KEY_DOWN) or self.powerup == 0:
                if pyxel.btn(pyxel.KEY_RIGHT):
                    # Drift
                    if self.momentum_x < 0:
                        speed_increment *= 2
                    # Movement
                    if not self.jump:
                        self.orientation = 1
                    if self.momentum_x < speed_limit:
                        self.momentum_x += speed_increment
                    else:
                        self.momentum_x = speed_limit

                # Left
                elif pyxel.btn(pyxel.KEY_LEFT):
                    # Drift
                    if self.momentum_x > 0:
                        speed_increment *= 2
                    # Movement
                    if not self.jump:
                        self.orientation = -1
                    if self.momentum_x > -speed_limit:
                        self.momentum_x -= speed_increment
                    else:
                        self.momentum_x = -speed_limit
                else:
                    if -speed_increment < self.momentum_x < speed_increment:
                        self.momentum_x = 0
                    elif self.momentum_x > 0:
                        self.momentum_x -= speed_increment
                    elif self.momentum_x < 0:
                        self.momentum_x += speed_increment

            # Deceleration
            else:
                if -speed_increment < self.momentum_x < speed_increment:
                    self.momentum_x = 0
                elif self.momentum_x > 0:
                    self.momentum_x -= speed_increment
                elif self.momentum_x < 0:
                    self.momentum_x += speed_increment

        # Out-of-bounds check
        if self.x <= 0:
            self.x = 0
            if self.momentum_x < 0:
                self.momentum_x = 0
        # Return
        self.x += self.momentum_x

    # Air movement method
    def player_movement_y(self, gravity):
        if self.hitpoints[3] < self.y_limit:
            if pyxel.btn(pyxel.KEY_X) and self.momentum_y < 0 and not self.dead:
                gravity *= 0.36
            self.momentum_y += gravity
            if self.momentum_y > 7:
                self.momentum_y = 7
        else:
            self.y = self.y_limit - self.hitbox_size[1]
            self.momentum_y = 0
            self.jump = False
        if not self.dead:
            if self.hitpoints[3] == self.y_limit and pyxel.btnp(pyxel.KEY_X):
                if abs(self.momentum_x) >= 2.5:
                    self.momentum_y -= 7 / 3 + 6 * gravity
                else:
                    self.momentum_y -= 2 + 6 * gravity
                self.jump = True
                self.frame_counter = 1
            if self.y >= 256:
                self.dead = True
        self.y += self.momentum_y

    # Mario animations
    def sprite_selection(self):
        if not self.dead:
            if self.invulnerable > 0 and self.spr_frame // 5 % 2 == 1:
                self.h = 0
            else:
                if self.powerup == 0:
                    self.h = 16
                    self.v = 0
                    self.hitbox_size = [14, 16]
                    # Jump animation
                    if self.jump:
                        self.u = 80
                        self.w = 16 * self.orientation
                    else:
                        # Stand animation
                        if self.momentum_x == 0:
                            self.u = 0
                            self.w = 13 * self.orientation
                        else:
                            # Run/Walk animation
                            if self.momentum_x * self.orientation > 0:
                                if pyxel.btn(pyxel.KEY_Z):
                                    if self.spr_frame // 6 % 3 == 0:
                                        self.u = 16
                                        self.w = 14 * self.orientation
                                    elif self.spr_frame // 6 % 3 == 1:
                                        self.u = 32
                                        self.w = 12 * self.orientation
                                    elif self.spr_frame // 6 % 3 == 2:
                                        self.u = 48
                                        self.w = 16 * self.orientation
                                else:
                                    if self.spr_frame // 10 % 3 == 0:
                                        self.u = 16
                                        self.w = 14 * self.orientation
                                    elif self.spr_frame // 10 % 3 == 1:
                                        self.u = 32
                                        self.w = 12 * self.orientation
                                    elif self.spr_frame // 10 % 3 == 2:
                                        self.u = 48
                                        self.w = 16 * self.orientation
                            # Drift animation
                            else:
                                self.u = 64
                                self.w = 14 * self.orientation
                if self.powerup == 1:
                    self.h = 32
                    self.v = 16
                    self.hitbox_size = [14, 32]
                    # Jump animation
                    if self.jump:
                        self.u = 64
                        self.w = 16 * self.orientation
                    elif pyxel.btn(pyxel.KEY_DOWN):
                        self.u = 80
                        self.h = 22
                        self.w = 16 * self.orientation
                        self.hitbox_size = [16, 22]
                    else:
                        # Stand animation
                        if self.momentum_x == 0:
                            self.u = 0
                            self.w = 16 * self.orientation
                        else:
                            # Run/Walk animation
                            if self.momentum_x * self.orientation > 0:
                                if pyxel.btn(pyxel.KEY_Z):
                                    if self.spr_frame // 6 % 3 == 0:
                                        self.u = 16
                                        self.w = 16 * self.orientation
                                    elif self.spr_frame // 6 % 3 == 1:
                                        self.u = 32
                                        self.w = 14 * self.orientation
                                    elif self.spr_frame // 6 % 3 == 2:
                                        self.u = 48
                                        self.w = 16 * self.orientation
                                else:
                                    if self.spr_frame // 10 % 3 == 0:
                                        self.u = 16
                                        self.w = 16 * self.orientation
                                    elif self.spr_frame // 10 % 3 == 1:
                                        self.u = 32
                                        self.w = 14 * self.orientation
                                    elif self.spr_frame // 10 % 3 == 2:
                                        self.u = 48
                                        self.w = 16 * self.orientation
                            # Drift animation
                            else:
                                self.u = 208
                                self.w = -16 * self.orientation

    # Screen scroll
    def scroll(self, offset):
        if self.x > 120:
            offset = self.x - 120
            self.x = 120
        else:
            return 0
        return offset

    # Mario Invulnerability
    def invulnerability(self):
        self.invulnerable -= 1

    # Mario death
    def die(self):
        self.no_movement = True
        self.dead = True
        self.momentum_x = 0
        self.momentum_y = -5
        self.u = 104
        self.v = 0
        self.w = 14
        self.h = 14
        self.y_limit = 300

    # Star timer
    def star_timer(self):
        if self.star and self.star_time < 600:
            self.star_time += 1
        if self.star and self.star_time >= 600:
            self.star = False
            self.star_time = 0
