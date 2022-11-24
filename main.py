import pyxel
from mario import Mario
from sprites import *


# Pyxel class
class Game:
    FPS = 60

    def __init__(
            self, w: int, h: int, c: str, frame=0, seconds=0, fps=FPS,
            offset=0, tmoffset=0, tmshift=False, lives=3, rem_time=400):
        pyxel.init(w, h, caption=c, fps=fps, scale=3)
        self.frame = frame
        self.seconds = seconds
        self.offset = offset
        self.tmoffset = tmoffset
        self.tmshift = tmshift
        self.lives = lives
        self.rem_time = rem_time
        pyxel.run(self.update, self.draw)

    # Time method
    def time(self):
        """
        This method keeps track of the seconds passed since the start
        of the program and is used to make calculations based
        on time.q
        """
        self.frame += 1
        if self.frame > 60:
            self.frame = 0
            self.seconds += 1
        for enemy in enemyList:
            enemy.sprite_time()
        mario.sprite_time()
        return self.seconds

    def time_counter(self):
        if self.frame == 30 or self.frame == 0:
            self.rem_time -= 1
        if self.rem_time <= 0:
            mario.die()

    @staticmethod
    def sprites_animations():
        mario.sprite_selection()
        for enemy in enemyList:
            enemy.enemy_sprites()

    @staticmethod
    def remove_instance():
        aux_inst = instanceList.copy()
        instanceList.clear()
        blockList.clear()
        powerupList.clear()
        for inst in aux_inst:
            if isinstance(inst, BreakableBrick) and inst.is_hit:
                pass
            elif isinstance(inst, Enemy) and inst.dead:
                pass
            elif isinstance(inst, Coin) and inst.timer():
                pass
            else:
                instanceList.append(inst)
                if isinstance(inst, HitBlock):
                    blockList.append(inst)
                if isinstance(inst, Item) and not inst.picked:
                    powerupList.append(inst)

    # TODO: literally everything
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        # Time
        self.time()
        self.time_counter()
        # Mario movement
        mario.player_movement(GRAVITY)
        mario.y_limit = 300
        # Screen scroll
        self.offset = mario.scroll(self.offset)
        self.tmoffset -= self.offset
        for inst in instanceList:
            if not isinstance(inst, Mario):
                inst.apply_offset(self.offset)
        # Entity movement
        for enemy in enemyList:
            enemy.y_limit = 300
            for inst in instanceList:
                if not isinstance(inst, Mario):
                    enemy.enemy_block_collision_check(inst)
            enemy.enemy_movement()
        # Collision detection
        for inst in instanceList:
            inst.hitbox()
            powerup = mario.collision_check(inst)
            if powerup is not None:
                powerupList.append(powerup)
                instanceList.append(powerup)
                powerup.x += self.tmoffset
        for powerup in powerupList:
            if isinstance(powerup, Coin):
                if powerup.timer():
                    del powerup
            elif isinstance(powerup, Mushroom):
                powerup.y_limit = 300
                for inst in instanceList:
                    powerup.mushroom_collision_check(inst)
                powerup.mushroom_movement()
        # Mario i-frames
        if mario.invulnerable > 0:
            mario.invulnerability()
        # Deletion of broken blocks and dead enemies
        self.remove_instance()

    def draw(self):
        # Load sprites file
        pyxel.load("marioassets.pyxres")
        # Background color
        pyxel.cls(12)
        # Tilemap
        if self.tmoffset < -1792 and not self.tmshift:
            self.tmshift = True
            self.tmoffset += 1792
            print("shifted tilemap")
        if not self.tmshift:
            pyxel.bltm(self.tmoffset, 0, 0, 0, 0, 256, 216)
        else:
            pyxel.bltm(self.tmoffset, 0, 0, 0, 32, 256, 216)
        # Animations
        self.sprites_animations()
        # Blocks
        for block in blockList:
            pyxel.blt(block.x, block.y, block.image, block.u, block.v, *block.hitbox_size)
        # Enemies
        for enemy in enemyList:
            pyxel.blt(enemy.x, enemy.y, 0, enemy.u, enemy.v, enemy.w, enemy.h)
        pyxel.blt(mario.x, mario.y, 0, mario.u, mario.v, mario.w, mario.h)
        # Items
        for item in powerupList:
            pyxel.blt(item.x, item.y, 0, item.u, item.v, item.w, item.h)
        # Interface
        pyxel.text(24, 4, "MARIO", 7)
        pyxel.text(24, 10, f"{mario.score:06d}", 7)
        pyxel.blt(88, 10, 0, 240, 240, 5, 8)
        pyxel.text(88, 10, f"  x {mario.coins:02d}", 7)
        pyxel.text(152, 4, "WORLD", 7)
        pyxel.text(156, 10, "1-1", 7)
        pyxel.text(216, 4, "TIME", 7)
        pyxel.text(220, 10, f"{self.rem_time:03d}", 7)
        # Win screen
        if self.tmshift and self.tmoffset <= -1442:
            pyxel.rect(0, 0, 256, 216, 0)
            pyxel.text(100, 115, "LEVEL COMPLETED", 7)
        # GROUND AND BLOCKS

        # RANDOM DEBUG STUFF
        pyxel.text(0, 0, f"{powerupList}", 0)
        for powerup in powerupList:
            if isinstance(powerup, Mushroom):
                pyxel.text(0, 10, f"{powerup.y_limit}", 0)

