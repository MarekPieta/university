--Marek Pieta marekpieta95@gmail.com

--Usuwanie kolejnych tabeli w odpowiedniej kolejnosci
DROP TABLE kolej.naprawaLokomotywy;
DROP TABLE kolej.naprawaWagonu;
DROP TABLE kolej.wagon;
DROP TABLE kolej.lokomotywa;
DROP TABLE kolej.mechanik;
DROP TABLE kolej.maszynista;
DROP TABLE kolej.sklad;
DROP TABLE kolej.zakupionyBilet;
DROP TABLE kolej.bilet;
DROP TABLE kolej.trasa;

--Na koniec usuniecie pustego schematu
DROP SCHEMA kolej;
