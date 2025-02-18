import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import pickle
import random
import warehouse_robot_env as wr

def run_q_learning(episodes, is_training=True, render=False):
    
    env = gym.make('warehouse-robot-v0', render_mode='human' if render else None)

    if(is_training):
        q = np.zeros((env.unwrapped.grid_rows, env.unwrapped.grid_cols, 3, env.action_space.n))
    else:
        f = open('v0_warehouse_solution.pkl', 'rb')
        q = pickle.load(f)
        f.close()

    learning_rate_a = 0.9
    discount_factor_g = 0.9
    epsilon = 1

    steps_per_episode = np.zeros(episodes)

    step_count=0
    for i in range(episodes):
        if(render):
            print(f'Episode {i}')

        state = env.reset()[0]
        terminated = False

        while(not terminated):
            if is_training and random.random() < epsilon:
                action = env.action_space.sample()
            else:                
                q_state_idx = tuple(state) 

                action = np.argmax(q[q_state_idx])
            
            new_state,reward,terminated,_,_ = env.step(action)

            q_state_action_idx = tuple(state) + (action,)

            q_new_state_idx = tuple(new_state)

            if is_training:
                q[q_state_action_idx] = q[q_state_action_idx] + learning_rate_a * (
                        reward + discount_factor_g * np.max(q[q_new_state_idx]) - q[q_state_action_idx]
                )

            state = new_state

            step_count+=1
            if terminated:
                steps_per_episode[i] = step_count
                step_count = 0

        epsilon = max(epsilon - 1/episodes, 0)

    env.close()

    sum_steps = np.zeros(episodes)
    for t in range(episodes):
        sum_steps[t] = np.mean(steps_per_episode[max(0, t-100):(t+1)])
    plt.plot(sum_steps)
    plt.savefig('v0_warehouse_solution.png')

    if is_training:
        f = open("v0_warehouse_solution.pkl","wb")
        pickle.dump(q, f)
        f.close()


if __name__ == '__main__':
    run_q_learning(1000, is_training=True, render=False)
    run_q_learning(1, is_training=False, render=True)