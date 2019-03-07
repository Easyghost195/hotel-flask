CREATE SCHEMA HotelBis;
SET search_path TO HotelBis, public;
-- Les entités
CREATE TABLE HotelBis.Client (
  idClient serial NOT NULL,
  nom text NOT NULL,
  prenom text NOT NULL,
  mail text NOT NULL, -- en attendant un type email -- type citext (sase insensitive text)
  password text NOT NULL,
  -- clefs candidates
  PRIMARY KEY (idClient),
  UNIQUE (mail)
);
CREATE TABLE HotelBis.Chambre (
  idChambre serial NOT NULL,
  tarif integer NOT NULL CHECK (tarif > 0),
  -- clefs candidates
  PRIMARY KEY (idChambre)
);
CREATE TABLE HotelBis.Bar (
  boisson text NOT NULL,
  prix integer NOT NULL CHECK (prix > 0),
  -- clefs candidates
  PRIMARY KEY (boisson)
);
-- Les associations
CREATE TABLE HotelBis.Reservation (
  idFacture serial NOT NULL,
  idClient serial NOT NULL,
  idChambre serial NOT NULL,
  date_debut date NOT NULL,
  date_fin date NOT NULL,
  reglee boolean NOT NULL,
  date_reglement date NOT NULL DEFAULT 'epoch',
  -- clefs candidates
  PRIMARY KEY (idFacture),
  UNIQUE (idClient, idChambre, date_debut),
  UNIQUE (idClient, idChambre, date_fin),
  -- Clefs étrangères
  FOREIGN KEY (idClient) REFERENCES HotelBis.Client(idClient),
  FOREIGN KEY (idChambre) REFERENCES HotelBis.Chambre(idChambre),
  -- Contrainte intégrité élémentaire
  CHECK (date_debut < date_fin),
  CHECK ((not reglee) or (date_reglement>=date_fin))
);
CREATE TABLE HotelBis.Consommation (
  idChambre serial NOT NULL,
  jour date NOT NULL,
  boisson text NOT NULL,
  quantite integer NOT NULL CHECK (quantite > 0),
  -- clefs candidates
  PRIMARY KEY (idChambre, jour, boisson),
  -- Clefs étrangères
  FOREIGN KEY (idChambre) REFERENCES HotelBis.Chambre(idChambre),
  FOREIGN KEY (boisson) REFERENCES HotelBis.Bar(boisson)
);
