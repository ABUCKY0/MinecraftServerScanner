import argparse
import ipaddress
import json
import os
import threading
from tqdm import tqdm
from mcstatus import JavaServer, BedrockServer

def scan_ip(ip, server_type, progress_bar):
    for port in args.port:
        try:
            if server_type == 'java':
                server = JavaServer(str(ip), int(port), timeout=10)
            elif server_type == 'bedrock':
                server = BedrockServer(str(ip), int(port), timeout=10)
            else:
                return
            status = server.status()
            print(f'Minecraft {server_type} server found at {ip}:{port} ({status.players.online}/{status.players.max} players')
            data = {
                'ip': ip,
                'port': port,
                'version': status.version.name,
                'protocol_version': status.version.protocol,
                'motd': status.description,
                'players_online': status.players.online,
                'players_max': status.players.max,
                'latency': status.latency
            }
            message = f'Minecraft {server_type} server found at {ip}:{port} ({data["players_online"]}/{data["players_max"]} players)'
            if (args.debug):
                print(message)
            with open(output_file_json, 'a') as f_json:
                if os.path.isfile(output_file_json):
                    f_json.write(',\n')
                else:
                    f_json.write('[\n')
                json.dump(data, f_json)
            with open(output_file_text, 'a') as f_text:
                f_text.write(message + '\n')
            print("made it this far so you know your code is working now")
        except ConnectionRefusedError:
            if args.debug:
                print(f'Connection refused to {ip}:{port}')
            with open("error2.log", "a") as errlog:
                errlog.write(f'Connection refused to {ip}:{port}' + "\n")
        except ConnectionResetError:
            if args.debug:
                print(f'Connection reset to {ip}:{port}')
            with open("error2.log", "a") as errlog:
                errlog.write(f'Connection reset to {ip}:{port}' + "\n")
        except ConnectionAbortedError:
            if args.debug:
                print(f'Connection aborted to {ip}:{port}')
            with open("error2.log", "a") as errlog:
                errlog.write(f'Connection aborted to {ip}:{port}' + "\n")
        except TimeoutError:
            if args.debug:
                print(f'Timeout connecting to {ip}:{port}')
            with open("error2.log", "a") as errlog:
                errlog.write(f'Timeout connecting to {ip}:{port}' + "\n")
        except Exception as e:
            if args.debug:
                print(f'Error connecting to {ip}:{port}' + 'Error:' + str(e))
            with open("error.log", "a") as errlog:
                errlog.write(f'Error connecting to {ip}:{port}' + 'Error:' + str(e) + "\n")
        progress_bar.update(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scan Minecraft servers.')
    parser.add_argument('-j', '--java', metavar='CIDR', nargs='+', help='scan Java servers in the specified CIDR range')
    parser.add_argument('-b', '--bedrock', metavar='CIDR', nargs='+', help='scan Bedrock servers in the specified CIDR range')
    parser.add_argument('-d', '--debug', action='store_true', help='enable debug mode')
    parser.add_argument('-p', '--players', metavar='PLAYER', nargs='+', help='list of player names to search for')
    parser.add_argument('-pO', '--port', type=int, nargs="+",help='port to scan')
    args = parser.parse_args()

    output_file_json = 'minecraft_servers.json'
    output_file_text = 'minecraft_servers.txt'
    port = args.port or 25565
    print(f'Scanning port {port}')
    ipnum = 0
    threads = []
    exclude_ips = set()
    if os.path.isfile('exclude.conf'):
        with open('exclude.conf', 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                try:
                    ipaddress.IPv4Address(line)
                    exclude_ips.add(line)
                except ValueError:
                    pass
    print(str(len(exclude_ips)) + ' IPs excluded')
    if args.java:
        for cidr_range in args.java:
            ipnum += len(list(ipaddress.IPv4Network(cidr_range)))
        progress_bar = tqdm(total=ipnum*len(args.port) - len(exclude_ips), desc='Scanning Java servers', unit='ip')
        for cidr_range in args.java:
            for ip in ipaddress.IPv4Network(cidr_range):
                if ip not in exclude_ips:
                    thread = threading.Thread(target=scan_ip, args=(str(ip), 'java', progress_bar,))
                    threads.append(thread)
                    thread.start()
                else:
                    progress_bar.update(1)
        progress_bar.close()
    elif args.bedrock:
        for cidr_range in args.bedrock:
            progress_bar = tqdm(total=len(list(ipaddress.IPv4Network(cidr_range))), desc='Scanning Bedrock servers', unit='ip')
            for ip in ipaddress.IPv4Network(cidr_range):
                if ip in exclude_ips:
                    continue
                thread = threading.Thread(target=scan_ip, args=(str(ip), 'bedrock', progress_bar,))
                threads.append(thread)
                thread.start()
            progress_bar.close()
    if args.bedrock or args.java:
        for thread in threads:
            thread.join()

        with open(output_file_json, 'a') as f_json:
            if os.path.isfile(output_file_json):
                f_json.write(']')
            else:
                f_json.write('[\n]')
    with open(output_file_text, 'a') as f_text:
        pass