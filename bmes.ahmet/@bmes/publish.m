function outfile=bmes_publish(func, varargin)
% Usage: bmes.publish('myfunction.m')
%
% publish function/script, using Ahmet's default options (format:pdf,
% figureSnapMethod:getframe, imageFormat:jpg, maxOutputLines:100,showCode:true)
% Copyright (C) by Ahmet Sacan

if nargout; outfile=func_publish(func, varargin{:});
else func_publish(func, varargin{:}); end


%---------------------------------------------------------
%<func_embed_begin:func_publish.m>
function [outfile]=func_publish(func,varargin)
% % Usage: func_publish myfunction.m
%
% publish function/script, using Ahmet's default options (format:pdf,
% figureSnapMethod:getframe, imageFormat:jpg, maxOutputLines:100,showCode:true)
%
% Additional options are passed on to publish(): format,stylesheet,outputDir,imageFormat
% ,figureSnapMethod,useNewFigure,maxHeight,maxWidth,showCode,evalCode
% ,stopOnError,catchError,displayError,createThumbnail,maxOutputLines
% ,codeToEvaluate,font,titleFont,bodyFont,monospaceFont,maxThumbnailHeight
% ,maxThumbnailWidth
% Copyright (C) 2016 by Ahmet Sacan

if numel(varargin)==1&&numel(varargin{1})>4&&strcmp(varargin{1}(end-3:end),'.pdf'); varargin=[{'outfile'} varargin]; end

opt=struct('format','pdf', 'figureSnapMethod','getframe','imageFormat','jpg' ...
	,'maxOutputLines',100,'showCode',true,'outfile','');

%% convert any options from varargin into the opt structure.
for i=1:2:numel(varargin)
	name=varargin{i};
	value=varargin{i+1};
	opt.(name)=value;
end

%% if outfile is given, we get the format option from the outfile.
if ~isempty(opt.outfile)
	[~,~,opt.format]=fileparts(opt.outfile);
	opt.format(1)=[]; %remove the period from the extension.
end


%% if an output folder is not provided, use the same folder as the function, (html/ subfolder for html format).
mfile=which(func);
if ~isfield(opt,'outputDir')
	folder=fileparts(mfile);
	if strcmpi(opt.format,'html'); folder=[folder '/html']; end
	opt.outputDir=folder;
end


%% if outfile is given, use a temporary directory so we don't override the default file in the process.
if ~isempty(opt.outfile)
	origoutputdir=opt.outputDir;
	opt.outputDir=tempname;
end

%% convert the opt structure back into cell array form of option1,value1,...
args={};
fields=fieldnames(opt);
for i=1:numel(fields)
	if strcmp(fields{i},'outfile'); continue; end %we don't pass this to publish function. we handle it ourselves below.
	args{end+1}=fields{i};
	args{end+1}=opt.(fields{i});
end


for pass=1:2
	try
		outfile=publish(func,args{:});
		if ~isempty(opt.outfile)
			movefile(outfile,opt.outfile);
			outfile=opt.outfile;
			rmdir(opt.outputDir);
		end
	catch me
		if pass==1 && (strcmp(me.identifier,'MATLAB:publish:FileNotWritable')||strcmp(me.identifier,'MATLAB:MOVEFILE:OSError'))
			disp(me.message);
			if strcmp('Try again',questdlg(sprintf('Output file appears to be open.\nIf you want to try publishing again, close the program using the file and hit the "Try again" button below'),'try publish() again?','Try again','Cancel','Cancel'))
				continue;
			end
		end
		rethrow(me);
	end
end

if ~nargout; open(outfile); end
%<func_embed_end:func_publish.m>
