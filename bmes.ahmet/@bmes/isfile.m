function [ret]=isfile(path)
% Copyright (C) 2019 by Ahmet Sacan

if iscell(path); ret=cellfun(@bmes.isfile,path,'UniformOutput',true); return; end

if isnumeric(path)||isempty(path)||any(path==10); ret=false; return; end

if exist(path,'dir'); ret=false;
else
	inf=dir(path);
	ret=~isempty(inf);
end
