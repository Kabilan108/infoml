function [out]=projdatadir()
% Copyright (C) 2019 by Ahmet Sacan

projname=bmes.PROJECTNAME;
if isempty(projname)
	error('You must set bmes.PROJECTNAME() before you can use projdatadir().');
end

out=[bmes.datadir() '/' projname];
if ~bmes.isfolder(out); mkdir(out); end
