import datetime
import subprocess
import socket
import os
import json


# --- get folder path
cur_path = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(cur_path, "email_info.json")) as f:
    email_info = json.load(f)

# ---- REMEMBER TO CHANGE THE SEND_EMAIL AND RECEIVE_EMAIL TO YOUR CASE!
send_email = email_info["send_email"]
receive_email = email_info["receive_email"]
device_name = email_info["device_name"]
ip_record_file = email_info["log_file_name"]

# --- get ip and time
# - get all the ip info with ifconfig
# ip_info = str(subprocess.check_output('ifconfig wlan0', shell=True))
# - a python solution: https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_info = s.getsockname()[0]
s.close()

cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print("Boots on {} with ip {}".format(cur_time, ip_info))

# --- write the email
with open(os.path.join(cur_path, ip_record_file), 'w') as f:
    f.write("To: {}\n".format(receive_email))
    f.write("From: {}\n".format(send_email))
    f.write("Subject: {} boots on {}\n\n".format(device_name, cur_time))
    f.write('{}\n'.format(ip_info))
f.close()

# --- send the email
subprocess.call('/bin/cat {} |  /usr/bin/msmtp {}'.
                format(os.path.join(cur_path, ip_record_file), receive_email), shell=True)
