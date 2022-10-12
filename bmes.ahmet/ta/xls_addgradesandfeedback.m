function outfile=xls_addgradesandfeedback(infile,varargin)
% Note: If this file is found elsewhere, it is just a "slave" copy of
% Ahmet's libmatlab/xls_addgradesandfeedback.m
%
%{
* The Excel file should be formatted in the following ways:
  * Each row represents a student.
  * Each column represents a graded item.
  * Column headers (in the first row) should contain the names/descriptions of
the graded items. These names/descriptions will be compiled into feedback
description for each student.
  * One column should have the column name "grade". This is where the total
  grade for each student will be automatically calculated.
  * One column should have the column name "feedback". This is where a
  detailed break-down of graded items will be compiled.

* Possible points for the graded items can be given in one of these two ways:
   * Provide a row, whose student name is "Weights:" or "Points:". Then have the points
   in each cell for this fake student.
   * Include the points for each graded item in the column names, followed
   by a colon, e.g., "50pt: Correct output".
   * If none of the above is done, we'll assume each graded item is weighed
   equally.
* Possible points can be specified as integers or floating numbers, or
   percentages. The word "pt" is optional. e.g., "0.5", "10pt", "5%" "5percent".
* Using percent sign has problems (because Excel or Matlab interprets them
as number whereas we need them as text). Use e.g. "5percent" instead. Or,
use "x5%".
* Possible bonus points beyond the main graded items can be marked with a
prefix of 'extra+' or 'bonus+' e.g, 'extra+5%'.


* Total Points (typically 10 or 100)  a student can earn can be specified in the following ways:
  * Provide as input argument: xls_addgradesandfeedback(..., 'totalpoints',100)
  * Specify it as the possible points for the "grade" column.
  * If not specified, we'll use totalpoints=100.

* The grade entries for a student's graded item is interpreted either as
a fraction/multiplication of how much a graded item is worth, or as a
direct value of points. This is controlled by the 'isfractional' argument.
You can specify the isfractional argumenta as true or false. e.g.,
xls_addgradesandfeedback(..., 'isfractional',true)
  * If you do not specify the isfractional argument, it will be set to true
  if all of the student grade entries you entered are between 0 and 1; and
  false otherwise.
  * Even when isfractional is false, you can force a particular grade entry
  to be multiplicative by prefixing it with a multiplication or x sign, e.g.,
  "x0.5" or "x50%".
  * Even when isfractional is true, you can force a particular grade entry
  to be direct point values by adding "pt" suffix, e.g., "5pt"
  * If you provide a grade as a percent, e.g. "5percent", it will be used
  as a percent of the totalpoints, not of that graded part.


* The column title for each graded item becomes the feedback for that entry.
If you would like to provide additional details for a student's grade
entry, use their grade followed by colon, followed by additional comments.
e.g., "0.5: You need to report absolute value of the error."

%}
% by Ahmet Sacan (with logic/code contributions by Adam Craig)
o = struct( ...
	'outfile','' ... %defaults to be same as infile
	,'totalpoints',[] ... %if empty, use value available in <Grading row, Grade column>, otherwise use 100.
	,'round',2 ... % round to this many decimal places.
	,'isfractional',[] ... % true|false. if left empty, we'll use true if all student grades are between 0 and 1. Even with non-fractional grading you can use multiplication to  force a particular grade to be fractional. e.g. "*0.5"
	);
for i=1:2:numel(varargin); o.(varargin{i})=varargin{i+1}; end

if ~exist('infile','var')
	infile = 'c:/sim2/exam.20213/.ahmet/bmes673.finalexam.20213.grading.xlsx';
	%infile = 'temp.xlsx';
end

outfile=o.outfile;
if isempty(outfile); outfile = infile; end

% Read & parse the cells
original_cells = readcell(infile);
rs=parsecells(original_cells);
[R,C]=size(original_cells);

%% Identify weights & names rows.
namesrow=1;
% *** Configuration1: 'Weights:' appears in the first row/first column.
Iweights=cellfun(@(x)any(strcmpi({'Weights:','Points:'},x)),{rs.text},'UniformOutput',1);
if any(Iweights,'all')
	[weightsrow,col] = ind2sub([R,C],find(Iweights));
	weightsrow = unique(weightsrow);
	if numel(weightsrow)>1; error('You must have only one row labeled as "Weights:" or "Points:"'); end
	if weightsrow==1; namesrow=2; end
