import datetime
import subprocess
import socket
import os
import json
import sys

def send_email(sender, receiver, message, temp_file):
    with open(temp_file, 'w') as f:
        f.write("To: {}\n".format(receiver))
        f.write("From: {}\n".format(sender))
        f.write(message)
    subprocess.call('/bin/cat {} |  /usr/bin/msmtp {}'.
                    format(temp_file, receiver), shell=True)

if __name__ == "__main__":
    cur_path = os.path.dirname(os.path.realpath(__file__))
   
    is_check = False
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        is_check = True

    with open(os.path.join(cur_path, "email_info.json")) as f:
        email_info = json.load(f)
    sender = email_info["send_email"]
    receiver = email_info["receive_email"]
    device_name = email_info["device_name"]
    ip_record_file = email_info["log_file_name"]

    # --- get ip and time
    # --- tutorial: https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    cur_ip = s.getsockname()[0]
    s.close()
    cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    temp_file = os.path.join(cur_path, ip_record_file)
    
    if not is_check:
        print("Boots on {} with ip {}".format(cur_time, cur_ip))
        message = "Subject: {} boots on {}\n\n{}\n".format(device_name, cur_time, cur_ip)
        send_email(sender, receiver, message, temp_file)
    else:
        with open(os.path.join(cur_path, ip_record_file), 'r') as f: 
            ip_info = f.readlines()
            old_ip = ip_info[-1][:-1]
        if old_ip != cur_ip:
            print("IP changed on {} to {}".format(cur_time, cur_ip))
            message = "Subject: {} IP changed on {}\n\n{}\n".format(device_name, cur_time, cur_ip)
            send_email(sender, receiver, message, temp_file)
