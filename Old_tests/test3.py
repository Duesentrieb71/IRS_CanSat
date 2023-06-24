import os
import sys


# create folder named "data"

os.mkdir("data")

# check if folder exists

if os.path.exists("data"):
    print("data folder exists")
else:
    print("data folder does not exist")