% *** Configuration2: Weights are embedded within the names.
else
	weightsrow = namesrow;
	if all(isnan([rs(weightsrow,:).value])) || isempty([rs(weightsrow,:).comment])
		warning('You need to either mark one of the rows as "Weights:" or embed points within the column names. eg., "10pt: Correct output.". You have done neither. I assume each column is worth equally and/or you specify the points in the student grade entries.');
		for j=1:C
			% Only set weight-value of columns that contain some grade. (ie., avoid
			% assigning grades to Firstname,Lastname,etc. columns).
			if any(~isnan([rs(:,j).value])); rs(weightsrow,j).value=100; end
		end
	end
end
studentrows=1:R;
studentrows([namesrow weightsrow])=[];

%% Identify grade & feedback columns
names = {rs(namesrow,:).comment};
gradecol = find(strcmpi(names,'Grade'));
feedbackcol = find(strcmpi(names,'Feedback'));
if isempty(gradecol)
	original_cells{namesrow,end+1}='Grade';
	gradecol=size(original_cells,2);
	rs(:,gradecol)=parsecells(repmat({''},R,1));
elseif numel(gradecol)>1
	warning('There are multiple columns labeled as "Grade", using the last one.');
	gradecol=gradecol(end);
end
if isempty(feedbackcol)
	original_cells{namesrow,end+1}='Feedback';
	feedbackcol=size(original_cells,2);
	rs(:,feedbackcol)=parsecells(repmat({''},R,1));
elseif numel(feedbackcol)>1
	warning('There are multiple columns labeled as "Feedback", using the last one.');
	feedbackcol=feedbackcol(end);
end

[R,C]=size(original_cells);


%% Identify gradeablecols & penaltycols
rsweights=rs(weightsrow,:);
weights=[rsweights.value];
gradeablecols = true(1,C);
gradeablecols([gradecol feedbackcol]) = false;
gradeablecols(isnan(weights)) = false;
penaltycols = [rsweights.ispenalty];
bonuscols = [rsweights.isbonus];
percentcols = [rsweights.ispercent];

%% Determine totalpoints and weights2points multipliers
sumpointweights=sum(weights(gradeablecols & weights>0 & ~bonuscols & ~percentcols));
sumpercentweights=sum(weights(gradeablecols & weights>0 & ~bonuscols & percentcols));
totalpoints=o.totalpoints;
if isempty(totalpoints)
	%Use value if already present in <weightsrow, grade_column>
	if ~isnan(weights(gradecol))&&weights(gradecol); totalpoints=weights(gradecol);
	else
		if sumpointweights==10; totalpoints=10;
		else totalpoints = 100; end
		if isempty(rs(weightsrow,gradecol).comment); original_cell(weightsrow,gradecol)=totalpoints;
		else original_cell(weightsrow,gradecol)=sprintf('%g: %s',totalpoints,rs(weightsrow,gradecol).comment); end
	end
end

weights2points_multiplier = (totalpoints-sumpercentweights/100*totalpoints)/sumpointweights;
weights_points(~percentcols) = weights(~percentcols)*weights2points_multiplier;
weights_points(percentcols) = weights(percentcols)*totalpoints/100;


%% Check & report missing values.
ss={}; lastr=0;
for i=studentrows
	for j=1:C
		if ~gradeablecols(j)||penaltycols(j)||bonuscols(j)||~weights(j); continue; end
		if isnan(rs(i,j).value)
			if lastr&&lastr~=i; ss{end}=[ss{end} newline]; end
			ss{end+1}=sprintf( '(%u,%u)', i,j);
			lastr=i;
		end
	end
end
if ~isempty(ss)
	fprintf('Warning: The following cells (row,col) are missing or the grades in them cannot be parsed:\n%s\n',strjoin(ss,', '));
end

%% Determine o.isfractional:  if all student grade entries are between [0..1], we assume weights are fractional.
if isempty(o.isfractional)
	rsvals=rs(studentrows, gradeablecols & ~penaltycols & ~bonuscols  & ~[rsweights.iseach]);
	%we'll only use cells with pure-number specification for determination of
	%isfractional.
	rsvals(isnan([rsvals.value])  | [rsvals.ispercent] | [rsvals.ispoints] | [rsvals.isbonus] | [rsvals.isfractional] )=[];
	vals=[rsvals.value];
	o.isfractional=all(abs(vals)<=1);
end



