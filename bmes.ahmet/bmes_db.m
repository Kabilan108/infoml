classdef bmes_db
	% This is a very limited version of zdb() class.
	%Ahmet Sacan.
	properties
		db=[];
		driver=''; %sqlite|database|sqlitemex|bmessqlitemex|zdb
	end
	methods
		function d=bmes_db(dsn,driver,create)
			if exist('driver','var')&&strcmpi(driver,'create'); create=true; clear('driver'); end
			if exist('driver','var')&&islogical(driver); create=driver; clear('driver'); end
			if ~exist('create','var'); create=true; end
			
			if exist('driver','var'); d.driver=driver; end
			if isempty(dir(dsn))
				whichdsn=which(dsn);
				if isempty(whichdsn);
					if create; f=fopen(dsn,'w'); fclose(f);
					else error(sprintf('Database file [%s] does not exist. Provide full path to the file or add its container folder to your path.',dsn)); end
				else
					dsn=whichdsn;
				end
			end
			
			%try to create zdb(). If it fails, we'll replicate some of the basic
			%functions here.
			if isempty(d.driver)||strcmp(d.driver,'zdb')
				if isempty(dir(dsn)); f=fopen(dsn,'w'); fclose(f); end
				if any(exist('zdb')==[2 5 3])
					try
						driverfunc=str2func('zdb'); %we don't want zdb to be detected as a dependency; we only want to use it if it is available..
						d.db=driverfunc(dsn);
						d.db.connect;
						d.driver='zdb';
					catch me
						fprintf('--- WARNING: I got error when using zdb(). I will try database()...\nThe error was: %s\n',me.message);
						d.driver='';
					end
				elseif strcmp(d.driver,'zdb')
					fprintf('--- WARNING: You do not have the zdb library installed (or it is not on your Matlab Path). Trying other drivers..');
					d.driver='';
				end
			end
			if isempty(d.driver)||strcmp(d.driver,'bmessqlitemex')
				if any(exist('bmessqlitemex')==[3])
					d.db=bmessqlitemex('open',dsn);
					d.driver='bmessqlitemex';
				elseif strcmp(d.driver,'bmessqlitemex')
					error(sprintf('bmessqlitemex.%s not available.',mexext));
				end
			end
			if isempty(d.driver)||strcmp(d.driver,'database')
				if any(exist('database')==[2 5 3])
					try
						jarfilename='sqlite-jdbc-3.32.3.2.jar';
						jarfile=[tempdir '/' jarfilename];
						if isempty(dir(jarfile))
							url=['https://github.com/xerial/sqlite-jdbc/releases/download/3.32.3.2/' jarfilename];
							fprintf('--- NOTICE: downloading sqlite jdbc file: %s...\n',url);
							urlwrite(url,jarfile);
						end
						warning('off','MATLAB:Java:DuplicateClass');
						%javaclasspath(unique([javaclasspath('-dynamic'); jarfile],'stable'));
						javaaddpath(jarfile);
						d.db=database('','','','org.sqlite.JDBC',['jdbc:sqlite:' dsn]);
						d.driver='database';
					catch me
						fprintf('--- WARNING: I got error when using database(). I will use bmesdb() with limited features...\nThe error was: %s\n',me.message);
						d.driver='';
					end
				elseif strcmp(d.driver,'database')
					fprintf('--- WARNING: You do not have the Matlab Database toolbox installed. Switching to sqlite.mex driver..');
					d.driver='';
				end
			end
			if isempty(d.driver)||strcmp(d.driver,'sqlitemex')
				if any(exist('sqlitemex')==[3])
					d.db=sqlitemex('open',dsn);
					d.driver='sqlitemex';
				elseif strcmp(d.driver,'sqlitemex')
					error(sprintf('sqlitemex.%s not available.',mexext));
				end
			end
			if isempty(d.driver)||strcmp(d.driver,'sqlite')
				if any(exist('sqlite')==[2 5 6]);
					d.db=sqlite(dsn);
					d.driver='sqlite';
				elseif strcmp(d.driver,'sqlite')
					if verLessThan('matlab', '9'); error('sqlite() function is not found. Your Matlab version needs to be at least 2016a. Please update your Matlab.');
					else error('sqlite() not found. You may need to install Matlab''s Database Toolbox.?'); end
				end
			end
		end
		function d=delete(d)
			if strcmp(d.driver,'sqlite'); d.db.close; end
		end
		
		function ret=query(d,sql,varargin)
			if strcmp(d.driver,'zdb')
				ret=d.db.query(sql,varargin{:});
			elseif strcmp(d.driver,'bmessqlitemex')
				ret=bmessqlitemex(d.db,sql,varargin{:});
			elseif strcmp(d.driver,'sqlitemex')
				ret=sqlitemex(d.db,sql,varargin{:});
			elseif strcmp(d.driver,'database')
				res=d.db.exec(sql);
				meta=res.ResultSet.getMetaData; %we get to retrieve columnnames before fetch(). otherwise sqlite-jdbc gives error (possibly b/c it clears result after a fetch).
				fs=cell(1,meta.getColumnCount());
				for fi=1:numel(fs); fs{fi}=char(meta.getColumnLabel(fi)); end
				for fi=1:numel(fs); fs{fi}=regexprep(fs{fi},'[^a-zA-Z0-9_]','_'); end
				es=res.fetch.Data;
				ret=cell2struct(es,fs,2);
			else %using matlab's sqlite mex.
				persistent runonce;
				es=d.db.fetch(sql);
				if istable(es) %newer versions of matlab (>=2022?) now return a table object.
					ret=table2struct(es);
				else
					if isempty(runonce)
						fprintf('--- WARNING: Using limited database functionality where columnames are not available.\nWe will use fake columnnames col1,col2,col3, etc. when needed.');
						runonce=1;
					end
					if isempty(es);
						ret=struct; ret(1)=[];
					else
						fs=cell(1,size(es,2));
						for fi=1:numel(fs); fs{fi}=sprintf('col%d',fi); end
						ret=cell2struct(es,fs,2);
					end
				end
			end
		end
		function ret=getone(d,sql,varargin)
			if strcmp(d.driver,'zdb')
				ret=d.db.getone(sql,varargin{:});
			else
				ret=d.query(sql,varargin{:});
				fs=fieldnames(ret);
				ret=ret(1).(fs{1});
			end
		end
		function ret=getcol(d,sql,varargin)
			if strcmp(d.driver,'zdb')
				ret=d.db.getcol(sql,varargin{:});
			else
				ret=d.query(sql,varargin{:});
				if isempty(ret); return; end
				ret=struct2cell(ret)';
				ret=ret(:,1);
				if all(cellfun(@isnumeric,ret,'UniformOutput',1)); ret=cell2mat(ret); end
			end
		end

		%this returns the results as a cell array. available to match matlab's sqlite()'s signature.
		function ret=fetch(d,sql)
			if strcmp(d.driver,'zdb')||strcmp(d.driver,'sqlitemex')||strcmp(d.driver,'bmessqlitemex')
				ret=d.query(sql);
				ret=struct2cell(ret)';
			elseif strcmp(d.driver,'database')
				res=d.db.exec(sql);
				ret=res.fetch.Data;
			else %using matlab's sqlite mex.
				ret=d.db.fetch(sql);
			end
		end		
		%this returns the results as a cell array. available to match matlab's sqlite()'s signature.
		function exec(d,sql)
			if strcmp(d.driver,'zdb');
				d.db.query(sql);
			elseif strcmp(d.driver,'sqlitemex')
				sqlitemex(d.db,sql);
			elseif strcmp(d.driver,'bmessqlitemex')
				bmessqlitemex(d.db,sql);
			elseif strcmp(d.driver,'database')
				d.db.exec(sql);
			else %using matlab's sqlite mex.
				d.db.exec(sql);
			end
		end
		
		%this returns the results as a cell array. available to match matlab's sqlite()'s signature.
		function close(d)
			if strcmp(d.driver,'zdb');
				d.db.disconnect();
			elseif strcmp(d.driver,'bmessqlitemex')
				bmessqlitemex(d.db,'close');
			elseif strcmp(d.driver,'sqlitemex')
				sqlitemex(d.db,'close');
			else %database or sqlite()
				d.db.close();
			end
		end
		%available to match matlab's sqlite()'s signature.
		function insert(d,tablename,colnames,row)
			if isa(row,'table'); row=table2cell(row); end
			if strcmp(d.driver,'zdb')
				d.db.table(tablename).insert(cell2struct(row,colnames));
			elseif strcmp(d.driver,'sqlitemex')||strcmp(d.driver,'bmessqlitemex')
				for i=1:numel(row)
					if isnumeric(row{i})||islogical(row{i})
						if isempty(row{i}); row{i}='null';
						else row{i}=num2str(row{i}); end
					elseif ischar(row{i});
						row{i}=strrep(row{i},'\','\\');
						row{i}=strrep(row{i},'"','\"');
						row{i}=['"' row{i} '"'];
					else
						error(sprintf('Unsupported data type: %s',evalc('disp(row{i})')));
					end
				end
				sql=sprintf('INSERT INTO %s(%s) VALUES(%s)',tablename,strjoin(colnames,','),strjoin(row,','));
				if strcmp(d.driver,'sqlitemex'); sqlitemex(d.db,sql);
				elseif strcmp(d.driver,'bmessqlitemex'); bmessqlitemex(d.db,sql);
				else error('not supposed to get here.'); end					
			elseif strcmp(d.driver,'database')
				d.db.datainsert(tablename,colnames,row);
			else %using matlab's sqlite mex.
				d.db.insert(tablename,colnames,row);
			end
		end
		
		function nodisp(d)
			fprintf('You don''t want to know.');
		end
		
	end
end