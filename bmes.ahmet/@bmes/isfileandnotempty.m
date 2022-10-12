function [ret]=isfileandnotempty(path)
% Copyright (C) 2019 by Ahmet Sacan

if ~bmes.isfile(path); ret=false; return; end


inf=dir(path);
ret=inf.bytes;
