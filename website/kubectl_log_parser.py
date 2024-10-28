import subprocess
from prometheus_client import start_http_server, Gauge

player_gauge = Gauge('minecraft_players', 'Number of players on the Minecraft server')

def parse_line_for_player_count(line, player_count):
    if "has joined the game" in line:
        player_count += 1
    elif "has left the game" in line:
        player_count -= 1
    return player_count

def format_log_line(line):
    if "has joined the game" in line:
        return f"{line.split(' ')[1]} has joined the game"
    elif "has left the game" in line:
        return f"{line.split(' ')[1]} has left the game"
    elif "joined as a spectator" in line:
        return f"{line.split(' ')[1]} joined as a spectator"
    return line

def monitor_kubectl_logs(output_file_path):
    player_count = 0
    last_player_count = -1  # Initialize to a value that will ensure the first count is logged
    process = subprocess.Popen(["kubectl", "logs", "-f", "kind-minecraft"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    with open(output_file_path, "w") as output_file:
        for line in iter(process.stdout.readline, ''):
            player_count = parse_line_for_player_count(line, player_count)
            formatted_line = format_log_line(line)
            if player_count != last_player_count:
                player_gauge.set(player_count)
                output_file.seek(0) 
                output_file.truncate()  
                output_file.write(f"Current player count: {player_count}\n")
                last_player_count = player_count

            if any(phrase in line for phrase in ["has joined the game", "has left the game", "joined as a spectator"]):
                output_file.write(formatted_line + "\n")
                output_file.flush()
                print(formatted_line.strip())
    
    process.stdout.close()
    process.wait()

if __name__ == '__main__':
    output_file_path = "../players.txt"
    start_http_server(8001)  
    monitor_kubectl_logs(output_file_path)
