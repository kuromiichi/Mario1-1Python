# Default class for all sprites in the game
import pyxel


class Sprite:
    def __init__(self, x: int, y: int, image: int, u: int, v: int, w: int, h: int,
                 orientation=1, spr_frame=0, hitbox_size=None, hitpoints=None):
        self.x = x
        self.y = y
        self.image = image
        self.u = u
        self.v = v
        self.w = w
        self.h = h
        self.orientation = orientation
        self.spr_frame = spr_frame
        if hitbox_size is None:
            self.hitbox_size = []
        else:
            self.hitbox_size = hitbox_size
        if hitpoints is None:
            self.hitpoints = []

    def sprite_time(self):
        self.spr_frame += 1
        if self.spr_frame > 60:
            self.spr_frame = 0

    def hitbox(self):
        self.hitpoints = []
        self.hitpoints.append(self.x)
        self.hitpoints.append(self.y)
        if self.hitbox_size:
            self.hitpoints.append(self.x + self.hitbox_size[0])
            self.hitpoints.append((self.y + self.hitbox_size[1]))
        else:
            if self.orientation > 0:
                self.hitpoints.append(self.x + self.w)
            else:
                self.hitpoints.append(self.x - self.w)
            self.hitpoints.append(self.y + self.h)

    def apply_offset(self, offset):
        self.x -= offset


# ITEM CLASSES
# Class for items
class Item(Sprite):
    def __init__(
            self, x: int, y: int, image: int, u: int, v: int, w: int, h: int,
            orientation=1, spr_frame=0, hitbox_size=None, hitpoints=None, item=0, picked=False, spawned=False):
        super().__init__(x, y, image, u, v, w, h, orientation, spr_frame, hitbox_size, hitpoints)
        self.item = item
        self.picked = picked
        self.spawned = spawned

    def pick_up(self):
        self.picked = True
        self.h = 0


# Class for coins
class Coin(Item):
    def __init__(
            self, x: int, y: int, image=0, u=40, v=88, w=10, h=16,
            orientation=1, spr_frame=0, hitbox_size=None, hitpoints=None, picked=False, spawned=False, coin_timer=30):
        super().__init__(x, y, image, u, v, w, h, orientation, spr_frame, hitbox_size, hitpoints, picked, spawned)
        if hitbox_size is None:
            self.hitbox_size = [16, 16]
        self.coin_timer = coin_timer

    def timer(self):
        if self.coin_timer > 0:
            self.coin_timer -= 1
            return False
        else:
            return True


# Class for mushroom power-ups
class Mushroom(Item):
    def __init__(
            self, x: int, y: int, image=0, u=72, v=103, w=16, h=16,
            orientation=1, spr_frame=0, hitbox_size=None, hitpoints=None, picked=False, spawned=False, y_limit=192):
        super().__init__(x, y, image, u, v, w, h, orientation, spr_frame, hitbox_size, hitpoints, picked, spawned)
        self.y_limit = y_limit
        if hitbox_size is None:
            self.hitbox_size = [16, 16]

    def mushroom_collision_check(self, other):
        if self is not other and not isinstance(other, Enemy):
            if other.hitpoints[2] > self.hitpoints[0] and self.hitpoints[2] > other.hitpoints[0]:
                if self.hitpoints[3] >= other.hitpoints[1] and self.hitpoints[1] < other.hitpoints[3]:
                    self.y_limit = other.hitpoints[1]
            if other.hitpoints[3] > self.hitpoints[1] and self.hitpoints[3] > other.hitpoints[1] + 4:
                if self.hitpoints[2] >= other.hitpoints[0] > self.hitpoints[2] - 4 or \
                        self.hitpoints[0] <= other.hitpoints[2] < self.hitpoints[0] + 4:
                    self.orientation *= -1

    def mushroom_movement(self):
        speed = 0.5
        if self.y_limit > self.hitpoints[3]:
            self.y += 1.5
            if self.orientation == 1:
                self.x += speed / 2
            else:
                self.x -= speed / 2
        else:
            if self.orientation == 1:
                self.x += speed
            else:
                self.x -= speed


# Class for fire flower power-ups
class FireFlower(Item):
    def __init__(
            self, x: int, y: int, image: int, u: int, v: int, w: int, h: int,
            orientation=1, spr_frame=0, hitbox_size=[16, 16], hitpoints=None, picked=False, spawned=False):
        super().__init__(x, y, image, u, v, w, h, orientation, spr_frame, hitbox_size, hitpoints, picked, spawned)


