CREATE VIEW HotelBis.Facture AS SELECT idFacture, nom, prenom, mail, ((date_fin - date_debut)*tarif) AS Nuitees, sum(quantite * prix) AS Total_conso
FROM HotelBis.Chambre NATURAL JOIN HotelBis.Reservation NATURAL JOIN HotelBis.Consommation NATURAL JOIN HotelBis.Bar NATURAL JOIN HotelBis.Client
WHERE date_debut <= jour AND
      jour < date_fin
GROUP BY idFacture, nom, prenom, mail, date_debut, date_fin, tarif;
