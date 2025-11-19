#Clienti Insert

INSERT INTO clienti(Nume,Prenume,Telefon,Email,Adresa,TipClient,CUI) VALUES 
('Andrei','Popescu','0723123456','andrei.popescu@gmail.com','Str. Laleleor 10, Bucuresti','Persoana Fizica',NULL);


INSERT INTO clienti(Nume,Prenume,Telefon,Email,Adresa,TipClient,CUI) VALUES 
('AutoServ SRL', '-', '0219988776', 'contact@autoserv.ro', 'Str. Depozitelor 3, Timisoara', 'Persoana Juridica', 'RO45678901'),
('Radu', 'Mihai', '0724111222', 'mihai.radu@gmail.com', 'Str. Libertatii 5, Brasov', 'Persoana Fizica', NULL),
('TechParts SRL', '-', '0213332211', 'office@techparts.ro', 'Calea Victoriei 89, Bucuresti', 'Persoana Juridica', 'RO22334455'),
('Enache', 'Cristina', '0740555666', 'cristina.enache@gmail.com', 'Str. Florilor 17, Iasi', 'Persoana Fizica', NULL);

INSERT INTO clienti(Nume,Prenume,Telefon,Email,Adresa,TipClient,CUI) VALUES 
('Maria','Ionescu','0734567890','maria.ionescu@yahoo.com','Bd. Mihai Viteazau, Cluj-Napoca','Persoana Fizica',NULL);

#Vehicule Insert

INSERT INTO VEHICULE (ClientID, NumarInmatriculare, SerieSasiu, Marca, Model, AnFabricatie, CodMotor, CapacitateCilindrica, TipCombustibil) VALUES
(1, 'B123ABC', 'WVWZZZ1JZXW000001', 'Volkswagen', 'Golf IV', 2003, '1.9TDI', 1896, 'Diesel'),
(8, 'CJ08XYZ', 'VF1BB05CF12345678', 'Renault', 'Clio', 2010, 'K4M', 1598, 'Benzina'),
(9, 'TM45AUT', 'WAUZZZ8E55A123456', 'Audi', 'A4', 2015, 'CAGA', 1968, 'Diesel'),
(10, 'BV99MHI', 'WDB2030061A876543', 'Mercedes', 'C200', 2012, 'M271', 1796, 'Benzina'),
(11, 'B77SRL', '3FA6P0H73ER123789', 'Ford', 'Mondeo Hybrid', 2019, 'HEV2.0', 1999, 'Hibrid'),
(16, 'IS11CRS', '5YJ3E1EA7LF123456', 'Tesla', 'Model 3', 2020, 'EL123', NULL, 'Electric');

#Mecanici Insert 
INSERT INTO MECANICI (Nume, Prenume, DataAngajarii) VALUES
('Marin', 'Alexandru', '2018-04-10'),
('Dumitrescu', 'Ion', '2020-09-01'),
('Stan', 'Bogdan', '2017-02-15'),
('Vasilescu', 'Marius', '2019-06-20'),
('Pop', 'Robert', '2021-03-05'),
('Neagu', 'Florin', '2022-01-11');

#Servicii Insert
INSERT INTO SERVICII (Denumire, Descriere, TarifOra, TimpEstimativ) VALUES
('Schimb ulei motor', 'Inlocuire ulei si filtru ulei', 120.00, 1.0),
('Diagnoza motor', 'Verificare erori sistem motor', 150.00, 0.5),
('Inlocuire placute frana fata', 'Demontare si montare placute fata', 100.00, 1.2),
('Inlocuire ambreiaj', 'Schimb complet kit ambreiaj', 200.00, 4.0),
('Verificare sistem climatizare', 'Testare si completare freon', 130.00, 1.0),
('Geometrie roti', 'Reglaj directie si unghiuri', 110.00, 0.8);

#Insert furnizori
INSERT INTO FURNIZORI (NumeFurnizor, PersoanaContact, Telefon, Email, CUI) VALUES
('AutoParts Romania SRL', 'George Tudor', '0214556677', 'office@autoparts.ro', 'RO999888777'),
('DieselTech SRL', 'Adrian Marin', '0214551122', 'contact@dieseltech.ro', 'RO11223344'),
('EcoMotors SRL', 'Ioana Preda', '0234557788', 'sales@ecomotors.ro', 'RO22334455'),
('CarSystems SA', 'Mihai Dragomir', '0312223344', 'support@carsystems.ro', 'RO33445566'),
('ElectricAuto SRL', 'Andrei Pavel', '0217789922', 'info@electricauto.ro', 'RO44556677'),
('BrakeLine SRL', 'Sorin Mihalache', '0244223011', 'sales@brakeline.ro', 'RO55667788');

