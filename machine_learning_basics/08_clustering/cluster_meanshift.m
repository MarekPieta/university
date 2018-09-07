%
%   TOPIC: Mean Shift Clustering
%
% ------------------------------------------------------------------------

close all
clear clc
clearvars

%% Load data.

I = imread('peppers.png');
I = imresize(I, 0.25);

%% Perform mean shift clustering.

[fimg, labels, modes] = edison_wrapper(I, @RGB2Luv, 'SpatialBandWidth', 20, 'RangeBandWidth', 20, ...
'MinimumRegionArea', 500);  % FIXME: implement

%% Visualize results.

I_segm = Luv2RGB(fimg);

BW_boundaries = boundarymask(labels);
BW_boundaries = bwmorph(BW_boundaries, 'thin',Inf);

figure(1); clf(1)
subplot(1,3,1); imshow(I); title('original image');
subplot(1,3,2); imshow(I_segm, []); title('clustered image');
subplot(1,3,3); imshow(imoverlay(I, BW_boundaries, 'g')); title('cluster boundaries')

