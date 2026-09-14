# Nutrient Solution Manager – Projektkonzept (Python)

## 1. Projektidee

Der **Nutrient Solution Manager** ist eine Anwendung zur Verwaltung und späteren automatischen Regelung mehrerer Nährlösungstanks für Pflanzen.

Das Projekt ist als langfristiges Lernprojekt konzipiert. Es soll moderne Backend-Entwicklung, Datenbankentwicklung, Simulation und später die Anbindung echter Hardware praktisch miteinander verbinden.

Die Anwendung wird vollständig in **Python** entwickelt.

Ziel ist kein reines Übungsprojekt, sondern ein schrittweise erweiterbares System, das zunächst simuliert arbeitet und später reale Sensoren und Aktoren über MQTT und ESP32 ansteuern kann.

---

# 2. Technologiestack

Der geplante Haupt-Stack besteht aus:

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- Alembic
- Docker
- Docker Compose
- pytest
- uv und `pyproject.toml`
- INTEGER Auto-Increment als Primärschlüssel (PostgreSQL `SERIAL` / `IDENTITY`)

Spätere Erweiterungen:

- MQTT
- ESP32
- Sensorik
- Dosierpumpen
- Scheduler für automatische Regelzyklen
- Analyse- und Optimierungsfunktionen

---

# 3. Ziele des Lernprojekts

Mit dem Projekt sollen insbesondere folgende Technologien und Konzepte praktisch gelernt und angewendet werden:

- Entwicklung von REST APIs mit FastAPI
- Datenvalidierung mit Pydantic
- Datenbankmodellierung mit PostgreSQL
- ORM mit SQLAlchemy
- Datenbankmigrationen mit Alembic
- Dependency Injection in FastAPI
- Service-orientierte Architektur
- Trennung von API, Fachlogik und Infrastruktur
- Docker und Docker Compose
- automatisierte Tests mit pytest
- Simulation von Sensoren und Aktoren
- später MQTT-Kommunikation
- spätere Integration von ESP32-Hardware

---

# 4. Grundprinzip der Anwendung

Mehrere Tanks enthalten Nährlösungen für unterschiedliche Pflanzen.

Jeder Tank wird unabhängig verwaltet und kann einer Pflanze sowie einer bestimmten Wachstumsphase zugeordnet werden.

Ein Tank soll regelmäßig überprüft und bei Bedarf reguliert werden.

Die grundsätzliche Reihenfolge eines Regelzyklus ist:

1. Füllstand prüfen
2. Wasser auffüllen
3. Mischen beziehungsweise Stabilisierung abwarten
4. Neue Messwerte berücksichtigen
5. EC prüfen
6. Benötigte Düngermenge anhand der aktiven Rezeptur berechnen
7. Dünger proportional dosieren
8. Mischen und erneut messen
9. pH prüfen
10. pH+ oder pH- dosieren
11. Mischen und erneut messen
12. Ergebnisse und Aktionen speichern

---

# 5. Fachliche Anforderungen

## 5.1 Pflanzen

Eine Pflanze wird zentral verwaltet und kann mehreren Tanks zugeordnet werden.

Beispiel:

- Basilikum
- Tomate
- Salat

Eine Pflanze besitzt beispielsweise:

- Id
- Name
- Beschreibung

---

## 5.2 Wachstumsphasen

Jede Pflanze kann beliebig viele Wachstumsphasen besitzen.

Eine Wachstumsphase definiert unter anderem:

- Name
- Reihenfolge
- EC-Minimum
- EC-Zielwert
- EC-Maximum
- pH-Minimum
- pH-Zielwert
- pH-Maximum

Beispiel:

### Basilikum – Wachstumsphase 1

- EC: 5,0 bis 5,5
- EC-Ziel: 5,25
- pH: 6,0 bis 6,5
- pH-Ziel: 6,25

### Basilikum – Wachstumsphase 2

- EC: 5,5 bis 6,0
- EC-Ziel: 5,75
- pH: 6,0 bis 6,5
- pH-Ziel: 6,25

---

# 6. Dünger

Dünger werden zentral verwaltet und können von mehreren Rezepturen verwendet werden.

Ein Dünger besitzt zunächst:

- Id
- Name
- Beschreibung
- EC-Wirkung pro ml pro Liter

Beispiel:

| Dünger | EC-Wirkung |
|---|---:|
| Dünger A | 1 ml/L erhöht EC um 0,1 |
| Dünger B | 1 ml/L erhöht EC um 0,2 |
| Dünger C | 1 ml/L erhöht EC um 0,1 |

