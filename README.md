# Raspberry Pi IP Reporter
Report the IP of your Raspberry Pi(or boards like Jetson Nano) with emails when it boots, and update the IP if it changes.  

## Setup static IP on Pi
1. Check your home network settings.

    Run `ifconfig`, and look for the section under `wlan0` to figure out your network settings. Most home Wifi routers support networks of 255 available devices in one of the three private IPv4 ranges,
    1. Class A: 10.0.0.0–10.255.255.255
    2. Class B: 172.16.0.0–172.31.255.255
    3. Class C: 192.168.0.0–192.168.255.255

    For example, if you found 
    
    `inet 10.0.0.250  netmask 255.255.255.0  broadcast 10.0.0.255` 
    
    under `wlan0`, it means the current device IP is `10.0.0.250` and the home network is on Class A range, and your network has 255 available IP(most likely), from `10.0.0.1 to 10.0.0.255`.
2. Set up static IP by editting `/etc/dhcpcd.conf`:
    ```
    interface wlan0
    static ip_address=10.0.0.250/24    
    static routers=10.0.0.1            # Your router IP
    static domain_name_servers=10.0.0.1 8.8.8.8  # Router DNS + Google DNS
    ```
    1. `10.0.0.250` is the local ip you picked for you pi. the last number should in [2, 254]. 
    2. `/24` is length of subnet mask for you network and decided by `netmask 255.255.255.0`. 
    3. `10.0.0.1` is your local router's IP, and `10.0.0.255` is reserved for local network broadcast.
    4. `8.8.8.8` is the second DNS address(google's DNS)
3. Reboot and check,
    ```
    ifconfig wlan0      # check new IP
    ping 8.8.8.8        # Test Connection
    ping google.com     # Test DNS
    ```

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
