function [condadir]=runjupyter(notebookdir,condadir)
% notebookdir can be a folder where you want to start from or an ipynb filename you want to load.
% Copyright (C) 2020 by Ahmet Sacan
if ~exist('notebookdir','var')||isempty(notebookdir); notebookdir='./'; end
notebookdir=strrep(notebookdir,'\','/');
if ~bmes.io_isrealpath(notebookdir); notebookdir=[pwd '/' notebookdir]; end

if ~isfolder(notebookdir)
	notebookfile=notebookdir;
	if ~isfile(notebookfile)
		if isempty(regexp(notebookfile,'\..{1,5}$','once')); error(sprintf('No such file or folder: %s',notebookfile)); end
		f=fopen(notebookfile,'a');
		if ~isempty(regexp(notebookfile,'\.ipynb$','once'));	fprintf(f,'{"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 4}\n'); end
		fclose(f);
	end
	[notebookdir notebookfile ext]=fileparts(notebookdir);
	notebookfile=[notebookfile ext];	
end

oldpwd=pwd;
cd(notebookdir);

if ~ispc
	[~,jupyterexe]=system('which jupyter');
	if isempty(jupyterexe)&&ismac
		jupyterexe2=['/Users/' bmes.username '/opt/anaconda3/bin/jupyter'];
		if isfile(jupyterexe2); jupyterexe=jupyterexe2;
		else warn('Cannot locate jupyter executable location. Make sure jupyter is on your PATH'); jupyterexe='jupyter'; end
	end
	if exist('notebookfile','var')
		cmd=sprintf('"%s" notebook --NotebookApp.disable_check_xsrf=True "%s" &',jupyterexe,notebookfile);
	else
		cmd=sprintf('"%s" notebook &',jupyterexe);
	end
	fprintf('---NOTICE: Running command: %s\n',cmd);
	system(cmd);
	cd(oldpwd);
	return;
end


if bmes.sys_issacan
	if exist('condadir','var')&&~isempty(condadir)
		config('condadir',condadir);
	elseif config('?condadir')
		condadir=config('condadir');
	end
end

if ~exist('condadir','var')||isempty(condadir)
	condadir=getenv('CONDA_PREFIX');
end
if ~exist('condadir','var')||isempty(condadir)
	dirs={'C:/ProgramData/Anaconda3','C:/ProgramData/Anaconda3',[getenv('USERPROFILE') '/Anaconda'],[getenv('USERPROFILE') '/Anaconda3']};
	for di=1:numel(dirs)
		if isfile([dirs{di} '/python.exe'])
			condadir=dirs{di};
			break;
		end
	end
end
if ~exist('condadir','var')||isempty(condadir)
	error('I could not locate Anaconda in the usual places. You can still use this function, but you must provide the location of the Anaconda directory (e.g., ''C:/ProgramData/Anaconda3'') as the second argument to this function.');
end

oldpath=getenv('PATH');
oldcondadir=getenv('CONDA_PREFIX');
subdirs={'','Library/mingw-w64','Library/usr/bin','Library/bin','Scripts'};
newpath=oldpath;
for si=1:numel(subdirs)
	dir=[condadir '/' subdirs{si}];
	%if ~isfolder(dir); warning(sprintf('Folder [%s] does not exist.',dir)); end
	newpath=[dir ';' newpath];
end
setenv('PATH', newpath );
setenv('CONDA_PREFIX',condadir);

if exist('notebookfile','var')
	cmd=sprintf('"%s/Scripts/jupyter.exe" notebook --NotebookApp.disable_check_xsrf=True "%s" &',condadir,notebookfile);
else
	%	cmd=sprintf('"%s/python.exe" "%s/cwp.py" "%s" "%s/python.exe" "%s/Scripts/jupyter-notebook-script.py" "%s" &',condadir,condadir,condadir,condadir,condadir,runinfolder);
	%cmd=sprintf('"%s/Scripts/jupyter-notebook.exe" --notebook-dir="%s" &',condadir,notebookdir);
	cmd=sprintf('"%s/Scripts/jupyter.exe" notebook &',condadir);
end
fprintf('---NOTICE: Running command: %s\n',cmd);
[stat,msg]=system(cmd);
setenv('PATH', oldpath );
setenv('CONDA_PREFIX',oldcondadir);
if ~isempty(strtrim(msg)); fprintf('%s\n',msg); end
if stat;
	msg='Received an error while trying to run jupyter.';
	if any(condadir,' ');
		msg=[msg newline ' Having a space character in the location you installed Anaconda is sometimes a problem.'];
		if ispc;
			msg=[msg newline ' Try removing and reinstalling Anaconda. Select "for All Users" when installing Anaconda.'];
		else
			msg=[msg newline ' Try removing and reinstalling Anaconda somewhere else.'];
		end	
	end
	error(msg);
end
cd(oldpwd);
if ~nargout; clear condadir; end