Die Software behandelt die Kombination der Dünger als virtuelle Rezeptur.

Die einzelnen Dünger werden jedoch getrennt berechnet und später auch getrennt dosiert.

---

# 7. Rezepturen

Jede Wachstumsphase kann höchstens eine Dünger-Rezeptur besitzen.

Eine Phase ohne Rezeptur ist erlaubt, etwa wenn zunächst nur Wasser und pH verwaltet werden.
Mehrere parallele Rezepturen pro Phase sind in der ersten Version nicht vorgesehen.

Eine Rezeptur besteht aus beliebig vielen Bestandteilen.

Beispiel:

- Dünger A: 30 %
- Dünger B: 30 %
- Dünger C: 40 %

Die Summe der Rezeptanteile soll 100 % ergeben.

Das System darf nicht auf eine feste Anzahl von Düngern beschränkt sein.

---

# 8. Tanks

Tanks sind eigenständige Objekte und werden unabhängig von Pflanzen verwaltet.

Ein Tank besitzt beispielsweise:

- Id
- Name
- Ziel-Füllstand
- zugeordnete Pflanze
- aktive Wachstumsphase
- aktuelle Messwerte
- Messhistorie

Beispiel:

- Tank: Gewächshaus Basilikum 1
- Ziel-Füllstand: 30 Liter
- Pflanze: Basilikum
- aktive Wachstumsphase: Phase 2

Mehrere Tanks können dieselbe Pflanze und Wachstumsphase verwenden.

---

# 9. Messungen

Alle Messwerte sollen gespeichert werden.

Ein Messwert enthält beispielsweise:

- Id
- Tank
- Zeitpunkt
- Füllstand
- EC
- pH
- Temperatur (später)
- Quelle

Mögliche Quellen:

- Simulation
- Manual
- Sensor
- MQTT

Zu Beginn werden Messwerte durch Simulation oder manuelle Eingaben erzeugt.

Später:

ESP32 → MQTT → Nutrient Solution Manager

---

# 10. EC-Regelung

Die EC-Regelung verwendet die aktive Rezeptur einer Wachstumsphase.

## Beispiel

Tankvolumen:

30 Liter

Ist-EC:

1,2

Ziel-EC:

2,0

Rezept:

- Dünger A: 30 %
- Dünger B: 30 %
- Dünger C: 40 %

EC-Wirkung:

- A: +0,1 EC pro ml/L
- B: +0,2 EC pro ml/L
- C: +0,1 EC pro ml/L

## Berechnung der Rezeptwirkung

Für 1 ml Gesamtmischung pro Liter:

0,3 × 0,1 + 0,3 × 0,2 + 0,4 × 0,1 = 0,13 EC

Die virtuelle Rezeptur erhöht den EC rechnerisch um:

0,13 EC pro ml/Liter.

## Benötigte Menge

EC-Differenz:

2,0 - 1,2 = 0,8

Benötigte Gesamtmischung pro Liter:

0,8 / 0,13 = 6,15 ml/L

Bei 30 Litern:

6,15 × 30 = 184,5 ml Gesamtmenge

Aufteilung:

- Dünger A: 55,35 ml
- Dünger B: 55,35 ml
- Dünger C: 73,8 ml

Wichtig:

Die einzelnen Dünger werden entsprechend des berechneten Rezeptverhältnisses dosiert.

Es wird nicht nach jedem einzelnen Dünger geprüft, ob der Ziel-EC bereits erreicht wurde, da dadurch das gewünschte Rezeptverhältnis zerstört werden könnte.

Nach einer vollständigen Dosierung erfolgt:

1. Mischen
2. Stabilisierung
3. erneute Messung
4. bei Bedarf Berechnung einer weiteren Korrektur

---

# 11. pH-Regelung

Die pH-Regelung wird unabhängig von der EC-Regelung behandelt.

Grundlogik:

- Ist-pH über Maximum → pH- erforderlich
- Ist-pH unter Minimum → pH+ erforderlich
- Ist-pH innerhalb des Bereichs → keine Aktion

Da die Wirkung von pH+ und pH- nicht zuverlässig linear berechnet werden kann, soll die spätere Regelung iterativ erfolgen.

Regelkreis:

1. pH messen
2. Abweichung feststellen
3. kleine Dosiermenge bestimmen
4. pH+ oder pH- dosieren
5. Mischen
6. Stabilisierung abwarten
7. erneut messen
8. gegebenenfalls wiederholen

---

# 12. Zielbereiche

Werte innerhalb des erlaubten Bereichs sollen nicht ständig korrigiert werden.

Beispiel EC:

