%
%   TOPIC: Linear Regression - Qualitative Predictors
%
% ------------------------------------------------------------------------

close all
clearvars

carseats = readtable('data/carseats.csv');

lm = fitlm(carseats, 'Sales~CompPrice+Income+Advertising+Population+Price+ShelveLoc+Age+Education+Urban+US+Income:Advertising+Price:Age')
disp(lm);