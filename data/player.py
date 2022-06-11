from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import * 

class Player(Entity):
    def __init__(self, textures, models, **kwargs):
        self.controller = FirstPersonController(**kwargs)
        super().__init__(
            parent = self.controller
        )
        self.textures = textures
        self.models = models

        self.mp5 = Entity(
            scale = 0.5,
            parent = self.controller.camera_pivot,
            texture = self.textures[0],
            model = self.models[0],
            position = (1.4, -1.5, 2.5),
            rotation = (0, -90, 0),
            collider = "box",
            shader = basic_lighting_shader,
            visible = False,
            cooldown = 0.5
        )

        self.ak47 = Entity(
            scale = 1.5,
            parent = self.controller.camera_pivot,
            texture = self.textures[1],
            model = self.models[1],
            position = (2.5, -1.5, 5),
            rotation = (0, 90, 0),
            collider = "mesh",
            shader = basic_lighting_shader,
            visible = True,
            cooldown = 0.5
        )

        self.weapons = [self.mp5, self.ak47]
        self.initial_rotations = [weapon.rotation for weapon in self.weapons]
        self.initial_positions = [weapon.position for weapon in self.weapons]
        self.current_weapon = 0
        self.switch_weapon()
        self.previous_position = self.position
        self.initial_speed = self.controller.speed
        self.sprinting = False

    def switch_weapon(self):
        for i , v in enumerate(self.weapons):
            if i == self.current_weapon:
                v.visible = True
            else:
                v.visible = False

    def weapon_bobbing(self):
        try:
            weapon = self.weapons[self.current_weapon]
            angle_x = mouse.velocity[0] * self.controller.mouse_sensitivity[0] * 2 * time.dt
            angle_z = mouse.velocity[1] * self.controller.mouse_sensitivity[1] * 2 * time.dt
            weapon.rotation_y += angle_x
            if self.current_weapon == 0:
                weapon.rotation_z -= angle_z
            else:
                weapon.rotation_z += angle_z

            if mouse.velocity[0] == 0:
                angle_y = weapon.rotation_y - self.initial_rotations[self.current_weapon][1]
                angle_z = weapon.rotation_z - self.initial_rotations[self.current_weapon][2]
                weapon.rotation_y -= angle_y * 2 * time.dt
                weapon.rotation_z -= angle_z * 2 * time.dt

        except IndexError or ValueError:
            pass

    def sprint(self):
        if self.sprinting:
            self.controller.speed = self.initial_speed + 20
        else:
            self.controller.speed = self.initial_speed

    def view_bobbing(self):
        weapon = self.weapons[self.current_weapon]
        if self.sprinting:
            if self.current_weapon == 0:
                max_rotation = self.initial_rotations[self.current_weapon] + Vec3(0, 0, -70)
                max_displacement = self.initial_positions[self.current_weapon] + Vec3(0, 1, -1)
            else:
                max_rotation = self.initial_rotations[self.current_weapon] + Vec3(0, 0, 85)
                max_displacement = self.initial_positions[self.current_weapon] + Vec3(0, 1, -3)
            angle = max_rotation - weapon.rotation
            displacement = max_displacement - weapon.position
            weapon.position += displacement * 2 * time.dt
            weapon.rotation += angle * 2 * time.dt
        else:
            angle = weapon.rotation - self.initial_rotations[self.current_weapon]
            displacement = weapon.position - self.initial_positions[self.current_weapon]
            weapon.position -= displacement * 2 * time.dt
            weapon.rotation -= angle * 2 * time.dt






    def shoot_animation(self):
        pass
        #if 1 == 1:
        #    weapon = self.weapons[self.current_weapon]
        #    angle_z = 5
        #    if key == "left mouse down":
        #        weapon.rotation_z += angle_z

        #    else:
        #        angle = weapon.rotation_z - self.initial_rotations[self.current_weapon][2]
        #        weapon.rotation_z -= angle * 0.3


    def input(self, key):
        try:
            if self.sprinting == False:
                self.current_weapon = int(key) - 1
                self.switch_weapon()
        except ValueError or IndexError:
            pass

    def update(self):
        self.weapon_bobbing()
        self.view_bobbing()
        self.sprint()
        if held_keys["left shift"]:
            self.sprinting = True
        else:
            self.sprinting = False
