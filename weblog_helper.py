#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import ipaddress
from datetime import datetime
from collections import defaultdict

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

parser.add_argument(
    "--top-ips",
    type=int,
    required=False,
    help="Get Top IPs",
)

parser.add_argument(
    "--rpm",
    required=False,
    help="Get Request Per Minute",
    action="store_true",
)

parser.add_argument(
    "--start-time",
    type=str,
    required=False,
    help="Start time",
)

parser.add_argument(
    "--end-time",
    type=str,
    required=False,
    help="End time",
)


def get_top_ips(log_file_data, no_of_ips):
    try:
        # defaultdict with '0' as value : https://stackoverflow.com/a/31838824
        ipList, sortedIPList = defaultdict(int), []
        for log in log_file_data:
            IP = log.split(SEPARATOR)[0]
            ipList[IP] = ipList[IP] + 1
        sortedIPList = sorted(
            ipList.items(), key=lambda kv: (kv[1], kv[0]), reverse=True
        )
    except Exception as e:
        print(f"Exception in get_top_ips {e}")
    return sortedIPList[:no_of_ips]


def get_rpm(log_file_data):
    try:
        # defaultdict with '0' as value : https://stackoverflow.com/a/31838824
        timeList, sortedTimeList = defaultdict(int), []
        for log in log_file_data:
            timeStamp = log.split(SEPARATOR)[3]
            timeStamp = timeStamp[
                1:-3
            ]  # Removing '[' and ':SS]'; Can also convert string to timestamp but is that required 🤔
            timeList[timeStamp] = timeList[timeStamp] + 1
        sortedTimeList = sorted(
            timeList.items(), key=lambda kv: (kv[1], kv[0]), reverse=False
        )
    except Exception as e:
        print(f"Exception in get_rpm {e}")
    return sortedTimeList


def get_logs_for_given_timeperiod(log_file_data, start_time, end_time):
    output_log = []
    start_time = datetime.strptime(start_time, "%H:%M")
    end_time = datetime.strptime(end_time, "%H:%M")
    for log in log_file_data:
        try:
            timeStamp = log.split(SEPARATOR)[3]
            timeStamp = timeStamp[1:]
            d = datetime.strptime(timeStamp, "%d/%b/%Y:%H:%M:%S")
            if (d.hour >= start_time.hour and d.minute >= start_time.minute) and (
                d.hour <= end_time.hour and d.minute <= end_time.minute
            ):
                output_log.append(log)
        except Exception as e:
            print(f"Error in get_logs_for_given_timeperiod : {e}")
    return output_log


def parse_logs(log_file_data, ip):
    """
    Used to parse logs and return filtered output on the basis of ip
    If the ip is `None`, it returns all the log lines

    Parameters
    ----------
    log_file_data : list
        Log file data, each line parsed into one entity of the list
    ip : str
        IP according to which we need to filter out the output
    Returns
    --------
    list
        A list of filtered log lines on the basis of IP
    """
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
        if args.start_time is not None and args.end_time is not None:
            log_file_data = get_logs_for_given_timeperiod(
                log_file_data, args.start_time, args.end_time
            )
        if args.top_ips is not None:
            sortedIPList = get_top_ips(log_file_data, args.top_ips)
            for ip in sortedIPList:
                print(ip)
        elif args.rpm is not None:
            sortedTimeList = get_rpm(log_file_data)
            for timeData in sortedTimeList:
                print(timeData)
        else:
            filtered_logs = parse_logs(log_file_data, args.ip)
            for log in filtered_logs:
                print(log, end="")
    except Exception as e:
        print(f"Error reading log file : {e}")


if __name__ == "__main__":
    main()