- Minimum: 5,0
- Ziel: 5,25
- Maximum: 5,5

Beispiel pH:

- Minimum: 6,0
- Ziel: 6,25
- Maximum: 6,5

Regel:

- innerhalb Minimum und Maximum → keine Korrektur
- außerhalb des Bereichs → Korrektur in Richtung Zielwert

---

# 13. Regulation Run

Ein vollständiger Regelvorgang wird als eigener Durchlauf gespeichert.

Ein Regulation Run enthält beispielsweise:

- Id
- Tank
- Startzeit
- Endzeit
- Modus
- Status

Mögliche Modi:

- Simulation
- Dry Run
- Automatic

## Simulation

Das System arbeitet mit simulierten Sensoren und Aktoren.

## Dry Run

Das System berechnet notwendige Aktionen, führt diese jedoch nicht aus.

Beispiel:

- 3 Liter Wasser hinzufügen
- 25 ml Dünger A
- 25 ml Dünger B
- 33 ml Dünger C

## Automatic

Später werden reale Aktoren angesteuert.

Beispiel:

FastAPI / Regulation Engine
→ MQTT
→ ESP32
→ Dosierpumpe

---

# 14. Regulation Actions

Jede während eines Regulation Runs geplante oder ausgeführte Aktion wird gespeichert.

Beispiele:

- Wasser hinzufügen
- Dünger dosieren
- pH+ dosieren
- pH- dosieren
- Mischen
- Warten / Stabilisieren
- Warnung
- Fehler

Eine Regulation Action enthält beispielsweise:

- Id
- RegulationRunId
- Typ
- Menge
- Einheit
- Status
- Details
- Zeitpunkt

Dadurch kann später nachvollzogen werden:

- Was wurde wann geplant?
- Was wurde tatsächlich ausgeführt?
- Welche Mengen wurden dosiert?
- Warum wurde eine Aktion durchgeführt?
- Wo ist ein Fehler aufgetreten?

---

# 15. Sicherheitsmechanismen

Für spätere automatische Regelzyklen müssen Sicherheitsgrenzen definiert werden.

Beispiele:

- maximale Wassermenge pro Regelzyklus
- maximale Düngermenge pro Regelzyklus
- maximale Menge pH+
- maximale Menge pH-
- maximale Anzahl von Korrekturversuchen
- maximale Dauer eines Regelzyklus

Wenn eine Grenze überschritten wird:

1. Regelvorgang stoppen
2. Status auf Fehler setzen
3. Fehler speichern
4. Warnung erzeugen
5. manuelle Prüfung erforderlich

---

# 16. Simulation

Da zu Beginn keine echte Hardware erforderlich sein soll, wird eine Simulationsschicht entwickelt.

Beispielzustand:

- Volumen: 25 L
- EC: 4,7
- pH: 6,8

Ein simuliertes Regulation Run kann folgende Schritte durchführen:

1. Füllstand prüfen
2. Wasser simuliert hinzufügen
3. neue Messwerte erzeugen
4. EC prüfen
5. Rezept berechnen
6. Dünger simuliert dosieren
7. neue EC-Messung erzeugen
8. pH prüfen
9. pH-Korrektur simulieren
10. neue Messung erzeugen
11. Ergebnisse speichern

Die Fachlogik soll dabei nicht von der Simulation abhängig sein.

Später sollen Simulation und reale Hardware dieselben Schnittstellen verwenden.

---

# 17. Technische Architektur

Die Anwendung wird in Schichten organisiert.

```text
HTTP Request
     │
     ▼
FastAPI Router
     │
     ▼
Pydantic Schema
     │
     ▼
Service Layer
     │
     ├── Regulation Engine
     ├── Calculations
     └── Simulation / Hardware Interfaces
     │
     ▼
SQLAlchemy
     │
     ▼
PostgreSQL
```

Die FastAPI Router enthalten möglichst wenig Fachlogik.

Die eigentliche Fachlogik befindet sich in Services und Berechnungskomponenten.

---

# 18. Pydantic

Pydantic wird für Datenvalidierung und API-Schemas verwendet.

Beispiele:

- PlantCreate
- PlantUpdate
- PlantResponse
- FertilizerCreate
- TankCreate
- MeasurementCreate
- RegulationRunResponse

Pydantic-Schemas und SQLAlchemy-Modelle werden getrennt gehalten.

## SQLAlchemy

SQLAlchemy beschreibt die Persistenz und Datenbankbeziehungen.

## Pydantic

Pydantic beschreibt:

- API Requests
- API Responses
- Validierung
- Datenübertragung zwischen Schichten, sofern sinnvoll

