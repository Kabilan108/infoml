import bmes
import os
import sys

if __name__ != "__main__" or len(sys.argv) < 2:
    sys.exit("You need to run this script directly (not import it) and provide the name of the module you want to install.\nUsage: " +
             sys.argv[0]+" importname [packagename]")


importname = sys.argv[1]
if ',' in importname:
    if len(sys.argv) >= 3:
        sys.exit("When using csv of multiple packages, you need to use the format: importname1:packagename1,importname2:packagename2,importname3,...  (package name is optional when it is the same as importname).")
    importnames = importname.split(',')
    packagenames = importnames
    for i in range(len(importnames)):
        if ':' in importnames[i]:
            importnames[i], packagenames[i] = importnames[i].split(':', 1)
else:
    importnames = [importname]
    packagenames = importnames
    if len(sys.argv) >= 3:
        packagenames = [sys.argv[2]]

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
for i in range(len(importnames)):
    print('installing '+importnames[i]+' ...')
    #import sys,os; sys.path.append(os.environ['BMESAHMETDIR']); import bmes
    bmes.pipinstall(importnames[i], packagenames[i])
