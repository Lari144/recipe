# User story rezept löschen

Rezept wird ausgewält und dann aus der Datenbank gelöscht 

## Actors

* User

## Input

Name, Zutaten, Beschreibung, ....

## Output 

Daten aus der Datenbank gelöscht

## Errors

* Eintrag kann nicht richtig ausgewählt werden
* Eintrag ist nicht richtig mit den anderen Tables verknüpft - wird nicht richtig gelöscht
* wird nur aus der Gui aber nicht aus der Datenbank gelöscht

# User story Diätvorschriften

Als Person mit Ernährungseinschränkungen möchte ich in der Lage sein, Rezepte nach bestimmten Ernährungsbedürfnissen zu filtern, wie z.B. glutenfreie oder vegane Optionen

## Actors

* User

## Input

Auswahl von Filter

## Output 

Das passende Rezept mit Filter

## Errors

* Das Rezept wird nicht gefunden bzw. existiert nicht in der Datenbank -> Error, dass es dieses Rezept nicht gibt