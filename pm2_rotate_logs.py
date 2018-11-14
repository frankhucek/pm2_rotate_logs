import os
import shutil
import time
import sys
from subprocess import call

user_home_dir = os.path.expanduser("~")
log_file_location = user_home_dir + "/logs"


def pm2_rotate_logs(process_name):
    try:
        print("rotating log files")

        pm2_log_dir = user_home_dir+"/.pm2/logs"
        new_log_dir = log_file_location+"/pm2"
        if not os.path.exists(new_log_dir):
            os.makedirs(new_log_dir)

        filelist = os.listdir(pm2_log_dir)
        process_name_files = list(filter(lambda logfile: process_name in logfile, filelist))

        timezone, _ = time.tzname
        curr_time = time.strftime("%m-%d-%Y_%H:%M:%S")

        for file in process_name_files:
            new_file_name = file.split(".")[0] + curr_time + timezone + ".txt"
            copy_file(user_home_dir+"/.pm2/logs/"+file, new_log_dir+"/"+new_file_name)
        call(("pm2 flush " + process_name), shell=True)
    except Exception as ex:
        print("Error occurred: " + ex)


def copy_file(src, dest):
    try:
        shutil.copyfile(src,dest)
    except Exception as ex:
        print("Error occurred while copying files: " + ex)


def main():
    process_name = sys.argv[1]
    pm2_rotate_logs(process_name)


if __name__ == "__main__":
    main()
