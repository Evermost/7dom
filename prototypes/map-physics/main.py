from pandac.PandaModules import * 
import direct.directbase.DirectStart

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletDebugNode

from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode

from panda3d.bullet import BulletBoxShape

from panda3d.bullet import BulletCharacterControllerNode



################
# housekeeping #
################

# import stage model and make it render
#stage = loader.loadModel("models/environment")
#stage.reparentTo(render)

# disable the default mouse-controls for the camera
#base.disableMouse()



################
# worldkeeping #
################

# the actual world
world = BulletWorld()
world.setGravity(Vec3(0, 0, -9.81))

# a nodepath for attaching things
worldNP = render.attachNewNode('World')

# this would render the shapes, I wish I knew of this earlier
debugNP = worldNP.attachNewNode(BulletDebugNode('Debug'))
debugNP.show()
world.setDebugNode(debugNP.node())

# task to update the world
def update(task):
	dt = globalClock.getDt()
	world.doPhysics(dt)
	return task.cont
taskMgr.add(update, 'update')



##########
# ground #
##########

"""As expected, Bullet physical entities have:
		a Body with the vectors, 
		a Shape for the collisions,
		and I assume constrains and other such properties.
		
This ground entity is a static object, immovable, but solid. 
Which we achieve by not setting the mass."""

# body
node = BulletRigidBodyNode('ground')
#node.setMass(1.0)

# shape
shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
node.addShape(shape)

# attach to the nodetree via a parent, for easier access
np = render.attachNewNode(node)
np.setPos(0, 0, -2)

# attach to the Bullet world
world.attachRigidBody(node)

# The ground is as yet invisible. Deal with it.



#######
# Box #
#######

"""This box is a prop, like a regular old crate.
Therefore, it needs to be a Dynamic object."""

# body
node = BulletRigidBodyNode('Box')
node.setMass(1.0)

# shape
shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
node.addShape(shape)

# attach to the nodetree via a parent, for easier access
np = render.attachNewNode(node)
np.setPos(0, 5, 2)

# attach to the Bullet world
world.attachRigidBody(node)

# this is unnecessary since debug is on
## make it visible																#BUG: model does not match up with the shape, offset properly
#model = loader.loadModel('models/box.egg')
#model.flattenLight()
#model.reparentTo(np)



#############
# character #
#############

"""Bullet character controllers are a special Body.

It behaves as one expect an FPS character to behave: does not bounce, 
is always upright, and is controlled via velocity, not forces.

It still uses a Shape, but has other ways of assigning physical properties.

It seems to a bit incomplete: I moved the ground, and it didn't fall with it.
It also reacts strangely to the prop box. But I think that might be my fault...
Most people seem to be making their own CCs. But I think we don't need to yet."""

# shape
shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))

# bullect character object
node = BulletCharacterControllerNode (shape, 1)
 
# attach to the nodetree via a parent, for easier access which isn't really done
np = render.attachNewNode(node)
np.setPos(0, 0, 2)
#np.setR(10)
 
# attach to the Bullet world, as a character, note
world.attach_character(node)

# This isn't necessary anymore due to debug
## make it visible																#BUG: this model too did not match the actual shape, be careful next time
#model = loader.loadModel('models/box.egg')
#model.flattenLight()
#model.reparentTo(np)

# focus the camera at it
base.cam.setPos(0, -10, 0)
base.cam.lookAt(0, 0, 0)

# punks jump up: space
def jump():
	node.doJump()
base.accept('space', jump)

# forward: w
def walk():
	node.setLinearMovement(Vec3(0, 1, 0), True)
base.accept('w-repeat', walk)
base.accept('w', walk)

# backward: s
def walk():
	node.setLinearMovement(Vec3(0, -1, 0), True)
base.accept('s-repeat', walk)
base.accept('s', walk)

# forward: a
def walk():
	node.setLinearMovement(Vec3(-1, 0, 0), True)
base.accept('a-repeat', walk)
base.accept('a', walk)

# forward: d
def walk():
	node.setLinearMovement(Vec3(1, 0, 0), True)
base.accept('d-repeat', walk)
base.accept('d', walk)

# stop
def stop():
	node.setLinearMovement(Vec3(0, 0, 0), True)
base.accept('w-up', stop)
base.accept('s-up', stop)
base.accept('a-up', stop)
base.accept('d-up', stop)



####################
# runs the program #
####################

run()

