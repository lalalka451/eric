import subprocess
import time
import os

# Change to the correct working directory
os.chdir('/root/l2tg')

# List of processes to monitor with their commands
PROCESSES = [
    ("reddit_scraper_arm64.py", "nohup python reddit_scraper_arm64.py > reddit.py.log 2>&1 &"),
    ("javbus_scraoer.py", "nohup python javbus_scraoer.py > jav.log 2>&1 &"),
    ("lihkg_gif.py", "nohup python lihkg_gif.py > lihkg_gif.log 2>&1 &"),
    ("twitter.py", "nohup python twitter.py > twitter.log 2>&1 &"),
    ("auto_forward.py", "nohup python auto_forward.py > auto_forward.log 2>&1 &"),
    ("get_twitter_user_chinese_without_account.py", "nohup python get_twitter_user_chinese_without_account.py > get_twitter_user_chinese_without_account.log 2>&1 &"),
    ("twitter_all2.py", "nohup python twitter_all2.py > twitter_all2.log 2>&1 &"),
    ("get_twitter_user.py", "nohup python get_twitter_user.py > get_twitter_user.log 2>&1 &"),
    ("zodgame.py", "nohup python zodgame.py > zodgame.log 2>&1 &")
]


def check_process_running(process_name):
    try:
        output = subprocess.check_output(["ps", "aux"])
        return process_name.encode() in output
    except:
        return False

def restart_process(command):
    subprocess.Popen(command, shell=True)

def monitor_processes():
    while True:
        print("\nChecking processes...")
        for process_name, command in PROCESSES:
            if not check_process_running(process_name):
                print(f"{process_name} is not running. Restarting...")
                restart_process(command)
            else:
                print(f"{process_name} is running.")
        time.sleep(300)  # Check every 5 minutes

if __name__ == "__main__":
    monitor_processes()