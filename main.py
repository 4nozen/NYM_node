import os
import subprocess

class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    ITALICS = '\033[3m'
    FADED = '\033[2m'
    UNDERLINE = '\033[4m'

def is_node_running():
    info_process = subprocess.run("ps -A | grep nym-node'", shell=True, capture_output=True, text=True).stdout
    if info_process == "":
        print(f"{Color.OKGREEN}Lets install it.{Color.ENDC}")
        print("")
        return True
    else:
        print(f"{Color.FAIL}nym-node is exists.{Color.ENDC}")
        print("EXIT")
        os.system("exit")
        return False

def host_requirements():
    print(f"""    minimum requirements:
    {Color.FAIL}{Color.BOLD}CPU(s): 4, RAM: 4GB
    HDD: 40GB storage
    IPv4 and IPv6
    1TB bandwidth and 1Gbps port speed{Color.ENDC}""")
    print("")

    info_cpu = subprocess.run("lscpu | grep 'CPU(s):'", shell=True, capture_output=True, text=True).stdout
    info_cpu = str(info_cpu).split('\n')[0].replace("                               ", " ")

    info_mem = subprocess.run("lsmem | grep 'Total online memory:'", shell=True, capture_output=True, text=True).stdout
    info_mem = str(info_mem).split('\n')[0].replace("      ", " ")

    info_hd = subprocess.run("lsblk | grep 'disk'", shell=True, capture_output=True, text=True).stdout
    info_hd = str(info_hd).split('\n')[0].replace("sda", "HDD:").replace("      ", " ")

    info_op = subprocess.run("hostnamectl | grep 'Operating'", shell=True, capture_output=True, text=True).stdout


    print(f"""    your requirements:{Color.OKGREEN}
    {info_cpu}
    {info_mem}
    {info_hd}
    {info_op}
    {Color.ENDC}
    """)

def continue_or_exit():
    answer = input("What to continue? (y/n): ")
    if  answer == "y" or answer == "Y":
        print("LFG!")
        node_install()
    elif answer == "n" or answer == "N":
        print("EXIT")
        os.system("exit")
    else:
        continue_or_exit()

def node_install():
    git_node = "https://github.com/nymtech/nym/releases/download/nym-binaries-v2024.8-wispa/nym-node"
    if os.path.exists("nym-node"):
        print("nym-node already exists. EXIT")
        # os.system("exit")
    else:
        print(f"Downloading nym-node...{git_node}")
        os.system(f"wget {git_node}")
    
    # os.system("sudo su")
    os.system("chmod +x nym-node")
    os.system("mv nym-node /usr/local/bin/")
    # os.system("cp nym-node /usr/local/bin/")
    os.system("which nym-node")
    os.system("nym-node --version")

    node_name = input("Enter your node name: ")
    os.system(f'nym-node run --id {node_name} --init-only --mode mixnode --verloc-bind-address 0.0.0.0:1790 --public-ips "$(curl -4 https://ifconfig.me)" --accept-operator-terms-and-conditions')
    linux_user = subprocess.run("who", shell=True, capture_output=True, text=True).stdout.split(" ")[0]
    # linux_user = 'root'
    os.system(f"""sudo echo '[Unit]
Description=Nym Node 1.1.5
StartLimitInterval=350
StartLimitBurst=10

[Service]
User={linux_user}
LimitNOFILE=65536
ExecStart=/usr/local/bin/nym-node run --id {node_name} --deny-init --mode mixnode --accept-operator-terms-and-conditions
KillSignal=SIGINT
Restart=on-failure
RestartSec=30

[Install]
WantedBy=multi-user.target' | tee /etc/systemd/system/nym-node.service""")
    # os.system("systemctl daemon-reload")
    os.system("systemctl enable nym-node")
    os.system("systemctl start nym-node")
    # os.system("systemctl status nym-node.service")
    os.system("exit")
    print("------------------logs-------------------")
    os.system("journalctl -u nym-node.service -n 20 --no-pager")
    os.system(f"nym-node bonding-information --id {node_name}")



if __name__ == '__main__':
    os.system("clear")
    is_node_running()
    host_requirements()
    continue_or_exit()