# Class for star power-ups
class Star(Item):
    def __init__(
            self, x: int, y: int, image: int, u: int, v: int, w: int, h: int,
            orientation=1, spr_frame=0, hitbox_size=[16, 16], hitpoints=None, picked=False, spawned=False):
        super().__init__(x, y, image, u, v, w, h, orientation, spr_frame, hitbox_size, hitpoints, picked, spawned)


# BLOCK CLASSES
# Main class for solid blocks
class Block(Sprite):
    def __init__(
            self, x: int, y: int, image: int, u: int, v: int, w: int, h: int,
            orientation=1, spr_frame=0, hitbox_size=None, hitpoints=None, hidden=False):
        super().__init__(x, y, image, u, v, w, h, orientation, spr_frame, hitbox_size, hitpoints)
        self.hidden = hidden


class Stair(Block):
    def __init__(
            self, x: int, y: int, image: int, u=64, v=72, w=16, h=16,
            orientation=1, spr_frame=0, hitbox_size=None, hitpoints=None, hidden=False):
        super().__init__(x, y, image, u, v, w, h, orientation, spr_frame, hitbox_size, hitpoints, hidden)


class Ground(Block):
    def __init__(
            self, x: int, y: int, image: int, u=0, v=72, w=16, h=16,
            orientation=1, spr_frame=0, hitbox_size=None, hitpoints=None, hidden=False):
        super().__init__(x, y, image, u, v, w, h, orientation, spr_frame, hitbox_size, hitpoints, hidden)


# Class for hittable blocks
class HitBlock(Block):
    def __init__(
            self, x: int, y: int, image: int, u: int, v: int, w: int, h: int,
            orientation=1, spr_frame=0, hitbox_size=None, hitpoints=None, hidden=False, is_hit=False):
        super().__init__(x, y, image, u, v, w, h, orientation, spr_frame, hitbox_size, hitpoints, hidden)
        self.is_hit = is_hit


# Class for breakable bricks
class BreakableBrick(HitBlock):
    def __init__(
            self, x: int, y: int, image=0, u=16, v=72, w=32, h=88,
            orientation=1, spr_frame=0, hitbox_size=None, hitpoints=None, hidden=False, is_hit=False):
        super().__init__(x, y, image, u, v, w, h, orientation, spr_frame, hitbox_size, hitpoints, hidden, is_hit)
        if hitbox_size is None:
            self.hitbox_size = [16, 16]

    def brick_break(self):
        self.h = 0
        self.is_hit = True
        self.u = 32
        self.v = 128


# Class for bricks with items
class ItemBrick(HitBlock):
    def __init__(
            self, x: int, y: int, item_obj=None, image=0, u=16, v=72, w=32, h=88,
            orientation=1, spr_frame=0, hitbox_size=None, hitpoints=None,
            item=0, hidden=False, count=1, counting=False,
            is_hit=False):
        super().__init__(x, y, image, u, v, w, h, orientation, spr_frame, hitbox_size, hitpoints, hidden, is_hit)
        if hitbox_size is None:
            self.hitbox_size = [16, 16]
        if item_obj is None:
            self.item_obj = Coin(self.x + 3, self.y - 16)
        else:
            self.item_obj = item_obj
        self.item = item
        self.count = count
        self.counting = counting

    def hit(self):
        if self.count <= 0:
            self.is_hit = True
            self.u = 32
            self.v = 72


# Class for item blocks
class ItemBlock(HitBlock):
    def __init__(
            self, x: int, y: int, item_obj=None, image=0, u=48, v=72, w=16, h=16,
            orientation=1, spr_frame=0, hitbox_size=None, hitpoints=None,
            item=0, hidden=False, is_hit=False):
        super().__init__(x, y, image, u, v, w, h, orientation, spr_frame, hitbox_size, hitpoints, hidden, is_hit)
        if hitbox_size is None:
            self.hitbox_size = [16, 16]
        if item_obj is None:
            self.item_obj = Coin(self.x + 3, self.y - 16)
        else:
            self.item_obj = item_obj
        self.item = item

    def hit(self):
        self.is_hit = True
        self.hidden = False
        self.u = 32
        self.v = 72


# Class for pipes
class Pipe(Block):
    def __init__(
            self, x: int, y: int, image: int, u=0, v=88, w=32, h=24,
            orientation=1, spr_frame=0, hitbox_size=None, hitpoints=None, hidden=False, can_access=False):
        super().__init__(x, y, image, u, v, w, h, orientation, spr_frame, hitbox_size, hitpoints, hidden)
        self.can_access = can_access


