--Marek Pieta marekpieta95@gmail.com

--Tworzenie schematu kolej
CREATE SCHEMA IF NOT EXISTS kolej;


/*
  Tworzy tablice reprezentujaca dana trase. Posiada pola reprezentujace miasto poczatkowe
  i miasto koncowe (nazwy miast).
*/
CREATE TABLE kolej.trasa(
	id INTEGER PRIMARY KEY,
	miasto_poczatkowe VARCHAR(40) NOT NULL,
	miasto_koncowe VARCHAR(40) NOT NULL
);

/*
  Tworzy tabele reprezentujaca bilet okreslonego typu,
  klucz podstawowy to "id",
  klucz obcy to "id_trasy - laczy z tabela trasa,
  przy usuwaniu klucza obcego trasa usuwa tez caly rekord z tabeli bilet - nie powinno byc biletow
  dla nieistniejacych tras,
  przy aktualizacji pozwala na zmiane,
  posiada pola reprezentujące typ bletu, cene (wieksza od zera)
  nazwy przystanku początkowego i końcowego,
  pola opisujace poszczegolne atrybuty nie moga byc puste.
*/
CREATE TABLE kolej.bilet (
	id INTEGER PRIMARY KEY,
	typ VARCHAR(30) NOT NULL,
	cena FLOAT NOT NULL CHECK (cena > 0),
	nazwa_przystanku_poczatek VARCHAR(40) NOT NULL,
	nazwa_przystanku_koniec VARCHAR(40) NOT NULL,
	id_trasy INTEGER NOT NULL REFERENCES kolej.trasa ON DELETE CASCADE ON UPDATE CASCADE
);

/*
  Tworzy tabele reprezentujaca zakupione bilety (pojedyncze sztuki). 
  Klucz obcy to id_biletu - laczy z tabela bilet.
  Przy usuwaniu klucza obcego usuwa tez caly rekord z tabeli zakupionyBilet 
  - zakupiony bilet musi byc reprezentowany przez pewien typ biletu.
  Przy aktualizacji pozwala na zmiane.
  Zawiera pola opisujace godzine przyjazdu, godzine odjazdu oraz date odjazdu
  (zaklada sie ze kurs nie trwa dluzej niz 24 godziny).
  Pola opisujace poszczegolne atrybuty nie moga byc puste.
*/
CREATE TABLE kolej.zakupionyBilet(
	id INTEGER PRIMARY KEY,
	id_biletu INTEGER NOT NULL REFERENCES kolej.bilet ON DELETE CASCADE ON UPDATE CASCADE,
	data_odjazdu DATE NOT NULL,	
	godzina_przyjazdu TIME NOT NULL,
	godzina_odjazdu TIME NOT NULL
);


/*
  Tworzy tablice reprezentujaca mechanikow odpowiedzialnych za naprawy lokomotyw i wagonow.
  Mechanicy moga byc zatrudniani przez firme zewnetrzna (okresla to pole nazwa_firmy; przyjmuje
  on wartosc NULL, gdy mechanik jest zatrudniony przez nasza firme). Tablica zawieta tez pola
  opisujace imie i nazwisko mechanika.
*/
CREATE TABLE kolej.mechanik(
	id INTEGER PRIMARY KEY,
	imie VARCHAR(40) NOT NULL,
	nazwisko VARCHAR(40) NOT NULL,
	nazwa_firmy VARCHAR(40)
);

/*
  Tworzy tablice reprezentujaca pojedynczy sklad.
  Klucz obcy to id_trasy - laczy z tabela trasa.
  Przy usuwaniu klucza obcego ustawia go na NULL,
  przy aktualizacji pozwala na zmiane. 
*/
CREATE TABLE kolej.sklad(
	id INTEGER PRIMARY KEY,
	id_trasy INTEGER NOT NULL REFERENCES kolej.trasa ON DELETE SET NULL ON UPDATE CASCADE
);

