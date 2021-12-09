#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import ipaddress

SEPARATOR = " "
parser = argparse.ArgumentParser(
    description="weblog_helper.py is a python script that parses NCSA Common (access log) log files and filters the output on the basis of IP address or CIDR range."
)
parser.add_argument(
    "--ip",
    type=str,
    required=False,
    help="Filter logs with this IP",
)
parser.add_argument(
    "--log-file",
    type=str,
    required=False,
    default="public_access.log.txt",
    help="Log file path",
)


def parse_logs(log_file_data, ip):
    # A global try-catch in case any issues with `ip` the function
    # should exit
    filtered_logs = []
    try:
        # if no ip is supplied, display all log lines
        if ip is None:
            ip = "0.0.0.0/0"
        network = ipaddress.ip_network(ip)
        for log in log_file_data:
            try:
                # Adding try-catch here, in case one of the log line is faulty
                IP = log.split(SEPARATOR)[0]
                IP = ipaddress.ip_address(IP)
                if IP in network:
                    filtered_logs.append(log)
            except Exception as e:
                print(f"Exception in loop : {e}\nlog : {log}\n")
    except Exception as e:
        print(f"Overall exception in parse_logs : {e}\nip : {ip}\n")
    finally:
        return filtered_logs


def main():
    args = parser.parse_args()
    try:
        with open(args.log_file, "r") as f:
            log_file_data = f.readlines()
        filtered_logs = parse_logs(log_file_data, args.ip)
        for log in filtered_logs:
            print(log, end="")
    except Exception as e:
        print(f"Error reading log file : {e}")


if __name__ == "__main__":
    main()
