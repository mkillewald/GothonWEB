class Room(object):

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.paths = {}
        
    def go(self, direction):
        return self.paths.get(direction, None)
        
    def add_paths(self, paths):
        self.paths.update(paths)
        
central_corridor = Room("Central Corridor",
"""
The Gothons of Planet Percal #25 have invaded your ship and destroyed
your entire crew.  You are the last surviving member and your last
mission is to get the neutron destruct bomb from the Weapons Armory,
put it in the bridge, and blow the ship up after getting into an 
escape pod.

You're running down the central corridor to the Weapons Armory when
a Gothon jumps out, red scaly skin, dark grimy teeth, and evil clown costume
flowing around his hate filled body.  He's blocking the door to the
Armory and about to pull a weapon to blast you.
"""
)

central_corridor_try_again = Room(central_corridor.name, central_corridor.description +
"""
Sorry, try again. Maybe you should ask for 'help'.
"""
)

central_corridor_help = Room(central_corridor.name, central_corridor.description +
"""
Do you choose to shoot!, dodge! or tell a joke?
"""
)

central_corridor_shoot = Room('Death', 
"""
Quick on the draw you yank out your blaster and fire it at the Gothon.
His clown costume is flowing and moving around his body, which throws
off your aim.  Your laser hits his costume but misses him entirely.  This
completely ruins his brand new costume his mother bought him, which
makes him fly into an insane rage and blast you repeatedly in the face until
you are dead.  Then he eats you.
"""
)

central_corridor_dodge = Room("Death", 
"""
Like a world class boxer you dodge, weave, slip and slide right
as the Gothon's blaster cranks a laser past your head.
In the middle of your artful dodge your foot slips and you
bang your head on the metal wall and pass out.
You wake up shortly after only to die as the Gothon stomps on
your head and eats you.
"""
)

laser_weapon_armory = Room("Laser Weapon Armory",
"""
Lucky for you they made you learn Gothon insults in the academy.
You tell the one Gothon joke you know:
Lbhe zbgure vf fb sng, jura fur fvgf nebhaq gur ubhfr, fur fvgf nebhaq gur ubhfr.
The Gothon stops, tries not to laugh, then busts out laughing and can't move.
While he's laughing you run up and shoot him square in the head
putting him down, then jump through the Weapon Armory door.

You do a dive roll into the Weapon Armory, crouch and scan the room
for more Gothons that might be hiding.  It's dead quiet, too quiet.
You stand up and run to the far side of the room and find the
neutron bomb in its container.  There's a keypad lock on the box
and you need the code to get the bomb out.  If you get the code
wrong 10 times then the lock closes forever and you can't
get the bomb.  The code is 3 digits.
"""
)

laser_weapon_armory_help = Room(laser_weapon_armory.name, laser_weapon_armory.description +
"""
You have a total of 10 tries at guesing the 3 digit lock code.
Good luck!
"""
)

laser_weapon_armory_death = Room("Death",
"""
The lock buzzes one last time and then you hear a sickening
melting sound as the mechanism is fused together.
You decide to sit there, and finally the Gothons blow up the
ship from their ship and you die.
"""
)

the_bridge = Room("The Bridge",
"""
The container clicks open and the seal breaks, letting gas out.
You grab the neutron bomb and run as fast as you can to the
bridge where you must place it in the right spot.

You burst onto the Bridge with the netron destruct bomb
under your arm and surprise 5 Gothons who are trying to
take control of the ship.  Each of them has an even uglier
clown costume than the last.  They haven't pulled their
weapons out yet, as they see the active bomb under your
arm and don't want to set it off.
""")

the_bridge_try_again = Room(the_bridge.name, the_bridge.description +
"""
Sorry, try again. Perhaps you should ask for 'help'.
"""
)

the_bridge_help = Room(the_bridge.name, the_bridge.description +
"""
Do you choose to slowly place or throw the bomb?
"""
)

the_bridge_death = Room("Death",
"""
In a panic you throw the bomb at the group of Gothons
and make a leap for the door.  Right as you drop it a
Gothon shoots you right in the back killing you.
As you die you see another Gothon frantically try to disarm
the bomb. You die knowing they will probably blow up when
it goes off.
"""
)

escape_pod = Room("Escape Pod",
"""
You point your blaster at the bomb under your arm
and the Gothons put their hands up and start to sweat.
You inch backward to the door, open it, and then carefully
place the bomb on the floor, pointing your blaster at it.
You then jump back through the door, punch the close button
and blast the lock so the Gothons can't get out.
Now that the bomb is placed you run to the escape pod to
get off this tin can.

You rush through the ship desperately trying to make it to
the escape pod before the whole ship explodes.  It seems like
hardly any Gothons are on the ship, so your run is clear of
interference.  You get to the chamber with the escape pods, and
now need to pick one to take.  Some of them could be damaged
but you don't have time to look.  There's 5 pods, which one
do you take?
""")

escape_pod_help = Room(escape_pod.name, escape_pod.description +
"""
Choose one the five numbered escape pods 1 through 5.
"""
)

the_end_winner = Room("The End",
"""
You jump into pod 2 and hit the eject button.
The pod easily slides out into space heading to
the planet below.  As it flies to the planet, you look
back and see your ship implode then explode like a
bright star, taking out the Gothon ship at the same
time. 

Congratulations, you won!
""")

the_end_loser = Room("The End",
"""
You jump into a random pod and hit the eject button.
The pod escapes out into the void of space, then
implodes as the hull ruptures, crushing your body
into jam jelly. 

So sad after making it this far, you lose.
"""
)

generic_death = Room("Death", "You died.")

escape_pod.add_paths({
    'help': escape_pod_help,
    '2': the_end_winner,
    '*': the_end_loser
})

the_bridge.add_paths({
    'help': the_bridge_help,
    'throw the bomb': the_bridge_death,
    'slowly place the bomb': escape_pod,
    '*': the_bridge_try_again
})

laser_weapon_armory.add_paths({
    'help': laser_weapon_armory_help,
    '123': the_bridge,
    '*': laser_weapon_armory_death
})

central_corridor.add_paths({
    'help': central_corridor_help,
    'shoot!': central_corridor_shoot,
    'dodge!': central_corridor_dodge,
    'tell a joke': laser_weapon_armory,
    '*': central_corridor_try_again
})

central_corridor_help.paths = central_corridor.paths
central_corridor_try_again.paths = central_corridor.paths
laser_weapon_armory_help.paths = laser_weapon_armory.paths
the_bridge_help.paths = the_bridge.paths
the_bridge_try_again.paths = the_bridge.paths
escape_pod_help.paths = escape_pod.paths

START = central_corridor
