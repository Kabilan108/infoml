function addtosyspath(dir)
% Copyright (C) 2019 by Ahmet Sacan

path=getenv('PATH');
args={};
if ispc; args{end+1}='ignorecase'; end
if isempty(regexp([pathsep path pathsep],[pathsep dir pathsep],'once',args{:}))
	setenv('PATH', [path pathsep dir]);
end

