%
%   TOPIC: Support Vector Machines
%
% ------------------------------------------------------------------------

close all
clearvars

%% Generate data.

rng(1); % For reproducibility

n_cls = 100; % Number of samples in each class.

r = sqrt(rand(n_cls,1)); % Radius
t = 2 * pi * rand(n_cls,1);  % Angle
X_cls1 = [r .* cos(t), r .* sin(t)]; % Points

r2 = sqrt(3 * rand(n_cls,1) + 1); % Radius
t2 = 2 * pi * rand(n_cls,1);      % Angle
X_cls2 = [r2 .* cos(t2), r2 .* sin(t2)]; % points

X = vertcat(X_cls1, X_cls2);
Y = vertcat(-1 * ones(n_cls,1), +1 * ones(n_cls,1));

%% Fit a model.

svm = fitcsvm(X, Y, 'KernelFunction','RBF','BoxConstraint', Inf);

%% Visualize data and the model.
Y1 = Y == -1;
Y2 = Y == 1;

hold on;
%training data
plot(X(Y1,1), X(Y1,2), 'r*');
plot(X(Y2,1), X(Y2,2), 'b*');
plot(X(svm.IsSupportVector, 1), X(svm.IsSupportVector, 2), 'ko')

[newX1, newX2] = meshgrid(-2:0.01:2);
scores = predict(svm, [newX1(:), newX2(:)]);
scores = reshape(scores, size(newX1));
contour (newX1, newX2, scores, [0 0]);


legend('Training - class 1', 'Training - class 2', 'Support vectors',...
     'Decision boundary');
xlabel('X_1');
ylabel('X_2');