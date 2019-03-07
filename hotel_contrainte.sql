-- puis appeler la fonction dans une contrainte d'integrite
ALTER TABLE HotelBis.Reservation ADD CONSTRAINT DatesPossibles
  CHECK(HotelBis.DatesDebutFinCorrectes(idfacture,idChambre, date_debut, date_fin));

ALTER TABLE HotelBis.Consommation ADD CONSTRAINT ConsoPossible
  CHECK(HotelBis.DateConsommationCorrecte(idChambre, jour));
