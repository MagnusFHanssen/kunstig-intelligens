from world import *
from renderer import *
from my_enums import Scenario


wrld = World(Scenario.A)

print(wrld.r_map)

r = Renderer()

looping = True
i = 0

while looping:
    # Logic and stuff here

    # Render the frame
    r.update((4, 4), (9, 9), (2, 8))
    time.sleep(1.0 / 60.0)
