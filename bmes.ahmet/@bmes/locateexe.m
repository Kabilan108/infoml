function [out]=locateexe(exe,dieifnotfound)
% Copyright (C) 2020 by Ahmet Sacan

if any(exe=='/')||any(exe=='\'); out=exe; end
if ~exist('dieifnotfound','var'); dieifnotfound=true; end

out='';
if any(exe=='"'); error(sprintf('exe name containing double-quote character not allowed: [%s]',exe)); end
if ispc; whichcmd='where';
else; whichcmd='which'; end
[status,tryfile]=system(sprintf('%s "%s"',whichcmd,exe));
if ~status && ~isempty(tryfile)
	out=strtrim(tryfile);
	%windows may return multiple hits
	out=regexprep(out,'\r?\n.*','');
end

if isempty(out)&&dieifnotfound
	error(sprintf('Cannot locate executable [%s] on system path. You need to add the folder containing that executable to your system.',exe));
end

