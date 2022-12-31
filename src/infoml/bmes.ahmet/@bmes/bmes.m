% by AhmetSacan
% a "hot" copy is available in Ahmet's dropbox/share/bmes.ahmet/
classdef bmes
	methods (Static)		
		% function to provide static data storage.
		function ret=getset(name,val)
			persistent data;
			if nargin>1
				if isempty(data); data=struct; end
				data.(name)=val;
				ret=val;
			else
				if isempty(data)||~isfield(data,name)
					%error(sprintf('Undefined static variable [%s]',name));
					%return [] by default.
					ret=[];
				else
					ret=data.(name);
				end
			end
		end
		
		function ret=PROJECTNAME(varargin); ret=bmes.getset('PROJECTNAME',varargin{:}); end
		function ret=CUSTOMDATADIR(varargin); ret=bmes.getset('CUSTOMDATADIR',varargin{:}); end
		function ret=CUSTOMDBFILE(varargin); ret=bmes.getset('CUSTOMDBFILE',varargin{:}); end
		function ret=db(varargin); ret=bmes.getset('db',varargin{:}); end
		function ret=CUSTOMPYEXE(varargin); ret=bmes.getset('CUSTOMPYEXE',varargin{:}); end
		function ret=CUSTOMRSCRIPTEXE(varargin); ret=bmes.getset('CUSTOMRSCRIPTEXE',varargin{:}); end
		function ret=CUSTOMWEKAFOLDER(varargin); ret=bmes.getset('CUSTOMWEKAFOLDER',varargin{:}); end
		function ret=CUSTOMJAVAEXE(varargin); ret=bmes.getset('CUSTOMJAVAEXE',varargin{:}); end
		function ret=sys_issacan(); ret=strncmpi(bmes.computername,'sacan',5); end
		function ret=sys_programsfolder(); if ispc; ret='C:/Program Files/'; elseif ismac; ret='/Applications/'; else ret='/bin'; end; end

		
		ret=isfolder(folder); %this is kept for backward compatibility to pre-matlab2017b
		ret=isfile(file); %this is kept for backward compatibility to pre-matlab2017b
		ret=isfileandnotempty(file);
		ret=firstexistentfolder(folders);
		ret=firstexistentfile(files);
		function mkdirif(folder); if ~bmes.isfolder(folder); mkdir(folder); end; end
		ret=username();
		ret=userhomedir();
		function ret=userdownloaddir(); ret=[bmes.userhomedir '/Downloads']; end
		ret=tempdir();
		ret=datadir();
		ret=projdatadir(); %project subfolder within datadir().
		file=sanitizefilename(file);
		file=downloadurl(url,file,overwrite);
		outfile=publish(func,varargin);
		out=computername();
		s=io_head(file,n);
		out=io_isrealpath(path);
		out=locateexe(exe,dieifnotfound);
		out=numcputhreads();		
		out=pyexe();
		out=rscriptexe();
		out=javaexe();
		out=bwaexe();
		out=wekafolder();
		out=weka(method,methodjar,args,javaexe);
		condadir=runjupyter(runinfolder,condadir);
		seq=int2aa(num);
		aa=aa2int(seq);
		
		addtosyspath(dir);
		arff=arffload(file);
		h=fig(name);
	end
end

