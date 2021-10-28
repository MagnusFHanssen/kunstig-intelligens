from world import *
from my_enums import Scenario
from agents import BountyHunter, Bandit

scenario_a = [(9, 0), (9, 1), (8, 1), (8, 2), (7, 2), (7, 3), (6, 3), (6, 4), (5, 4), (5, 5), (4, 5), (4, 6), (4, 6),
              (3, 6), (2, 6), (2, 7), (1, 7), (1, 8), (1, 9), (0, 9)]

scenario_d_1 = [(9, 0), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9),
                (9, 9), (8, 9), (7, 9), (6, 9), (5, 9), (4, 9), (3, 9), (2, 9), (1, 9), (0, 9),
                (0, 9), (0, 9), (0, 9), (0, 9), (0, 9), (0, 9), (0, 9), (0, 9), (0, 9), (0, 9)]
scenario_d_2 = [(9, 9), (8, 9), (7, 9), (6, 9), (5, 9), (4, 9), (3, 9), (3, 8), (2, 8), (2, 7),
                (2, 6), (2, 5), (2, 4), (3, 4), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (7, 4),
                (7, 3), (7, 4), (7, 3), (7, 4), (7, 3), (7, 4), (7, 3), (7, 4), (7, 3), (7, 4)]
scenario_d_3 = [(9, 0), (8, 0), (8, 1), (8, 2), (7, 2), (7, 3), (6, 3), (6, 4), (5, 4), (5, 5),
                (4, 5), (4, 6), (3, 6), (2, 6), (2, 7), (1, 7), (1, 8), (1, 9), (0, 9), (1, 9),
                (0, 9), (1, 9), (0, 9), (1, 9), (0, 9), (1, 9), (0, 9), (1, 9), (0, 9), (1, 9)]

s = Scenario.A

bounty_hunter = BountyHunter(s, (9, 0))
bandit = Bandit(s, (3, 8))

world = World(s)

world.set_agent(bounty_hunter)
world.set_agent(bandit)

world.train()

world.show_solution()

bounty_hunter.q_table.print_table()

print(world.convergent)
print(world.current_episode)

world.plot_max_q_change()

print(world.q_change_list[-1:])

