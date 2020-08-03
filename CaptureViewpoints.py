# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 12:29:27 2019
CaptureViewpoints when executed  gets the date of the newest file in the windows assets folder
It then takes all files with that date and copies them to the Viewpoints folder while adding the ending .jpg
There it checks the imagesize of the newly added files and moves phone pictures to the phone folder
@author: Malte Gergeleit
"""

import glob
import os
import time
import shutil
import re
import PIL

## Folders
Assets = r'C:\Users\malte\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets'
Viewpoints = r'C:\Users\malte\Desktop\Wallpaper\Viewpoints'
Phone = r'C:\Users\malte\Desktop\Wallpaper\Viewpoints\Phone'

## Get the date of the file that was last added to the assets folder
files = list(filter(os.path.isfile, glob.glob(Assets + "\*")))
files.sort(key=lambda x: os.path.getmtime(x),reverse=True)
NewestDate = time.localtime(os.path.getmtime(files[0]))

## move files to new folder 1 by 1


for i  in range(len(files)):
    # get creation date of file (day precision)
    FileDate = time.localtime(os.path.getmtime(files[i]))
    # Check against NewestDate
    if NewestDate[0]-FileDate[0] == 0  and NewestDate[1]-FileDate[1] == 0 and NewestDate[2]-FileDate[2] == 0:
        # copy and rename file
        shutil.copy(files[i],Viewpoints)
        oldName = Viewpoints +'\\' + re.split('\\\\' , files[i])[-1]
        newName = Viewpoints +'\\' + str(FileDate[0])+'_'+str(FileDate[1])+'_'+str(FileDate[2])+'_'+str(i) + '.jpg'
        try:
            os.rename(oldName,newName)
        except FileExistsError:
              print("File already exists in 'Viewpoints'")
              os.remove(oldName)                                            
        # Check width against height
        im = PIL.Image.open(newName)
        width, height = im.size
        del im 
        if height > width:
            try:
                shutil.move(newName,Phone)
            except OSError:
                print("File already exists in 'Phone'")
                os.remove(newName)

print("Done")