# ENEMY CLASSES
# Main class for enemies
class Enemy(Sprite):
    def __init__(
            self, x: int, y: int, image: int, u: int, v: int, w: int, h: int, orientation=1,
            spr_frame=0, hitbox_size=None, hitpoints=None, speed=1, y_limit=176, stomped=False, dead=False,
            dead_timer=0):
        super().__init__(x, y, image, u, v, w, h, orientation, spr_frame, hitbox_size, hitpoints)
        self.speed = speed
        self.y_limit = y_limit
        self.stomped = stomped
        self.dead = dead
        self.dead_timer = dead_timer

    def enemy_block_collision_check(self, other):
        if not self.dead:
            # Ground collision
            if isinstance(other, Goomba) and other.stomped:
                pass
            elif isinstance(self, Koopa) and self.hit and isinstance(other, Enemy) and self is not other:
                if self.hitpoints[1] < other.hitpoints[3] and self.hitpoints[3] > other.hitpoints[1] + 4:
                    if self.hitpoints[2] >= other.hitpoints[0] > self.hitpoints[2] - 4 or \
                            self.hitpoints[0] <= other.hitpoints[2] < self.hitpoints[0] + 4:
                        other.dead = True
            elif self is not other:
                if self.hitpoints[0] < other.hitpoints[2] and self.hitpoints[2] > other.hitpoints[0]:
                    if self.hitpoints[3] >= other.hitpoints[1] and self.hitpoints[1] < other.hitpoints[3]:
                        self.y_limit = other.hitpoints[1]
                if self.hitpoints[1] < other.hitpoints[3] and self.hitpoints[3] > other.hitpoints[1] + 4:
                    if self.hitpoints[2] >= other.hitpoints[0] > self.hitpoints[2] - 4 or \
                            self.hitpoints[0] <= other.hitpoints[2] < self.hitpoints[0] + 4:
                        self.orientation *= -1

    def enemy_movement(self):
        if not self.stomped:
            self.speed = 0.5
            if self.x <= 256 and not self.dead:
                if self.hitpoints[3] < self.y_limit:
                    self.y += 1.5
                    if self.orientation == 1:
                        self.x += self.speed / 2
                    else:
                        self.x -= self.speed / 2
                else:
                    if self.orientation == 1:
                        self.x += self.speed
                    else:
                        self.x -= self.speed
            if self.y >= 300:
                self.dead = True
        else:
            if isinstance(self, Koopa):
                if self.hit:
                    self.speed = 1
                    if self.y_limit > self.hitpoints[3]:
                        self.y += 1.5
                        if self.orientation == 1:
                            self.x += self.speed / 2
                        else:
                            self.x -= self.speed / 2
                    else:
                        if self.orientation == 1:
                            self.x += self.speed
                        else:
                            self.x -= self.speed


# Class for Goombas
class Goomba(Enemy):
    def __init__(
            self, x: int, y: int, image=0, u=0, v=48, w=16, h=16,
            orientation=-1, spr_frame=0, hitbox_size=None, hitpoints=None,
            speed=0.5, y_limit=176, stomped=False, dead_timer=0):
        super().__init__(x, y, image, u, v, w, h, orientation, spr_frame, hitbox_size, hitpoints, speed, y_limit,
                         stomped, dead_timer)

    def enemy_sprites(self):
        if not self.stomped:
            if self.spr_frame // 10 % 2 == 0:
                self.w = 16
            else:
                self.w = -16
        else:
            self.dead_timer += 1
            if self.dead_timer <= 30:
                self.u = 16
            else:
                self.h = 0
                self.dead = True


# Class for Koopas
class Koopa(Enemy):
    def __init__(
            self, x: int, y: int, image=0, u=32, v=50, w=16, h=22,
            orientation=-1, spr_frame=0, hitbox_size=None, hitpoints=None, speed=0.5, y_limit=176, stomped=False,
            hit=False, dead_timer=0):
        super().__init__(x, y, image, u, v, w, h, orientation, spr_frame, hitbox_size, hitpoints, speed, y_limit,
                         stomped, dead_timer)
        self.hit = hit

    def enemy_sprites(self):
        if not self.stomped:
            self.h = 22
            self.v = 48
            self.w = 16 * self.orientation
            self.hitbox_size = [16, 22]
        else:
            self.dead_timer += 1
            self.h = 14
            self.u = 48
            self.v = 50
            self.hitbox_size = [16, 14]
            if self.dead_timer >= 120 and not self.hit:
                self.dead_timer = 0
                self.stomped = False