---

# 19. Datenmodell

Die geplanten Kernobjekte sind. Alle `Id`-Felder sind ganze Zahlen (`INTEGER`). Die Datenbank vergibt sie beim INSERT (`AUTO INCREMENT` / PostgreSQL `SERIAL` bzw. `IDENTITY`).

## Plant

- Id
- Name
- Description

## GrowthStage

- Id
- PlantId
- Name
- Order
- EcMin
- EcTarget
- EcMax
- PhMin
- PhTarget
- PhMax

## Recipe

- Id
- GrowthStageId
- Name

## RecipeItem

- Id
- RecipeId
- FertilizerId
- Percentage

## Fertilizer

- Id
- Name
- Description
- EcEffectPerMlPerLiter

## Tank

- Id
- Name
- TargetVolume
- PlantId
- CurrentGrowthStageId

## Measurement

- Id
- TankId
- Timestamp
- Volume
- Ec
- Ph
- Temperature
- Source

## RegulationRun

- Id
- TankId
- StartedAt
- FinishedAt
- Mode
- Status

## RegulationAction

- Id
- RegulationRunId
- Type
- Amount
- Unit
- Status
- Details
- Timestamp

---

# 20. Objektbeziehungen

```text
Plant
  │
  └── 1 : n
        │
        ▼
   GrowthStage
        │
        └── 1 : 0..1
              │
              ▼
            Recipe
              │
              └── 1 : n
                    │
                    ▼
                RecipeItem
                    │
                    └── n : 1
                          │
                          ▼
                      Fertilizer


Tank
 ├── Plant
 ├── CurrentGrowthStage
 ├── Measurements
 │
 └── RegulationRuns
       │
       └── RegulationActions
```

---

# 21. Projektstruktur

Die geplante Projektstruktur lautet:

```text
nutrient-solution-manager/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── api/
│   │   ├── routers/
│   │   │   ├── plants.py
│   │   │   ├── growth_stages.py
│   │   │   ├── fertilizers.py
│   │   │   ├── recipes.py
│   │   │   ├── tanks.py
│   │   │   ├── measurements.py
│   │   │   └── regulation.py
│   │   │
│   │   └── dependencies.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── plant.py
│   │   ├── growth_stage.py
│   │   ├── fertilizer.py
│   │   ├── recipe.py
│   │   ├── tank.py
│   │   ├── measurement.py
│   │   ├── regulation_run.py
│   │   └── regulation_action.py
│   │
│   ├── schemas/
│   │   ├── plant.py
│   │   ├── growth_stage.py
│   │   ├── fertilizer.py
│   │   ├── recipe.py
│   │   ├── tank.py
│   │   ├── measurement.py
│   │   └── regulation.py
│   │
│   ├── services/
│   │   ├── plant_service.py
│   │   ├── tank_service.py
│   │   ├── measurement_service.py
│   │   └── regulation_service.py
│   │
│   ├── calculations/
│   │   ├── volume_calculator.py
│   │   ├── ec_calculator.py
│   │   └── ph_controller.py
│   │
│   ├── simulation/
│   │   ├── sensor_simulator.py
│   │   └── actuator_simulator.py
│   │
│   └── enums/
│       ├── measurement_source.py
│       ├── regulation_mode.py
│       ├── regulation_status.py
│       └── action_type.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── api/
│
├── alembic/
│
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

---

# 22. Architekturprinzipien

## API Layer

Verantwortlich für:

- HTTP Requests
- Routing
- Request Validation
- HTTP Responses

Technologie:

- FastAPI
- Pydantic

Die API-Schicht enthält keine komplexe Fachlogik.

---

## Service Layer

Verantwortlich für:

- Geschäftsprozesse
- Orchestrierung
- Koordination von Datenbank und Fachlogik

Beispiele:

- PlantService
- TankService
- MeasurementService
- RegulationService

---

## Calculation Layer

Enthält reine Berechnungslogik.

Beispiele:

- EC-Berechnung
- Wasserbedarfsberechnung
- Düngerverteilung
- pH-Korrekturentscheidung

Diese Komponenten sollen möglichst unabhängig von:

- FastAPI
- PostgreSQL
- SQLAlchemy
- MQTT

sein.

Dadurch können sie einfach getestet werden.

---

## Infrastructure

Verantwortlich für externe Systeme.

Beispiele:

- PostgreSQL
- SQLAlchemy
- Sensor-Simulation
- MQTT
- ESP32-Kommunikation

---

# 23. Datenbank

Als Datenbank wird PostgreSQL verwendet.

SQLAlchemy übernimmt die Abbildung zwischen Python-Objekten und Datenbanktabellen.

Alembic übernimmt:

- Erstellung von Migrationen
- Versionsverwaltung des Datenbankschemas
- Änderungen an Tabellen und Beziehungen

---

# 24. API

Die REST API wird mit FastAPI entwickelt.

Geplante Ressourcen:

```text
/plants
/growth-stages
/fertilizers
/recipes
/tanks
/measurements
/regulation-runs
```

Beispiele:

```text
POST   /plants
GET    /plants
GET    /plants/{id}
PUT    /plants/{id}
DELETE /plants/{id}
```

Später:

```text
POST /tanks/{id}/measurements
POST /tanks/{id}/regulation-runs
GET  /regulation-runs/{id}
```

---

# 25. Tests

Das Projekt soll automatisierte Tests enthalten.

Geplant:

## Unit Tests

Tests für:

- EC-Berechnung
- Rezeptberechnung
- Verteilung der Düngermengen
- Zielbereichsprüfung
- Sicherheitsgrenzen

## Integration Tests

Tests für:

- SQLAlchemy
- PostgreSQL
- Services
- Datenbankbeziehungen

## API Tests

Tests für:

- FastAPI Endpunkte
- Request Validation
- Response Models
- Fehlerbehandlung

---

# 26. Docker

Die Anwendung wird containerisiert.

Geplante Services:

```text
docker-compose
│
├── api
│   └── FastAPI
│
└── database
    └── PostgreSQL
