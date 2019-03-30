INSERT INTO HotelBis.Chambre
  VALUES(DEFAULT,20);
INSERT INTO HotelBis.Chambre
  VALUES(DEFAULT,20);
INSERT INTO HotelBis.Chambre
  VALUES(DEFAULT,20);
INSERT INTO HotelBis.Chambre
  VALUES(DEFAULT,30);
INSERT INTO HotelBis.Chambre
  VALUES(DEFAULT,30);
INSERT INTO HotelBis.Chambre
  VALUES(DEFAULT,30);
INSERT INTO HotelBis.Chambre
  VALUES(DEFAULT,30);
INSERT INTO HotelBis.Chambre
  VALUES(DEFAULT,40);
INSERT INTO HotelBis.Chambre
  VALUES(DEFAULT,40);
INSERT INTO HotelBis.Chambre
  VALUES(DEFAULT,40);

INSERT INTO HotelBis.Bar
  VALUES('Biere',2);
INSERT INTO HotelBis.Bar
  VALUES('Coca',2);
INSERT INTO HotelBis.Bar
  VALUES('Pastis',4);
INSERT INTO HotelBis.Bar
  VALUES('Whisky',4);

INSERT INTO HotelBis.Client
  VALUES(DEFAULT,'Dupont','Martin','martin.dupont@ici.fr','ici.fr');
INSERT INTO HotelBis.Client
  VALUES(DEFAULT,'Martin','Dupont','dupont.martin@ici.fr','ici.fr');
INSERT INTO HotelBis.Client
  VALUES(DEFAULT,'Dupont','Martin','martin.dupont@labas.fr','labas.fr');
INSERT INTO HotelBis.Client
  VALUES(DEFAULT,'Martin','Dupont','dupont.martin@labas.fr','labas.fr');
INSERT INTO HotelBis.Client
  VALUES(DEFAULT,'Durand','Durant','durant.durand@ailleurs.fr','ailleurs.fr');

INSERT INTO HotelBis.Reservation
  VALUES(DEFAULT,1,1,'2017-11-10','2017-11-15',FALSE, DEFAULT);
INSERT INTO HotelBis.Reservation
  VALUES(DEFAULT,2,1,'2017-11-20','2017-11-25',FALSE, DEFAULT);
INSERT INTO HotelBis.Reservation
  VALUES(DEFAULT,3,1,'2017-12-10','2017-12-15',FALSE, DEFAULT);
INSERT INTO HotelBis.Reservation
  VALUES(DEFAULT,4,1,'2017-12-20','2017-12-25',FALSE, DEFAULT);

INSERT INTO HotelBis.Consommation
  VALUES(1,'2017-11-11','Biere',1);
INSERT INTO HotelBis.Consommation
  VALUES(1,'2017-11-12','Pastis',2);