#Insert Piese
INSERT INTO PIESE (FurnizorID, CodPiesa, Denumire, Descriere, StocDisponibil, PretVanzare, PretAchizitie) VALUES
(1, 'OL-MANN123', 'Filtru ulei Mann', 'Filtru pentru motoare diesel/benzina, cod MANN123', 45, 50.00, 30.00),
(6, 'FR-ATE456', 'Placute frana ATE', 'Set plăcuțe frână față, compatibil VW/Audi', 25, 180.00, 120.00),
(1, 'CL-LUK789', 'Kit ambreiaj LUK', 'Kit ambreiaj complet pentru VW Golf', 10, 1200.00, 900.00),
(4, 'FA-BOS222', 'Filtru aer Bosch', 'Filtru aer pentru motoare 1.6/1.9 TDI', 60, 80.00, 50.00),
(5, 'BT-VAR333', 'Baterie auto Varta 70Ah', 'Baterie auto 12V 70Ah', 20, 500.00, 380.00),
(2, 'SN-ABS007', 'Senzor ABS Bosch', 'Senzor ABS pentru roată față stânga', 15, 250.00, 170.00);

#Insert Specializari 
INSERT INTO SPECIALIZARI (Denumire, Descriere) VALUES
('Mecanica generala', 'Reparații și întreținere generală vehicule'),
('Electrică auto', 'Diagnoză și reparații instalații electrice'),
('Sisteme de frânare', 'Montaj, verificare și înlocuire componente frânare'),
('Transmisie și ambreiaj', 'Diagnoză și înlocuire piese transmisie și ambreiaj'),
('Sisteme climatizare', 'Service aer condiționat și încălzire'),
('Diagnoză electronică', 'Citire și interpretare coduri de eroare');

#Insert 
INSERT INTO MECANICI_SPECIALIZARI (MecanicID, SpecializareID) VALUES
(1, 1),
(1, 3),
(2, 2),
(2, 6),
(3, 4),
(4, 5),
(5, 1),
(5, 2),
(6, 3),
(6, 5),
(3, 1),
(4, 6);

INSERT INTO DEVIZE (VehiculID, DataPrimire, DataFinalizare, Kilometraj, DescriereProblemaClient, ObservatiiMecanic, StareDeviz, CostTotalEstimativ) VALUES
(1, '2025-10-10 09:00:00', '2025-10-10 16:00:00', 230000, 'Zgomot la motor și martor service aprins', 'Posibil filtru ulei înfundat', 'Finalizata', 320.00),
(2, '2025-10-11 08:30:00', NULL, 145000, 'Frânele scârțâie', NULL, 'In Lucru', 450.00),
(3, '2025-10-09 10:00:00', '2025-10-09 18:00:00', 98000, 'Ambreiajul patinează', 'Necesită înlocuire completă kit ambreiaj', 'Finalizata', 1800.00),
(4, '2025-10-08 09:00:00', '2025-10-08 13:30:00', 120500, 'Aer condiționat nu mai răcește', 'Pierdere freon', 'Finalizata', 250.00),
(5, '2025-10-12 10:00:00', NULL, 75500, 'Verificare periodică completă', NULL, 'Deschisa', 600.00),
(6, '2025-10-07 11:00:00', '2025-10-07 14:30:00', 35000, 'Verificare sistem frânare', 'Totul în regulă', 'Finalizata', 150.00);

INSERT INTO COMANDA_PIESE (DevizID, PiesaID, Cantitate, PretUnitarVanzare) VALUES
(1, 1, 1, 50.00),
(2, 2, 1, 180.00),
(3, 3, 1, 1200.00),
(4, 4, 1, 80.00),
(5, 5, 1, 500.00),
(6, 6, 1, 250.00);

INSERT INTO MANOPERA (DevizID, ServiciuID, MecanicID, OreLucrate, TarifOraAplicat, CostLinie) VALUES
(1, 1, 1, 1.0, 120.00, 120.00),
(2, 3, 2, 1.2, 100.00, 120.00),
(3, 4, 3, 4.0, 200.00, 800.00),
(4, 5, 4, 1.0, 130.00, 130.00),
(5, 2, 5, 1.0, 150.00, 150.00),
(6, 6, 6, 0.8, 110.00, 88.00);

INSERT INTO FACTURA (DevizID, SerieNumar, DataEmitere, DataScadenta, TotalFaraTVA, ValoareTVA, TotalCuTVA, StarePlata) VALUES
(1, 'FV-1001', '2025-10-10', '2025-10-25', 170.00, 32.30, 202.30, 'Platita'),
(2, 'FV-1002', '2025-10-11', '2025-10-26', 300.00, 57.00, 357.00, 'Neplatita'),
(3, 'FV-1003', '2025-10-09', '2025-10-24', 1600.00, 304.00, 1904.00, 'Platita'),
(4, 'FV-1004', '2025-10-08', '2025-10-23', 250.00, 47.50, 297.50, 'Platita'),
(5, 'FV-1005', '2025-10-12', '2025-10-27', 600.00, 114.00, 714.00, 'Neplatita'),
(6, 'FV-1006', '2025-10-07', '2025-10-22', 150.00, 28.50, 178.50, 'Platita');





