function [file]=downloadurl(url,file,overwrite)
% download file if it is not already downloaded before.
% Copyright (C) 2019 by Ahmet Sacan
if ~exist('overwrite','var');
	if exist('file','var')&&(islogical(file)||isnumeric(file)); overwrite=file; clear('file');
	else overwrite=false; end
end

%if url is not a remote address, assume it is a local file.
if isempty(regexp(url,'^(https?://|ftps?://)','once'))
	if ~exist('file','var'); file=url; return; end
	if ~overwrite; finfo=dir(file); if ~isempty(finfo)&&finfo.bytes; return; end; end
	copyfile(url,file);
	return;
end


if ~exist('file','var')
	file=[bmes.userdownloaddir()  '/' bmes.sanitizefilename(url) ];
elseif ~isempty(regexp(file,'/$','once')) %||bmes.isfolder(file)
	file=[file  '/' bmes.sanitizefilename(url) ];
end

if ~overwrite; finfo=dir(file); if ~isempty(finfo)&&finfo.bytes; return; end; end

file=strrep(strrep(file,'\','/'), '//', '/');
if ~any(file=='/')
	file=[bmes.tempdir() '/' file];
	if ~overwrite; finfo=dir(file); if ~isempty(finfo)&&finfo.bytes; return; end; end
	file=strrep(strrep(file,'\','/'), '//', '/');
end

fprintf('--- NOTICE: Attempting to download & save url [ %s ] to file [ %s ] ...\n',url,file);
[filedir,filebase,fileext]=fileparts(file);
if isempty(filedir); tmpfile=['.download.' filebase fileext];
else tmpfile=[filedir '/.download.' filebase fileext]; end

if ~isempty(regexp(url,'^https?://','once')) %websave only works for web links. urlwrite also works for ftp links.
	file2=websave(tmpfile,url,weboptions('Timeout',Inf,'CertificateFilename','')); %websave may change filename and add extension of its own deciding.
else
	file2=urlwrite(url,tmpfile,'Timeout',inf);
end

file2=strrep(strrep(file2,'\','/'), '//' ,'/');
if ispc&&~strcmpi(file2,file)||~ispc&&~strcmp(file2,file);
	try
		movefile(file2,file);
	catch me
		if ~strcmp(me.identifier,'MATLAB:MOVEFILE:SourceAndDestinationSame')
			rethrow(me);
		end
	end
end

