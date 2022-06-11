from ursina import *
from ursina.prefabs.health_bar import HealthBar

class Mob:
    def __init__(self, position):
        self.name = "mob"
        self.mob = Entity(
            model = "sphere",
            texture = "brick",
            scale = (2, 5, 2),
            texture_scale = (10, 10, 10),
            position = position,
            collision = True,
            collider = "mesh"
        )
        self.speed = 7
        self.health = 100
        self.heath_bar = HealthBar(
            parent = self.mob,
            value = self.health,
            show_text = False,
            position = Vec3(self.mob.x, self.mob.y + 10, self.mob.z)
        )

    def move_towards(self, player):
        #dist = Vec3(player.x, player.y, player.z) - self.mob.position
        dist = player.get_position() - self.mob.position
        dist = dist.normalized()
        self.mob.x += dist.x * self.speed * time.dt
        #self.mob.y += dist.y * self.speed * time.dt
        self.mob.z += dist.z * self.speed * time.dt
