function [ret] = computername()
% Copyright (C) 2008 by Ahmet Sacan
ret  = sys_computername();


%---------------------------------------------------------
%<func_embed_begin:sys_computername.m>
function [ret] = sys_computername()
% Copyright (C) 2008 by Ahmet Sacan

persistent name;
if isempty(name)
  if ispc
    name=getenv('COMPUTERNAME');
  else
    name=getenv('HOSTNAME');
		if isempty(name)
			[status,name]=system('hostname');
			if status; name='';
			elseif ~isempty(name)&&name(end)==10; name=name(1:end-1); end
		end
  end
end
if isempty(name); name='unknown'; end
ret=lower(name);
%<func_embed_end:sys_computername.m>
