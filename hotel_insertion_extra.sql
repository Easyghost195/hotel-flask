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
-- reservations impossibles
-- INSERT INTO HotelBis.Reservation
--   VALUES(DEFAULT,5,1,'2017-11-11','2017-11-14',FALSE, DEFAULT);
-- INSERT INTO HotelBis.Reservation
--   VALUES(DEFAULT,5,1,'2017-11-19','2017-11-26',FALSE, DEFAULT);
-- INSERT INTO HotelBis.Reservation
--   VALUES(DEFAULT,5,1,'2017-12-9','2017-12-14',FALSE, DEFAULT);
-- INSERT INTO HotelBis.Reservation
--   VALUES(DEFAULT,5,1,'2017-12-21','2017-12-26',FALSE, DEFAULT);

INSERT INTO HotelBis.Consommation
  VALUES(1,'2017-11-11','Biere',1);
INSERT INTO HotelBis.Consommation
  VALUES(1,'2017-11-12','Pastis',2);
-- consommations impossibles
-- INSERT INTO HotelBis.Consommation
--   VALUES(1,'2017-11-5','Pastis',2);
