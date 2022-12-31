function plibmatlabfolder=zoz_registeranddownload(varargin)
% Copyright (C) 2018 by Ahmet Sacan

if ~exist('varargin','var'); varargin={}; end

%% Injectable Settings, to be modified by product::downloadfile.
%<INJECTABLE SETTINGS>
LICENSEBASEURL='http://sacan.biomed.drexel.edu/lic';
PRODUCT='progbank';
EDUONLY=true;
%</INJECTABLE SETTINGS>

if regexp(sys_computername,'^sacanlap.*') %we'll do this again, when LICENSEBASEURL is needed. we do it here in case we hit a return.
	global opt_setactivate_uselocal;
	if ~isempty(opt_setactivate_uselocal) && opt_setactivate_uselocal
		LICENSEBASEURL='http://localhost/lic';
	end
end

%form parameter values name,email,injectstartuppath,injectstartupsettings can be specified in options.
%if all inputs are given, we skip asking the user in a gui_form.
o=struct( ...
	'product',PRODUCT ...
	,'eduonly',EDUONLY ...
	,'licensebaseurl',LICENSEBASEURL ...
	,'onlydirectcall',1 ...
	,'purge',0 ...
);
if o.onlydirectcall&&numel(dbstack)~=1; error('You must call zoz_registeranddownload directly from commandline (or turn off this restriction with o.onlydirectcall=false.'); end


for i=1:2:numel(varargin)-1
	o.(varargin{i})=varargin{i+1};
end

