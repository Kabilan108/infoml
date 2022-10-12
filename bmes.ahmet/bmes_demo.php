<?php
#by AhmetSacan
#See README.txt for installation instructions.

(@include_once getenv('BMESAHMETDIR').'/bmes.php') or die('<b>ERROR while running '.basename(__DIR__).'/'.basename(__FILE__).'</b>: Failed to load bmes.php, make sure you have a copy of bmes.php and have set the BMESAHMETDIR environment variable.');


echo "datadir: ". bmes::datadir()."<br>\n";
echo "dbfile: ". bmes::dbfile()."<br>\n";
echo "pythonexe: ".bmes::pyexe()."<br>\n";
echo "matlabexe: ".bmes::matlabexe()."<br>\n";

$db = bmes::db();
