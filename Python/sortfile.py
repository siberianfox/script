import os
import shutil

cur = os.getcwd()
print(cur)

#Move biggest size mp3 file from directory to root directory 
def move():
    for root, dirs, files in os.walk(cur):
        
        #Only folder that just contain file
        if len(dirs) != 0 or len(files) == 0:
            continue
        
        mp3 = list(filter(lambda x: os.path.splitext(x)[1] == '.mp3', files))
        
        root_base    = os.path.basename(root)
        
        size      = 0
        mp3_abs   = ""
        mp3_base  = ""

        for f in mp3:
            f_abs = os.path.join(root, f) # absolute file path
            if  "pb" in f:
                mp3_abs  = f_abs
                mp3_base = f
                size = os.stat(f_abs).st_size
                break

        print("moving file %50s to root, size is %d" % (mp3_base, size))
        shutil.copy(mp3_abs, cur)
        os.rename(os.path.join(cur, mp3_base), os.path.join(cur, root_base + ".mp3"))


        
move()