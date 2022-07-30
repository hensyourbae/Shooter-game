from ursina import *
from ursina import curve
from ursina.prefabs.first_person_controller \
    import FirstPersonController
app = Ursina()
Sky()
ground = Entity(model='plane',texture='ground',collider='mesh',scale=(100,1,10))

player = FirstPersonController(
    position=(0,2,-5)
)

wall1 = Entity(
    model='cube',
    texture='wall',
    collider='cube',
    scale=(100,10,5),
    position=(0,5,50),
    color=color.gray
)
wall2 = duplicate(wall1,z=-50)
wall3 = duplicate(wall1,rotation_y=90,x=-50,z=0)
wall4 = duplicate(wall3,x=50)
wall5 = duplicate(wall1, position=(0,2,0),scale=(20,5,0.5),color=color.white)

weapon = Entity(
    model='Ak74',
    parent=camera.ui,
    scale=2.5,
    color=color.gold,
    texture='white_cube',
    position=(0.8,-0.6),
    rotation=(-10,-20)
)

from random import uniform
enemies = []
objects = []
for i in range(4):
    enemy=FrameAnimation3d(
        'assests\pp',
        color=color.black,
        fps=10,
        scale=0.022,
        position=(uniform(-45,45),
                    uniform(33,45))
    )
    asObject=Entity(
        model='assets\pp_1',
        rotation_x=20,
        collider='box',
        parent=enemy,
        scale=(0.65,0.5,1),
        position=(0,30,0)
    )
    asObject.visible=False
    enemy.look_at(player)
    enemy.rotation_x=270
    enemy.rotation_z=-50
    enemies.append(enemy)
    objects.append(asObject)

def update():
    if held_keys['left mouse']:
        weapon.position = (0.75,-0.55)
    else:
        weapon.position = (0.8,-0.6)
    if player.y <=5:
        player.y=2
    for enemy in enemies:
        if enemy.visible:
            enemy.look_at(player)
            enemy.rotation_x=270
            enemy.rotation_z=-50
            dist = distance(enemy,player)
            if dist > 5:
                enemy.resume()
                diff_x = player.x - enemy.x
                diff_z = player.z - enemy.z
                enemy.x += 4*time.dt*diff_x(abs(diff_x))
                enemy.z += 4*time.dt*diff_z/abs(diff_z)
            else:
                enemy.pause()

def respawnEnemy(enemy):
    enemy.visible=True

def input(key):
    if key=='left mouse down':
        for obj, en in zip(object, enemies):
            if obj.hovered:
                en.position=(uniform(-45,45),
                                2,uniform(33,45))
                en.visible=False
                invoke(respawnEnemy,en,delay=3)
            dust = Entity(model=Circle(),
                            parent=camera.ui,
                            scale=0.03,color=color.red,
                            position=(0.14,-0.05,))
            dust.animate_scale(0.001,
                            duration=.1,
                            curve = curve.linear)
            dust.fade_out(duration=0.1)
app.run()
