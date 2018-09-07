clear all;
close all;
clc;

%generowanie danych
dzien = 8;
rok = 1995;
rand('state',dzien*rok);
randn('state',dzien*rok);
%zbiór ucz¹cy
x = [ones(200,1) rand(200,30)*2-1 ];
wp = [1 rand(1,10)*0.5+0.5, rand(1,10)*0.3, zeros(1,10)]';
y = (wp'*x' + randn(1,200)*0.1)';

%zbiór testowy
xt = [ones(200,1) rand(200,30)*2-1];
yt = (wp'*xt' + randn(1,200)*0.1)';
      
[~,~,~,inmodel]=stepwisefit(x(:,2:end),y);
x3=x(:,[true inmodel]); %usuniêcie nieistotnych atrybutów      
x3t=xt(:,[true inmodel]);

w3=(x3'*x3)^(-1)*x3'*y;

y3=(w3'*x3')';

y3t = (w3'*x3t')';

error_train = sum((y3 - y).^2)
error_test = sum((y3t - y).^2)

%regresja grzbietowa
lambda=0:0.001:1;
w4=ridge(y,x(:,2:end),lambda,0);

figure(1);
plot(lambda, w4(11,:));
title('Jedna z wag wyznaczonych przez ridge');
xlabel('{\lambda}');
ylabel('waga');

%dane treningowe
for i=1:length(lambda)
    y4(:,i) = (w4(:,i)'*x')';
    E4(i) = sum((y-y4(:,i)).^2);
end
 
figure(2);
plot(lambda, E4);
title('Blad dla danych treningowych w zaleznosci od {\lambda} - ridge');
xlabel('{\lambda}');
ylabel('Wartosc bledu');

%dane testowe
 for i=1:length(lambda)
    y4t(:,i) = (w4(:,i)'*xt')';
    E4t(i) = sum((yt-y4t(:,i)).^2);
 end
 
figure(3);
plot(lambda, E4t);
title('Blad dla danych testowych w zaleznosci od {\lambda} - ridge');
xlabel('{\lambda}');
ylabel('Wartosc bledu');

%Zwiekszanie parametru lambda zapobiega zjawisku za duzego dopasowywania
%sie modelu do danych treningowych. "Overfitting" ogranicza mozliwosc 
%generalizacji modelu dla nowych danych (np. zbior testowy). W przypadku
%za duzych wartosci lambda mozemy uzyskac model zle odzwierciedlajacy
%rzecywiste zaleznosci z uwagi na mozliwosc wystapienie "underfitting"'u.

lambda=0:0.000001:0.003;
[w5, FitInfo] = lasso(x(:,2:end),y,'Lambda',lambda);
w5_0=FitInfo.Intercept;

w5 = [w5_0; w5];

figure(4);
plot(lambda, w5(2,:));
title('Jedna z wag wyznaczonych przez lasso');
xlabel('{\lambda}');
ylabel('waga');

%dane treningowe
for i=1:length(lambda)
    y5(:,i) = (w5(:,i)'*x')';
    E5(i) = sum((y-y5(:,i)).^2);
end
 
figure(5);
plot(lambda, E5);
title('Blad dla danych treningowych w zaleznosci od {\lambda} - lasso');
xlabel('{\lambda}');
ylabel('Wartosc bledu');

%dane testowe
 for i=1:length(lambda)
    y5t(:,i) = (w5(:,i)'*xt')';
    E5t(i) = sum((yt-y5t(:,i)).^2);
 end

figure(6);
plot(lambda, E5t);
title('Blad dla danych testowych w zaleznosci od {\lambda} - lasso');
xlabel('{\lambda}');
ylabel('Wartosc bledu');

% W przypadku wartosci bledow dla zbioru treningowego i testowego
% wystepuja analogiczne tendencje jak w przypadku metody ridge.
% "Lasso" zeruje wartoœci mniej istotnych wspó³czynników, ridge tylko
% je ogranicza (widoczne dla wiekszych wartosci lambda).
% Ponadto w przypadku metody "lasso" wartosci parametru
% lambda s¹ generalnie ni¿sze. 