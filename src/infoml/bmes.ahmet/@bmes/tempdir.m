function [out]=tempdir()
% Copyright (C) 2019 by Ahmet Sacan

persistent ret;
if isempty(ret)
	ret2=strrep(tempdir,'\','/');
	if ~ret2(end)=='/'; ret2=[ret2 '/']; end
	ret2=[ret2 'bmes'];
	if ~bmes.isfolder(ret2); mkdir(ret2); end
	ret=ret2;
end
out=ret;


