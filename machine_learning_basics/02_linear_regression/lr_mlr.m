%
%   TOPIC: Multiple Linear Regression
%
% ------------------------------------------------------------------------

close all
clearvars


boston = readtable('data/boston.csv');
boston_subset = boston(:, {'LSTAT','AGE', 'MEDV'});

figure(1)
scatter3(boston_subset.LSTAT, boston_subset.AGE, boston_subset.MEDV);
hold on;

lm =  fitlm (boston_subset);
disp(lm)
coef = coefCI(lm, 0.05);

xv = linspace(min(boston_subset.LSTAT), max(boston_subset.LSTAT), 100);
yv = linspace(min(boston_subset.AGE), max(boston_subset.AGE), 100);
[xval,yval] = meshgrid(xv,yv);

zval = lm.Coefficients.Estimate(1) + lm.Coefficients.Estimate(2)*xval + lm.Coefficients.Estimate(3)*yval;
surf(xval, yval, zval);


figure(2);
scatter3(boston_subset.LSTAT, boston_subset.AGE, boston_subset.MEDV);
hold on;
lmm = fitlm(boston_subset, 'MEDV~1+AGE*LSTAT');
disp(lmm);
coef = coefCI(lm, 0.05);
zval = lmm.Coefficients.Estimate(1) + lmm.Coefficients.Estimate(2)*xval + lmm.Coefficients.Estimate(3)*yval + lmm.Coefficients.Estimate(4).*yval.*xval;
surf(xval, yval, zval);

figure(3);
subplot(1,2,1);
scatter(boston_subset.LSTAT, boston_subset.MEDV);
hold on;
lm1 = fitlm(boston_subset, 'MEDV~1+LSTAT+LSTAT^2');
disp(lm1);
coef = coefCI(lm, 0.05)
xv = linspace(min(boston_subset.LSTAT), max(boston_subset.LSTAT), 100)';
xv2 = ((linspace(min(boston_subset.LSTAT), max(boston_subset.LSTAT), 100)).^2)';
yv = lm1.Coefficients.Estimate(1) + lm1.Coefficients.Estimate(2)*xv + lm1.Coefficients.Estimate(3)*xv2;
plot(xv, yv);

subplot(1,2,2);
scatter(boston_subset.LSTAT, boston_subset.MEDV)
hold on;
lm2 = fitlm(boston_subset, 'MEDV~1+LSTAT');
disp(lm2);
coef = coefCI(lm, 0.05);
xv = linspace(min(boston_subset.LSTAT), max(boston_subset.LSTAT), 100)';
yv = lm2.Coefficients.Estimate(1) + lm2.Coefficients.Estimate(2)*xv;
plot(xv, yv);

anova_lm1 = anova(lm1)
anova_lm2 = anova(lm2)