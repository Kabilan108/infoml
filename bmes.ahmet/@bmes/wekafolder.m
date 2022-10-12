function [out]=wekafolder(varargin)
% return location of weka installation.
% Copyright (C) 2019 by Ahmet Sacan

if ~isempty(bmes.CUSTOMWEKAFOLDER); out=bmes.CUSTOMWEKAFOLDER; return; end
persistent ret;
if ~isempty(ret); out=ret; return; end

ds=dir(bmes.sys_programsfolder); ds={ds.name};
I=find(~cellfun(@isempty,regexp(ds,'^weka','ignorecase','once'),'UniformOutput',1));
if isempty(I)
	error(sprintf('Cannot locate Weka under [ %s ].\nDownload and install Weka following instructions available at: https://waikato.github.io/weka-wiki/downloading_weka/\nIf you have installed Weka installed other than under [ %s ] folder, use bmes.CUSTOMWEKAPATH(''/path/to/your/wekafolder'') to set your own weka folder.',bmes.sys_programsfolder,bmes.sys_programsfolder));
end
ret=[bmes.sys_programsfolder '/' ds{I(end)}];
out=ret;
