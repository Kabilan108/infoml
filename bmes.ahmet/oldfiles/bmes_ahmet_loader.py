# 20191214: This loader is obsolete. The recommended method is to use environment variables.
# On Windows do:
#  setx /M BMESAHMETDIR C:/Path/To/bmes.ahmet
# On Mac do:
#  launchctl setenv BMESAHMETDIR /path/to/bmes.ahmet
#  sudo echo "setenv BMESAHMETDIR /path/to/bmes.ahmet" >> /etc/launchd.conf
# Then, in your python code, just do:
# import sys,os; sys.path.append(os.environ['BMESAHMETDIR']); import bmes

# You may make a copy of this file and place it in your working directory to help automate find & load bmes.ahmet folder.
# The recommended way of including bmes_ahmet is to keep it in your dropbox folder and
# set up BMESAHMETDIR environment variable to point to that folder. If BMESAHMETDIR environment
# variable is not available, this set up code will try user dropbox folders for a subfolder called
# bmes.ahmet
# This file adjusts the python path so you can include Ahmet's shared dropbox folder.
# by Ahmet Sacan.


import sys

if 'bmes' not in sys.modules:
    print('setting up python path for bmes.ahmet...')
    # import ahmet's bmes module that contains useful functions for downloading files from web.
    import os
    if 'BMESAHMETDIR' in os.environ:
        # this is only for ahmet's computer.
        sys.path.append(os.environ['BMESAHMETDIR'])
    else:
        # this is only for ahmet's computer.
        sys.path.append('D:/ahmet/doc/Dropbox/share/bmes.ahmet')
        # if bmes.ahmet is not in your PYTHONPATH and none of the following can locate where you have your bmes.ahmet folder,
        #  you will need to hard-code it.
        sys.path.append('../bmes.ahmet')
        sys.path.append('../../bmes.ahmet')
        try:
            import pathlib
            sys.path.append(str(pathlib.Path.home())+'/Dropbox/bmes.ahmet')
        except:  # pathlib module may not be installed by default if we are using python2
            sys.path.append(os.path.expanduser('~')+'/Dropbox/bmes.ahmet')
    import bmes