%% Set up inputs
inputs=struct('name', {'product','name','email','installdir','injectstartuppath','injectstartupsettings','activatelicense'} ...
	,'label',{'Product:', 'Full Name:', 'Email:', 'Installation Folder','Insert path to startup script','Insert recommended settings to startup script','Activate license'} ...
	,'style',{'text','','', '', 'checkbox','checkbox','checkbox'} ...
	,'default',{o.product,'','',[strrep(sys_userpath(),'\','/') '/zozani'], 1,1,1} ...
	);
%if we have any o options given, merge them in as values here.
names={inputs.name};
params=struct;
hasallinputs=true;
for ni=1:numel(names)
	name=names{ni};
	if isfield(o,name)
		inputs(strcmp(names,name)).value=o.(name);
	else
		hasallinputs=false;
	end
end


%% ask the user if any options are missing in o.
while ~hasallinputs
	params=gui_form(inputs, 'remember','zoz_register', 'name','zozani: register and download');
	if isempty(params); fprintf('--- NOTICE: Registration cancelled by the user.\n'); return; end
	msg='';
	name=params.name;
	email=params.email;
	if isempty(name)||isempty(find(name==' ',1)); msg=[msg sprintf('* You must provide your full name.\n')]; end
	if o.eduonly && (isempty(email)||isempty(regexp(email,'^[\w-\.]+@([\w-]+\.)+(edu\.\w\w|edu)$','once'))); msg=[msg sprintf('* You must provide an academic email address (with a .edu domain).\n')]; end
	if ~o.eduonly && (isempty(email)||isempty(regexp(email,'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$','once'))); msg=[msg sprintf('* You must provide a valid email address.\n')]; end
	if isempty(msg); break; end
	cont=questdlg(sprintf('\\fontsize{15}%s\nTry again ? ',msg),'zoz_download','OK','Cancel',struct('Interpreter','tex','Default','Cancel'));
	if ~strcmp(cont,'OK'); fprintf('--- NOTICE: Registration cancelled by the user.\n'); return; end
	%remove the values we got from o, to give gui_form::remember storage a
	%chance now.
	inputs=rmfield(inputs,'value');
end


target=mexext();
if numel(target)>3&&strcmp(target(1:3),'mex'); target=target(4:end); end
matlabversion=version('-release');

regurl=sprintf('%s/reg/%s?name=%s&email=%s&target=%s&matlabversion=%s&agree=1&submit=1&skipsendemail=1',o.licensebaseurl,o.product,urlencode(name),urlencode(email),target,matlabversion);
sfile=websave('zoz_registeranddownload.html',regurl);
s=fileread(sfile);
downloadurl=regexp_token(s,'<a href=''([^'']+)''>Click here to download</a>');
if isempty(downloadurl)
	web(sfile);
	error('Cannot parse download-url from registration. Server response is shown in browser.');
end
delete(sfile);

installdir=params.installdir;
if ~io_isdir(installdir); mkdir(installdir); end
plibmatlabfolder=[installdir '/lib'];
downloadfile=[sys_userpath() '/zoz_download.zip'];

evalin('caller','save(''.zoz_registeranddownload_caller.mat'');'); evalin('caller','clear;');
zoz_download_stage2('libmatlabfolder',plibmatlabfolder,'purge',o.purge,'downloadurl',downloadurl,'singlefiledownload',0,'downloadfile',downloadfile);
evalin('caller','load(''.zoz_registeranddownload_caller.mat'');'); delete('.zoz_registeranddownload_caller.mat');

addpath(plibmatlabfolder);
if params.activatelicense&&any(exist('opt_setactivate')==[2 5 6])
	licensefile=[plibmatlabfolder '/libahmet.lic'];
	if io_isfile(licensefile);
		eval('opt_setactivate(o.product,false,licensefile)'); %this is so that func_embed doesn't try to embed opt_setactivate here.
	end
end

[changed,s]=zoz_injectstartup(plibmatlabfolder, params.injectstartuppath, params.injectstartupsettings);
if changed;	eval(s); end

fprintf('Installation completed. The library has been installed in: %s\n',fileparts(plibmatlabfolder));
if ~nargout; clear plibmatlabfolder; end







%---------------------------------------------------------
%<func_embed_begin:gui_form.m>
function [ret]=gui_form(es,varargin)
%es can be a struct array with fields name,style (default:edit).
% or a struct with fieldnames as input names and each value a struct with
% its properties.
% or cellstr (each a name).
% or each entry can be given as a cell array.
% NOTE: keep this implementation "simple", b/c it is used by zoz_registeranddownload.
% Copyright (C) 2018 by Ahmet Sacan

if ~exist('es','var');
	%fprintf('---NOTICE: using demo with the following arguments:\n');
	es={{'name'} ,{'email'} };
	es=struct('name', {'name','email','addstartup'}, 'label',{'Full Name:', 'Email:','Add library path in startup script'}, 'style',{'','', 'checkbox'},'hint',{'enter full name','',''});
	varargin={'remember','contact'};
end

%% Options
o=struct( ...
	'name','gui_form' ...
	,'singleton',true ... 
	,'remember','' ... %remember the values that have been typed in. provide a string as a named store. use true to use o.name as the storage key
);
for i=1:2:numel(varargin)-1
	o.(varargin{i})=varargin{i+1};
end
if islogical(o.remember)
	if o.remember; o.remember=o.name;
	else o.remember=[]; end
end
if ~isempty(o.remember)
	o.remember=lower(regexprep(o.remember,'[^a-zA-Z0-9]',''));
end


%% handle different ways of specifying inputs
if iscellstr(es)
	for i=1:numel(es); es2(i).name=es{i}; end
	es=es2;
elseif iscell(es)
	for i=1:numel(es)
		e=es{i};
		es2(i).name=e{1};
		if numel(e)>=2;
			if iscellstr(e{2}); es2(i).options=e{2};
			else es(i).default=e{2}; end
		end
	end
	es=es2;
elseif isstruct(es) && numel(es)==1
	% see any of the struct's values is a cellstr or cell or struct, then we
	% unroll its format to flat struct.
	fs=fieldnames(es);
	fieldasinput=false;
	for fi=1:numel(fs)
		f=es(fi); e=es.(f);
		if iscell(e)||isstruct(e); fieldasinput=true; break; end
	end
	if fieldasinput
		es2=struct;
		for fi=1:numel(fs)
			f=es(fi); e=es.(f);
			es2(fi).name=f;
			if ischar(e)||isnumeric(e)||islogical(e); es2(fi).default=e;
			elseif iscellstr(e); es2(fi).options=e;
			elseif isstruct(e)
				efs=fieldnames(e);
				for efi=1:numel(efs)
					es2(fi).(efs{efi})= e.(efs{efi});
				end
			else error(sprintf('Unknown input specification for input [%s]',f)); end
		end
	end
elseif ~isstruct(es)
	error('Input specification must be cellstr, cell, or struct');
end


%% create figure
hfig=[];
if o.singleton
	hfig=handle(findall(0,'type','figure','name',o.name));
	if ~isempty(hfig); hfig=hfig(1); set(0,'CurrentFigure',hfig); clf(hfig); end
end
if isempty(hfig); hfig=figure('name',o.name); end


%% set up remember storage
persistent allremembered;
remembered=[];
if ~isempty(o.remember)
	DIR=fileparts(which(mfilename('fullpath')));
	rememberfile=[DIR '/zoz_gui_form.remember.mat'];
	% if DIR is a dropbox folder and we don't have write permissions, we
	% won't be able to write a file there.
	fid=fopen(rememberfile,'a'); if fid>0; fclose(fid); end
	if fid<0;	rememberfile=[sys_userpath() '/zoz_gui_form.remember.mat']; end
	
	if isempty(allremembered); allremembered=struct; end
	if isfield(allremembered,o.remember); remembered=allremembered.(o.remember);
	elseif exist(rememberfile,'file')
		ofile=load(rememberfile);
		if isfield(ofile,o.remember); remembered=ofile.(o.remember); end
	end
end



%% add inputs
hfig.Position(4)=(numel(es)+2)*30;
ypadding=0.02;
eheight=max(0.05, (1-2*ypadding)/(numel(es)+1) - ypadding);
currenty=1-ypadding-eheight;
hs=struct;
hint='';
for i=1:numel(es)
	e=es(i);
	name=e.name;
	if isfield(e,'style')&&~isempty(e.style); style=e.style;
	else
		if isfield(e,'options')&&~isempty(e.options)
			if size(e.options,1)==1&&size(e.options,2)>1; e.options=e.options'; end
			style='popopmenu';
		else
			style='edit';
		end
	end
	if isfield(e,'label')&&~isempty(e.label); label=e.label; else; label=[name ':']; end
	if isfield(e,'hint'); hint=e.hint; end
	
	
	if isfield(e,'value')&&~(isnumeric(e.value)&&isempty(e.value)); default=e.value;
	elseif ~isempty(remembered)&&isfield(remembered,name); default=remembered.(name);
	elseif isfield(e,'default')&&~isempty(e.default); default=e.default;
	else; default=''; end
	
	name=lower(regexprep(name,'[^a-zA-Z0-9]',''));
	es(i).name=name;
	if strcmp(style,'checkbox')
		h=uicontrol('style',style,'Parent',hfig,'Units','normalized','Position',[0.05,currenty,0.85,eheight],'FontUnits','normalized','FontSize',0.7,'HorizontalAlignment','left','String',label);
	else
		hs.([name '_label'])=uicontrol('style','text','Parent',hfig,'Units','normalized','Position',[0.05,currenty,0.3,eheight],'FontUnits','normalized','FontSize',0.7,'String',label,'HorizontalAlignment','left');
		h=uicontrol('style',style,'Parent',hfig,'Units','normalized','Position',[0.41,currenty,0.55,eheight],'FontUnits','normalized','FontSize',0.7,'HorizontalAlignment','left');
	end
	hs.(name)=h;
	if strcmp(style,'popopmenu')
		h.String=e.options;
		if ischar(default);	I=find(strcmp(e.options,default),1); end
		if isempty(default); default=1; end
		h.Value=default;
	elseif strcmp(style,'checkbox')
		if isempty(default); default=0; end
		h.Value=default;
	else
		h.String=default;
		%h.KeyPressFcn=@(h,evt)gui_form_onkeypress(hfig); %this doesn't work,
		%because an edit box's String value is not up to date when we call
		%onkeypress.
	end
	if ~isempty(hint)
		hs.([name '_hint'])=uicontrol('style','pushbutton','Parent',hfig,'Units','normalized','Position',[0.96,currenty,0.04,eheight],'FontUnits','normalized','FontSize',0.7,'String','?','Callback',@(~,~)helpdlg(hint,[name ' : ' o.name]));
	end		
	currenty=currenty-eheight-ypadding;
end
currenty=currenty-ypadding; %1 extra padding.
hs.okbutton = uicontrol('style','pushbutton','Parent',hfig,'Units','normalized','Position',[0.16,currenty,0.3,eheight],'FontUnits','normalized','FontSize',0.7,'String','OK');
hs.cancelbutton = uicontrol('style','pushbutton','Parent',hfig,'Units','normalized','Position',[0.54,currenty,0.3,eheight],'FontUnits','normalized','FontSize',0.7,'String','Cancel');
currenty=currenty-eheight-ypadding;


hfig.ResizeFcn=@(h,evt)gui_form_onresize(hs);
hfig.CloseRequestFcn=@(h,evt)gui_form_onclose(hfig);
hfig.KeyPressFcn=@(h,evt)gui_form_onkeypress(hfig);
hs.cancelbutton.Callback=@(h,evt)gui_form_onclose(hfig);
hs.okbutton.Callback=@(h,evt)gui_form_onok(hfig);

gui_form_onresize(hs);
uiwait(hfig);

ret=[];
if isempty(getappdata(hfig,'canceled'))
	ret=struct;
	for i=1:numel(es)
		name=es(i).name;
		style=es(i).style;
		h=hs.(name);
		if ~isvalid(h); error(sprintf('Invalid/deleted handle for [%s]',name)); end
		if strcmp(style,'popopmenu'); ret.(name)=h.String{h.Value};
		elseif strcmp(style,'checkbox'); ret.(name)=h.Value;
		elseif strcmp(style,'text'); continue;
		else ret.(name)=h.String; end
	end
	if ~isempty(o.remember)
		allremembered.(o.remember) = ret;
		eval([o.remember '=ret;']);
		save(rememberfile, o.remember);
	end
end
delete(hfig);


function gui_form_onclose(hfig)
setappdata(hfig,'canceled',1);
uiresume;

function gui_form_onok(hfig)
uiresume;

function gui_form_onkeypress(hfig)
key = get(hfig,'CurrentKey');
if strcmp(key,'return'); gui_form_onok(hfig);
elseif strcmp(key,'escape'); gui_form_onclose(hfig);
end
			

function gui_form_onresize(hs)
fs=fieldnames(hs);
for fi=1:numel(fs)
	h=hs.(fs{fi});
	if ~isvalid(h); break; end
	h.FontSize=0.7;
	h.FontUnits='points';
	if h.FontSize>20
		h.FontSize=20;
		h.FontUnits='normalized';
	else
		h.FontUnits='normalized';
		h.FontSize=0.7;
	end
	if h.Extent(3)>0.9*h.Position(3)||h.Extent(4)>0.8*h.Position(4)
		h.FontSize=h.FontSize*min(0.9*h.Position(3)/h.Extent(3), 0.8*h.Position(4)/h.Extent(4));
	end
end
%<func_embed_end:gui_form.m>

%---------------------------------------------------------
%<func_embed_begin:io_isdir.m>
function [ret]=io_isdir(path)
% does not deal with path being an ftp folder. and does not do
% io_realpath(path)
% Copyright (C) 2018 by Ahmet Sacan
if isnumeric(path)||isempty(path)||any(path==10); ret=false; return; end

%TODO: eventually, make isfolder() the only option.
persistent isdirfunc;
if isempty(isdirfunc)
	%isfolder() is available in >Matlab2017b and is prefered, because it doesn't search the Matlab search path like isdir() does.
	if any(exist('isfolder')==[2 5 6]); isdirfunc=@isfolder;
	else isdirfunc=@isdir; end
end
ret=isdirfunc(path);
%<func_embed_end:io_isdir.m>

%---------------------------------------------------------
%<func_embed_begin:io_isfile.m>
function [ret]=io_isfile(path)
% Copyright (C) 2018 by Ahmet Sacan

if isnumeric(path)||isempty(path)||any(path==10); ret=false; return; end

persistent hasisfilefunc
if isempty(hasisfilefunc); hasisfilefunc=any(exist('isfile')==[2 5 6]); end
if hasisfilefunc
	ret=isfile(path);
else
	if exist(path,'dir'); ret=false;
	else
		inf=dir(path);
		ret=~isempty(inf);
	end			
end
%<func_embed_end:io_isfile.m>

%---------------------------------------------------------
%<func_embed_begin:regexp_token.m>
function [ret]=regexp_token(s,pattern,varargin)
% noncapture groups have syntax (?:...)
% if s is a cellarray, the output is also a cell array.
% Copyright (C) 2013 by Ahmet Sacan
if iscell(s)
	ret=cell(size(s));
	for i=1:numel(s)
		ret{i}=regexp_token(s{i},pattern,varargin{:});
	end
	return;
end

ret=regexp(s,pattern,'once','tokens',varargin{:});
if isempty(ret); ret=''; return; end
ret=ret{1};
if iscell(ret); ret=ret{1}; end
%<func_embed_end:regexp_token.m>

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

%---------------------------------------------------------
%<func_embed_begin:sys_userpath.m>
function [ret] = sys_userpath()
% return the first folder in userpath (usually USERHOME/Documents/MATLAB).
% Copyright (C) 2011 by Ahmet Sacan

[~,ret]=evalc('userpath');
ret(find(ret==pathsep,1):end)=[];
if isempty(ret); ret=[sys_userhomedir() '/Documents/MATLAB']; end
%<func_embed_end:sys_userpath.m>

%---------------------------------------------------------
%<func_embed_begin:zoz_download_stage2.m>
function [ret]=zoz_download_stage2(varargin)
% not intended for direct call. used by zoz_download() and
% zoz_registeranddownload()
% Copyright (C) 2018 by Ahmet Sacan
o=struct( ...
	'libmatlabfolder','' ...
	,'purge',0 ...
	,'downloadurl','' ...
	,'downloadfile','' ...
	,'singlefiledownload', false ...
);
for i=1:2:numel(varargin)-1
	o.(varargin{i})=varargin{i+1};
end
if isempty(o.libmatlabfolder)||isempty(o.downloadurl)||isempty(o.downloadfile); error('Expecting libmatlabfolder and downloadurl'); end
url=o.downloadurl;
downloadfile=o.downloadfile;
plibmatlabfolder=o.libmatlabfolder;
if o.purge; url=[url '&purge=1']; end

hwait=handle(findall(0,'type','figure','tag','TMWWaitbar','name','zoz_download'));
if ~isempty(hwait); hwait=hwait(1); end
if isempty(hwait); hwait=waitbar(0,'Checking server availability...','name','zoz_download','CreateCancelBtn','setappdata(gcbf,''canceling'',1)'); end

runstats=struct('avgtime',60,'maxtime',600, 'tic',tic, 'esttime',60, 'progress',0.1);
downloadready=false;
while true
	if getappdata(hwait,'canceling'); fprintf('Installation interrupted by user.\n'); delete(hwait); return; end
	runstats.progress=0.1+toc(runstats.tic)/runstats.esttime*0.8;
	if ~downloadready; waitbar(runstats.progress,hwait,'Waiting for download package to be prepared by the server...');
	else waitbar(0.95,hwait,'Downloading the package...'); end
	sdownloadfile=websave(downloadfile,url,weboptions('Timeout',600));
	if downloadready; downloadfile=sdownloadfile; break; end
	s=fileread(sdownloadfile);
	if str_pos(s,'Your product is ready'); downloadready=true; end
	toks=regexp_tokens(s,'setTimeout\("location.href=''([^'']+)''",(\d+)\)');
	if isempty(toks)
		toks=regexp_tokens(s,'location.href=''([^'']+)''');
		if isempty(toks); error(sprintf('Cannot find the redirect url from server response. Downloaded file: %s',downloadfile)); end
		toks{2}='100';
	end
	refreshtime=str2double(toks{2})/1000;
	url=url_relative(toks{1},url);
	if downloadready; continue; end
	
	
	%% runstats
	toks=regexp_tokens(s,'<runstats avgtime=''([^'']+)'' maxtime=''([^'']+)'' />');
	if ~isempty(toks)
		if ~isempty(toks{1}); runstats.avgtime=str2double(toks{1}); end
		if ~isempty(toks{2}); runstats.maxtime=str2double(toks{2}); end
	end
	runstats.elapsed=toc(runstats.tic);
	runstats.esttime=runstats.avgtime*1.1;
	if runstats.elapsed+refreshtime>runstats.avgtime*1.1; runstats.esttime=runstats.maxtime; end
	if runstats.elapsed+refreshtime>runstats.maxtime; runstats.esttime=runstats.elapsed+refreshtime; end
	
	%% wait before the next refresh
	t=0;
	while t<refreshtime
		if getappdata(hwait,'canceling'); fprintf('Installation interrupted by user.\n'); delete(hwait); return; end
		runstats.progress=0.1+(runstats.elapsed+t)/runstats.esttime*0.8;
		waitbar(runstats.progress,hwait,'Waiting for download package to be prepared by the server...');
		pause(0.1);
		t=t+0.1;
	end
end

delete(hwait);

if o.singlefiledownload
	[topdir,name,ext]=fileparts(downloadfile);
	files={[name ext]};
else
	topdir=[io_ensureendslash(sys_userpath()) '.zoz_download_zip'];
	topdir=strrep(topdir,'\','/');
	if ~io_isdir(topdir); mkdir(topdir); end	
	[files]=unzip(downloadfile,topdir);
	files=strrep(files,'\','/');
	
	topdir=io_ensureendslash(topdir);
	for i=1:numel(files)
		if ~str_isprefix(files{i},topdir); error('unexpected unzipped file [%s] not under topdir [%s]',files{i},topdir); end
		files{i}=str_removeprefix(files{i},topdir); 
	end
end
delete(downloadfile);

zozinstallmatfile=[sys_userpath '/.zoz_install.mat'];
save(zozinstallmatfile,'files','topdir','plibmatlabfolder');

evalin('caller','save(''.zoz_download_caller.mat'');'); evalin('caller','clear;');
zoz_install;
evalin('caller','load(''.zoz_download_caller.mat'');'); delete('.zoz_download_caller.mat');

try; rmdir(topdir);
catch me
	%we'll probably just have some empty directories. no big deal.
	fprintf('--- NOTICE: Failed to cleanup temporary directory [%s]. Error was: %s\n',topdir,me.message);
end
%<func_embed_end:zoz_download_stage2.m>

%---------------------------------------------------------
%<func_embed_begin:zoz_injectstartup.m>
function [changed,s]=zoz_injectstartup(plibmatlabfolder, injectstartuppath, injectstartupsettings)
% Copyright (C) 2018 by Ahmet Sacan

changed=false; s='';
if ~injectstartuppath && ~injectstartupsettings; return; end
file=[sys_userpath '/startup.m'];
eol=sprintf('\n');
if io_isfile(file); olds=fileread(file); else olds=''; end
if injectstartuppath && isempty(regexp([eol olds],['\n\s*%<begin-zozani-addpath:' plibmatlabfolder '>.*\n\s*%<end-zozani-addpath>'],'once'))
	s=[s '%<begin-zozani-addpath:' plibmatlabfolder '>' eol];
	s=[s 'addpath(''' plibmatlabfolder ''');' eol];
	s=[s '%<end-zozani-addpath>' eol eol];
end
if injectstartupsettings && isempty(regexp([eol olds],['\n\s*%<begin-zozani-settings:' plibmatlabfolder '>.*\n\s*%<end-zozani-settings>'],'once'))
	funcs={'matlab_setasvprefs','matlab_settabprefs','matlab_lightcolortheme','matlab_disableeditorwarnings','fig_setpretty'};
	s=[s eol '%<begin-zozani-settings:' plibmatlabfolder '>' eol];
	for fi=1:numel(funcs)
		f=funcs{fi};
		s=[s 'if any(exist(''' f ''')==[2 5 6]); ' f '(); end' eol];
	end
	s=[s 'dbstop error;' eol];
	s=[s '%<end-zozani-settings>' eol eol];
end
if ~isempty(s)
	f=fopen(file,'w'); fwrite(f,[olds eol eol s]);	fclose(f);
end
%<func_embed_end:zoz_injectstartup.m>

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

%---------------------------------------------------------
%<func_embed_begin:io_ensureendslash.m>
function [name]=io_ensureendslash(name)
% make sure name ends with '/'
% Copyright (C) 2015 by Ahmet Sacan

if isempty(name); name='/';
elseif name(end)=='\'; name(end)='/';
elseif name(end)~='/'; name(end+1)='/'; end
%<func_embed_end:io_ensureendslash.m>

%---------------------------------------------------------
%<func_embed_begin:str_isprefix.m>
function ret=str_isprefix(str,pre)
% check if str has prefix pre.
% pre can be a cell array, we'd return true if str has any of those
% prefixes.
% we don't ssupport str to be a cell array. Use strs_isprefix() for that.
% Copyright (C) 2009,2014 by Ahmet Sacan
%{
if iscell(str);
	ret=false(size(str));
	for i=1:numel(str); ret(i)=str_isprefix(str{i},pre); end
	return;
end
%}
if iscell(pre);
	for pi=1:numel(pre)
		if isempty(pre{pi}) || (numel(pre{pi})<=numel(str) && all(str(1:numel(pre{pi}))==pre{pi})); ret=true; return; end
	end
	ret=false;
	return;
end

%if isempty(str); ret=isempty(pre); return; end
ret=isempty(pre) || (numel(pre)<=numel(str) && all(str(1:numel(pre))==pre));
%<func_embed_end:str_isprefix.m>

%---------------------------------------------------------
%<func_embed_begin:str_pos.m>
function [pos]=str_pos(s,needle)
% return first occurence of needle in s.
% Copyright (C) 2015 by Ahmet Sacan

pos=strfind(s,needle);
if isempty(pos); pos=0;
else pos=pos(1); end
%<func_embed_end:str_pos.m>

%---------------------------------------------------------
%<func_embed_begin:regexp_tokens.m>
function [ret]=regexp_tokens(s,pattern,varargin)
% Copyright (C) 2013 by Ahmet Sacan
ret=regexp(s,pattern,'once','tokens',varargin{:});
if nargout>1
	varargout=cell(1,nargout);
	for i=1:min(nargout,numel(ret))
		varargout{i}=ret{i};
	end
elseif isempty(ret); ret={}; return; end
%<func_embed_end:regexp_tokens.m>

%---------------------------------------------------------
%<func_embed_begin:str_removeprefix.m>
function [s]=str_removeprefix(s,pre)
% Copyright (C) 2012 by Ahmet Sacan
if iscell(s); s=cellfun(@(x)str_removeprefix(x,pre),s,'UniformOutput',0); return; end
if str_isprefix(s,pre); s(1:numel(pre))=[]; end
%<func_embed_end:str_removeprefix.m>

%---------------------------------------------------------
%<func_embed_begin:url_relative.m>
function ret=url_relative(href,basehref)
%# if basehref is null, we assume $_SERVER[PHP_SELF], use http::self($href) to obtain full uri
%	if(is_null($basehref)) $basehref=$_SERVER['PHP_SELF'];
%	elseif(is_null($href)) $href=$_SERVER['PHP_SELF'];
if isempty(basehref); ret=href; return; end
if str_isprefix(href,'#'); ret=[basehref href]; return; end
basehref=regexprep(basehref,'\?.*','');
if isempty(strtrim(href)); ret=basehref; return; end
href=strrep(href,'&amp;','&');
href=regexprep(href,'^\./','');
if regexp_find(href,'^(?:f|ht)tps?://'); ret=href; return; end
if ~str_poschar(basehref,'/'); ret=href; return; end
base=regexp(basehref,'^((?:f|ht)tp.?://)?[^/]+','match','once');
if str_isprefix(href,'/'); ret=[base href]; return; end
if regexp_find(basehref,'^((?:f|ht)tp.?://)?[^/]+/?$'); ret=[base '/' href]; return; end
if regexp_find(basehref,'/$'); ret=[basehref href]; return; end
basefile=io_basename_simple(basehref);
basedir=io_dirname(basehref);
if (str_poschar(basefile,'.')||~str_ispostfix(basehref,'/')) && ~regexp_find(href,'^[\?#]'); ret=[basedir '/' href]; return; end
ret=[basehref '/' href];
%<func_embed_end:url_relative.m>

%---------------------------------------------------------
%<func_embed_begin:zoz_install.m>
function zoz_install(varargin)
% copy files that were downloaded as a zip file. Information is assumed to
% be contained in [sys_userpath '/' func '.m']
% make sure this function is self-contained.
% Copyright (C) 2018 by Ahmet Sacan
o=struct( ...
	'echo',sys_issacan ...
);
for i=1:2:numel(varargin)-1
	o.(varargin{i})=varargin{i+1};
end


evalin('caller','save(''.zoz_install_caller.mat'');');  evalin('caller','clear;');
evalin('base','save(''.zoz_install_base.mat'');');  evalin('base','clear;');
clear mex;

zozinstallmatfile=[sys_userpath '/.zoz_install.mat'];
if isempty(dir(zozinstallmatfile))
	error(sprintf('Missing installation file %s.',zozinstallmatfile));
end
load(zozinstallmatfile,'files','topdir','plibmatlabfolder');


%% remove all the paths that are under plibmatlabfolder
if plibmatlabfolder(end)~='/'; plibmatlabfolder=[plibmatlabfolder '/']; end
oldpaths=split(path,pathsep);
temppaths={};
for i=1:numel(oldpaths)
	oldpath=oldpaths{i};
	oldpath=strrep(oldpath,'\','/');
	if oldpath(end)~='/'; oldpath=[oldpath '/']; end
	if ~strncmp(oldpath,plibmatlabfolder,numel(plibmatlabfolder))
		temppaths{end+1}=oldpath;
	end
end


hwait=handle(findall(0,'type','figure','tag','TMWWaitbar','name','zoz_download'));
if ~isempty(hwait); hwait=hwait(1); end
if isempty(hwait); hwait=waitbar(0,'Installing files...','name','zoz_download','CreateCancelBtn','setappdata(gcbf,''canceling'',1)'); end

oldpwd=pwd;
cd(sys_userpath);

backupdir = [sys_userpath '/.zoz_download.backup'];
if topdir(end)~='/'; topdir(end+1)='/'; end
if plibmatlabfolder(end)~='/'; plibmatlabfolder(end+1)='/'; end
%% move over the files
for i=1:numel(files)
	file=files{i};
	if getappdata(hwait,'canceling'); fprintf('Installation interrupted by user.\n'); delete(hwait); return; end
	
	src = [topdir file];
	if strncmp(file,'lib/',4); dst=[plibmatlabfolder file(5:end)];
	elseif numel(files)==1;  dst=[plibmatlabfolder file];
	else dst=[plibmatlabfolder '../' file]; end
	
	if io_isdir(src); mkdir(dst); continue; end
	[dstfolder]=fileparts(dst);
	if ~io_isdir(dstfolder); mkdir(dstfolder); end
	if ~io_isfile(src); fprintf('--- WARNING: Source file %s does not exist. Perhaps it was already installed.\n', src); continue; end
	
	try
		if io_isfileext(src,'p,lic,dll,mexw32,mexw64,mexmaci64,mexa64'); obackup=false; end %dont backup binary files.
		copied=io_copyfile_simple(src,dst,struct('echo',o.echo,'move',1,'skipsame',1,'backupdir',obackup,'deleteemptysrcdir',1));
		if copied; waitbar((i-1)/numel(files),hwait,sprintf('Installing file: %s',file)); end
	catch me
		cd(oldpwd);
		path(strjoin(oldpaths,pathsep));
		rethrow(me);
	end
end
delete(hwait);

cd(oldpwd);
path(strjoin(oldpaths,pathsep));
evalin('base','load(''.zoz_install_base.mat'');'); delete('.zoz_install_base.mat');
evalin('caller','load(''.zoz_install_caller.mat'');'); delete('.zoz_install_caller.mat');

delete(zozinstallmatfile);
%<func_embed_end:zoz_install.m>

%---------------------------------------------------------
%<func_embed_begin:io_basename_simple.m>
function [ret]=io_basename_simple(path)
% Copyright (C) 2018 by Ahmet Sacan

[dir,name,ext]=fileparts(path);
ret=[name ext];
%<func_embed_end:io_basename_simple.m>

%---------------------------------------------------------
%<func_embed_begin:io_dirname.m>
function ret=io_dirname(path)
% Copyright (C) 2008 by Ahmet Sacan
if iscell(path); ret=cellfun(@io_dirname,path,'UniformOutput',0); return; end

%remove the trailing /
path=regexprep(path,'([^/\\])[/\\]+$','$1');
[ret]=fileparts(path);
ret=strrep(ret,'\','/');
if isempty(ret); ret='.'; end
%<func_embed_end:io_dirname.m>

%---------------------------------------------------------
%<func_embed_begin:str_poschar.m>
function [pos]=str_poschar(str,c)
% return location of first occurence of character c (or 0 if it is not
% present). c can contain more than one character. The first occurrence will be returned.
% Copyright (C) 2010 by Ahmet Sacan

if numel(c)>1
	I=false(size(str));
	for i=1:numel(c)
		I=I|str==c(i);
	end
	pos=find(I,1);
else
	pos=find(str==c,1);
end
if isempty(pos); pos=0; end
%<func_embed_end:str_poschar.m>

%---------------------------------------------------------
%<func_embed_begin:regexp_find.m>
function [ret,toks]=regexp_find(s,pattern,varargin)
% Copyright (C) 2012 by Ahmet Sacan
if size(s,1)>1&&size(s,2)==1; s=s'; end

if nargout>1
  [ret toks]=regexp(s,pattern,'once','start','tokens',varargin{:});
else
  ret=regexp(s,pattern,'once',varargin{:});
end
if isempty(ret); ret=0;
elseif iscell(ret)
	for i=1:numel(ret); if isempty(ret{i}); ret{i}=0; end; end
	ret=cell2mat(ret); %this was commented out for some reason (possibly b/c we were previously returning false&numeric mixed, preventing cell2mat). it's more convenient if it is a numeric array.
end
%<func_embed_end:regexp_find.m>

%---------------------------------------------------------
%<func_embed_begin:str_ispostfix.m>
function ret=str_ispostfix(str,pre)
% TODO: move to mex file, similar to str_isprefix
% Copyright (C) 2009 by Ahmet Sacan

%if isempty(str); ret=isempty(pre); return; end
if isempty(pre); ret=true; return; end;
if numel(pre)>numel(str); ret=false; return; end
ret=all(str(end-numel(pre)+1:end)==pre);
%<func_embed_end:str_ispostfix.m>

%---------------------------------------------------------
%<func_embed_begin:io_copyfile_simple.m>
function ret=io_copyfile_simple(src,dst,o)
% this only works for copying files (not folders)
% backupdir must be 'false' or a path to store overridden files/folders.
% skipsame=true: we check contents and if they are the same, we don't
% bother with copy (so the filemtime of dst won't change)
% Copyright (C) 2018 by Ahmet Sacan
if ~exist('o','var'); o=struct; end
if ~isfield(o,'move'); o.move=false; end %move instead of copy
if ~isfield(o,'deleteemptysrcdir'); o.deleteemptysrcdir=false; end %after a move, should we delete the containing folder if it now became empty?
if ~isfield(o,'skipsame'); o.skipsame=true; end
if ~isfield(o,'backupdir'); o.backupdir=false; end
if ~isfield(o,'nextnonexistent'); o.nextnonexistent=false; end
if ~isfield(o,'echo'); o.echo=true; end
if o.echo&&~isfield(o,'echoprompt'); if o.move; o.echoprompt='moving'; else o.echoprompt='copying'; end; end

if islogical(o.backupdir)&&~o.backupdir; usebackupdir=false;
elseif ischar(o.backupdir); usebackupdir=true;
else error('backupdir argument should be a path or false'); end

if o.nextnonexistent && usebackupdir; error('Only one of backupdir or nextnonexistent should be provided.'); end

if ~io_isfile(src); error(sprintf('Source file %s does not exist.', src)); end
if io_isdir(dst);	error(sprintf('Destination file [%s] already exists as a folder. Refusing to copy a file to folder destination.', dst)); end

ret=false;
if io_isfile(dst)
	src=strrep(src,'\','/');
	dst=strrep(dst,'\','/');
	if strcmp(src,dst); return; end
	
	srcinfo=dir(src);
	dstinfo=dir(dst);
	if o.skipsame
		if srcinfo.bytes==dstinfo.bytes
			srctxt=fileread(src);
			dsttxt=fileread(dst);
			if numel(srctxt)==numel(dsttxt)&&all(srctxt==dsttxt)
				if o.move; delete(src); if o.deleteemptysrcdir&&numel(dir(fileparts(src)))==2; rmdir(fileparts(src)); end; end
				return;
			end
		end
	end
	if o.nextnonexistent
		[dstdir,dstname,dstext]=fileparts(dst);
		i=1;
		while true
			dst=[dstdir '/' dstname '.' int2str(i) dstext];
			if ~io_isfile(dst)&&~io_isdir(dst); break; end
			if o.skipsame
				dstinfo=dir(dst);
				if srcinfo.bytes==dstinfo.bytes
					if ~exist('srctxt','var'); 	srctxt=fileread(src); end
					dsttxt=fileread(dst);
					if numel(srctxt)==numel(dsttxt)&&all(srctxt==dsttxt)
						if o.move; delete(src); if o.deleteemptysrcdir&&numel(dir(fileparts(src)))==2; rmdir(fileparts(src)); end; end
						return;
					end
				end
			end
			i=i+1;
		end
	elseif usebackupdir
		if ~io_isdir(o.backupdir); mkdir(o.backupdir); end
		[dstdir,dstname,dstext]=fileparts(dst);
		inbackup=[o.backupdir '/' dstname dstext];
		io_copyfile_simple(dst,inbackup,struct('move',false,'echoprompt','backingup','skipsame',true,'backupdir',false,'nextnonexistent',true));
	end
end

if o.echo; fprintf('%s: %s --> %s\n',o.echoprompt,src,dst); end
if o.move
	movefile(src,dst);
	if o.deleteemptysrcdir&&numel(dir(fileparts(src)))==2; rmdir(fileparts(src)); end
else
	copyfile(src,dst);
end
ret=true;
%<func_embed_end:io_copyfile_simple.m>

%---------------------------------------------------------
%<func_embed_begin:io_isfileext.m>
function [ret]=io_isfileext(file,ext)
% Copyright (C) 2012 by Ahmet Sacan
if iscell(file); ret=cellfun(@(f)io_isfileext(f,ext),file,'UniformOutput',true); return; end
if ischar(ext)&&str_pos(ext,','); ext=cell_csv(ext); end
if iscell(ext); ret=any(cellfun(@(e)io_isfileext(file,e),ext,'UniformOutput',true)); return; end

ext=str_ensureprefix(ext,'.');
ret=str_ispostfixi(file,ext);
%<func_embed_end:io_isfileext.m>

%---------------------------------------------------------
%<func_embed_begin:sys_issacan.m>
function [ret]=sys_issacan(varargin)
% Copyright (C) 2012 by Ahmet Sacan
ret=regexp_find(sys_computername,'^sacan');
%<func_embed_end:sys_issacan.m>

%---------------------------------------------------------
%<func_embed_begin:cell_csv.m>
function [s]=cell_csv(s)
%convert a comma delimited string to a cell array of items.
% Copyright (C) 2012 by Ahmet Sacan
if ~ischar(s); return; end
s=str_explodebychar(s,',');
%<func_embed_end:cell_csv.m>

%---------------------------------------------------------
%<func_embed_begin:str_ensureprefix.m>
function [s]=str_ensureprefix(s,pre)
% Copyright (C) 2012 by Ahmet Sacan
if iscell(s)
	dbg_warnonce('use strs_ensureprefix() instead.');
	for i=1:numel(s); s{i}=str_ensureprefix(s{i},pre); end
else
	if ~str_isprefix(s,pre); s=[pre s]; end
end
%<func_embed_end:str_ensureprefix.m>

%---------------------------------------------------------
%<func_embed_begin:str_ispostfixi.m>
function [ret]=str_isprefixi(str,pre)
% Copyright (C) 2012 by Ahmet Sacan
ret=str_ispostfix(lower(str),lower(pre));
%<func_embed_end:str_ispostfixi.m>

%---------------------------------------------------------
%<func_embed_begin:str_explodebychar.m>
function [ret]=str_explodebychar(s,delim)
% explodes the string s by the single delimiter character and returns a cell array.
% prefer this over str_explode when splitting with a single character and you
% don't need additional functionality as in str_explode()
% Matlab now has strsplit(). but this code is much faster. :) If you do use
% strsplit, you may want to use 'CollapseDelimiters',false option.
% TODO: move to a mex file.
% Copyright (C) 2012 by Ahmet Sacan

if isempty(s); ret={}; return; end
I=find(s==delim);
if isempty(I); ret={s}; return; end
ret=cell(1,numel(I)+1);
ret{1}=s(1:I(1)-1);
for i=1:numel(I)-1
  ret{i+1}=s(I(i)+1:I(i+1)-1);
end
ret{numel(I)+1}=s(I(end)+1:end);
%<func_embed_end:str_explodebychar.m>

%---------------------------------------------------------
%<func_embed_begin:dbg_warnonce.m>
function [ret]=dbg_warnonce(cond,msg,cutlevels)
% Copyright (C) 2012 by Ahmet Sacan
if ischar(cond)&&~exist('msg','var'); msg=cond; cond=true; end
if ~exist('cutlevels','var'); cutlevels=0; end
dbg_warn(cond,msg,true,cutlevels+1);
%<func_embed_end:dbg_warnonce.m>

%---------------------------------------------------------
%<func_embed_begin:dbg_warn.m>
function dbg_warn(cond,msg,once,cutlevels)
% Copyright (C) 2010 by Ahmet Sacan

persistent MSGS;
if ischar(cond)
  if ~exist('msg','var'); msg=cond; cond=true;
  elseif islogical(msg)&&~exist('once','var'); once=msg; msg=cond; cond=true; end
end
if ~cond; return; end
if ~exist('once','var'); once=false; end
if ~exist('cutlevels','var'); cutlevels=0; end
if ~exist('msg','var'); msg=''; end
msg=str_eol(msg);
isnotice=strcmp(dbg_callername,'dbg_note');
if isnotice; s='--- NOTICE:'; cutlevels=cutlevels+1;
else s='--- WARNING:'; end
s=sprintf('%s at %s : ',s,dbg_stack(true,[],cutlevels+1));
if numel(regexprep(s,'<[^>]+>',''))+numel(msg)>=80; s(end+1)=eol; end
if once
	if isempty(MSGS); MSGS=containers.Map; end
	hash=msg; if numel(hash)>1000; hash=hash(1:1000); end
  if MSGS.isKey(hash); return; end
  MSGS(hash)=true;
end
fprintf('%s%s',s,msg);
%<func_embed_end:dbg_warn.m>

%---------------------------------------------------------
%<func_embed_begin:dbg_callername.m>
function name=dbg_callername(cutlevels,varargin)
% Copyright (C) 2011 by Ahmet Sacan
if ~exist('cutlevels','var'); cutlevels=0; end
st=dbg_caller(cutlevels+1,varargin{:});
if isempty(st); name='';
else name=st.name; end
%<func_embed_end:dbg_callername.m>

%---------------------------------------------------------
%<func_embed_begin:dbg_stack.m>
function varargout=dbg_stack(usehtml,st,cutlevels)
%TODO: rename this to dbg_trace
% return a nice printable stack information
% Copyright (C) 2008 by Ahmet Sacan
if ~exist('usehtml','var')||isempty(usehtml); usehtml=sys_isdeployed&&matlab_isdesktop;
elseif isstruct(usehtml)&&~exist('st','var');
  st=usehtml;
  usehtml=true;
end
if ~exist('cutlevels','var'); cutlevels=0; end
if ~exist('st','var')||(isnumeric(st)&&isempty(st));
  [st,i] = dbstack('-completenames');
  if numel(st)>1; st=st(2:end); end
end
if cutlevels; st=st(cutlevels+1:end); end
ret='';
for i=1:numel(st)
	if i>1; ret=[ret ', ']; end
  if usehtml
    ret=[ret sprintf('<a href="matlab: opentoline(''%s'', %d)">%s:%d</a>' ...
    ,st(i).file,st(i).line,io_basename(st(i).file),st(i).line)];
  else
    ret=[ret sprintf('%s:%d' ...
    ,io_basename(st(i).file),st(i).line)];
  end
end
if nargout; varargout{1}=ret;
else fprintf('%s\n',ret); end

function file=io_basename(path)
[~,name,ext]=fileparts(path);
file=[name ext];
%<func_embed_end:dbg_stack.m>

%---------------------------------------------------------
%<func_embed_begin:eol.m>
function s=eol()
%return a new line character.
% Copyright (C) 2006 by Ahmet Sacan
%s=sprintf('\n');
s=char(10);
%<func_embed_end:eol.m>

%---------------------------------------------------------
%<func_embed_begin:str_eol.m>
function [s]=str_eol(s)
% Copyright (C) 2012 by Ahmet Sacan
%s=str_ensurepostfix(s,eol);
if ~isempty(s)&&s(end)~=10; s=[s 10]; end
%<func_embed_end:str_eol.m>



%---------------------------------------------------------
%<func_embed_begin:dbg_caller.m>
function ret=dbg_caller(cutlevels,ignorefuncs)
% usage: dbg_caller(1,{'cache_load','cache_save'})
% Copyright (C) 2011 by Ahmet Sacan
if ~exist('cutlevels','var'); cutlevels=0; end

ret=[];
st=dbstack('-completenames');
if exist('ignorefuncs','var');
  for i=numel(st):-1:1
    if any(strcmp(ignorefuncs,st(i).name))
      st(i)=[];
    end
  end
end
if numel(st)>=3+cutlevels; ret=st(3+cutlevels); end
%<func_embed_end:dbg_caller.m>


%---------------------------------------------------------
%<func_embed_begin:matlab_isdesktop.m>
function [ret]=matlab_isdesktop()
%return whether matlab is running in desktop mode (not with -nodesktop)
% Copyright (C) 2012 by Ahmet Sacan
% I don't know if things change, so let's store the result of the first
% call.

% 20140100:i think this is enough
ret=usejava('desktop')&&usejava('jvm');

% menu() function uses "matlab.ui.internal.isFigureShowEnabled()", but that
% still gives true in "-nodesktop".

%{
%before 2014:
persistent ret2;
if ~usejava('desktop')||~usejava('jvm'); ret2=false; end

if isempty(ret2)
  ret2=false;
  for i=1:1 %for loop is here so we can 'break'
    if sys_issystemuser; break; end
    if ~ret2; myfprintf('haseditor? ');
      %ret2=~com.mathworks.mlservices.MLEditorServices.getEditorApplication.getOpenEditors().isEmpty();
    end
    if ~ret2; myfprintf('hascommandwindow? ');
      pause(3);
      ret2=~isempty(com.mathworks.mlservices.MatlabDesktopServices.getDesktop.getGroupMembers('Command Window'));
    end
  end
end
ret=ret2;
%}

%{
if isempty(ret2)
	ret2=false;
	gs2=com.mathworks.mlservices.MatlabDesktopServices.getDesktop.getGroupTitles();
	gs=cell(1,numel(gs2)+1);
	for i=1:numel(gs2); gs{i}=char(gs2(i)); end
	gs=[{'Command Window'} gs];
	for i=1:numel(gs);
		myfprintf('%s? ',gs{i});
		ret2=~isempty(com.mathworks.mlservices.MatlabDesktopServices.getDesktop.getGroupMembers(gs{i}));
	end
	if ~ret2; myfprintf('hasmainframe? ');
		ret2=com.mathworks.mlservices.MatlabDesktopServices.getDesktop.hasMainFrame; end
	if ~ret2; myfprintf('getmainframe? ');
		ret2=~isempty(com.mathworks.mlservices.MatlabDesktopServices.getDesktop.getMainFrame); end
	if ~ret2; myfprintf('haseditor? ');
		ret2=~com.mathworks.mlservices.MLEditorServices.getEditorApplication.getOpenEditors().isEmpty(); end
else
	myfprintf('persistent? ');
end
myfprintf('ret=%d\n',ret2);
ret=ret2;
%}

%function myfprintf(varargin)
%fprintf(varargin{:});
%<func_embed_end:matlab_isdesktop.m>

%---------------------------------------------------------
%<func_embed_begin:sys_isdeployed.m>
function oldval=sys_isdeployed(newval)
% same as isdeployed(), except it can be controlled.
% Copyright (C) 2011 by Ahmet Sacan
persistent theval;
if isempty(theval); theval=isdeployed; end
oldval=theval;
if exist('newval','var'); theval=newval; end
%<func_embed_end:sys_isdeployed.m>
