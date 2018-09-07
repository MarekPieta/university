%
%   TOPIC: Quadratic Discriminant Analysis
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

is_train = (smarket.Year < 2005);
smarket_train = smarket(is_train,:);
smarket_test = smarket(~is_train,:);
true_groups = smarket_test.Direction;

cdiscr = fitcdiscr(smarket_train, 'Direction~Lag1+Lag2', 'DiscrimType', 'quadratic');
fprintf('Class names:\n')
disp(cdiscr.ClassNames)
fprintf('Group means:\n')
disp(cdiscr.Mu)
fprintf('Prior probabilities of groups:\n')
disp(cdiscr.Prior)

K = cdiscr.Coeffs(1,2).Const;
L = cdiscr.Coeffs(1,2).Linear;
Q = cdiscr.Coeffs(1,2).Quadratic;

f = @(x1,x2) K + L(1)*x1 + L(2)*x2 + Q(1,1)*x1.^2 + ...
    (Q(1,2)+Q(2,1))*x1.*x2 + Q(2,2)*x2.^2;
hold on;
h2 = ezplot(f,[-6 6 -6 6]);
h2.Color = 'r';
h2.LineWidth = 2;

X = smarket(:, 1:8);

predicted_values = predict(cdiscr, smarket_test(:, 1:8));

cp = classperf(cellstr(smarket_test.Direction), cellstr(predicted_values));
cp.CountingMatrix
cp.ErrorRate