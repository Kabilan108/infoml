<?
# 20191214: This loader is obsolete. The recommended method is to use environment variables.
# On Windows do:
#  setx /M BMESAHMETDIR C:/Path/To/bmes.ahmet
# On Mac do:
#  launchctl setenv BMESAHMETDIR /path/to/bmes.ahmet
#  sudo echo "setenv BMESAHMETDIR /path/to/bmes.ahmet" >> /etc/launchd.conf
# Then, in your php code, just do:
# require_once getenv('BMESAHMETDIR').'/bmes.php';

# You can make a copy of this file and place it in your working directory.
# This file finds and loads Ahmet's shared bmes class.
# by Ahmet Sacan.

#return list of all user directories on this computer.
#if $firstsubdirorfile is given, we return the first such path found within a user folder.
# e.g., bmes_userdirs('Dropbox/bmes.ahmet');
function bmes_userdirs($firstsubdirorfile=null){
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

function bmes_ahmet_loader(){
if(!class_exists('bmes',false)){
	$foundbmes=false;
	if($trydir=getenv('BMESAHMETDIR')){
		require_once "$trydir/bmes.php";
		$foundbmes=true;
	}
	if(!$foundbmes){
		foreach(['D:/ahmet/doc/Dropbox/share/bmes.ahmet','../bmes.ahmet','../../bmes.ahmet'] as $trydir){
			if(is_dir($trydir)&&is_file("$trydir/bmes.php")){
				#echo "Loading $trydir/bmes.php ...<br>\n";
				require_once "$trydir/bmes.php";
				$foundbmes=true;
				break;
			}
		}
	}
	if(!$foundbmes){
		if($tryfile=bmes_userdirs('Dropbox/bmes.ahmet/bmes.php')){
			#echo "Loading $tryfile ...<br>\n";
			require_once $tryfile;
			$foundbmes=true;
		}
	}
}
if(!$foundbmes){
	trigger_error("ERROR: bmes.ahmet could not be located within the expected Dropbox location.<br>You can set BMESAHMET environment variable to where you keep bmes.ahmet folder.\n");
	die();
}
}

bmes_ahmet_loader();
