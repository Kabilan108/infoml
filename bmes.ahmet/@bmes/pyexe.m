function [out]=pyexe(varargin)
% return location of python executable.
% search for common installation locations.
% If you want to use your own pyexe path, call bmes.pyexe('/your/own/path')
% once and future calls to bmes.pyexe() will return your custom path. If
% you want to skip the recommended path-setting done here, call
% bmes.CUSTOMPYEXE('/your/own/path') instead.
% Copyright (C) 2019 by Ahmet Sacan

persistent ret;
if ~isempty(ret)&&isempty(varargin); out=ret; return; end

ret = bmes.CUSTOMPYEXE(varargin{:});

if isempty(ret)&&ispc
	tryfile='c:/ProgramData/Anaconda3/python.exe';
	if bmes.isfile(tryfile); ret=tryfile;
	else
		tryfile=['c:/Users/' bmes.username '/Anaconda3/python.exe'];
		if bmes.isfile(tryfile); ret=tryfile; end
	end
end

if isempty(ret); ret=bmes.locateexe('python',false); end


if ispc&&~isempty(ret)&&~isempty(strfind(lower(ret),'anaconda'))
	%#otherwise, load module numpy or sqlite3 doesn't work, because it can't find some dlls
	retdir=fileparts(ret);
	bmes.addtosyspath([retdir]);
	bmes.addtosyspath([retdir '/Library/mingw-w64/bin']);
	bmes.addtosyspath([retdir '/Library/usr/bin']);
	bmes.addtosyspath([retdir '/Library/bin']);
	bmes.addtosyspath([retdir '/Scripts']);
	%the following don't seem to be needed.
	%bmes.addtosyspath([retdir '/Library']);
	%bmes.addtosyspath([retdir 'lib/site-packages/IPython/extensions']);
end

if isempty(ret); ret='python'; end %this is our fallback command if we don't find a specific location.

out=ret;

