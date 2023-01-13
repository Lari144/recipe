# recipe

GUI: TKinter | Datenbank: sqlite

Aufgaben:
- GUI wo man eigene Rezepte eingeben kann (Name, Zutaten) - Eingabefelder
- Datenbank erstellen - sqlite
- GUI wo man den Rezeptnamen eingeben kann
- neue GUI oder Abschnitt wo man das Rezept dann sieht
- Erste Abfrage ob man ein Rezept suchen oder eingeben möchte

# User Stories:

# User story rezept eingabe

Rezept sollte eingeben und dann in die Datenbank gespeichert werden

## Actors

* User

## Input

Name, Zutaten, Beschreibung, ....

## Output 

Daten in der Datenbank auffindbar

## Errors

* bestimmte Datansätze können leer sein -> dazu affordern es zu befüllen
* doppelte Einträge könnten gemacht werden -> nicht zulassen wenn es den namen schon gibt

-----------------------------------------

# User story rezept ausgabe

Rezeptname wird eingegeben und das passende rezept ausgegeben

## Actors

* User

## Input

Name

## Output 

Das Rezept mit Name, Beschreibung, Zutaten, ....

## Errors

* Das Rezept wird nicht gefunden bzw. existiert nicht in der Datenbank -> Error, dass es dieses Rezept nicht gibt

-----------------------------------------
