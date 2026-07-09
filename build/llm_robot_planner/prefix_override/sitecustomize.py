import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/shital-tiwari/ros2_ws/install/llm_robot_planner'
