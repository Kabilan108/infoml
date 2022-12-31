function h=fig(name)
% support name'd figures
% if name is one of true / false: we turn off/on named fig's.
% When off, we avoid generating new figure windows.
% Copyright (C) 2010 by Ahmet Sacan


if ~exist('name','var'); name=''; end
persistent usenewfig;
if isempty(usenewfig); usenewfig=true; end

if isempty(name); h=[];
else
	if islogical(name); usenewfig=name; return;
	elseif isnumeric(name)||ishandle(name); h=figure(name);	return;
	elseif ~ischar(name);	error('name argument must be a text argument.'); end
	
	h=findobj('type','figure','name',name);
end

if usenewfig
	if isempty(h)
		h=figure('Name',name);
	else
		set(0,'CurrentFigure',h);
	end
else
	if isempty(h)
		h=gcf;
		set(h,'Name',name);
	end
	set(0,'CurrentFigure',h);
end
if ~nargout
    clear h;
end
