function [out]=firstexistentfolder(folders)
% returns first among the folders that exist on this computer.
% returns empty [], if none of the folders exist.
% Copyright (C) 2021 by Ahmet Sacan

out=[];
for i=1:numel(folders)
	if bmes.isfolder(folders{i});
		out=folders{i};
		return;
	end
end
