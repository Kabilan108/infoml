by AhmetSacan.

I may make further changes to this folder. Rather than copying this folder
elsewhere, keep using it in your Dropbox,  so that any changes I make would be
synchronized and you would make use of the most recent version. 

Below, you can find instructions for Python, php, and Matlab in separate sections.


===== Instructions for PYTHON and PHP: Setting BMESAHMETDIR environment variable

Create an environment variable called BMESAHMETDIR on your computer:
* On Windows, start a command line as Administrator, and run:
   setx /M BMESAHMETDIR C:/Path/To/bmes.ahmet
 
 You may need to restart your computer for this change to take effect.

* On Mac, open a terminal and run:
   launchctl setenv BMESAHMETDIR /path/to/bmes.ahmet
   sudo echo "setenv BMESAHMETDIR /path/to/bmes.ahmet" >> /etc/launchd.conf



===== Instructions for PYTHON:

After setting the BMESAHMETDIR environment variable as instructed above, in your python code, add the following code:

import sys,os; sys.path.append(os.environ['BMESAHMETDIR']); import bmes


If unsuccessful, Python will give you an error that bmes module cannot be found.
If loading is successful, you can try an example function from bmes module, e.g.:
  print(bmes.tempdir())



===== Instructions for PHP:

After setting the BMESAHMETDIR environment variable as instructed above, in your python code, add the following code:

(@include_once getenv('BMESAHMETDIR').'/bmes.php') or die('<b>ERROR while running '.basename(__DIR__).'/'.basename(__FILE__).'</b>: Failed to load bmes.php, make sure you have a copy of bmes.php and have set the BMESAHMETDIR environment variable.');

If unsuccessful, php will give you an error that the bmes.php file cannot be loaded. 
If loading is successful, you can further try an example function from bmes class, e.g.:
  echo bmes::tempdir();




===== Simple/Beginner Instructions for MATLAB:

Add this folder to your "Matlab Path". In your Matlab window, click under
the Home menu, the "Set Path" icon to  reach the list of folders that are
on your Matlab Path, and add bmes.ahmet to that list. Save & Close.

To test if you have successfully added bmes.ahmet to your Matlab, try the
following in your Matlab command window:

>> bmes.tempdir


If Matlab complains that 'Undefined variable "bmes" or class
"bmes.tempdir".' that means you did not add bmes.ahmet folder to your
Matlab path. If however you see a folder name printed, that means success.



===== Advanced/Alternative Instructions for MATLAB:

Follow the instructions above for "Instructions for PYTHON and PHP: Setting BMESAHMETDIR environment variable".
Run the following in the Command Line:

>> if isempty(getenv('BMESAHMETDIR')); error('Missing environment variable BMESAHMETDIR or it points to incorrect/missing folder');
>> elseif ~isfolder(getenv('BMESAHMETDIR')); error('BMESAHMETDIR environment variable points to incorrect/missing folder');
>> else addpath(getenv('BMESAHMETDIR')); end


To test if you have successfully added bmes.ahmet to your Matlab, try the
following in your Matlab command window:

>> bmes.tempdir


If Matlab complains that 'Undefined variable "bmes" or class
"bmes.tempdir".' that means you did not add bmes.ahmet folder to your
Matlab path. If however you see a folder name printed, that means success.



