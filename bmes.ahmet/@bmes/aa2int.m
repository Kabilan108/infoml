function [num]=aa2int(seq,varargin)
% replicates matlab's aa2int() functionality.
% seq can be a single character or a vector of characters.
% Copyright (C) 2020 by Ahmet Sacan

map='ARNDCQEGHILKMFPSTWYVBZX*-';
num=zeros(1,numel(seq),'uint8');
%num(regexp(seq,'[^ARNDCQEGHILKMFPSTWYVBZX\*\-]'))=0; %no need; they are already zero.
for i=1:numel(map)
	num( seq==map(i)) =i;
end
