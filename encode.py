import subprocess
import sys
import re
import os
import time
import colorama
from colorama import Fore

colorama.init()
 
command = "HandBrakeCLI -O --encoder x264  -b 60 -r 5 -i \"%s\" -o \"%s\""

abs_curdir = os.path.abspath(os.curdir)
abs_upper, abs_folder = os.path.split(abs_curdir)

abs_des_root = ""

SUPPORT = ('mp4', "mov")    #Only support these file type.
REST    = 200               #How many time should rest after one job.
DELETE  = False             #Delete the file when finish

def get_percent(io):
    io = open(io, "r",errors = "ignore")
    r = re.findall("\nEncoding.*, (\d+.\d+)[\s]*%.*$",io.read())
    if len(r) != 0:
        print("%s %%" % r[0], end="\r")

class prog():
    def __init__(self):
        self.finish = 0
        self.remain = 0

PROGRESS = prog()

def calculate_files():
    num = 0
    for root, dir, files in os.walk(os.curdir):
        for f in files:  
            ps = f.split('.') #prefix, suffix
            if len(ps) >= 2 and ps[len(ps) - 1].lower() in SUPPORT:
                num += 1
    return num

if abs_upper == abs_curdir:
    print("Put the script into folder, not root")
    input("")
    sys.exit(1)

# main folder
try:
    abs_des_root = os.path.join(abs_upper, abs_folder + "_finished")
    print("Creating root %s " % abs_des_root)
    os.mkdir(abs_des_root)
except FileExistsError:
    print("Folder exist, do the job now...\n")

# process every single files/folder
for root, dir, files in os.walk(os.curdir):
    root = os.path.abspath(root)
    root = root[len(abs_curdir) + 1:] # +1 happend to jump '\ 

    abs_des_folder = os.path.join(abs_des_root, root)
    print((Fore.YELLOW + "\nCreating folder % s....." + Fore.RESET) % abs_des_folder, end="")

    try:
        os.mkdir(abs_des_folder)
        print("")
    except FileExistsError:
        print((Fore.GREEN + "%s exist" + Fore.RESET) % root)

    for f in files:  
        ps = f.split('.') #prefix, suffix
        if len(ps) >= 2 and ps[len(ps) - 1].lower() not in SUPPORT:
            print("skip file %s" % f)
            continue

        src_file = os.path.join(root, f)
        abs_des_file = os.path.join(abs_des_folder, f)
        abs_des_tmp  = os.path.join(abs_des_folder, "TMP")

        if os.path.exists(abs_des_file):
            print("%s Already finished" % f)
            PROGRESS.finish += 1
            continue

        c = command % (src_file, abs_des_tmp)
        print("handling file %s....\ncommand:%s\n" % (f, c))
        out = open("log.txt","w")
        p = subprocess.Popen(c, stdout = out, stderr = out)

        print("Delete Mode: %s" % DELETE)
        PROGRESS.remain = calculate_files()
        print("Remain %d finished %d" % (PROGRESS.remain, PROGRESS.finish))

        while True:
            #if process exit
            if p.poll() != None:
                # if no erro
                if p.poll() == 0:
                    print("100.00%\n")
                    os.rename(abs_des_tmp, abs_des_file)
                    if DELETE : os.remove(src_file)
                    break
                else:
                    input("error at %s" % f)
                    sys.exit(1)

            time.sleep(1)
            get_percent("log.txt")

        # Take a break, in case of CPU usage too high...
        # I just don't want my computer fan run too fast...
        print("Rest %d seconds...." % REST)

        exp_time = time.time() + REST
        while time.time() < exp_time:
            time.sleep(1)
            print("Resting, remain time %d \r" % (exp_time - time.time()), end="")

        PROGRESS.finish += 1

        print("")

input("All finish\n")
sys.exit(0)


