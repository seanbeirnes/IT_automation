# Reads a syslog file and creates a report based on errors found and user usage data.
import sys
import re
import operator
import csv

def is_info(string):
    pattern = "ticky: INFO"
    result = re.search(pattern, string)
    if result:
        return True
    else:
        return False

def is_error(string):
    pattern = "ticky: ERROR"
    result = re.search(pattern, string)
    if result:
        return True
    else:
        return False

def get_user(string):
    pattern = "\((.*)\)$"
    result = re.search(pattern, string)
    if result:
        return result.groups(1)[0].strip()
    else:
        return False

def get_error(string):
    pattern = "ticky: ERROR ([\w ']*)"
    result = re.search(pattern, string)
    if result:
        return result.groups(1)[0].strip()

def get_errors_report(file):
    errors = {}
    f = open(file)
    for line in f:
        this_line = line.strip()
        if is_error(this_line):
            error = get_error(this_line)
            if errors.get(error):
                errors[error] += 1
            else:
                errors[error] = 1
    return sorted(errors.items(), key=operator.itemgetter(1), reverse=True)
            
def get_user_report(file):
    users = {}
    f = open(file)
    for line in f:
        this_line = line.strip()
        user = get_user(this_line)
        if user not in users:
            users[user] = {"info":0, "error":0}
        user_stats = users[user]
        if is_error(this_line):
            user_stats["error"] += 1
        elif is_info(this_line):
            user_stats["info"] += 1
        users[user] = user_stats
    return sorted(users.items())

file = "syslog.log"
users = get_user_report(file)
errors = get_errors_report(file)

users_header = ["Username", "INFO", "ERROR"]
with open("user_statistics.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(users_header)

for user in users:
    user_name = user[0]
    user_stats = user[1]
    row = [user_name, user_stats["info"], user_stats["error"]]
    with open("user_statistics.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow(row)

errors_header = ["Error", "Count"]
with open("error_message.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(errors_header)

for error in errors:
    error_type = error[0]
    error_count = error[1]
    row = [error_type, error_count]
    with open("error_message.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow(row)
