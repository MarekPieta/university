%
%   TOPIC: Logistic Regression
%
% ------------------------------------------------------------------------

close all
clearvars

smarket = readtable('data/smarket.csv');
smarket.Direction = categorical(smarket.Direction, {'Up','Down'});
summary(smarket);

%whole dataset
glm = fitglm(smarket, 'Direction~Lag1+Lag2+Lag3+Lag4+Lag5+Volume', 'Distribution', 'binomial');
disp(glm);
yhat = predict(glm, smarket) > 0.5;
yhat = categorical(yhat, [0,1], {'Up', 'Down'});
cp = classperf(cellstr(smarket.Direction), cellstr(yhat));
cp.CountingMatrix
cp.ErrorRate

%only older dataset
is_train = (smarket.Year < 2005);
smarket_train = smarket(is_train,:);
smarket_test = smarket(~is_train,:);

glm = fitglm(smarket_train,'Direction~Lag1+Lag2+Lag3+Lag4+Lag5+Volume', 'Distribution', 'binomial');
disp(glm);
yhat = predict(glm, smarket_test) > 0.5;
yhat = categorical(yhat, [0,1], {'Up', 'Down'});

cp = classperf(cellstr(smarket_test.Direction), cellstr(yhat));
cp.CountingMatrix
cp.ErrorRate

%only older dataset - choosing only some parameters
is_train = (smarket.Year < 2005);
smarket_train = smarket(is_train,:);
smarket_test = smarket(~is_train,:);

glm = fitglm(smarket_train, 'Direction~Lag1+Lag2', 'Distribution', 'binomial');
disp(glm);
yhat = predict(glm, smarket_test) > 0.5;
yhat = categorical(yhat, [0,1], {'Up', 'Down'});

cp = classperf(cellstr(smarket_test.Direction), cellstr(yhat));
cp.CountingMatrix
cp.ErrorRate