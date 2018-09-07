%% Uczenie maszynowe AiR, 2018
%%
%% Cwiczenie: K-najblizszych sasiadow
% Cel: Wykorzystanie wbudowanych funkcji do klasyfikacji danych przy pomocy
% algorytmu k-nn

% Prosze uzupelnic brakujace fragmenty zgodnie z instrukcj? (FIXME)


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% K-nearest 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Prosze pobrac dane
clear all
%Fisher's 1936 iris data
load fisheriris.mat

%lub
% Cardiac arrhythmia data from the UCI machine learning repository:
%load arrhythmia.mat

% Prosze zapoznac sie ze zbiorem danych -> zmienna Description w Workspace

%Prosze uzywac funkcji fitcknn(), funkcja knnclassify() zostanie w
%przyszlosci ca?lkowicie wycofana

%Zadania

% Zaprojektuj klasyfikator typu k najblizszych sasiadow (k-NN) do
% rozpoznawania kwiatow irysa lub rodzaju arytmii.

% Zadanie 1

% Podziel zbior danych na uczacy i testowy. Losowo wybierz 5 danych do
%zbioru testowego

X = meas;
Y = species;
number_of_elements_in_test = 5;

X_learn = [];
X_test = [];
Y_learn = [];
Y_test = [];


for i=1:number_of_elements_in_test
   random_number =  randi(size(X,1));
   X_test = [X_test; X(random_number, :)];
   X = [X(1:random_number-1,:); X(random_number+1:end, :)];
   Y_test = [Y_test; Y(random_number)];
   Y = [Y(1:random_number-1); Y(random_number+1:end)];
end

Y_learn = Y;
X_learn = X;

% Zadanie 2
% Narysuj dane uczace oraz testowe
figure(1)
feature1 = X_learn(:,1)
feature2 = X_learn(:,2)
hold on;
logical_index = ismember(Y_learn, 'setosa');
plot(feature1(logical_index), feature2(logical_index), 'g*');

logical_index = ismember(Y_learn, 'versicolor');
plot(feature1(logical_index), feature2(logical_index), 'y*');

logical_index = ismember(Y_learn, 'virginica');
plot(feature1(logical_index), feature2(logical_index), 'b*');

hold on;
plot(X_test(:,1), X_test(:,2), 'r*')

xlabel('X(1)');
ylabel('X(2)');
title ('Training data and test data')

% Zadanie 3 
% Znajdz 5 punktow najblizszych punktowi badanemu (pierwszy ze zbioru testowego)
% Skorzystaj z funkcji knnsearch()

neighbors = knnsearch(X_learn,X_test(1,:),'k',5,'distance','euclidean');

% Narysuj te punkty na wykresie

plot(X_test(1,1), X_test(1,2), 'kd');
plot (X_learn(neighbors, 1), X_learn(neighbors, 2), 'gh');

legend('setosa', 'versicolor', 'virginica', 'Test Data', 'selected point', 'nearest neighbors')

% Zadanie 4
%Ustal gatunki sasiadow. Skorzystaj z funckji tabulate()

species = tabulate(species(neighbors));

% Zadanie 5
% Wykorzystujac funkcj? fitcknn() stworz klasyfikator dla k=4

KNN = fitcknn(X_learn, Y_learn, 'NumNeighbors', 4);


%Zadanie 6 
%Sklasyfikuj dane ze zbioru testowego, funkcja predict()

Y_predicted = predict(KNN, X_test);

%Zadanie 7
% W procedurze 10-krotnej walidacji krzyzowej znajdz optymalna wartosc liczby najblizszych sasiadow k:
%Przydatne funckje: crossvalind(), fitcknn()
%Dokladnosc klasyfikatora: ACC

k_max = 20;
for k = 1:k_max
    classifier = fitcknn(X_learn, Y_learn, 'NumNeighbors', k);
    Y_predicted = predict(classifier, X_test);
    ACC(k) = 0;
    for i=1:number_of_elements_in_test
       if (strcmp(Y_predicted{i,1},Y_test{i,1}))
           ACC(k) = ACC(k) + 1;
       end
    end
    ACC(k) = ACC(k)/number_of_elements_in_test;
end

%Narysuj wykres zaleznosci dokladnosci klasyfikatora (ACC) od wartosci k.
figure(2);
plot(1:k_max, ACC);
title('Classification accuracy ')
xlabel('k')
ylabel('ACC')

%Wybierz optymalna wartosc k

k_optimal = find(ACC==max(ACC));

%Zadanie 8
% Przedstaw na wykresie granice klas

%Stworz klasyfikator kNN dla 2 wybranych parametrow:
param1 = X_learn(:,1);
param2 = X_learn(:,2);
params = [param1 param2]
classifier = fitcknn(params, Y_learn, 'NumNeighbors', 3);

%Dane testowe- przestrzen (X- parametry)(odkomentuj:)
x1_range = min(X(:,1)):.01:max(X(:,1));
x2_range = min(X(:,2)):.01:max(X(:,2));
[xx1, xx2] = meshgrid(x1_range, x2_range);
XGrid = [xx1(:) xx2(:)];

% Sklasyfikuj dane ze zbioru testowego

Y_predicted = predict(classifier, XGrid);

% Narysuj wykres (gscatter())
figure(3);
gscatter(xx1(:), xx2(:), Y_predicted);

% DODATKOWO
%Prosze zapoznac sie z parametrami funkcji fitcknn() : metryki
%odleglosci(distance metrics), wagi (Distance Weights) ect.