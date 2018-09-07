--Marek Pieta marekpieta95@gmail.com

--wpisanie do bazy danych przykladowych danych
INSERT INTO kolej.trasa (id, miasto_poczatkowe, miasto_koncowe) VALUES
	(1, 'Krakow', 'Warszawa'),
	(2, 'Tarnow', 'Rzeszow');

INSERT INTO kolej.sklad (id, id_trasy) VALUES
	(1, 1),
	(2, 2),
	(3, 2),
	(4, 2);

INSERT INTO kolej.mechanik (id, imie, nazwisko, nazwa_firmy) VALUES
	(1, 'Jan', 'Nowak', 'Paletex'),
	(2, 'Zbigniew', 'Wkretarka', 'Paletex'),
	(3, 'Wlodzimierz', 'Kowalski', NULL),
	(4, 'Jerzy', 'Wisniewski', 'Zagloba');

INSERT INTO kolej.lokomotywa (id, model, id_skladu) VALUES
	(1, 'l14', 1),
	(2, 'l17', 2),
	(3, 'l240', 3),
	(4, 'l14', 4);

INSERT INTO kolej.wagon (id, model, klasa, id_skladu) VALUES
	(1, 'o14', 1, 1),
	(2, 'o14', 2, 1),
	(3, 'o14', 3, 1),
	(4, 'o14', 4, 1),
	(5, 'o44', 0, 2),
	(6, 't100', 0, 3),
	(7, 't34', 0, 4),
	(8, 't23', 0, 4);

INSERT INTO kolej.maszynista (id, imie, nazwisko, pensja, data_zatrudnienia, id_skladu) VALUES
	(1, 'Andrzej', 'Kierowca', 4000, '2010-10-01', 1),
	(2, 'Jaroslaw', 'Cynamon', 2000, '2010-03-05',  2),
	(3, 'Waldemar', 'Kawa', 3000, '2000-02-01', 3),
	(4, 'Jakub', 'Indeks', 8000, '2016-12-01', 4);

INSERT INTO kolej.naprawaLokomotywy(id, id_lokomotywy, id_mechanika, data_naprawy) VALUES
	(1, 1, 4, '2017-05-20'),
	(2, 3, 4,'2014-05-20'),
	(3, 2, 4, '2015-07-22');

INSERT INTO kolej.naprawaWagonu(id, id_wagonu, id_mechanika, data_naprawy) VALUES
	(1, 1, 4, '2017-03-22'),
	(2, 4, 3, '2017-04-23');


INSERT INTO kolej.bilet(id, typ, cena, nazwa_przystanku_poczatek, nazwa_przystanku_koniec, id_trasy) VALUES
	(1, 'normalny', 60, 'Tarnow', 'Rzeszow', 2),
	(2, 'normalny', 30, 'Tarnow', 'Sedzibory', 2),
	(3, 'normalny', 20, 'Tarnow', 'Debice', 2),	
	(4, 'normalny', 20, 'Debice', 'Sedzibory', 2),
	(5, 'normalny', 30, 'Debice', 'Rzeszow', 2),
	(6, 'normalny', 10, 'Sedzibory', 'Rzeszow', 2),
	(7, 'normalny', 5 , 'Krakow Dworzec Glowny', 'Krakow Biezanow', 1),
	(8, 'normalny', 20 , 'Krakow Dworzec Glowny', 'Czestochowa', 1),
	(9, 'normalny', 40 , 'Krakow Dworzec Glowny', 'Radom', 1),
	(10, 'normalny', 100 , 'Krakow Dworzec Glowny', 'Warszawa Dworzec Glowny', 1),
	(11, 'ulgowy', 50 , 'Krakow Dworzec Glowny', 'Warszawa Dworzec Glowny', 1),
	(12, 'ulgowy', 30, 'Tarnow', 'Rzeszow', 2),	
	(13, 'ulgowy', 3, 'Krakow Dworzec Glowny', 'Krakow Biezanow', 1),
	(14, 'normalny', 10, 'Krakow Dworzec Glowny', 'Czestochowa', 1),
	(15, 'normalny', 20, 'Krakow Dworzec Glowny', 'Radom', 1),
	(16, 'normalny', 15, 'Krakow Biezanow', 'Czestochowa', 1),
	(17, 'normalny', 25, 'Krakow Biezanow', 'Radom', 1),
	(18, 'normalny', 60, 'Krakow Biezanow', 'Warszawa Dworzec Glowny', 1),
	(19, 'normalny', 30, 'Czestochowa', 'Radom', 1),
	(20, 'normalny', 35, 'Czestochowa', 'Warszawa Dworzec Glowny', 1),
	(21, 'normalny', 20, 'Radom', 'Warszawa Dworzec Glowny', 1);  

INSERT INTO kolej.zakupionyBilet(id, id_biletu, data_odjazdu, godzina_przyjazdu, godzina_odjazdu) VALUES
	(1, 1, '2017-10-10', '15:30', '15:45'),
	(2, 1, '2017-10-10', '0:30', '1:45'),
	(3, 1, '2017-10-10', '15:30', '15:45'),
	(4, 3, '2017-10-10', '15:30', '15:45'),
	(5, 3, '2017-10-10', '15:30', '15:45'),
	(6, 3, '2017-10-10', '15:30', '15:45'),
	(7, 3, '2017-10-10', '15:30', '15:45'),
	(8, 3, '2017-10-10', '15:30', '15:45'),
	(9, 5, '2017-10-10', '15:30', '15:45'),
	(10, 5, '2017-10-10', '15:30', '17:45'),
	(11, 5, '2017-10-10', '15:30', '17:45'),
	(12, 6, '2017-11-10', '15:30', '17:45'),
	(13, 6, '2017-11-10', '15:30', '17:45'),
	(14, 6, '2017-11-10', '14:30', '15:45'),
	(15, 6, '2017-11-10', '15:30', '16:45'),
	(16, 6, '2017-11-10', '16:30', '17:45'),
	(17, 6, '2017-11-10', '18:30', '19:45'),
	(18, 6, '2017-11-17', '19:30', '20:45'),
	(19, 8, '2017-10-16', '15:30', '15:45'),
	(20, 8, '2017-10-15', '15:30', '15:45'),
	(21, 8, '2017-10-14', '15:30', '15:45'),
	(22, 8, '2017-10-13', '15:30', '15:45'),
	(23, 8, '2017-10-12', '15:30', '15:45'),
	(24, 8, '2017-10-11', '15:30', '15:45');
