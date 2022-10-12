function [seq]=int2aa(num,varargin)
% replicates matlab's int2aa(), with basic functionality.
% num can be a single number or a vector of numbers.
% Copyright (C) 2020 by Ahmet Sacan

map='ARNDCQEGHILKMFPSTWYVBZX*-';
seq=blanks(numel(num));
I=num>=1 & num<=numel(map);
seq(I) = map(num(I));
seq(~I) = '?';
	