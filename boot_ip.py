import datetime
import subprocess
import os

send_email = 'mail1@gmail.com'
receive_email = 'mail2@gmail.com'
ip_record_file = 'ip_info.txt'

# get folder path
cur_path = os.path.dirname(os.path.realpath(__file__))

# get ip and time
ip_info = str(subprocess.check_output('ifconfig wlan0', shell=True))
ip_idx = ip_info.find('inet addr')
ip_info = ip_info[ip_idx:].split('  ')[0]
cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# write the email
with open(os.path.join(cur_path, ip_record_file), 'w') as f:
    f.write("To: {}\n".format(receive_email))
    f.write("From: {}\n".format(send_email))
    f.write("Subject: Pi boots on {}\n\n".format(cur_time))
    f.write('{}\n'.format(ip_info))
f.close()

# send the email
subprocess.call('/bin/cat {} |  /usr/bin/msmtp {}'.
                format(os.path.join(cur_path, ip_record_file), receive_email), shell=True)