```

Später optional:

```text
├── mqtt
│   └── Mosquitto
│
└── scheduler
```

---

# 27. Entwicklungsphasen

## Phase 1 – Projektgrundlage

- Python-Projekt erstellen
- FastAPI einrichten
- PostgreSQL einrichten
- Docker Compose einrichten
- SQLAlchemy konfigurieren
- Alembic konfigurieren
- Grundstruktur erstellen

---

## Phase 2 – Stammdaten

Implementierung von:

- Fertilizer
- Plant
- GrowthStage
- Recipe
- RecipeItem
- Tank

Dazu:

- SQLAlchemy Models
- Pydantic Schemas
- Services
- API Endpunkte
- Tests

---

## Phase 3 – Messungen

Implementierung von:

- Measurement Model
- Measurement Service
- Simulation
- Messhistorie
- Messquellen

---

## Phase 4 – Regulation Engine

Implementierung von:

1. Füllstandsprüfung
2. Wasserbedarfsberechnung
3. EC-Prüfung
4. Rezeptauswahl
5. EC-Berechnung
6. proportionale Düngerverteilung
7. pH-Prüfung
8. pH-Korrekturentscheidung
9. Sicherheitsgrenzen

---

## Phase 5 – Simulation und Historie

Implementierung von:

- Simulation Mode
- Dry Run
- RegulationRun
- RegulationAction
- Statusverwaltung
- Fehlerbehandlung

---

## Phase 6 – Hardware

Implementierung von:

- MQTT
- ESP32
- Sensorwerte
- Aktoren
- Dosierpumpen
- automatische Regelzyklen

---

# 28. Aktueller nächster Schritt

Der operative nächste Schritt steht im Lernpfad:

**LE 1.1 – Python-Projektstruktur und virtuelle Umgebung**

Das fachliche Datenmodell wird nicht vorab in einem großen Block finalisiert. Es wird
entlang der Lerneinheiten konkretisiert: zuerst Projektgrundlage, dann Stammdaten
(`Fertilizer`, `Plant`, `GrowthStage`, `Recipe`), später Tank, Messungen und Regulation.

Fachliche Reihenfolge der Stammdaten bleibt:

```text
Plant
    │
    └── GrowthStage
            │
            └── Recipe
                    │
                    └── RecipeItem
                            │
                            └── Fertilizer
```

Danach:

```text
Tank
    │
    ├── Measurement
    │
    └── RegulationRun
            │
            └── RegulationAction
```

---

# 29. Grundprinzip für die weitere Entwicklung

Die Anwendung soll schrittweise wachsen.

Die erste Version benötigt:

- keine echte Hardware
- keine MQTT-Kommunikation
- keine Dosierpumpen

Stattdessen wird zunächst mit:

- PostgreSQL
- FastAPI
- Pydantic
- SQLAlchemy
- Simulation

gearbeitet.

Die Fachlogik wird so entwickelt, dass Simulation und reale Hardware später austauschbar sind.

Dadurch kann das Projekt bereits vollständig getestet und weiterentwickelt werden, bevor die erste echte Hardware angeschlossen wird.
