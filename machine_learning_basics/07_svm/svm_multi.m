%
%   TOPIC: Multiclass Support Vector Machines
%
% ------------------------------------------------------------------------

close all
clearvars

%% Load data.

load fisheriris
X = meas(:, 1:2);
Y = species;

%% Fit a model.

rng(1); % For reproducibility

template = templateSVM('KernelFunction', 'rbf');
svm = fitcecoc(X, Y, 'Learners', template, 'FitPosterior', true);

%% Visualize data and the model.

svm.CodingMatrix
%columns - binary learners; rows classes
%each binary learner distinguishes between two classes
%denoted as 1 or -1 in rows for the classes
%(1 vs 1 classification)

Y1 = ismember(Y, 'setosa');
Y2 = ismember(Y, 'versicolor');
Y3 = ismember(Y, 'virginica');

figure(1);
hold on;
plot(X(Y1, 1), X(Y1, 2), 'r*');
plot(X(Y2, 1), X(Y2, 2), 'g*');
plot(X(Y3, 1), X(Y3, 2), 'b*');

step = 0.1;
[newX1, newX2] = meshgrid(min(X(:,1)):step:max(X(:,1)),min(X(:,2)):step:max(X(:,2)));

[values, ~, ~, posterior] = predict(svm, [newX1(:), newX2(:)]);

for i = 1:size(posterior, 2)
   temp_posterior = reshape(posterior(:,i), size(newX1));
   contour(newX1, newX2, temp_posterior, [0.5, 0.5]);
end

legend('Training - class 1', 'Training - class 2', 'Training - class 3');
xlabel('X_1');
ylabel('X_2');