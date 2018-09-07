%
%   TOPIC: Support Vector Classifiers
%
% ------------------------------------------------------------------------

close all
clearvars

%% Generate data.

rng(1); % For reproducibility

% Generate data from a normal distribution.
n_cls = 20; % Number of samples in each class.
X = vertcat(...
    horzcat(normrnd(0.5,1, n_cls,1), normrnd(0.4,1, n_cls,1)), ...
    horzcat(normrnd(-0.3,1, n_cls,1), normrnd(-0.5,1, n_cls,1)) ...
    );
Y = vertcat(-1 * ones(n_cls,1), +1 * ones(n_cls,1));

%% Fit a model.
csvm = fitcsvm(X, Y);

%% Make predictions.

newX = [
    1, -0.4;
    1, -0.85
    ];

newY = predict(csvm, newX)

%% Visualize data and the model.

figure(1);
Y1 = Y==-1;
Y2 = Y==1;

newY1 = newY==-1;
newY2 = newY==1;

hold on;
%training data
plot(X(Y1,1), X(Y1,2), 'r*');
plot(X(Y2,1), X(Y2,2), 'b*');
plot(X(csvm.IsSupportVector, 1), X(csvm.IsSupportVector, 2), 'ko')
%perdictions
plot(newX(newY1,1), newX(newY1,2), 'rd');
plot(newX(newY2,1), newX(newY2,2), 'bd');

x_1 = -3:0.01:3;

x_2 = (-csvm.Bias*csvm.KernelParameters.Scale - x_1*csvm.Beta(1))/(csvm.Beta(2));

plot(x_1, x_2, 'k');

legend('Training - class 1', 'Training - class 2', 'Support vectors',...
    'Predicted - class 1', 'Predicted - class 2', 'Decision boundary');
xlabel('X_1');
ylabel('X_2');



%% Get posteriors.
posterior = fitPosterior(csvm, X, Y);
newY_posterior = predict(posterior,newX)
