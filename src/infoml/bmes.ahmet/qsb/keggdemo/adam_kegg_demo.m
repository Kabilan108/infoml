%% KEGG Demo
% Adam Craig, 2021-04-21:
% 
% In this demo, we donwload a protein-protein interaction network,
% plot the network,
% use Infomap to find putative modules within the network,
% plot the individual modules,
% and list the genes in each module.
% We make extensive use of MATLAB's graph and network methods.
% Read more about them here:
% https://www.mathworks.com/help/matlab/graph-and-network-algorithms.html

%% Additional Resources
% For detailed information about networks and how they are modeled, see:
%   http://www.networksciencebook.com/
% For KEGG Pathways, see:
%   https://www.kegg.jp/
% Interactome:
%   http://interactome.dfci.harvard.edu/C_elegans/index.php?page=download
% https://www.mathworks.com/help/matlab/graph-and-network-algorithms.html
% https://www.mapequation.org/infomap/#Install
% https://david.ncifcrf.gov/summary.jsp


%% Download and plot the PPI network
% Download C. elegans PPI network based on yeast 2-hybrid assay from
% Simonis, N., Rual, J. F., Carvunis, A. R., Tasan, M., Lemmens, I.,
% Hirozane-Kishikawa, T., ... & Vidal, M. (2009).
% Empirically controlled mapping of the Caenorhabditis elegans
% protein-protein interactome network. Nature methods, 6(1), 47-54.

% data = webread('http://interactome.dfci.harvard.edu/C_elegans/graphs/sequence_edges/wi2007.txt');
% numcols = 2;
data = webread('http://interactome.dfci.harvard.edu/C_elegans/graphs/sequence_edges/wi8.txt');
numcols = 5;
% Parse the file.
cellsrow = strsplit(data,{'\n','\t'},'CollapseDelimiters',false);
% We omit the column headers, since we do not need them.
% We also omit the empty cell strsplit leaves at the end.
cells = reshape( cellsrow(numcols+1:end-1), numcols, [] )';
% Create the graph.
G = graph( cells(:,1), cells(:,2) );
% Plot the graph.
figure
plot(G)
title('full C. elegans PPI network')

%% Extract the largest connected component

[bins,binsizes] = conncomp(G);
[~, maxbin] = max(binsizes);
Gcc = subgraph(G,bins == maxbin);
figure
plot(Gcc)
title('largest connected component of C. elegans PPI network')
% Print out some info about how much of the network is in this component.
N = numnodes(G);
M = numedges(G);
Ncc = numnodes(Gcc);
Mcc = numedges(Gcc);
fprintf('The largest connected component has %u of %u genes (%.1f%%) and %u of %u interactions (%.1f%%).\n', ...
    Ncc, N, 100*Ncc/N, Mcc, M, 100*Mcc/M)

%% Find Infomap comunities.
% Infomap is a a command-line utility that finds communities in networks
% based on an information-theoretic approach based on
% how the network topology influnces a random walk on the network.
% It is available here: https://www.mapequation.org/infomap/#Install

% Write the edge list of the connected component to a file.
% The endpoints will be given as numeric indices, not gene names.
% This is what Infomap expects,
% but it means we will need to go back into MATLAB to get gene names.

[s, t] = findedge(Gcc);
edgefile = 'edges.txt';
writematrix([s, t],edgefile,'FileType','text','Delimiter','\t');
% -i link-list tells Infomap the input format is a list of edges.
% -o clu tells Infomap the output format is a single-level partitioning
% into communities.
system( sprintf('infomap -i link-list -o clu %s .', edgefile) )

% Infomap automatically names the output file based on the input file.
clufile = strrep(edgefile,'.txt','.clu');
infomapclu = readmatrix(clufile,'FileType','text','CommentStyle','#');
% Convert these community assignments into a format where
% community(i) is the community assignment of node i.
I = infomapclu(:,1);
community = zeros( size(I) );
community(I) = infomapclu(:,2);
ucommunity = unique(community);
numcoms = numel(ucommunity);
fprintf('Infomap partitioned the network into %u communities.\n', numcoms)
figure
histogram( categorical(community) )
title('Infomap community sizes')

%% Plot the individual communities, and save them to files.

% Save the list from the largest connected component first.
% We will use this as our list of background genes.
writecell( Gcc.Nodes.Name, 'background.txt' )

for i = 1:numcoms
    com = ucommunity(i);
    isincom = community == com;
    if nnz(isincom) > 1
        Gcom = subgraph(Gcc,isincom);
        % plot
        figure
        plot(Gcom)
        % save
        writecell( Gcom.Nodes.Name, sprintf('community%u.txt',com) )
    end
end