% For each student, compute a grade, and compile a feedback report.
for i=studentrows
	studentpts = 0;
	ss=cell(nnz(gradeablecols));
	for j = find(gradeablecols)
		partname=names{j};
		partpoints=weights_points(j);
		r=rs(i,j);
		if isnan(r.value)&&isempty(r.text)&&isempty(r.comment) && ~partpoints; continue; end

		value=r.value;
		if isnan(value); value=0; end
		if r.ispoints; isfractional=false;
		elseif r.isfractional; isfractional=true;
		elseif r.ispercent; isfractional=false;
		elseif rsweights(j).iseach; isfractional=true;
		else isfractional=o.isfractional && abs(value)<=1; end

		%if i==3 && j==9 &&bmes.sys_issacan; dbg_stop; end
		points=value;
		if isfractional
			if r.ispercent; points=points/100; end
			if points>1 && ~r.isfractional && ~rsweights(j).iseach %only warn if we this is due to o.fractional and not explicitly in student grade entry.
				warning(sprintf('isfractional is set true, but the entry for <%u,%u> "%s" is greater than 1: %s\n', i, j, partname, r.text));
			end
			points = points * partpoints;
		else
			if r.ispercent; points=points/100*totalpoints; end			
		end
		%for penalty cols, make sure the points is a negative grade.
		if penaltycols(j); points=-abs(points); end


		if points==0  && (penaltycols(j)||bonuscols(j)) %don't include penalty/bonus comments in the feedback
			%ss{j}=''; %pass, it is already empty -- nothing to do.
		elseif points==0 && partpoints==0 %for parts that have no grade associated, just show the comment.
			if ~isnan(r.value);
				if r.value==1;     ss{j} = sprintf('* [not graded]: %s',partname);
				elseif r.value==0; ss{j} = sprintf('* ([not graded] 0 out of 0pt): %s',partname);
				else               ss{j} = sprintf('* ([not graded] %g out of 0pt): %s',r.value, partname); end
			else ss{j} = sprintf('* %s',partname); end
		else
			if points<0; signstr='';
			else signstr='+'; end
			if penaltycols(j)
				ss{j} = sprintf('%s%gpt: %s', ...
					signstr, round(points,o.round), partname);
			else
				ss{j} = sprintf('%s%gpt (out of %gpt): %s', ...
					signstr, round(points,o.round), round(partpoints,o.round), partname);
			end				
			studentpts = studentpts + points;
		end
		if ~isempty(r.comment); ss{j} = [ss{j} ' -- ' r.comment]; end
	end

	total_text = sprintf( 'Total: %g', round(studentpts,o.round) );
	original_cells{i,gradecol}=studentpts;
	ss=ss(~cellfun(@isempty,ss,'UniformOutput',1));
	all_lines = [{'Parts:'}; ss; total_text];
	%is_not_empty = cellfun( @(x) ~isempty(x), all_lines );
	%all_lines = all_lines(is_not_empty)
	original_cells{i,feedbackcol}=strjoin( all_lines, newline  );
end


% Save the table with the new columns.
% xlswrite preserves Excel formatting, so let's use that instead.
%writecell(original_cells,out_file_name)
if any(exist('xls_write')==[2 5 6]);
	xls_write(outfile,original_cells);
	if ~nargout; sys_open(outfile); clear outfile; end
else
	xlswrite(outfile,original_cells);
end


%-----------------------------------------------------------------------------
function rs=parsecells(cells)
[R,C]=size(cells);
rs=[];
for i=1:R
	for j=1:C
		s=cells{i,j};
		r = struct('original',s,'value',nan,'text','','isbonus',false,'isfractional',false,'ispercent',false,'ispoints',false,'iseach',false,'comment','');
		if isa(s,'missing'); s=''; end
		if isnumeric(s)
			r.value=s;
			r.text=num2str(s);
			r.comment = '';
		else
			r.text=s;
			r.comment=s;
			e = regexp(s,'^\s*(?:up to\s*)?(?<isbonus>\+?(?:extra|bonus)?)\s*(?<isfractional>[\*x])?(?<value>[\+\-]?(?:x|\d+|\d+\.\d+|\.\d+))\s*(?<ispercent>(?:%|percent))?\s*(?<ispoints>(?:pts?|points?))?\s*(?<iseach>(?:each?))?\s*(?<comment>[: ].*)?$','names','once');
			if ~isempty(e)
				if strcmpi(e.value,'x') %x is a shorthand for "x1"
					e.value='1';
					e.isfractional=1;
				end
				r.value=str2double(e.value);
				r.comment=strtrim(regexprep(e.comment,'^\s*:\s*',''));
				r.isbonus=~isempty(e.isbonus);
				r.isfractional=~isempty(e.isfractional);
				r.ispercent=~isempty(e.ispercent);
				r.ispoints=~isempty(e.ispoints);
				r.iseach=~isempty(e.iseach); %e.g., use " -10percent each" for late penalty, so that the numbers in that column are interpreted as multipliers rather than points.
			end
		end
		r.ispenalty=~isnan(r.value) && r.value<0;
		if isempty(rs); rs=r; else rs(i,j)=r; end
	end
end
