%% Uczenie maszynowe AiR, 2018
%%
%% Cwiczenie: Drzewa decyzyjne
% Cel: Ilustracja roznych aspektow budowania drzew decyzyjnych i ich weryfikowania

% Prosze uzupelnic brakujace fragmenty zgodnie z instrukcja (FIXME)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Decision Trees
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Prosze pobrac dane
clear all
close all
load fisheriris.mat

%Prosze zapoznac sie ze zmiennymi meas oraz species

% Zadanie 1
%Wyswietlic informacje statystyczne na temat probek danych takie jak:
% Srednia wartosc atrybutu
% wartosc maksymalna atrybutu - wartosc minimalna atrybutu
% odchylenie standardowe
for i=1:4
    mean_value(i) = mean(meas(:,i));
    max_value(i) = max(meas(:,i));
    min_value(i) = min(meas(:,i));
    std_value(i) = std(meas(:,i));
end

mean_value
max_value
min_value
std_value
%Zadanie 2
% Przy pomocy funkcji gscatter() prosze wyswietlic wczytane dane dla
% atrybutow:
% a) sepal length <->sepal width (kolumna 1 i 2)
figure(1);
gscatter(meas(:,1), meas(:,2), species);
xlabel('sepal length');
ylabel('sepal width');

% b) petal length <->petal width (kolumna 3 i 4)
figure(2)
gscatter(meas(:,3), meas(:,4), species);
xlabel('petal length');
ylabel('petal width');

%Zadanie 3
% Utworz drzewo decyzyjne przy pomocy funkcji fitctree() lub
% ClassificationTree.fit()
CT = fitctree(meas, species);

% Zapoznaj sie z powstalym obiektem

% Zadanie 4
% Zapoznaj sie z graficzna i regulowa reprezentacja drzewa (funkcja view()):

%FIXME (werjsa graficzna i regulowa)
view(CT);
view(CT,'mode','graph');

% Zadanie 5
%Wyznacz klasy dla ka?dego przykladu trenujacego (dane meas, funkcja predict()):

species_predicted = predict(CT, meas);

% Zadanie 6
% Wyznacz macierz bledow (ang. confusion matrix) przy pomocy funkcji
% confusion matrix - funkcja cunfusionmat()

confusion_matrix = confusionmat(species, species_predicted);

% Zadanie 7
%Wyswietl macierz przy pomocy funkcji disp()

disp(confusion_matrix);

% Zadanie 8
% Wyznacz macierz bledow uzywajac funkcji plotconfusion() (wczesniej konwertuj species i wynik predykcji na wektory numeryczne:

species_num(1,:) = strcmp(species,'setosa');
species_num(2,:) = strcmp(species,'versicolor');
species_num(3,:) = strcmp(species,'virginica');

species_predicted_num(1,:) = strcmp(species_predicted,'setosa');
species_predicted_num(2,:) = strcmp(species_predicted,'versicolor');
species_predicted_num(3,:) = strcmp(species_predicted,'virginica');

plot_confusion = plotconfusion(double(species_num), double(species_predicted_num)); 


%% Zadanie 9
% Oblicz podstawowe miary na podstawie macierzy bledow:

%for setosa
TP1 = 50;
TN1 = 100;
FP1 = 0;
FN1 = 0;

% czulosc:
TPR1 = TP1/(TP1+FN1)

% swoistosc:
TNR1 = TN1/(FP1+TN1)

% precyzja:
precision1 = TP1/(TP1+FP1)

% dokladnosc:
ACC1 = (TP1+TN1)/(TP1+TN1+FP1+FN1)

%for versicolor
TP2 = 47;
TN2 = 100;
FP2 = 0;
FN2 = 3;

% czulosc:
TPR2 = TP2/(TP2+FN2)

% swoistosc:
TNR2 = TN2/(FP2+TN2)

% precyzja:
precision2 = TP2/(TP2+FP2)

% dokladnosc:
ACC2 = (TP2+TN2)/(TP2+TN2+FP2+FN2)

%for virginica
TP3 = 50;
TN3 = 97;
FP3 = 3;
FN3 = 0;

% czulosc:
TPR3 = TP3/(TP3+FN3)

% swoistosc:
TNR3 = TN3/(FP3+TN3)

% precyzja:
precision3 = TP3/(TP3+FP3)

% dokladnosc:
ACC3 = (TP3+TN3)/(TP3+TN3+FP3+FN3)

% Zadanie 10
%% Funkcja fitctree() po ustawieniu parametru 'CrossVal' 'on' uzywa 10-krotnej walidacji krzyzowej (ang. 10-fold crossvalidation). 
%Utworz drzewo decyzyjne

CT2 = fitctree(meas, species, 'CrossVal', 'on');

% Odpowiedz na pytanie:
% Ile drzew zostalo wygenerowanych: 10

% Zadanie 11
%Wyswietl pierwsze drzewo:
view(CT2.Trained{1},'Mode','graph');

% Zadanie 12
%Ocen dzialanie modelu po wlaczeniu walidacji krzyzowej (ang. crossvalidation). 

for i = 1:10
    species_predicted = predict(CT2.Trained{i}, meas);
    i
    confusion_matrix2 = confusionmat(species, species_predicted)
end

%Odpowiedz: Po wlaczeniu waliacji krzyzowej uzyskujemy wieksza ilosc drzew,
%ktore moga pozwalac na uzyskanie roznych wynikow klasyfikacji. Dodatkowo
%walidacja krzyzowa pomaga uniknac zbytniego dopasowania sie modelu do
%danych uczacych.

% Zadanie 13
%Uzyj funkcji kfoldLoss() do oceny dzialania modelu.
kfoldLoss(CT2)

% Zadanie 14
%Ustal optymalna strukture drzewa wykorzystujac procedure walidacji krzyzowej.
%W petli generuj drzewa dla parametru "minimalna liczba przykladow w lisciu" (MinLeaf) zmienianego od 2 do 100 (parametr m). 
%Kazde takie drzewo oceniaj w procedurze walidacji krzyzowej:
for m = 2:100
       CTm = fitctree(meas, species, 'CrossVal', 'on', 'MinLeaf', m);
       kfL(m-1) = kfoldLoss(CTm);
end

% Zadanie 15
%Sporzadz wykres bledu w zaleznosci od parametru m. Wyznacz optymalna wartosc m (najwieksza wartosc m, przy ktorej blad utrzymuje sie na niskim poziomie).

figure(3);
plot (2:100, kfL);
too_big = find(kfL > 0.1);
m = too_big(1);
xlabel('m')
ylabel('kfL')

% Zadanie 16
%Pokaz optymalne drzewo w postaci graficznej:
CT_opt = fitctree(meas, species, 'CrossVal', 'on', 'MinLeaf', m);
view(CT_opt.Trained{1});

% Zadanie 17
%Porownaj blad osiagany przez drzewo optymalne z bledem osiaganym przez drzewo wygenerowane przy domyslnych ustawieniach parametrow:
CT_default = fitctree(meas, species, 'CrossVal', 'on');
L_opt = kfoldLoss(CT_opt)
L_default = kfoldLoss(CT_default)

%DODATKOWO:
%Prosze przeanalizowac:
%This example shows how to optimize hyperparameters automatically using fitctree. The example uses Fisher's iris data.

%X = meas;
%Y = species;
%Mdl = fitctree(X,Y,'OptimizeHyperparameters','auto')

