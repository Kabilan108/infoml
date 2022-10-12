function [out]=weka(method,methodjar,args,javaexe)
% methodjar can be left empty if the method is internally available in
% weka.
% if javaexe is not provided, we use bmes.locateexe('java') to find the
% java that is on the path.
% Copyright (C) 2020 by Ahmet Sacan


% set the paths to java and Weka.
% Download Weka from: http://www.cs.waikato.ac.nz/ml/weka/downloading.html
% If you don't already have Java installed in your computer, download a
% version of Weka that contains the Java installer.
wekafolder=bmes.wekafolder;
if ~exist('javaexe','var')||isempty(javaexe)
	javaexe=bmes.locateexe('java'); %In case java is not on your "PATH", specify the full-path here.
end


wekafolder=strrep(wekafolder,'\','/'); %java doesn't like backslashes in paths.
wekajar = [wekafolder '/weka.jar'];
if ~bmes.isfile(wekajar); error('It appears you have either not installed Weka or not specified its install location correctly.'); end
if ~isempty(methodjar)&&~bmes.isfile(methodjar); error(sprintf('No such file [%s]. Make sure you provide the correct path to the method jar file.',methodjar)); end


if false %we used to call weka using matlab's internal java, which runs into problems if there's mismatch between matlab's java and weka's java versions.
	javaaddpath(wekajar);	
	% if a methodjar is provided, load it too.
	if ~isempty(methodjar); javaaddpath(methodjar); end
	
	import(method)
	out=evalc([method '.main(args);']);
else
	classpath=[wekajar];
	if ~isempty(methodjar)
		if ispc; classpath=[classpath ';' methodjar];
		else classpath=[classpath ':' methodjar]; end
	end

	I=cellfun(@isnumeric,args,'UniformOutput',1);
	args(I)=cellfun(@str2num,args(I),'UniformOutput',0);
	cmd=['"' javaexe '" -cp "' classpath '" ' method ' ' strjoin(args,' ')];
	fprintf('---NOTICE: Running command: %s\n', cmd);
	[status,out]=system(cmd);
end
