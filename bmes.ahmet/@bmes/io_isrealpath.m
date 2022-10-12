function ret = io_isrealpath(path)
% return true if path is an absolute path 
% an aboslute path is one that starts with a '/' or that contains ':'
% Copyright (C) 2014 by Ahmet Sacan

ret=~isempty(path) && ...
  (io_isslash(path(1)) ...
  ||~isempty(regexp(path,'^[^/\\]+:','once')));
 
%---------------------------------------------------------
%<func_embed_begin:io_isslash.m>
function ret = io_isslash(chr)
% return true if chr is '/' or '\'
% Copyright (C) 2010 by Ahmet Sacan
ret=chr=='/'||chr=='\';
%<func_embed_end:io_isslash.m>
