import os
import pandas as pd
import numpy as np
count  = 0
for root, dirs, files in os.walk("Apple"):
        count+= len(files)
        if len(files) == 0:
            continue
        print("Folders inside" ,root , count)
        

 