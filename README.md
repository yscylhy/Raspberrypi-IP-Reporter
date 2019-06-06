# Raspberry Pi IP Reporter
Report the IP of your Raspberry Pi(or boards like Jetson Nano) with emails when it boots, and update the IP if it changes.  

## Prerequirst 
You will need an email account to send the ip info from your pi. It is suggested to register a new email for this purpose. Of course, WiFi is also required.

## Steps
1. [Connect your pi to wifi](https://raspberrypihq.com/how-to-connect-your-raspberry-pi-to-wifi/).
2. Install [msmtp](https://hostpresto.com/community/tutorials/how-to-send-email-from-the-command-line-with-msmtp-and-mutt/) to send emails from the Pi. My configuration file for a gmail account is in `msmtprc`.
3. Send the IP of your Pi. Remember to change emails in `boot_ip.py` for your case.
4. Update the IP of your Pi if it changes. Remember to change emails in `check_ip.py` for your case.
5. Creat [crontab jobs](https://www.dexterindustries.com/howto/auto-run-python-programs-on-the-raspberry-pi/) for IP report. Here are my settings for `sudo crontab -e`:  
    1. Ready for ssh connection: `@reboot sudo systemctl restart ssh`
    2. Report ip when it boots: `@reboot sleep 5 && sudo python3 your_path/boot_ip.py`
    3. Check ip every 10 minutes: `*/10 * * * * sudo python3 your_path/check_ip.py`

## Tips
1. If you configured the WiFi on your Pi before, you may encounter some [other problems](https://raspberrypi.stackexchange.com/questions/67311/failed-to-connect-to-non-global-ctrl-ifname-when-running-wpa-cli-reconfigure).
2. If the python scripts under crontab jobs do not work, run them manually first. Make sure all the parameters (emails and paths) are configured correctly based your RaspberryPi.
3. Remember to [enable wifi](https://askubuntu.com/questions/1277/how-do-i-configure-wifi-to-log-in-to-wpa-at-boot-time-regardless-of-user-being) when booting. The Raspberry Pi does not have this issue, but the Jetson nano does.
4. Set a enough sleep time before running `boot_ip.py`. Jetson may take upto 60 seconds.
