import gymnasium as gym
from gymnasium import spaces
from gymnasium.envs.registration import register
from gymnasium.utils.env_checker import check_env
import random

import warehouse_robot as wr
import numpy as np

register(
    id='warehouse-robot-v0',
    entry_point='warehouse_robot_env:WarehouseRobotEnv',
)


class WarehouseRobotEnv(gym.Env):
    metadata = {"render_modes": ["human"], 'render_fps': 4}

    def __init__(self, grid_rows=6, grid_cols=6, render_mode=None, stochastic=False):

        self.grid_rows=grid_rows
        self.grid_cols=grid_cols
        self.render_mode = render_mode
        self.stochastic = stochastic
    
        self.warehouse_robot = wr.WarehouseRobot(grid_rows=grid_rows, grid_cols=grid_cols, fps=self.metadata['render_fps'])

        self.action_space = spaces.Discrete(len(wr.RobotAction))

        self.observation_space = spaces.Box(
            low=0,
            high=np.array([self.grid_rows-1, self.grid_cols-1, self.grid_rows-1, self.grid_cols-1]),
            shape=(4,),
            dtype=np.int32
        )

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.warehouse_robot.reset(seed=seed)

        obs = np.concatenate((self.warehouse_robot.robot_pos, self.warehouse_robot.target_pos))

        info = {}

        if(self.render_mode=='human'):
            self.render()

        return obs, info

    def step(self, action):

        if self.stochastic:
            if random.random() < 0.1:
                target_reached, reward = self.warehouse_robot.perform_action(wr.RobotAction(action))
        else:
            target_reached, reward = self.warehouse_robot.perform_action(wr.RobotAction(action))

        terminated=False
        if target_reached:
            terminated=True

        obs = np.concatenate((self.warehouse_robot.robot_pos, self.warehouse_robot.target_pos))

        info = {}

        if(self.render_mode=='human'):
            print(wr.RobotAction(action))
            self.render()

        return obs, reward, terminated, False, info

    def render(self):
        self.warehouse_robot.render()

if __name__ == "__main__":
    env = gym.make('warehouse-robot-v0', render_mode='human')


    obs = env.reset()[0]

    total_reward = 0

    while(True):
        rand_action = env.action_space.sample()
        obs, reward, terminated, _, _ = env.step(rand_action)

        total_reward += reward

        print(obs)

        print("Task Complete:" ,terminated, " Reward: ", total_reward)

        if(terminated):
            obs = env.reset()[0]