function s=io_head(file,n)
% Get/Print the top n=10 lines of a file.
% Copyright (C) 2020 by Ahmet Sacan

if ~exist('n','var'); n=10; end

f=fopen(file);
if f<0; error(sprintf('Failed to open file [ %s ]',file)); end

s='';
for i=1:n
	line=fgets(f);
	if ~ischar(line); break; end
	s=[s line];
end

if ~nargout; fprintf('%s\n',s); clear s; end