import tensorflow as tf
import numpy as np
import gym
import matplotlib.pyplot as plt
from replay_buffer import ReplayBuffer
from actor import ActorNetwork
from critic import CriticNetwork
from ou_noise import OUNoise

ACTOR_LEARNING_RATE = 0.0001
CRITIC_LEARNING_RATE = 0.001
TAU = 0.001  # Soft target update rate
ENV_NAME = 'MountainCarContinuous-v0'
RANDOM_SEED = 1234
EXPLORE = 70
DEVICE = '/cpu:0'


def ddpg(episodes=1000, MINIBATCH_SIZE=40, GAMMA=0.99, epsilon=1.0, min_epsilon=0.01, BUFFER_SIZE=10000,
         train=True):
    with tf.Session() as sess:
        # configuring environment
        env = gym.make(ENV_NAME)
        # configuring the random processes
        np.random.seed(RANDOM_SEED)
        tf.set_random_seed(RANDOM_SEED)
        env.seed(RANDOM_SEED)
        # info of the environment to pass to the agent
        state_dim = env.observation_space.shape[0]
        print('State dimension: ', state_dim)
        action_dim = env.action_space.shape[0]
        print('Action dimension: ', action_dim)
        action_bound = np.float64(10)
        # Creating agent
        noise = OUNoise(action_dim, theta=0.4)
        actor = ActorNetwork(sess, state_dim, action_dim, action_bound, ACTOR_LEARNING_RATE, TAU, DEVICE)
        critic = CriticNetwork(sess, state_dim, action_dim, CRITIC_LEARNING_RATE, TAU, actor.get_num_trainable_vars(),
                               DEVICE)

        sess.run(tf.global_variables_initializer())

        # Initialize weights and memory
        actor.update_target_network()
        critic.update_target_network()
        replay_buffer = ReplayBuffer(BUFFER_SIZE, RANDOM_SEED)

        goal_hits = 0
        max_state = -1.
        try:
            if not train:
                critic.recover_critic()
                actor.recover_actor()
                print('Models restored successfully')
        except:
            print('Failed to restore models')

        # Data collection
        train_epsilon_log = []
        train_action_log = None
        train_action_w_noise_log = None
        train_action_noise_log = None
        train_reward_log = []
        train_efficiency_log = []
        train_steps_log = []
        test_action_log = None
        test_steps_log = []
        test_rewards_log = []
        test_efficiency_log = []

        for e in range(episodes):
            print('Episode ', e)
            if train:
                train_action_log = []
                train_action_noise_log = []
                train_action_w_noise_log = []
            else:
                test_action_log = []

            state = env.reset()
            state = np.hstack(state)
            ep_reward = 0
            ep_ave_max_q = 0
            done = False
            step = 0
            max_state_episode = -1
            epsilon -= (epsilon / EXPLORE)
            train_epsilon_log.append(round(epsilon, 3))
            epsilon = np.maximum(min_epsilon, epsilon)

            while not done:
                env.render()

                # 1. get action with actor, and add noise
                action_original = actor.predict(
                    np.reshape(state, (1, state_dim)))
                if train and e % 50 == 0 or e == 99 and train:
                    train_action_log.append(action_original[0])
                elif not train and e % 50 == 0 or e == 99 and not train:
                    test_action_log.append(action_original[0])

                noise_value = noise.noise()
                action = action_original + max(epsilon, 0) * noise_value if train else action_original
                if train and e % 50 == 0 or e == 99 and train:
                    train_action_noise_log.append(*noise_value * max(epsilon, 0))
                    train_action_w_noise_log.append(action[0])

                # 2. take action, see next state and reward :
                next_state, reward, done, info = env.step(action)

                if train:
                    # 3. Save in replay buffer:
                    replay_buffer.add(np.reshape(state, (actor.s_dim,)), np.reshape(action, (actor.a_dim,)), reward,
                                      done, np.reshape(next_state, (actor.s_dim,)))

                    # Keep adding experience to the memory until there are at least MINIBATCH_SIZE samples
                    if replay_buffer.size() > MINIBATCH_SIZE:
                        # 4. sample random minibatch of transitions:
                        s_batch, a_batch, r_batch, t_batch, s2_batch = replay_buffer.sample_batch(MINIBATCH_SIZE)

                        # Calculate targets
                        # 5. Train critic Network (states, actions, R + gamma* V(s', a')):
                        # 5.1 Get critic prediction = V(s', a')
                        # the a' is obtained using the actor prediction! or in other words : a' = actor(s')
                        target_q = critic.predict_target(s2_batch, actor.predict_target(s2_batch))

                        # 5.2 get y_t where:
                        y_t = []
                        for k in range(MINIBATCH_SIZE):
                            if t_batch[k]:
                                y_t.append(r_batch[k])
                            else:
                                y_t.append(r_batch[k] + GAMMA * target_q[k])

                        # 5.3 Train Critic!
                        predicted_q_value, _ = critic.train(s_batch, a_batch, np.reshape(y_t, (MINIBATCH_SIZE, 1)))

                        ep_ave_max_q += np.amax(predicted_q_value)

                        # 6 Compute Critic gradient (depends on states and actions)
                        # 6.1 therefore I first need to calculate the actions the current actor would take.
                        a_outs = actor.predict(s_batch)
                        # 6.2 I calculate the gradients
                        grads = critic.action_gradients(s_batch, a_outs)
                        actor.train(s_batch, grads[0])

                        # Update target networks
                        actor.update_target_network()
                        critic.update_target_network()

                state = next_state
                if next_state[0] > max_state_episode:
                    max_state_episode = next_state[0]

                ep_reward = ep_reward + reward
                step += 1

            if done:
                noise.reset()
                if state[0] > 0.45:
                    goal_hits += 1

            if max_state_episode > max_state:
                max_state = max_state_episode

            if train:
                train_reward_log.append(round(ep_reward, 3))
            else:
                test_rewards_log.append(round(ep_reward, 3))

            if train and e % 50 == 0 or e == 99 and train:
                plt.plot(train_action_log)
                plt.title(f'Actions in episode {e} during training')
                plt.xlabel('Step')
                plt.ylabel('Action')
                plt.savefig(f'plots/training_actions_{e}.jpg')
                plt.show()

                plt.plot(train_action_noise_log)
                plt.title(f'Noise for episode {e} during training')
                plt.xlabel('Step')
                plt.ylabel('Noise')
                axes = plt.gca()
                min_x, max_x = axes.get_xlim()
                min_y, max_y = axes.get_ylim()
                plt.text(max_x - max_x * 0.36, max_y - max_y * 0.1,
                         f'long term mean: {np.round(np.average(train_action_noise_log), 3)}',
                         bbox=dict(facecolor='black', alpha=0.3))
                plt.savefig('plots/noise_example.jpg')
                plt.savefig(f'plots/training_noise_{e}.jpg')
                plt.show()

                plt.plot(train_action_w_noise_log)
                plt.title(f'Actions w/ noise in episode {e} during training')
                plt.xlabel('Step')
                plt.ylabel('Action w/ noise')
                plt.savefig(f'plots/training_actions_w_noise_{e}.jpg')
                plt.show()
            elif not train and e % 50 == 0 or e == 99 and not train:
                plt.plot(test_action_log)
                plt.title(f'Actions in episode {e} during testing')
                plt.xlabel('Step')
                plt.ylabel('Action')
                plt.savefig(f'plots/testing_actions_{e}.jpg')
                plt.show()

            if train:
                train_efficiency_log.append(round(100. * (goal_hits / (e + 1.)), 3))
                train_steps_log.append(step)
            else:
                test_efficiency_log.append(round(100. * (goal_hits / (e + 1.)), 3))
                test_steps_log.append(step)

        if train:
            plt.plot(train_epsilon_log)
            plt.title('Epsilon decay during training')
            plt.xlabel('Episode')
            plt.ylabel('Epsilon')
            plt.savefig('plots/training_epsilon.jpg')
            plt.show()

            plt.plot(train_reward_log)
            plt.title('Rewards during training')
            plt.xlabel('Episode')
            plt.ylabel('Reward')
            axes = plt.gca()
            plt.text(.95, .95,
                     f'Max reward: {np.round(np.max(train_reward_log), 1)}\n'
                     f'Min reward: {np.round(np.min(train_reward_log), 1)}',
                     transform=axes.transAxes,
                     horizontalalignment='right', verticalalignment='top',
                     bbox=dict(facecolor='black', alpha=0.3))
            plt.savefig('plots/training_rewards.jpg')
            plt.show()

            plt.plot(train_efficiency_log)
            plt.title('Efficiency during training (goal hit ratio)')
            plt.xlabel('Episode')
            plt.ylabel('%')
            plt.savefig('plots/training_efficiency.jpg')
            plt.show()

            plt.plot(train_steps_log)
            plt.title('Steps during training')
            plt.xlabel('Episode')
            plt.ylabel('Steps')
            plt.savefig('plots/training_steps.jpg')
            plt.show()

            print('Saving model...')
            critic.save_critic()
            actor.save_actor()
            print('Model saved')
        else:
            plt.plot(test_steps_log)
            plt.title('Steps during testing')
            plt.xlabel('Episode')
            plt.ylabel('Value')
            plt.savefig('plots/testing_steps.jpg')
            plt.show()

            plt.plot(test_rewards_log)
            plt.title('Rewards during testing')
            plt.xlabel('Episode')
            plt.ylabel('Value')
            axes = plt.gca()
            plt.text(.95, .95,
                     f'Max reward: {np.round(np.max(test_rewards_log), 1)}\n'
                     f'Min reward: {np.round(np.min(test_rewards_log), 1)}',
                     transform=axes.transAxes,
                     horizontalalignment='right', verticalalignment='top',
                     bbox=dict(facecolor='black', alpha=0.3))
            plt.savefig('plots/testing_rewards.jpg')
            plt.show()

            plt.plot(test_efficiency_log)
            plt.title('Efficiency during testing (goal hit ratio)')
            plt.xlabel('Episode')
            plt.ylabel('Value')
            plt.savefig('plots/testing_efficiency.jpg')
            plt.show()


if __name__ == '__main__':
    ddpg(episodes=100, epsilon=1., train=True)
    # ddpg(episodes=100, train=False)