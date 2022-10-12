<?php
#by AhmetSacan

#Add your computer-specific folders here:
$CUSTOMDATADIRS = ['/Users/hayerk/Dropbox/database/', 'C:/Users/rawan/Dropbox/database/', 'C:/Users/James/Dropbox/database/', 'db.sqlite'];
$CUSTOMDBFILES = ['/Users/hayerk/Dropbox/database/db.sqlite', 'C:/Users/rawan/Dropbox/database/db.sqlite', 'C:/Users/James/Dropbox/database/db.sqlite' ];
$CUSTOMPYEXES = ['/Users/hayerk/anaconda3/envs/bmes/bin/python', 'C:/Users/rawan/Anaconda3/python.exe', 'C:/Users/James/Documents/Anaconda3/python.exe' ];


require_once __DIR__.'/bmes.php';
bmes::trycustomdatadirs( $CUSTOMDATADIRS );
bmes::trycustompyexes( $CUSTOMPYEXES );
bmes::trycustomdbfiles( $CUSTOMDBFILES );

#echo bmes::datadir();
#echo bmes::pyexe();
#echo bmes::dbfile();
