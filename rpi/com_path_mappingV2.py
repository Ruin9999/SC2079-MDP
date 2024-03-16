def map_commands_to_paths(data):
    commands = data["commands"]
    paths = data["path"]
    mapped_commands = []

    # Initialize variables to keep track of the paths associated with each command
    current_paths = []
    # Track the current path index for assigning to commands
    non_snap_path_index = 0

    # Iterate over commands
    for command in commands:
        # Handle SNAP, FIN, or commands to be skipped by not appending new paths but processing their logic
        if command in ["FIN", "FW002", "FW003", "BW002"]:
            # Append the command with its accumulated paths (if any) and reset current_paths
            mapped_commands.append((command, current_paths if current_paths else None))
            current_paths = []  # Reset for the next command
        elif command.startswith("SNAP"):
            # For SNAP commands, do not reset current_paths to allow accumulation
            mapped_commands.append((command, None))
        else:
            # For other commands, accumulate paths and then append to the command
            if non_snap_path_index < len(paths):
                current_paths.append(paths[non_snap_path_index])
                non_snap_path_index += 1  # Move to the next path for the next valid command

            # Once paths are accumulated for this command, append it to mapped_commands
            mapped_commands.append((command, current_paths))
            current_paths = []  # Reset for the next command

    # Handle the case where the last command(s) are "SNAP" or skipped ones without direct path assignments
    if current_paths:
        # If there are accumulated paths not yet appended because the last commands were skipped or "SNAP",
        # append these paths to the last valid command that was added to mapped_commands.
        for i in range(len(mapped_commands) - 1, -1, -1):
            if mapped_commands[i][1] is not None:
                mapped_commands[i][1].extend(current_paths)
                break

    return mapped_commands


if __name__ == "__main__":
    # Provided input data

    data =  {
        "commands": [
            "FW090",
            "FW003",
            "BR090",
            "BW002",
            "BW020",
            "FW003",
            "BR090",
            "BW002",
            "SNAP6_C",
            "BW040",
            "FW003",
            "BL090",
            "BW002",
            "FW050",
            "SNAP1_C",
            "BW090",
            "FW003",
            "BL090",
            "BW002",
            "FW010",
            "SNAP4_C",
            "BW020",
            "FW003",
            "BL090",
            "BW002",
            "SNAP5_C",
            "BW070",
            "FW003",
            "BR090",
            "BW002",
            "SNAP2_C",
            "BW040",
            "FW003",
            "BL090",
            "BW002",
            "FW090",
            "FW010",
            "FW003",
            "FL090",
            "FW090",
            "FW030",
            "FW003",
            "BR090",
            "BW002",
            "FW020",
            "SNAP3_C",
            "FIN"
        ],
        "distance": 184.0,
        "path": [
            {
                "d": 0,
                "s": -1,
                "x": 1,
                "y": 1
            },
            {
                "d": 0,
                "s": -1,
                "x": 1,
                "y": 10
            },
            {
                "d": 6,
                "s": -1,
                "x": 3,
                "y": 7
            },
            {
                "d": 6,
                "s": -1,
                "x": 5,
                "y": 7
            },
            {
                "d": 4,
                "s": 6,
                "x": 8,
                "y": 9
            },
            {
                "d": 4,
                "s": -1,
                "x": 8,
                "y": 13
            },
            {
                "d": 6,
                "s": -1,
                "x": 10,
                "y": 16
            },
            {
                "d": 6,
                "s": 1,
                "x": 5,
                "y": 16
            },
            {
                "d": 6,
                "s": -1,
                "x": 14,
                "y": 16
            },
            {
                "d": 0,
                "s": -1,
                "x": 17,
                "y": 14
            },
            {
                "d": 0,
                "s": 4,
                "x": 17,
                "y": 15
            },
            {
                "d": 0,
                "s": -1,
                "x": 17,
                "y": 13
            },
            {
                "d": 2,
                "s": 5,
                "x": 15,
                "y": 10
            },
            {
                "d": 2,
                "s": -1,
                "x": 8,
                "y": 10
            },
            {
                "d": 0,
                "s": 2,
                "x": 5,
                "y": 8
            },
            {
                "d": 0,
                "s": -1,
                "x": 5,
                "y": 4
            },
            {
                "d": 2,
                "s": -1,
                "x": 3,
                "y": 1
            },
            {
                "d": 2,
                "s": -1,
                "x": 12,
                "y": 1
            },
            {
                "d": 2,
                "s": 6,
                "x": 13,
                "y": 1
            },
            {
                "d": 0,
                "s": -1,
                "x": 15,
                "y": 4
            },
            {
                "d": 0,
                "s": -1,
                "x": 15,
                "y": 13
            },
            {
                "d": 0,
                "s": -1,
                "x": 15,
                "y": 16
            },
            {
                "d": 6,
                "s": -1,
                "x": 17,
                "y": 13
            },
            {
                "d": 6,
                "s": 3,
                "x": 15,
                "y": 13
            }
        ]
    }
    # Correct function call
    command_path_mapping = map_commands_to_paths(data)

    # Output the mapping for review
    for mapping in command_path_mapping:
        print(mapping)