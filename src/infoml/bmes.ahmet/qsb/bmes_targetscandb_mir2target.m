function [ret]=bmes_targetscandb_mir2target(mirna,scorethreshold,verbose)
% e.g.: 
% bmes_targetscandb_mir2target('hsa-miR-30a',0.9)
% by AhmetSacan

if ~exist('scorethreshold','var'); scorethreshold=0.8; end
if ~exist('verbose','var'); verbose=false; end

dbfile = bmes.downloadurl('http://sacan.biomed.drexel.edu/ftp/binf/targetscandb.sqlite');
d = bmes_db(dbfile,'sqlite');

sql=sprintf('SELECT distinct("generefseqid") FROM "mir2target" WHERE score>=%f AND mirna IN ("%s","%s-3p","%s-5p")',scorethreshold,mirna,mirna,mirna);
if verbose; fprintf('--- SQL: %s\n',sql); end
try
	ret=d.getcol(sql);
catch me
	if ~isempty(regexp(me.message,'The database .* is corrupt','once'))
		fprintf('\n--- ERROR: It appears that your database file did not download correctly.\n   Perhaps your internet connection broke during the download.\n   Delete the following file and try again:\n   %s\n\n',dbfile);
	end
	%rethrow doesn't allow dbstop where the error happens, so we'll rerun the
	%command.
	%rethrow(me);
	ret=d.getcol(sql);
end
