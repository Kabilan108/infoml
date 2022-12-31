% 20191214: This loader is obsolete. The recommended method is to use environment variables.
% On Windows do:
%  setx /M BMESAHMETDIR C:/Path/To/bmes.ahmet
% On Mac do:
%  launchctl setenv BMESAHMETDIR /path/to/bmes.ahmet
%  sudo echo "setenv BMESAHMETDIR /path/to/bmes.ahmet" >> /etc/launchd.conf
% Then, in your Matlab code, just do:
% addpath(getenv('BMESAHMETDIR'));


% You can make a copy of this file and place it in your working directory.

%% Add bmes.ahmet/ folder to path
% This file adjusts the Matlab's path so you can use functions available in
% Ahmet's shared dropbox folder. 
% by Ahmet Sacan.

trydir=getenv('BMESAHMETDIR');
if ~isempty(trydir)
	addpath(trydir);
	return
end

% I assume your dropbox folder is located under your home folder. If it is
% not, you will need to hardcode DROPBOX=... to the exact location of your
% dropbox.
if ispc; HOME=getenv('USERPROFILE');
else; HOME=getenv('HOME'); end
DROPBOX=[HOME '/Dropbox'];
%DROPBOX='...'; %Uncomment and fill in this line if necessary.

% I assume bmes.ahmet/ is available under your dropbox. If you moved it
% elsewhere or changed its name, you need to specify that.
BMESAHMETDIR=[DROPBOX '/bmes.ahmet'];
addpath(BMESAHMETDIR);
%BMESAHMETDIR='...'; %Uncomment and fill in this line if necessary.
if isempty(dir([BMESAHMETDIR '/']))
	error(sprintf('bmes.ahmet folder [%s] is missing.',BMESAHMETDIR));
end