# INITIAL SETUP
# Scenery
groundList = [
    Ground(0, 192, 0, hitbox_size=[1104, 24]),
    Ground(1136, 192, 0, hitbox_size=[240, 24]),
    Ground(1424, 192, 0, hitbox_size=[624, 24]),
    Ground(2048, 192, 0, hitbox_size=[402, 24]),
    Ground(2498, 192, 0, hitbox_size=[1000, 24])
]
breakableList = [
    BreakableBrick(321, 128),
    BreakableBrick(353, 128),
    BreakableBrick(385, 128),
    BreakableBrick(1281, 64),
    BreakableBrick(1297, 64),
    BreakableBrick(1313, 64),
    BreakableBrick(1329, 64),
    BreakableBrick(1345, 64),
    BreakableBrick(1361, 64),
    BreakableBrick(1377, 64),
    BreakableBrick(1393, 64),
    BreakableBrick(1457, 64),
    BreakableBrick(1473, 64),
    BreakableBrick(1489, 64),
    BreakableBrick(1265, 128),
    BreakableBrick(1233, 128),
    ItemBrick(1505, 128, count=5),
    BreakableBrick(1601, 128),
    ItemBrick(1617, 128, item=3),
    BreakableBrick(1905, 128),
    BreakableBrick(1953, 64),
    BreakableBrick(1969, 64),
    BreakableBrick(1985, 64),
    BreakableBrick(2065, 64),
    BreakableBrick(2113, 64),
    BreakableBrick(2081, 128),
    BreakableBrick(2097, 128),
    BreakableBrick(2705, 128),
    BreakableBrick(2721, 128),
    BreakableBrick(2737, 128),
    BreakableBrick(2753, 128)
]
itemblList = [
    ItemBlock(257, 128),
    ItemBlock(337, 128, item=1, item_obj=Mushroom(337, 112)),
    ItemBlock(369, 128),
    ItemBlock(353, 64),
    ItemBlock(1025, 112, u=150, v=0, hidden=True, item=1, item_obj=Mushroom(1025, 96)),
    ItemBlock(1249, 128, item=1, item_obj=Mushroom(1249, 112)),
    ItemBlock(1505, 64),
    ItemBlock(1697, 128),
    ItemBlock(1745, 128),
    ItemBlock(1745, 64, item=1, item_obj=Mushroom(1745, 48)),
    ItemBlock(1793, 128),
    ItemBlock(2081, 64),
    ItemBlock(2097, 64),
    ItemBlock(2737, 128)
]
pipeList = [
    Pipe(449, 160, 0, hitbox_size=[32, 32]),
    Pipe(609, 144, 0, hitbox_size=[32, 48]),
    Pipe(737, 128, 0, hitbox_size=[32, 64]),
    Pipe(913, 128, 0, hitbox_size=[32, 64]),
    Pipe(2625, 160, 0, hitbox_size=[32, 32]),
    Pipe(2881, 160, 0, hitbox_size=[32, 32])
]
stairList = [
    Stair(2161, 176, 0, hitbox_size=[16, 16]),
    Stair(2177, 160, 0, hitbox_size=[16, 32]),
    Stair(2193, 144, 0, hitbox_size=[16, 48]),
    Stair(2209, 128, 0, hitbox_size=[16, 64]),
    Stair(2305, 176, 0, hitbox_size=[16, 16]),
    Stair(2289, 160, 0, hitbox_size=[16, 32]),
    Stair(2273, 144, 0, hitbox_size=[16, 48]),
    Stair(2257, 128, 0, hitbox_size=[16, 88]),
    Stair(2385, 176, 0, hitbox_size=[16, 16]),
    Stair(2401, 160, 0, hitbox_size=[16, 32]),
    Stair(2417, 144, 0, hitbox_size=[16, 48]),
    Stair(2433, 128, 0, hitbox_size=[16, 64]),
    Stair(2449, 128, 0, hitbox_size=[16, 88]),
    Stair(2497, 128, 0, hitbox_size=[16, 88]),
    Stair(2513, 144, 0, hitbox_size=[16, 48]),
    Stair(2529, 160, 0, hitbox_size=[16, 32]),
    Stair(2545, 176, 0, hitbox_size=[16, 16]),
    Stair(2913, 176, 0, hitbox_size=[16, 16]),
    Stair(2929, 160, 0, hitbox_size=[16, 32]),
    Stair(2945, 144, 0, hitbox_size=[16, 48]),
    Stair(2961, 128, 0, hitbox_size=[16, 64]),
    Stair(2977, 112, 0, hitbox_size=[16, 80]),
    Stair(2993, 96, 0, hitbox_size=[16, 96]),
    Stair(3009, 80, 0, hitbox_size=[16, 112]),
    Stair(3025, 64, 0, hitbox_size=[16, 128]),
    Stair(3041, 64, 0, hitbox_size=[16, 128])
]

