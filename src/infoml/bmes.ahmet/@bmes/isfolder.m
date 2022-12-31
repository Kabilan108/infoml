function ret=isfolder(path)
% this is a copy of the .compat/2017b/isFolder.m
% Copyright (C) 2019 by Ahmet Sacan

if iscell(path); ret=cellfun(@bmes.isfolder,path,'UniformOutput',true); return; end

if isnumeric(path)||isempty(path)||any(path==10); ret=false; return; end

if exist(path,'dir'); ret=true;
else
	info=dir(path);
	ret=~isempty(info);
end
