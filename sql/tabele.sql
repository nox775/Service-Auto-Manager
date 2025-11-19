
-- 1. Tabela CLIENTI
CREATE TABLE CLIENTI (
    ClientID INT AUTO_INCREMENT PRIMARY KEY, 
    Nume VARCHAR(255) NOT NULL, 
    Prenume VARCHAR(255) NOT NULL, 
    Telefon VARCHAR(50) UNIQUE NOT NULL, 
    Email VARCHAR(255) UNIQUE NULL, 
    Adresa VARCHAR(500) NULL, 
    TipClient ENUM('Persoana Fizica', 'Persoana Juridica') NOT NULL,
    CUI VARCHAR(50) NULL, 
    
    CONSTRAINT chk_cui CHECK ((TipClient = 'Persoana Fizica' AND CUI IS NULL) OR (TipClient = 'Persoana Juridica'))
);

-- 2. Tabela VEHICULE
CREATE TABLE VEHICULE (
    VehiculID INT AUTO_INCREMENT PRIMARY KEY,
    ClientID INT NOT NULL,
    NumarInmatriculare VARCHAR(20) UNIQUE NOT NULL, 
    SerieSasiu VARCHAR(30) UNIQUE NOT NULL, 
    Marca VARCHAR(100) NOT NULL, 
    Model VARCHAR(100) NOT NULL, 
    AnFabricatie INT, 
    CodMotor VARCHAR(50) NULL, 
    CapacitateCilindrica INT NULL,
    TipCombustibil ENUM('Benzina', 'Diesel', 'Electric', 'Hibrid') NOT NULL,
    
    FOREIGN KEY (ClientID) REFERENCES CLIENTI(ClientID)
);

-- 3. Tabela MECANICI
CREATE TABLE MECANICI (
    MecanicID INT AUTO_INCREMENT PRIMARY KEY, 
    Nume VARCHAR(255) NOT NULL,
    Prenume VARCHAR(255) NOT NULL, 
    DataAngajarii DATE NOT NULL
);

-- 4. Tabela SERVICII
CREATE TABLE SERVICII (
    ServiciuID INT AUTO_INCREMENT PRIMARY KEY,
    Denumire VARCHAR(255) NOT NULL, 
    Descriere TEXT NULL, 
    TarifOra DECIMAL(10, 2) NOT NULL,
    TimpEstimativ DECIMAL(5, 2) NULL 
);

-- 5. Tabela FURNIZORI
CREATE TABLE FURNIZORI (
    FurnizorID INT AUTO_INCREMENT PRIMARY KEY,
    NumeFurnizor VARCHAR(255) NOT NULL, 
    PersoanaContact VARCHAR(255) NULL, 
    Telefon VARCHAR(50) NOT NULL, 
    Email VARCHAR(255) NOT NULL, 
    CUI VARCHAR(50) NULL
);

-- 6. Tabela PIESE
CREATE TABLE PIESE (
    PiesaID INT AUTO_INCREMENT PRIMARY KEY,
    FurnizorID INT NOT NULL, 
    CodPiesa VARCHAR(100) UNIQUE NOT NULL,
    Denumire VARCHAR(255) NOT NULL, 
    Descriere TEXT NULL,
    StocDisponibil INT NOT NULL DEFAULT 0, 
    PretVanzare DECIMAL(10, 2) NOT NULL, 
    PretAchizitie DECIMAL(10, 2) NULL, 
    
    FOREIGN KEY (FurnizorID) REFERENCES FURNIZORI(FurnizorID)
);

CREATE TABLE SPECIALIZARI (
    SpecializareID INT AUTO_INCREMENT PRIMARY KEY,
    Denumire VARCHAR(100) NOT NULL UNIQUE,
    Descriere TEXT NULL
);

-- 7. Tabela N:N - MECANICI_SPECIALIZARI
CREATE TABLE MECANICI_SPECIALIZARI (
    MecanicSpecializareID INT AUTO_INCREMENT PRIMARY KEY,
    MecanicID INT NOT NULL,
    SpecializareID INT NOT NULL,

    FOREIGN KEY (MecanicID) REFERENCES MECANICI(MecanicID),
    FOREIGN KEY (SpecializareID) REFERENCES SPECIALIZARI(SpecializareID),

    UNIQUE KEY uk_mecanic_specializare (MecanicID, SpecializareID)
);
-- 8. Tabela DEVIZE 
CREATE TABLE DEVIZE (
    DevizID INT AUTO_INCREMENT PRIMARY KEY,
    VehiculID INT NOT NULL, 
    DataPrimire DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    DataFinalizare DATETIME NULL, 
    Kilometraj INT NOT NULL,
    DescriereProblemaClient TEXT NOT NULL,
    ObservatiiMecanic TEXT NULL, 
    StareDeviz ENUM('Deschisa', 'In Lucru', 'Asteapta Piese', 'Finalizata', 'Anulata') NOT NULL DEFAULT 'Deschisa', 
    CostTotalEstimativ DECIMAL(10, 2) NULL,
    
    FOREIGN KEY (VehiculID) REFERENCES VEHICULE(VehiculID) 
);

-- 9. Tabela COMANDA_PIESE 
CREATE TABLE COMANDA_PIESE (
    ComandaPiesaID INT AUTO_INCREMENT PRIMARY KEY,
    DevizID INT NOT NULL, 
    PiesaID INT NOT NULL,
    Cantitate INT NOT NULL,
    PretUnitarVanzare DECIMAL(10, 2) NOT NULL,
    
    FOREIGN KEY (DevizID) REFERENCES DEVIZE(DevizID), 
    FOREIGN KEY (PiesaID) REFERENCES PIESE(PiesaID), 
    
    CHECK (Cantitate > 0)
);

-- 10. Tabela MANOPERA
CREATE TABLE MANOPERA (
    ManoperaID INT AUTO_INCREMENT PRIMARY KEY,
    DevizID INT NOT NULL,
    ServiciuID INT NOT NULL,
    MecanicID INT NOT NULL, 
    OreLucrate DECIMAL(5, 2) NOT NULL,
    TarifOraAplicat DECIMAL(10, 2) NOT NULL,
    CostLinie DECIMAL(10, 2) NOT NULL,
    
    FOREIGN KEY (DevizID) REFERENCES DEVIZE(DevizID),
    FOREIGN KEY (ServiciuID) REFERENCES SERVICII(ServiciuID), 
    FOREIGN KEY (MecanicID) REFERENCES MECANICI(MecanicID) 
);

-- 11. Tabela FACTURA
CREATE TABLE FACTURA (
    FacturaID INT AUTO_INCREMENT PRIMARY KEY,
    DevizID INT NOT NULL,
    SerieNumar VARCHAR(50) NOT NULL UNIQUE, 
    DataEmitere DATE NOT NULL,
    DataScadenta DATE NOT NULL,
    TotalFaraTVA DECIMAL(10, 2) NOT NULL, 
    ValoareTVA DECIMAL(10, 2) NOT NULL, 
    TotalCuTVA DECIMAL(10, 2) NOT NULL,
    StarePlata ENUM('Neplatita', 'Platita', 'Anulata') NOT NULL DEFAULT 'Neplatita', 
    
    UNIQUE KEY uk_deviz_facturat (DevizID),
    
    FOREIGN KEY (DevizID) REFERENCES DEVIZE(DevizID)
);