# by Ahmet Sacan.
# See the README.txt file for instructions on making this file available in python.
# imports and Utility functions

import sys,os
from venv import create

class bmes:
    PROJECTNAME=None  #used for projdatadir()
    CUSTOMDATADIR=None  #datadir() will return a default datadir,if you are not happy with that, set this variable.
    CUSTOMDBFILE=None  #dbfile() will return a default file, if you are not happy with that, set this variable.
    CUSTOMTEMPDIR=None
    CUSTOMPATH=None
    db=None #we'll store the database connection here.

def ispc():
	if not hasattr(ispc, 'ret'):
		import platform
		sys=platform.system();
		ispc.ret = sys=='Windows' or sys.startswith('CYGWIN')
	return ispc.ret;

def computername():
	import socket
	return socket.gethostname()

def iscomputername(name):
	return computername().lower() == name.lower()

def iscomputernameprefix(name):
	return computername().lower().startswith(name.lower())

def mkdirif(dir):
	if not os.path.isdir(dir): os.mkdir(dir, 0o777 )

def isfile(file):
    return os.path.isfile(file)

def isfileandnotempty(file):
    return os.path.isfile(file) and os.stat(file).st_size != 0

def isfolder(file):
    return os.path.isdir(file)

def tempdir():
	if bmes.CUSTOMTEMPDIR: return bmes.CUSTOMTEMPDIR;
	import tempfile
	ret=tempfile.gettempdir().replace("\\","/")+'/bmes';
	mkdirif(ret);
	return ret;

def selfdir():
    return selfdir.ret
selfdir.ret = os.path.dirname(os.path.abspath(__file__))

# datadir() gets the default datadir.
# if you want to use your own datadir, set bmes.CUSTOMDATADIR='/my/own/dir'
def datadir():
	if bmes.CUSTOMDATADIR: return bmes.CUSTOMDATADIR;
	if not hasattr(datadir, 'ret'): datadir.ret='';
	ret=datadir.ret;
	if not ret:
		if ispc():
			if os.path.isdir('c:/data/temp'): ret='c:/data/temp/bmes';
			else: ret='C:/bmes';
			mkdirif(ret)
		else: ret=tempdir(); #TODO: change this to a non-temp folder
		if bmes.PROJECTNAME: subdir=bmes.PROJECTNAME
		else: subdir=os.path.basename(os.path.dirname(selfdir()))+'_'+os.path.basename(selfdir())
		ret=ret+'/'+subdir
		mkdirif(ret)
		datadir.ret=ret;
	return ret;

def trycustomdatadirs( dirs ):
    #only try customdatadirs if bmes::$CUSTOMDATADIR is not set elsewhere.
    if not bmes.CUSTOMDATADIR:
        for x in dirs:
            if os.path.isdir(x):
                bmes.CUSTOMDATADIR=x;
                break;


def dbfile():
    if bmes.CUSTOMDBFILE: return bmes.CUSTOMDBFILE
    return datadir()+'/db.sqlite';
    #return selfdir()+'/db.sqlite';

def trycustomdbfiles( dirs ):
    #only try customdatadirs if bmes::$CUSTOMDBFILE is not set elsewhere.
    if not bmes.CUSTOMDBFILE:
        for x in dirs:
            if os.path.isfile(x):
                bmes.CUSTOMDBFILE=x;
                break;

def binpath():
    if bmes.CUSTOMPATH: return bmes.CUSTOMPATH
    #return datadir()+'/db.sqlite';
    return selfdir()+'/bin/geckodriver';

def trycustompath( dirs ):
    #only try customdatadirs if bmes::$CUSTOMPATH is not set elsewhere.
    if not bmes.CUSTOMPATH:
        for x in dirs:
            if os.path.isfile(x):
                bmes.CUSTOMPATH=x;
                break;


def testdb():
    import sqlite3
    if not bmes.db:
        bmes.db=sqlite3.connect('test.sqlite');
    return bmes.db;

def gettempfile(filename=None):
    import tempfile
    if filename:
        return tempdir() + '/' + filename;
    else:
        tf = tempfile.NamedTemporaryFile()
        tf.close()
        return tf.name;

def sanitizefilename(file):
    #https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    file = ''.join(c for c in file if c in valid_chars)
    if not file: file='noname'
    return file


def downloadurl(url,file='',overwrite=False):
    #%if url is not a remote address, assume it is a local file.
    if not (url.startswith('http://') or url.startswith('https://') or url.startswith('ftp://')):
        if not file:
            file=url
            return file
        if not overwrite:
            import os
            if isfileandnotempty(file): return file;
            import shutil;
            shutil.copyfile(url,file);
            return file;

    if not file:
        file=tempdir() + '/' + sanitizefilename(url.split("?")[0].split("/")[-1])
    elif file.endswith('/'):
        file=file + '/' + sanitizefilename(url)

    
    if isfileandnotempty(file): return file;

    file=file.replace('\\','/').replace('//','/');

    if not ('/' in file):
        file=tempdir() + '/' + file
        if isfileandnotempty(file): return file;
        file=file.replace('\\','/').replace('//','/');



    import sys
    if (sys.version_info > (3, 0)):
        import urllib.request
        urllib.request.urlretrieve(url, file)
    else:
        import urllib
        urllib.urlretrieve(url,file)
    return file

