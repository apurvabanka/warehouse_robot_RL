# Warehouse Robot RL

A robot operates in a warehouse grid where its task is to pick up items from specified locations and deliver them to designated drop-off points. The warehouse has shelves that act as obstacles and the robot must navigate around them efficiently.

# Steps to configure ENV

- Create a python virtual environment and activate it.
```CMD
python3 -m venv env
source env/bin/activate
```
- Install all the dependencies from the requirements.txt.
```CMD
pip install -r requirements.txt
```
- Run all the cells inside "warehouse_robot_env.ipynb".

# Folder Structure

- warehouse_robot.py - This file has the logic implementation for the warehouse robot for all the requred steps for Gym. The visualisation using pygame is included in this file.
- warehouse_robot_env.py - This file has the Gym implementation for warehouse robot env. The function logic from `warehouse_robot.py` file are used here. This file includes Gym model registration.
- warehouse_robot_env.ipynb - This file is a Jupyter notebook version of the `warehouse_robot_env.py` file. This file contains the outputs for the timestep runs.

A preview of the ENV is as below.

![Warehouse Robot GIF](warehouse_robot.gif)