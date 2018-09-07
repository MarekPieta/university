%% Zadanie 1

X=1:20
V=X>8
X(V)

A=[2:2:20]

%elementy na miejscach parzystych
A(2:2:end)

%elementy wieksze od 10
V1 = A>10
A(V1)

%elementy parzyste
V2 = (0 == mod(A, 2))
A(V2)

%suma elementow wiekszych od 10
sum(A(V1))

X=magic(5)

%elementy wieksze od 10
W1 = X>10
X(W1)

%suma elementow wiekszych od 10
sum(X(W1))

%wiersze parzyste
X(2:2:end,:)

%kolumny nieparzyste
X(:,1:2:end)

%suma wszystkich elementow
sum(X)

%% Zadanie 2
x=1:100000;
%petla for
t0=clock;
summary = 0
for i = 1:100000
    summary = summary + i;
end
summary
time1 = etime(clock,t0)

%sum
t0=clock;
sum(1:100000)
time2 = etime(clock,t0)

%% Zadanie 3
tic
summary = 0
for i = 1:100000
    summary = summary + 1/i.^2;
end
summary
toc

tic
sum( 1./(1:100000).^2)
toc

%% Zadanie 4
tic
summary = 0
for i = 1:1000
    summary = summary + i.^2;
end
summary
toc

tic
sum( (1:1000).^2)
toc

%% Zadanie 5
tic
summary = 0
for i = 1:502
    summary = summary + (-1).^(i+1) * 1./(2*i-1);
end
summary
toc

tic
sum( (-1).^((1:502)+1) .* 1./((2.*(1:502))-1))
toc

%W zadaniach 3,4,5 czasy wykonania sa mniejsze
%dla funkcji sum()

%% Zadanie 6

X = [-1 0 2;1 -2 1;-5 0 2]
res = X(X(1,:) > 0)
%Wynikiem jest -5.

%% Zadanie 7
N = 5
x = [1:N]
y = ones(N,1)
res7 = y*x

%% Zadanie 8
N = 5
x = [1:N]
y = [1:N]
res8 = min(x,y')


%% Zadanie 9
a1 = [0 1 1]
a2 = [1 0 1 1]

a1_dec = sum(a1.*2.^ (((length(a1))-1):-1:0) )
a2_dec = sum(a2.*2.^ (((length(a2))-1):-1:0) )

%% Zadanie 10
%a)
A = [2,1; 1,2]
B = [3; -1]
x = inv(A)*B

%b)
A = [2 3 1; 1 -2 7; 3 4 10]
B = [1; 17; 19]
x = inv(A)*B