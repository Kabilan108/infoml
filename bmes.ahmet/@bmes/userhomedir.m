function [ret]=userhomedir()
% Copyright (C) 2022 by Ahmet Sacan
ret=sys_userhomedir();


%---------------------------------------------------------
%<func_embed_begin:sys_userhomedir.m>
function [ret] = sys_userhomedir()
% return user's home directory. if output is not captured, we additionally chdir into
% userhomedir.
% Copyright (C) 2014 by Ahmet Sacan

if ispc
	ret=getenv('USERPROFILE');
	if isempty(ret)
		ret=winqueryreg('HKEY_CURRENT_USER','Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders','Personal');
		if isempty(ret); ret=['C:/Users/' strrep(sys_username(),'$','_')]; end
	end
else
	ret=getenv('HOME');
	if isempty(ret)
		if ismac; ret=['/Users/' sys_username()];
		else ret=['/home/' sys_username()]; end
	end
end

if ~nargout; cd(ret); end
%<func_embed_end:sys_userhomedir.m>

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
