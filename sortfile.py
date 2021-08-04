import os
import shutil

cur = os.getcwd()
print(cur)

#Move biggest size mp3 file from directory to root directory 
def move():
    for root, dirs, files in os.walk(cur):
        files = list(filter(lambda x: os.path.splitext(x)[1] == '.mp3', files))
        if len(dirs) == 0 and len(files) != 0:
            size         = 0
            target_abs   = ""
            target_base  = ""
            root_base    = os.path.basename(root)

            for f in files:
                f_abs = os.path.join(root, f) # absolute file path
                s = os.stat(f_abs).st_size
                if  s >= size:
                    size = s
                    target_abs  = f_abs
                    target_base = f

            print("moving file %50s to root, size is %d" % (target_base, size))
            shutil.copy(target_abs, cur)
            os.rename(os.path.join(cur, target_base), os.path.join(cur, root_base + ".mp3"))

move()