function [out]=rscriptexe(varargin)
% return location of Rscript executable.
% search for common installation locations.
% If you want to use your own path, call bmes.rscriptexe('/your/own/path')
% once and future calls to bmes.rscriptexe() will return your custom path.
% Copyright (C) 2022 by Ahmet Sacan

persistent ret;
if ~isempty(ret)&&isempty(varargin); out=ret; return; end

ret = bmes.CUSTOMRSCRIPTEXE(varargin{:});




if isempty(ret)&&ispc
	files=dir('C:/Program Files/R/R-*/bin/Rscript.exe');
	if ~isempty(files)
		ret=[files(end).folder '/' files(end).name];
	end
end

if isempty(ret)&&ismac
	tryfile='/Library/Frameworks/R.framework/Resources/Rscript';
	if bmes.isfile(tryfile); ret=tryfile; end
end

if isempty(ret); ret=bmes.locateexe('Rscript',false); end

if isempty(ret); ret='Rscript'; end %this is our fallback command if we don't find a specific location.

out=ret;

