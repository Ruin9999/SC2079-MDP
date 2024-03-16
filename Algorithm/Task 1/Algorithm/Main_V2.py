import time

from CommandGenerator import CommandGenerator
from Navigator import Navigator
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import importlib.util

app = Flask(__name__)
CORS(app)


@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "OK"})


@app.route("/navigate", methods=["POST"])
def path_finding():
    content = request.json
    size_x = content["size_x"]
    size_y = content["size_y"]
    robot_x = content["robot_x"]
    robot_y = content["robot_y"]
    robot_direction = int(content["robot_direction"])
    obstacles = content["obstacles"]

    navigator = Navigator(size_x, size_y, robot_x, robot_y, robot_direction)

    for obstacle in obstacles:
        navigator.add_obstacle(
            obstacle["x"], obstacle["y"], obstacle["d"], obstacle["id"]
        )

    start = time.time()
    # Get shortest path
    optimal_path, distance = navigator.get_optimal_order_dp()
    print(f"Time taken to find shortest path using A* search: {time.time() - start}s")
    print(f"Distance to travel: {distance} units")

    # Based on the shortest path, generate commands for the robot
    commands = CommandGenerator.generate(optimal_path, obstacles)

    # Get the starting location and add it to path_results
    path_results = [optimal_path[0].get_dict()]
    # Process each command individually and append the location the robot should be after executing that command to path_results
    i = 0

    print("Commands Length: {}".format(len(commands)))
    transformed_commands = []

    for command in commands:
        print(command)
        if (
            command.startswith("SNAP")
            or command.startswith("FIN")
            or command[-1] != "0"
        ):
            continue
        elif (
            command.startswith("FW")
            or command.startswith("FS")
            or command.startswith("BW")
            or command.startswith("BS")
        ):
            i += int(command[2:]) // 10
        else:
            i += 1
        print("Current i: {}".format(i))
        direction_commands = {"FL": 2, "FR": 3, "BL": 3, "BR": 3}
        num_dicts_to_add = direction_commands.get(command[:2], 1)
        for _ in range(num_dicts_to_add):
            path_results.append(optimal_path[i].get_dict())

    # Adding additional commands for turning
    for command in commands:
        if command.startswith("FL"):
            transformed_commands.append("FW003")
            transformed_commands.append("FL090")
        elif command.startswith("FR"):
            transformed_commands.append("FW002")
            transformed_commands.append("FR090")
        elif command.startswith("BL"):
            transformed_commands.append("FW003")
            transformed_commands.append("BL090")
            transformed_commands.append("BW002")
        elif command.startswith("BR"):
            transformed_commands.append("FW003")
            transformed_commands.append("BR090")
            transformed_commands.append("BW002")
        else:
            transformed_commands.append(command)

    return jsonify(
        {
            "data": {
                "distance": distance,
                "path": path_results,
                "commands": transformed_commands,
            },
            "error": None,
        }
    )


if __name__ == "__main__":

    try:
        # Construct the path to PC_CONFIG.py and import module
        config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'rpi', 'config'))
        config_path = os.path.join(config_dir, 'PC_CONFIG.py')
        spec = importlib.util.spec_from_file_location("PC_CONFIG", config_path)
        PC_CONFIG = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(PC_CONFIG)

        app.run(host=PC_CONFIG.HOST, port=PC_CONFIG.ALGO_PORT, debug=True)
    except:
        print('Unable to Connect to PC_CONFIG Host and Port. Switching to 0.0.0.0:8000.')
        app.run(host='0.0.0.0', port=8000, debug=True)