/*
  Tworzy tablice reprezentujaca maszyniste.
  Klucz obcy id_skladu odnosi sie do skladu, ktorym kieruje (zaklada sie ze maszynisci
  sa przypisani do skladow). Przy usuwaniu klucza obcego ustawia go na NULL,
  przy aktualizacji pozwala na zmiane. Pola imie, nazwisko, pensja oraz data_zatrudnienia
  opisuja odpowiednie cechy okreslonego maszynisty.
*/
CREATE TABLE kolej.maszynista(
	id INTEGER PRIMARY KEY,
	imie VARCHAR(40) NOT NULL,
	nazwisko VARCHAR(40) NOT NULL,
	pensja FLOAT NOT NULL CHECK (pensja > 0),
	data_zatrudnienia DATE NOT NULL,
	id_skladu INTEGER NOT NULL REFERENCES kolej.sklad ON DELETE SET NULL ON UPDATE CASCADE
);

/*
  Tworzy tablice reprezentujaca wagon.
  Klucz obcy id_skladu odnosi sie do skladu, do ktorego nalezy (zaklada sie ze wagony
  sa przypisane do skladow). Przy usuwaniu klucza obcego ustawia go na NULL,
  przy aktualizacji pozwala na zmiane. Pole model okresla takze typ wagonu (towarowy - "t"
  lub osobowy- "o"). Klasa wagonu okreslana jest zarowno dla wagonow towarowych, jak i osobowych.
*/
CREATE TABLE kolej.wagon(
	id INTEGER PRIMARY KEY,
	model VARCHAR(30) NOT NULL,
	klasa INTEGER NOT NULL CHECK (klasa >= 0) CHECK (klasa <= 4),
	id_skladu INTEGER NOT NULL REFERENCES kolej.sklad ON DELETE SET NULL ON UPDATE CASCADE
);

/*
  Tworzy tablice reprezentujaca lokomotywe.
  Klucz obcy id_skladu odnosi sie do skladu, do ktorego nalezy (zaklada sie ze lokomotywy
  sa przypisane do skladow). Przy usuwaniu klucza obcego ustawia go na NULL,
  przy aktualizacji pozwala na zmiane.
*/
CREATE TABLE kolej.lokomotywa(
	id INTEGER PRIMARY KEY,
	model VARCHAR(30) NOT NULL,
	id_skladu INTEGER NOT NULL REFERENCES kolej.sklad ON DELETE SET NULL ON UPDATE CASCADE
);

/*
  Tworzy tablice reprezentujaca pojedyncza naprawe wagonu. Posiada ona dwa klucze obce: id_wagonu
  - laczy z tabela wagon i id_mechanika - laczy z tabela mechanik. Przy usuwaniu klucza obcego usuwa
  rekord z tabeli naprawaWagonu, przy aktualizacji pozwala na zmiane.
*/
CREATE TABLE kolej.naprawaWagonu(
	id INTEGER PRIMARY KEY,
	id_wagonu INTEGER NOT NULL REFERENCES kolej.wagon ON DELETE CASCADE ON UPDATE CASCADE,
	id_mechanika INTEGER NOT NULL REFERENCES kolej.mechanik ON DELETE CASCADE ON UPDATE CASCADE,
	data_naprawy DATE NOT NULL
);

/*
  Tworzy tablice reprezentujaca pojedyncza naprawe lokomotywy. Posiada ona dwa klucze obce: id_lokomotywy
  - laczy z tabela lokomotywa i id_mechanika - laczy z tabela mechanik. Przy usuwaniu klucza obcego usuwa
  rekord z tabeli naprawaLokomotywy, przy aktualizacji pozwala na zmiane.
*/
CREATE TABLE kolej.naprawaLokomotywy(
	id INTEGER PRIMARY KEY,
	id_lokomotywy INTEGER NOT NULL REFERENCES kolej.lokomotywa ON DELETE CASCADE ON UPDATE CASCADE,
	id_mechanika INTEGER NOT NULL REFERENCES kolej.mechanik ON DELETE CASCADE ON UPDATE CASCADE,
	data_naprawy DATE NOT NULL
);
