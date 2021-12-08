# -*- coding: utf-8 -*-
import argparse
import ipaddress

SEPARATOR = " "
parser = argparse.ArgumentParser(description="Process logs.")
parser.add_argument(
    "--ip",
    type=str,
    required=True,
    help="Filter logs with this IP",
)
parser.add_argument(
    "--log-file",
    type=str,
    required=False,
    default="public_access.log.txt",
    help="Log file path",
)


def parse_logs(log_file, ip):
    network = ipaddress.ip_network(ip)
    with open(log_file, "r") as f:
        data = f.readlines()
    for log in data:
        IP = log.split(SEPARATOR)[0]
        IP = ipaddress.ip_address(IP)
        if IP in network:
            print(log, end="")


def main():
    args = parser.parse_args()
    parse_logs(args.log_file, args.ip)


if __name__ == "__main__":
    main()
