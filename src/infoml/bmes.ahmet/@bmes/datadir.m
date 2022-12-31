function [out]=datadir()
% Copyright (C) 2019 by Ahmet Sacan

out=bmes.CUSTOMDATADIR; if ~isempty(out); return; end

persistent ret;
if isempty(ret)
	if ispc
		if bmes.isfolder('d:/data/temp'); ret2='d:/data/temp/bmes';
		else ret2='c:/bmes'; end
		if ~bmes.isfolder(ret2); mkdir(ret2); end
	else
		ret2=bmes.tempdir;
	end
	
	ret=ret2;
end
out=ret;

