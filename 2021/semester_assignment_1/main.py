from world import *
from my_enums import Scenario
from agents import BountyHunter, Bandit

import PySimpleGUI as sg

sg.theme('DarkAmber')

layout = [[sg.Text('Choose the preferred options:')],
          [sg.Checkbox('Make graph', default=True, key='prnt_graph'),
           sg.Checkbox('Show fancy graphics', default=False, key='show_graphx'),
           sg.Checkbox('Show resulting policy', default=True, key='show_pol')],
          [sg.Text('Select scenario to run:')],
          [sg.Radio('A (policy iteration)', 'scenario', True, key='a_pi'),
           sg.Radio('A (Q-learning)', 'scenario', key='a_ql'),
           sg.Radio('B (Q-learning)', 'scenario', key='b_ql'),
           sg.Radio('C (Q-learning)', 'scenario', key='c_ql'),
           sg.Radio('D (Q-learning)', 'scenario', key='d_ql', disabled=True)],
          [sg.Text('Select max number of episodes:')],
          [sg.Radio('1', 'episodes', key='e_1'),
           sg.Radio('10', 'episodes', key='e_10'),
           sg.Radio('1000', 'episodes', key='e_1000'),
           sg.Radio('5000', 'episodes', True, key='e_5000'),
           sg.Radio('10000', 'episodes', key='e_10000'),
           sg.Radio('100000', 'episodes', key='e_100000')],
          [sg.Button('Launch'), sg.Button('Exit')]]

window = sg.Window('Agent setup', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Launch':
        print_graph = values['prnt_graph']
        fancy_graphics = values['show_graphx']
        show_policy = values['show_pol']
        model_based = False
        if values['a_pi']:
            model_based = True
            scen = Scenario.A
        elif values['a_ql']:
            scen = Scenario.A
        elif values['b_ql']:
            scen = Scenario.B
        elif values['c_ql']:
            scen = Scenario.C
        elif values['d_ql']:
            scen = Scenario.D
        else:
            break

        if values['e_1']:
            max_episodes = 1
        elif values['e_10']:
            max_episodes = 10
        elif values['e_1000']:
            max_episodes = 1000
        elif values['e_5000']:
            max_episodes = 5000
        elif values['e_10000']:
            max_episodes = 10000
        elif values['e_100000']:
            max_episodes = 100000
        else:
            break

        bounty_hunter = BountyHunter(scen, (9, 0), model_based)
        bandit = Bandit(scen, (3, 8))

        world = World(scen, max_episodes)

        world.set_agent(bounty_hunter)
        world.set_agent(bandit)

        print("\nStarting scenario {}".format(scen.name))

        world.train()

        print("System {} convergent after {} episodes".format(("IS" if world.convergent else "NOT"),
                                                              world.current_episode))

        if show_policy:
            print("Bounty hunter policy:")
            if model_based:
                bounty_hunter.print_policy()
            else:
                bounty_hunter.q_table.print_table()
            if scen == Scenario.C or scen == Scenario.D:
                print("Bandit policy:")
                bandit.q_table.print_table()

        if print_graph:
            if model_based:
                world.plot_max_v_change()
            else:
                world.plot_max_q_change()
                world.plot_rewards_over_time()

        print("The agents sampled the reward-function {} times".format(bounty_hunter.total_samples))

        if fancy_graphics:
            world.show_solution()

# TODO: Finish up parts c and d
