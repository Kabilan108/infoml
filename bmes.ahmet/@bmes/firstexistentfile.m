function [b]=firstexistentfile(files)
% returns first among the files that exist on this computer.
% returns empty [], if none of the files exist.
% Copyright (C) 2021 by Ahmet Sacan


out=[];
for i=1:numel(files)
	if bmes.isfile(files{i});
		out=files{i};
		return;
	end
end
