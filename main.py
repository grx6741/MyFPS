from data import player, enemy, bullet
from ursina import *

app = Ursina()

DirectionalLight(x = 0, y = 20, z = 0, shadow = True, rotation = (45, -45, 45))

player = player.Player(
    textures = [
        "resources/weaponModels/mp5/texture_mp5.png",
        "resources/weaponModels/ak47/texture_ak47.png"
    ],
    models = [
        "resources/weaponModels/mp5/mp5.obj",
        "resources/weaponModels/ak47/akm.obj"
    ],
    position = (0, 5, 0),
    collision = True,
    collider = "mesh",
    speed = 15,
    height = 10
)

plane = Entity(
    model = "plane",
    texture = "cog",
    scale = (100, 1, 100),
    position = (0, 0, 0),
    collider = "mesh"
)

app.run()
