from ursina import *

class Bullet(Entity):
    def __init__(self, speed = inf, lifetime=100, **kwargs):
        super().__init__(**kwargs)
        self.speed = speed
        self.lifetime = lifetime
        self.start = time.time()

    def update(self):
        ray = raycast(self.world_position, self.forward, distance = self.speed * time.dt)

        if not ray.hit and time.time() - self.start < self.lifetime:
            self.world_position += self.forward * self.speed * time.dt

        else:
            destroy(self)