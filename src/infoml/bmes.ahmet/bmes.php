<?php
#by AhmetSacan

umask(000); #allow files created by php usable by other users.

#by Ahmet Sacan
class bmes {
	static $PROJECTNAME=null; #if given, we use it when naming datadir.
	static $CUSTOMDATADIR=null; #set this if you need a custom datadir. use datadir() whenever you need to get datadir().
	static $CUSTOMDBFILE=null; #dbfile() will return a default file, if you are not happy with that, set this variable.
	static $db=null; #we'll store the database connection here.
	static $CUSTOMPYEXE=null; #pyexe() returns the path to python interpreter. set this to force a specific path. Can be an array if you want to provide multiple options. The first found file will be used. You can alternatively use BMESAHMET_PYEXE environment variable to set the location of python.exe on your computer.
	static $CUSTOMMATLABEXE=null; #Use this static variable to set a custom matlab.exe location. You can alternatively use BMESAHMET_MATLABEXE environment variable to set the location of python.exe on your computer.
	
	static function ispc(){
		static $ret;
		if(!isset($ret)) $ret= strtoupper(substr(PHP_OS, 0, 3)) === 'WIN';
		return $ret;
	}	
	static function username(){
		return getenv('USERNAME') ?: getenv('USER');
	}
	static function tempdir(){
		static $ret;
		if(!isset($ret)){
			$ret=sys_get_temp_dir().'/bmes';
			if(!is_dir($ret)) mkdir($ret,0777);
		}
		return $ret;
	}
	#returns $DATADIR if it is avalable. otherwise, returns a default datadir folder.
	static function datadir(){
		if(static::$CUSTOMDATADIR) return static::$CUSTOMDATADIR;
		static $ret;
		if(!isset($ret)){
			if(static::ispc()){
				if(is_dir($try='d:/data/temp')) $ret="$try/bmes/";
				else $ret="C:/bmes";
				if(!is_dir($ret)) mkdir($ret,0777);
			}
			else $ret=static::tempdir();
			if(static::$PROJECTNAME) $subdir=static::$PROJECTNAME;
			else $subdir=basename(dirname(__DIR__)).'_'.basename(__DIR__);
			$ret="$ret/$subdir";
			if(!is_dir($ret)) mkdir($ret,0777);
		}
		return $ret;
	}
	static function trycustomdatadirs($dirs){
		#only call trycustomdatadirs if bmes::$DATADIR is not set elsewhere.
		if(!bmes::$CUSTOMDATADIR){
			foreach($dirs as $x){
				if(is_dir($x)){ bmes::$CUSTOMDATADIR=$x; break; }
			}
		}		
	}
	
#return list of all user directories on this computer.
#if $firstsubdirorfile is given, we return the first such path found within a user folder.
# e.g., bmes::userdirs('Dropbox/bmes.ahmet');
static function userdirs($firstsubdirorfile=null){
	$ret=[];
	foreach(['/Users','C:/Users','/home'] as $usertopdir){
		if(is_dir($usertopdir)){
			$users = scandir($usertopdir);
			foreach($users as $user){
				if(strpos($user,'.')!==0){
					$userdir="$usertopdir/$user";
					$ret[]=$userdir;
					if(isset($firstsubdirorfile)&&(is_dir($trypath="$userdir/$firstsubdirorfile")||is_file($trypath))){
						return $trypath;
					}
				}
			}
		}
	}	
	return isset($firstsubdirorfile)?false:$ret;
}


static function addtosyspath($dir){
	$path=getenv('PATH');
	if(!preg_match('#'.preg_quote(PATH_SEPARATOR.$dir.PATH_SEPARATOR,'#').'#'.(static::ispc()?'i':''),PATH_SEPARATOR.$path.PATH_SEPARATOR)){
		#echo "Setting(".'PATH='.$path.PATH_SEPARATOR.$dir."...<br>\n";
		putenv('PATH='.$path.PATH_SEPARATOR.$dir);
		if(function_exists('apache_setenv'))	apache_setenv('PATH',$path.PATH_SEPARATOR.$dir);
		#echo "PATH is now ".getenv('PATH')."...<br>\n";
	}
}	
	static function firstfileinlist($list){
		foreach($list as $x){
			if(is_file($x)) return $x;
		}
		return false;
	}
	static function pyexe(){
		if(static::$CUSTOMPYEXE&&is_array(static::$CUSTOMPYEXE)) static::$CUSTOMPYEXE=static::firstfileinlist(static::$CUSTOMPYEXE);
		static $ret;
		if(isset($ret)) return $ret;
                if(($try=getenv('BMESAHMET_PYEXE'))&&is_file($try)){ $ret=$try; }
		if(!isset($ret)&&static::ispc()){
	    if(is_file($try='C:/ProgramData/Anaconda3/python.exe')) $ret=$try;
			elseif($try=bmes::userdirs('/Anaconda3/python.exe')) $ret=$try;
		}
		if(!isset($ret)){
			if(static::ispc()) $tryfile=shell_exec('where python');
			else $tryfile=shell_exec('which python');
			if($tryfile) $ret=trim($tryfile);
		}
		if(!isset($ret)&&static::ispc()){
			foreach(scandir('C:/Program Files/') as $prog){
				if(preg_match('#^python[\s\d\.]*#i',$prog)&&is_file($tryfile="C:/Program Files/$prog/python.exe")){
					$ret=$tryfile;
					break;
				}
			}
		}

		if(isset($ret)&&static::ispc()&&strpos(strtolower($ret),'anaconda')!==false){
			$retdir=dirname($ret);
			#otherwise, load module numpy or sqlite3 doesn't work, because it can't find some dlls
			foreach(['','/Library/mingw-w64/bin','/Library/usr/bin','/Library/bin','/Scripts','DLLs'] as $subdir){
				static::addtosyspath($retdir.'/'.$subdir);
			}
			#echo "<br>".getenv('PATH')."</b><br>\n";
		}
		if(!isset($ret)) $ret='python'; #%this is our fallback command if we don't find a specific location.
		return $ret;
	}
	static function matlabexe(){
		if(static::$CUSTOMMATLABEXE&&is_array(static::$CUSTOMMATLABEXE)) static::$CUSTOMMATLABEXE=static::firstfileinlist(static::$CUSTOMMATLABEXE);
		if(static::$CUSTOMMATLABEXE) return static::$CUSTOMMATLABEXE;
		static $ret;
                if(($try=getenv('BMESAHMET_MATLABEXE'))&&is_file($try)){ $ret=$try; }
		if(isset($ret)) return $ret;
		if(static::ispc()){
			foreach(scandir('C:/Program Files/MATLAB') as $ver){
				if(strpos($ver,'.')!==0 && is_file($tryfile="C:/Program Files/MATLAB/$ver/bin/matlab.exe")){
					$ret=$tryfile;
					break;
				}
			}
		}
		if(!isset($ret)){
			if(static::ispc()) $tryfile=shell_exec('where matlab');
			else $tryfile=shell_exec('which matlab');
			if($tryfile) $ret=trim($tryfile);
		}

		if(!isset($ret)) $ret='matlab'; #%this is our fallback command if we don't find a specific location.
		return $ret;
	}
	
	
	static function dbfile(){
		if(static::$CUSTOMDBFILE) return static::$CUSTOMDBFILE;
		#return static::datadir().'/db.sqlite';
		return __DIR__.'/db.sqlite';
	}
	static function trycustomdbfiles($files){
		if(!bmes::$CUSTOMDBFILE){
			foreach($files as $x){
				if(is_file($x)){ bmes::$CUSTOMDBFILE=$x; break; }
			}
		}		
	}
	static function db(){
		if(!isset(static::$db)){
			#create database connection
			#echo bmes::$CUSTOMDBFILE;
			#echo static::dbfile();
			$db=new PDO("sqlite:".static::dbfile());
			$db->setAttribute(PDO::ATTR_ERRMODE,PDO::ERRMODE_EXCEPTION);
		}
		return $db;
	}
	static function isdbtable($db,$tablename){
		return $db->query("SELECT name FROM sqlite_master WHERE type='table' AND name='$tablename'")->fetch();	
	}
	

	static function sanitizefilename($file){
		$file = mb_ereg_replace("([^\w\s\d\-_~,;\[\]\(\).])", '', $file);
		// Remove any runs of periods (thanks falstro!)
		$file = mb_ereg_replace("([\.]{2,})", '', $file);
		if($file==='') $file='noname';
		return $file;
	}
	
};


#echo 'datadir: '.bmes::datadir()."\n";
#echo 'pyexe: '.bmes::pyexe()."\n";