# default: 0, 192
mario = Mario(0, 192)

# ENEMIES
goombaList = [
    Goomba(353, 176, hitbox_size=[16, 16]),
    Goomba(642, 176, orientation=1, hitbox_size=[16, 16]),
    Goomba(817, 176, hitbox_size=[16, 16]),
    Goomba(841, 176, hitbox_size=[16, 16]),
    Goomba(1553, 176, hitbox_size=[16, 16]),
    Goomba(1577, 176, hitbox_size=[16, 16]),
    Goomba(1841, 176, hitbox_size=[16, 16]),
    Goomba(1865, 176, hitbox_size=[16, 16]),
    Goomba(2001, 176, hitbox_size=[16, 16]),
    Goomba(2025, 176, hitbox_size=[16, 16]),
    Goomba(2065, 176, hitbox_size=[16, 16]),
    Goomba(2088, 176, hitbox_size=[16, 16]),
    Goomba(1281, 48, hitbox_size=[16, 16]),
    Goomba(1313, 48, hitbox_size=[16, 16]),
    Goomba(2801, 176, hitbox_size=[16, 16]),
    Goomba(2825, 176, hitbox_size=[16, 16]),
]
koopaList = [
    Koopa(1713, 170, hitbox_size=[16, 22])
]

powerupList = []

enemyList = []

blockList = []

instanceList = [mario]

for ground in range(len(groundList)):
    instanceList.append(groundList[ground])

for brick in range(len(breakableList)):
    instanceList.append((breakableList[brick]))
    blockList.append(breakableList[brick])

for itemblock in range(len(itemblList)):
    instanceList.append(itemblList[itemblock])
    blockList.append(itemblList[itemblock])

for goomba in range(len(goombaList)):
    instanceList.append(goombaList[goomba])
    enemyList.append(goombaList[goomba])

for koopa in range(len(koopaList)):
    instanceList.append(koopaList[koopa])
    enemyList.append(koopaList[koopa])

for pipe in range(len(pipeList)):
    instanceList.append(pipeList[pipe])

for stair in range(len(stairList)):
    instanceList.append(stairList[stair])

# default: 256, 216
WIDTH = 256
HEIGHT = 216
CAPTION = "Cheap copy of Super Mario Bros."

GRAVITY = 0.3

for instance in instanceList:
    instance.hitbox()

Game(WIDTH, HEIGHT, CAPTION)

pyxel.run(Game.update, Game.draw)
