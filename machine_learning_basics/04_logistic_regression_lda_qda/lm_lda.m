%
%   TOPIC: Linear Discriminant Analysis
%
% ------------------------------------------------------------------------

close all
clearvars

smarket = readtable('data/smarket.csv');
smarket.Direction = categorical(smarket.Direction, {'Up','Down'});

figure(1);
gscatter(smarket.Lag1, smarket.Lag2, smarket.Direction);
xlabel('Lag1');
ylabel('Lag2');

cdiscr = fitcdiscr(smarket, 'Direction~Lag1+Lag2');
fprintf('Class names:\n')
disp(cdiscr.ClassNames)
fprintf('Group means:\n')
disp(cdiscr.Mu)
fprintf('Prior probabilities of groups:\n')
disp(cdiscr.Prior)

K = cdiscr.Coeffs(1,2).Const;
L = cdiscr.Coeffs(1,2).Linear;

f = @(x1,x2) K + L(1)*x1 + L(2)*x2;

hold on;
h2 = ezplot(f,[-6 6 -6 6]);
h2.Color = 'r';
h2.LineWidth = 2;

X = smarket(:, 1:8);
values = smarket{:, 9};

predicted_values = predict(cdiscr, X);

cp = classperf(cellstr(smarket.Direction), cellstr(predicted_values));
cp.CountingMatrix
cp.ErrorRate

%second prediction
lda_mdl = fitcdiscr(smarket, 'Direction~Lag1+Lag2');

[~, score, ~] = predict(lda_mdl, smarket);
yhat_t90 = (score(:,2) > 0.9);
yhat_t90 = categorical(yhat_t90, [0,1], {'Up', 'Down'});

cp = classperf(cellstr(smarket.Direction), cellstr(yhat_t90));
cp.CountingMatrix
cp.ErrorRate