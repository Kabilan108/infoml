function [ret]=numcputhreads()
% Copyright (C) 2021 by Ahmet Sacan

ret=sys_numthreads;

%---------------------------------------------------------
%<func_embed_begin:sys_numthreads.m>
function [ret]=sys_numthreads(varargin)
% Copyright (C) 2017 by Ahmet Sacan

if ispc; ret=getenv('NUMBER_OF_PROCESSORS');
elseif ismac; [~,ret]=system('sysctl -n hw.ncpu');
else ret=getenv('OMP_NUM_THREADS'); end

ret=str2double(ret);
if isnan(ret);
	warning('Failed to get number of threads. Using 2 x num-cores instead');
	ret=2*sys_numcores;
end
%<func_embed_end:sys_numthreads.m>

%---------------------------------------------------------
%<func_embed_begin:sys_numcores.m>
function [numcores]=sys_numcores(varargin)
% Copyright (C) 2017 by Ahmet Sacan

evalc('numcores=feature(''numCores'');');

%{
other options:
import java.lang.*;
r=Runtime.getRuntime;
ncpu=r.availableProcessors
%}
%<func_embed_end:sys_numcores.m>