def downloadfile(path):
    print('Obsolete function bmes.downloadfile(). Just use bmes.downloadurl() instead.')
    """If path is a URL, download it to a temp file and return the filename
    Otherwise, assume path is a filename and return as is.
    """
    return downloadurl(path)


#cur should be a database cursor that you already created.
#e.g.: isdbtable(cur, 'students')
def isdbtable(cur,tablename):
	if type(cur).__name__ == 'Connection': cur=cur.cursor()
	return len(cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='"+tablename+"'").fetchall())!=0


#if stderrfile is not given, we redirect to a temporary file and then print it.
def system_redirecttofile(cmd,stdoutfile=None,stderrfile=None):
    printstdout=False;
    printstderr=False;
    if stdoutfile:
        if not stderrfile:
            printstderr=True;
            stderrfile=gettempfile();
        cmd = cmd +  ' > "' + stdoutfile + '" 2>"' + stderrfile +'"';
    else:
        printstdout=True;
        stdoutfile=gettempfile();
        if stderrfile:
            cmd = cmd +  ' > "' + stdoutfile + '" 2>"' + stderrfile +'"';
        else:
            cmd = cmd +  ' > "' + stdoutfile + '" 2>&1';

    print('Executing command: ' + cmd)
    import os
    os.system(cmd)
    if printstdout:
        with open(stdoutfile,'r') as f: print(f.read())
        os.remove(stdoutfile);
    if printstderr:
        with open(stderrfile,'r') as f: print(f.read())
        os.remove(stderrfile);

#similar to matlab's system() call, with a few additional conveniences
def system(cmd,doprint=True):
    import subprocess
    if doprint: print("Executing command: " + cmd);
    try: out=subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e: out=e.output.decode()
    if doprint and out: print(out);
    return out;

def tryimportingpackage(importname):
    import importlib
    try: importlib.import_module(importname)
    except ImportError: return False
    return True
def ispackageinstalled(importname):
    return tryimportingpackage(importname)

# In most cases, importname and packagename are identical.
# Provide both when they are diferent.
# e.g., pipinstall('numpy')
# e.g., pipinstall('Bio', 'biopython')
#TODO: switch importname & packagename order like in pipuninstall
def pipinstall(importname,packagename=None,reinstall=False):
    if not packagename: packagename=importname;
    isinstalled=ispackageinstalled(importname)
    if reinstall and isinstalled:
        pipuninstall(packagename,False)
    if reinstall or not isinstalled:
        cmd=sys.executable + ' -m pip install -U ' + packagename;
        #!{sys.executable} -m pip install {packagename}
        #import os;
        #os.system(cmd)
        s=system(cmd)
        if 'ERROR: Could not install packages' in str(s) and 'Consider using the `--user` option' in str(s):
            cmd=sys.executable + ' -m pip install --user -U ' + packagename;
            system(cmd)
        if not tryimportingpackage(importname):
            print('FAILED to install ' + packagename);

#use importname=False to uninstall without checking if it is already installed.
def pipuninstall(packagename,importname=None):
    if importname is not False:
        if not importname: importname=packagename;
        isinstalled=ispackageinstalled(importname)
    if importname is False or isinstalled:
        print('Uninstalling ' + packagename + '...')
        system(sys.executable + ' -m pip uninstall -y ' + packagename)

#TODO: switch importname & packagename order like in pipuninstall
def condainstall(importname,packagename=None,reinstall=False,condaargs=[]):
    if not packagename: packagename=importname;
    if not reinstall: isinstalled=ispackageinstalled(importname)
    if reinstall or not isinstalled:
        try:
            print('Installing ' + packagename + ' ...');
            import conda.cli
            conda.cli.main('conda', 'install',  '-y', packagename,*condaargs)
        except ImportError:
            print('FAILED to install ' + packagename);
            print('Try installing the package with Anaconda Prompt. Try running the following:');
            print('conda update --all --yes')
        if not tryimportingpackage(importname):
            print('FAILED to install ' + packagename);

def unziptofolder(file,folder,createsubfolder=False):
    if createsubfolder:
        return
        from pathlib import Path
        folder = folder + '/' + Path(file).stem;
        mkdirif(folder)
    import zipfile;
    with zipfile.ZipFile(file,'r') as z: z.extractall(folder);


def bwaexe():
    DATADIR=datadir();
    out=DATADIR+'/bwa.exe';
    if not isfileandnotempty(out):
        if ispc:
            file=downloadurl('http://sacan.biomed.drexel.edu/ftp/prg/bwa.cyg.w64.zip',DATADIR+'/bwa.cyg.w64.zip');
            unziptofolder(file,DATADIR)
            import os
            os.rename(DATADIR + '/bwa.cyg.w64.exe', out);
        else:
            out=downloadurl('http://sacan.biomed.drexel.edu/ftp/prg/bwa.maci64.exe',out);
            system('/bin/chmod ugo+rwx "' + out + '"')
    return out;


def printsettings():
	print("computername: "+computername());
	#print "issacan: "+str(iscomputernameprefix('sacan'));
	print('datadir: '+datadir());
	print('tempdir: '+tempdir());
	print('dbfile: '+dbfile());

if __name__ == "__main__":
	printsettings()
	import os,pickle
	#print(os.environ)
	#pickle.dump(os.environ,open('python.env.pickle','wb'))
	#os.environ = pickle.load(open('python.env.pickle','rb'))
