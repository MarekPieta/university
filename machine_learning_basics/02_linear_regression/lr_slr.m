%
%   TOPIC: Simple Linear Regression
%
% ------------------------------------------------------------------------

close all
clearvars

boston = readtable('data/boston.csv');
boston_subset = boston(:, {'MEDV','LSTAT'});

figure(1)
scatter(boston_subset.LSTAT, boston_subset.MEDV)

lm =  fitlm (boston_subset.LSTAT, boston_subset.MEDV)
disp(lm)

coef = coefCI(lm, 0.05)
 
figure(2);

xval = min(boston_subset.LSTAT):0.01:max(boston_subset.LSTAT);
yhat = lm.Coefficients.Estimate(1) + lm.Coefficients.Estimate(2)*xval;
ylow = coef(1,1)+coef(2,1)*xval;
yupp = coef(1,2)+coef(2,2)*xval;
plot(boston_subset.LSTAT,boston_subset.MEDV,'k*');
hold on;
plot(xval,ylow,'r-.');
plot(xval,yupp,'r-.');
plot(xval,yhat,'b','linewidth',2);

figure(3)
plotResiduals(lm,'probability')
