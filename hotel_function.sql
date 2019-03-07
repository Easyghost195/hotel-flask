-- PostgreSQL n'accepte pas les contraintes d'integrite avec un SELECT
-- Il faut definir une fonction
CREATE FUNCTION HotelBis.DatesDebutFinCorrectes(integer, integer, date, date) 
  RETURNS boolean AS $$ 
SELECT NOT EXISTS (
  SELECT * 
  FROM HotelBis.Reservation
  WHERE $1 != idFacture
    AND $2 = idChambre 
    AND $3 <= date_fin
    AND $4 >= date_debut)
$$ LANGUAGE SQL;

CREATE FUNCTION HotelBis.DateConsommationCorrecte(integer, date) 
  RETURNS boolean AS $$ 
SELECT EXISTS (
  SELECT * 
  FROM HotelBis.Reservation
  WHERE $1 = idChambre 
    AND $2 >= date_debut
    AND $2 <= date_fin
    AND ((not reglee) or ($2 <= date_reglement))
    )
$$ LANGUAGE SQL;
