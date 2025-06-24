import os
import argparse
import subprocess

TEMPLATE = """port {port}

daemonize yes

bind 0.0.0.0

masterauth {password}

requirepass {password}

cluster-enabled yes

cluster-config-file nodes.conf

cluster-node-timeout 5000

appendonly yes

dir {dir}{sep}store

logfile {dir}{sep}log.txt
"""

def generate_redis_configs(base_dir, ports, password):
    for port in ports:
        dir_path = os.path.join(base_dir, str(port))
        abs_dir = os.path.abspath(dir_path)
        store_path = os.path.join(abs_dir, "store")

        os.makedirs(store_path, exist_ok=True)
        os.makedirs(abs_dir, exist_ok=True)

        config_path = os.path.join(abs_dir, "redis.conf")
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(TEMPLATE.format(port=port, dir=abs_dir, sep=os.sep, password=password))
        print(f"---> Generated config: {config_path}")

def start_redis_cluster(base_dir, ports):
    for port in ports:
        conf_path = os.path.join(base_dir, str(port), "redis.conf")
        if os.path.exists(conf_path):
            print(f"---> Starting Redis on port {port}")
            subprocess.Popen(["redis-server", conf_path])
        else:
            print(f"[Error] Config not found: {conf_path}")

def create_redis_cluster(ports, password):
    hostports = [f"127.0.0.1:{port}" for port in ports]
    cmd = [
        "redis-cli", "--cluster", "create", *hostports,
        "--cluster-replicas", "1", "-a", password
    ]
    print(f"---> Creating cluster with nodes: {', '.join(hostports)}")
    subprocess.run(cmd)

def stop_redis_cluster(ports):
    result = subprocess.run(
        ["ps", "aux"], capture_output=True, text=True
    )
    pids = []
    for line in result.stdout.splitlines():
        if "redis-server" in line and any(f":{port}" in line for port in ports):
            pid = line.split()[1]
            pids.append(pid)
    if pids:
        print(f"Stopping Redis processes: {', '.join(pids)}")
        for pid in pids:
            subprocess.run(["kill", pid])
    else:
        print("No matching Redis processes found.")


"""
# 初始化
python cluster_manager.py init --base-dir redis-cluster --ports 7000,7001,7002,7003,7004,7005 --password 10101
# --base-dir 持久化和配置的存储目录
# --port 端口
# --password 密码

# 启动
python cluster_manager.py start --base-dir redis-cluster --ports 7000,7001,7002,7003,7004,7005

# 创建（输入 yes）
python cluster_manager.py create --ports 7000,7001,7002,7003,7004,7005 --password 10101

# 停止
python cluster_manager.py stop --ports 7000,7001,7002,7003,7004,7005
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Redis Cluster Manager")
    subparsers = parser.add_subparsers(dest="command")

    # init
    parser_init = subparsers.add_parser("init", help="Generate redis.conf files")
    parser_init.add_argument("--base-dir", default=os.getcwd(), help="Base directory for configs")
    parser_init.add_argument("--ports", default="7000,7001,7002,7003,7004,7005", help="Ports")
    parser_init.add_argument("--password", required=True, help="Redis cluster password")

    # create
    parser_create = subparsers.add_parser("create", help="Create Redis cluster")
    parser_create.add_argument("--ports", default="7000,7001,7002,7003,7004,7005", help="Ports")
    parser_create.add_argument("--password", required=True, help="Redis cluster password")

    # start
    parser_start = subparsers.add_parser("start", help="Start Redis nodes")
    parser_start.add_argument("--base-dir", default=os.getcwd(), help="Base directory for configs")
    parser_start.add_argument("--ports", default="7000,7001,7002,7003,7004,7005", help="Ports")

    # stop
    parser_stop = subparsers.add_parser("stop", help="Stop Redis nodes")
    parser_stop.add_argument("--ports", default="7000,7001,7002,7003,7004,7005", help="Ports")

    args = parser.parse_args()
    ports = [int(p.strip()) for p in args.ports.split(",")]

    if args.command == "init":
        generate_redis_configs(args.base_dir, ports, args.password)
    elif args.command == "start":
        start_redis_cluster(args.base_dir, ports)
    elif args.command == "create":
        create_redis_cluster(ports, args.password)
    elif args.command == "stop":
        stop_redis_cluster(ports)
    else:
        parser.print_help()
