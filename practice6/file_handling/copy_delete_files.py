import shutil
import os

shutil.copy("choco.txt", "copy_choco.txt")
shutil.copy("choco.txt", "backup_choco.txt")

os.remove("copy_choco.txt")
os.remove("backup_choco.txt")