import time
                                        
from CommandGenerator2 import CommandGenerator
from Navigator import Navigator
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'OK'})

@app.route('/navigate', methods=['POST'])
def path_finding():
    content = request.json
    size_x = content['size_x']
    size_y = content['size_y']
    robot_x = content['robot_x']
    robot_y = content['robot_y']
    robot_direction = int(content['robot_direction'])
    obstacles = content['obstacles']

    navigator = Navigator(size_x, size_y, robot_x, robot_y, robot_direction)
    
    for obstacle in obstacles:
        navigator.add_obstacle(obstacle['x'], obstacle['y'], obstacle['d'], obstacle['id'])

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

    for command in commands:
        print(command)
        if command.startswith("SNAP"):
            continue
        if command.startswith("FIN"):
            continue
        if command[-1] == "2":
            continue
        elif command.startswith("FW") or command.startswith("FS"):
            i += int(command[2:]) // 10
        elif command.startswith("BW") or command.startswith("BS"):
            i += int(command[2:]) // 10
        else:
            i += 1

        print("Current i: {}".format(i))
        
        path_results.append(optimal_path[i].get_dict())
    return jsonify({
        "data": {
            'distance': distance,
            'path': path_results,
            'commands': commands
        },
        "error": None
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    #app.run(host='192.168.16.11', port=2040, debug=True)
    #app.run(host='192.168.80.27', port=2040, debug=True)
