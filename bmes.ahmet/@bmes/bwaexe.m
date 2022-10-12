function [out]=bwaexe(varargin)
% Copyright (C) 2020 by Ahmet Sacan

DATADIR=bmes.datadir;
out = [DATADIR '/bwa.exe'];


%%
if bmes.sys_issacan
	out = apt_getinapp('bwa','bwa*.exe');
end


%% Download bwa if not already there
if ~bmes.isfileandnotempty(out)
	if ispc
		zipfile=bmes.downloadurl('http://sacan.biomed.drexel.edu/ftp/prg/bwa.cyg.w64.zip',[DATADIR '/bwa.cyg.w64.zip']);
		fs=unzip(zipfile,DATADIR);
		movefile([DATADIR '/bwa.cyg.w64.exe'], out);
	elseif ismac
		out=bmes.downloadurl('http://sacan.biomed.drexel.edu/ftp/prg/bwa.maci64.exe',out);
		system(['chmod ugo+rwx "' out '"']);
	else
		error(sprintf('BWA not available on your (linux/unix) system. You can download bwa from:\nhttps://sourceforge.net/projects/bio-bwa/files/bwa-0.7.17.tar.bz2/download\nAfter you "make" bwa, move it to:\n%s',out));
	end
end

