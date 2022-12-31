function [ret]=username()
% Copyright (C) 2019 by Ahmet Sacan
ret=sys_username();

%---------------------------------------------------------
%<func_embed_begin:sys_username.m>
function [ret] = sys_username()
% Copyright (C) 2011 by Ahmet Sacan

persistent name;
if isempty(name)
  if ispc
    name=lower(getenv('USERNAME'));
  else
    name=getenv('USER');
  end
end
ret = name;
%<func_embed_end:sys_username.m>
			
		