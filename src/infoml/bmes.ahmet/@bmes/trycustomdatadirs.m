function trycustomdatadirs(dirs)
%only call trycustomdatadirs if bmes.DATADIR is not set elsewhere.
% Copyright (C) 2019 by Ahmet Sacan

dir=bmes.CUSTOMDATADIR;
if isempty(dir)
	for i=1:numel(dirs)
		if isfolder(dirs{i}); bmes.CUSTOMDATADIR(dirs{i}); break; end
	end
end
