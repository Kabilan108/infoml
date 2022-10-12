function [file]=sanitizefilename(file)
% Copyright (C) 2019 by Ahmet Sacan

%in case filename is truncated by other functions, reverse the path. This
%is useful when a url is being converted into a file.
if any(file=='/')||any(file=='\')
	file=strrep(file,'\','/');
	[dir,name,ext]=fileparts(file);
	dir=regexprep(dir,'https?://','');
	dir=strjoin(fliplr(strsplit(dir,'/')),'/');
	file=[name dir ext];
end


file = regexprep(file,'([^\w\s\d\-_~,;\[\]\(\).])', '');
file = regexprep(file,'([\.]{2,})', '');
if isempty(file); file='noname'; end
