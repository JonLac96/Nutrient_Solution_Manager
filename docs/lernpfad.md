# Lernpfad – Nutrient Solution Manager (Python)

Dieses Dokument ist unser gemeinsamer Fahrplan für die Entwicklung des **Nutrient Solution Managers**.

Es zerlegt das Projektkonzept in einzelne **Lerneinheiten (LE)**.

Jede Lerneinheit enthält:

- ein klares **Lernziel**,
- die Technologien und Konzepte, die dabei gelernt werden,
- eine Aufteilung, wer den Code hauptsächlich schreibt,
- einen **Checkpoint**, bevor wir zur nächsten Einheit weitergehen.

Der Lernpfad ist ein lebendes Dokument. Wir passen ihn an, wenn sich beim Entwickeln zeigt, dass eine andere Reihenfolge sinnvoller ist.

---

# 1. Technische Entscheidungen

| Thema | Entscheidung |
|---|---|
| Programmiersprache | **Python** |
| Python-Version | Aktuelle stabile Python-Version zum Projektstart |
| Web Framework | **FastAPI** |
| Datenvalidierung | **Pydantic** |
| ORM | **SQLAlchemy** |
| Datenbank | **PostgreSQL** |
| Datenbankmigrationen | **Alembic** |
| Tests | **pytest** |
| HTTP/API-Tests | FastAPI TestClient bzw. httpx |
| Integrationstest-Datenbank | PostgreSQL im Docker-Testcontainer bzw. später Testcontainers |
| API-Dokumentation | Automatisch durch FastAPI (OpenAPI, Swagger UI und ReDoc) |
| Containerisierung | **Docker** |
| Lokale Services | **Docker Compose** |
| Architektur | API → Service → Fachlogik → Infrastruktur |
| Primärschlüssel | **INTEGER, Auto-Increment** (PostgreSQL: `SERIAL` / `IDENTITY`) |
| Hardware-Kommunikation | später MQTT |
| Hardware | später ESP32 und Sensorik |
| Repository | GitHub |
| Git-Arbeitsweise | **Commits auf `main`** (Branches nur bei Bedarf) |
| Code-Formatierung | Ruff als Formatter/Linter, finale Konfiguration im Projekt |
| Abhängigkeitsverwaltung | **uv** + `pyproject.toml` inkl. Lockfile |

---

# 2. Zentrale Architektur

Die Anwendung wird grundsätzlich in folgende Bereiche getrennt:

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
     ├── Fachlogik / Regulation Engine
     ├── Berechnungen
     └── Simulation / Hardware-Abstraktionen
     │
     ▼
SQLAlchemy
     │
     ▼
PostgreSQL
```

Wichtig:

Die eigentliche Fachlogik soll möglichst unabhängig von FastAPI und PostgreSQL bleiben.

Dadurch kann dieselbe Fachlogik später verwendet werden für:

- REST API
- Simulation
- automatisierte Scheduler
- MQTT-Ereignisse
- reale ESP32-Hardware

---

# 3. Zusammenarbeitsprinzip

| Art der Aufgabe | Wer schreibt den Code | Meine Rolle |
|---|---|---|
| Fachliche Kernlogik (Berechnungen, Regeln, Regelkreise) | **Du** | Spezifikation vorab, Hilfestellung und Review danach |
| Python- und FastAPI-Grundlagen mit Lernwert | Gemeinsam bzw. ich zeige das erste Muster | Schrittweise Erklärung und Checkpoints |
| Projekt- und Infrastruktur-Setup | Gemeinsam in kleinen Schritten | Erklären, warum etwas benötigt wird |
| Reine Konfigurations-Boilerplate | Ich oder gemeinsam, abhängig vom Lernwert | Konzept kurz erklären |
| Wiederkehrende CRUD-Muster | Erstes Beispiel gemeinsam, danach **du** | Review und Feedback |
| SQLAlchemy-Modelle und Beziehungen | Erstes Beispiel gemeinsam, danach zunehmend **du** | Review und Erklärung |
| Tests | Zunächst gemeinsam, später zunehmend **du** | Testfälle spezifizieren und Review |

Grundprinzip:

Wir entwickeln nicht möglichst schnell möglichst viel Code.

Jede Lerneinheit soll ein konkretes Konzept vermitteln und am Ende ein funktionierendes Ergebnis besitzen.

---

# 4. Testing-Strategie

Tests entstehen von Anfang an und nicht erst am Ende des Projekts.

Es werden grundsätzlich drei Ebenen unterschieden.

## Unit Tests

Testen einzelne Funktionen oder Klassen isoliert.

Beispiele:

- EC-Berechnung
- Berechnung der Düngerverteilung
- Prüfung eines Zielbereichs
- Sicherheitsgrenzen

Ziel:

```text
Input
  │
  ▼
Calculation / Domain Logic
  │
  ▼
Expected Result
```

Unit Tests sollen möglichst keine:

- Datenbank
- HTTP-Requests
- Docker-Container

benötigen.

---

## Integration Tests

Testen mehrere Komponenten im Zusammenspiel.

Beispiele:

- Service speichert Daten über SQLAlchemy
- Beziehungen zwischen Plant und GrowthStage funktionieren
- PostgreSQL-Persistenz
- Datenbankconstraints

---

## API Tests

Testen die HTTP-Schnittstelle.

Beispiel:

```text
POST /plants
     │
     ▼
FastAPI Router
     │
     ▼
Pydantic Validation
     │
     ▼
Service
     │
     ▼
Database
```

Dabei wird geprüft:

- Statuscode
- Request-Validierung
- Response-Daten
- Fehlerbehandlung

---

# 5. Geplante Projektstruktur

```text
nutrient-solution-manager/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── api/
│   │   ├── routers/
│   │   └── dependencies.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   │
│   ├── models/
│   │
│   ├── schemas/
│   │
│   ├── services/
│   │
│   ├── calculations/
│   │
│   ├── simulation/
│   │
│   └── enums/
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

Die genaue Struktur kann sich während des Projekts weiterentwickeln.

---

# 6. Lerneinheiten

Status-Legende:

⬜ offen · 🔶 in Arbeit · ✅ abgeschlossen

---

# Phase 1 – Python Backend und Projektgrundlage

Ziel dieser Phase:

Eine lauffähige Python-Anwendung mit FastAPI, PostgreSQL, SQLAlchemy und Docker aufbauen.

---

## LE 1.1 – Python-Projektstruktur und virtuelle Umgebung

### Lernziel

Grundlagen eines professionellen Python-Projekts verstehen.

Themen:

- Projektstruktur
- Python-Packages
- `__init__.py`
- virtuelle Umgebungen
- Abhängigkeiten
- `pyproject.toml`
- **uv** (virtuelle Umgebung, Abhängigkeiten, Lockfile)
- Module und Imports

`pyproject.toml` wird in dieser Lerneinheit **erklärt und erst danach angelegt**.

Dabei muss klar werden:

- was die Datei ist,
- welches Problem sie löst,
- was typischerweise hineingehört,
- wie uv sie nutzt,
- warum wir nicht nur eine `requirements.txt` verwenden.

Nicht stillschweigend als reine Boilerplate erzeugen.

### Ergebnis

Ein leeres, strukturiertes Python-Projekt ist vorhanden.

### Wer schreibt

Gemeinsam.

### Status

✅ abgeschlossen

---

## LE 1.2 – FastAPI Grundgerüst

### Lernziel

Die grundlegende Funktionsweise einer Web API mit FastAPI verstehen.

Themen:

- FastAPI Application
- Endpunkte
- HTTP-Methoden
- Path Parameter
- Query Parameter
- automatische OpenAPI-Dokumentation

### Ergebnis

Die API startet und besitzt erste Test-Endpunkte.

Beispiel:

```text
GET /
GET /health
```

### Wer schreibt

Gemeinsam als erstes FastAPI-Beispiel.

### Status

✅ abgeschlossen

---

## LE 1.3 – Pydantic Grundlagen

### Lernziel

Verstehen, wie Daten in FastAPI validiert werden.

Themen:

- Pydantic BaseModel
- Request Models
- Response Models
- optionale Felder
- Validierung
- Typen
- Fehlermeldungen

### Ergebnis

Ein erster API-Endpunkt verarbeitet ein Pydantic-Modell.

### Wer schreibt

Gemeinsam.

### Status

✅ abgeschlossen

---

## LE 1.4 – Docker Compose + PostgreSQL

### Lernziel

Containerisierung und Datenbankbetrieb verstehen.

Themen:

- Docker Container
- Docker Compose
- PostgreSQL
- Environment Variables
- Volumes
- Persistenz

### Ergebnis

PostgreSQL läuft über Docker Compose.

### Wer schreibt

Gemeinsam mit Erklärung.

### Status

✅ abgeschlossen

---

## LE 1.5 – SQLAlchemy Grundgerüst

### Lernziel

Verstehen, wie Python-Objekte mit Datenbanktabellen verbunden werden.

Themen:

- SQLAlchemy Engine
- Session
- Declarative Models
- Columns
- Primary Keys
- Datenbankverbindung

### Ergebnis

Ein minimales SQLAlchemy-Modell kann mit PostgreSQL verbunden werden.

### Wer schreibt

Gemeinsam.

### Status

✅ abgeschlossen

---

## LE 1.6 – Alembic Migrationen

### Lernziel

Datenbankschema versionieren.

Themen:

- Migration
- Revision
- Upgrade
- Downgrade
- Schemaänderungen

### Ergebnis

Die erste Datenbankmigration wird erstellt und ausgeführt.

### Wer schreibt

Gemeinsam mit Erklärung.

### Status

✅ abgeschlossen

---

## LE 1.7 – pytest Grundlagen

### Lernziel

Automatisierte Tests in Python verstehen.

Themen:

- pytest
- Teststruktur
- Assertions
- Fixtures
- Arrange / Act / Assert

### Ergebnis

Ein erster Unit Test läuft erfolgreich.

### Wer schreibt

Gemeinsam.

### Status

✅ abgeschlossen

---

# Phase 2 – Erstes vollständiges Feature

Ziel dieser Phase:

Ein vollständiges Feature durch alle Schichten implementieren.

```text
API
 ↓
Pydantic
 ↓
Service
 ↓
SQLAlchemy
 ↓
PostgreSQL
```

---

## LE 2.1 – Fertilizer: SQLAlchemy Model

### Lernziel

Ein echtes Datenbankmodell erstellen.

Felder:

- Id
- Name
- Description
- EcEffectPerMlPerLiter

Themen:

- SQLAlchemy Model
- Tabellenname
- Datentypen
- Constraints

### Ergebnis

Die Tabelle `fertilizers` kann über Alembic erstellt werden.

### Wer schreibt

Erstes Beispiel gemeinsam.

### Status

✅ abgeschlossen

---

## LE 2.2 – Fertilizer: Pydantic Schemas

### Lernziel

SQLAlchemy Models und Pydantic Schemas klar voneinander unterscheiden.

Schemas:

- FertilizerCreate
- FertilizerUpdate
- FertilizerResponse

### Ergebnis

Requests und Responses sind sauber validiert.

### Wer schreibt

Du nach dem gemeinsamen Muster.

### Status

✅ abgeschlossen

---

## LE 2.3 – Fertilizer Service

### Lernziel

Geschäftslogik von der API trennen.

Themen:

- Service Layer
- Datenbankzugriff über Session
- Fehlerbehandlung

Methoden:

- create
- get
- get_all
- update
- delete

### Wer schreibt

Gemeinsam, danach Review.

### Status

✅ abgeschlossen

---

## LE 2.4 – Fertilizer API CRUD

### Lernziel

REST-Endpunkte mit FastAPI erstellen.

Endpunkte:

```text
POST   /fertilizers
GET    /fertilizers
GET    /fertilizers/{id}
PUT    /fertilizers/{id}
DELETE /fertilizers/{id}
```

### Ergebnis

Das erste vollständige CRUD-Feature funktioniert.

### Wer schreibt

Erstes Beispiel gemeinsam.

### Status

✅ abgeschlossen

---

## LE 2.5 – Fertilizer Tests

### Lernziel

Unit-, Integrations- und API-Tests unterscheiden.

Tests:

- Service Tests
- Datenbanktests
- API Tests

### Wer schreibt

Gemeinsam.

### Status

🔶 in Arbeit

---

# Phase 3 – Stammdaten und Beziehungen

Ziel:

Die zentralen Objekte des Systems modellieren.

---

## LE 3.1 – Plant

### Lernziel

Ein weiteres CRUD-Feature zunehmend selbstständig entwickeln.

### Wer schreibt

Du.

### Status

⬜ offen

---

## LE 3.2 – GrowthStage

### Lernziel

Eine 1:n-Beziehung modellieren.

```text
Plant
  │
  └── GrowthStage
```

Themen:

- Foreign Keys
- SQLAlchemy Relationships
- Datenbankreferenzen

### Wer schreibt

Du, mit Review.

### Status

⬜ offen

---

## LE 3.3 – Recipe

### Lernziel

Beziehungen zwischen GrowthStage und Recipe modellieren.

### Wer schreibt

Du.

### Status

⬜ offen

---

## LE 3.4 – RecipeItem

### Lernziel

Mehrere Beziehungen und fachliche Validierung.

```text
Recipe
   │
   └── RecipeItem
           │
           └── Fertilizer
```

Fachliche Regel:

Die Summe der Prozentwerte einer Rezeptur soll 100 % ergeben.

### Wer schreibt

Du.

### Status

⬜ offen

---

## LE 3.5 – Tank

### Lernziel

Mehrere Beziehungen in einem Objekt modellieren.

Tank verweist auf:

- Plant
- CurrentGrowthStage

### Wer schreibt

Du.

### Status

⬜ offen

---

# Phase 4 – Messungen und Simulation

Ziel:

Messwerte unabhängig von ihrer Quelle verarbeiten.

---

## LE 4.1 – Measurement Model

### Lernziel

Zeitreihendaten modellieren.

Felder:

- Tank
- Timestamp
- Volume
- EC
- pH
- Temperature
- Source

### Wer schreibt

Du.

### Status

⬜ offen

---

## LE 4.2 – Measurement Source Abstraktion

### Lernziel

Simulation und spätere Hardware austauschbar gestalten.

Konzept:

```text
Measurement Source
        │
        ├── Simulator
        │
        ├── Manual Input
        │
        ├── MQTT
        │
        └── Sensor
```

### Ergebnis

Die Fachlogik kennt nicht die konkrete Quelle des Messwerts.

### Wer schreibt

Du, Schnittstelle wird vorher gemeinsam geplant.

### Status

⬜ offen

---

## LE 4.3 – Messhistorie

### Lernziel

Zeitreihen speichern und abfragen.

Themen:

- Filter
- Query Parameter
- Sortierung
- Pagination (später optional)

### Wer schreibt

Du.

### Status

⬜ offen

---

## LE 4.4 – Sensor Simulation

### Lernziel

Eine einfache Simulation implementieren.

Die Simulation liefert zunächst:

- Volume
- EC
- pH

Später können Simulationen realistischer werden.

### Wer schreibt

Du.

### Status

⬜ offen

---

# Phase 5 – Regulation Engine

Ziel:

Die zentrale Fachlogik des Systems entwickeln.

Diese Phase ist bewusst weitgehend unabhängig von:

- FastAPI
- PostgreSQL
- Docker
- MQTT

Die Berechnungen sollen als reine Python-Logik testbar sein.

---

## LE 5.1 – Zielbereichsprüfung

### Lernziel

Min/Target/Max-Werte verarbeiten.

Regel:

```text
Wert innerhalb Min/Max
    → keine Aktion

Wert außerhalb
    → Korrektur Richtung Target
```

### Wer schreibt

Du.

### Status

⬜ offen

---

## LE 5.2 – Wasserbedarfsberechnung

### Lernziel

Füllstand mit Zielvolumen vergleichen.

Beispiel:

```text
Target Volume: 30 L
Current Volume: 25 L

Water Required: 5 L
```

### Wer schreibt

Du.

### Status

⬜ offen

---

## LE 5.3 – EC-Berechnung

### Lernziel

Rezepturbasierte Berechnung implementieren.

Die Berechnung umfasst:

1. EC-Differenz bestimmen
2. Wirkung der Rezeptur berechnen
3. Gesamtmenge bestimmen
4. Gesamtmenge proportional auf Dünger verteilen

### Wer schreibt

**Du**

Meine Rolle:

- Spezifikation
- Besprechung von Testfällen
- Code Review

### Status

⬜ offen

---

## LE 5.4 – pH-Regelungslogik

### Lernziel

Einen iterativen Regelkreis modellieren.

```text
Measure
   │
   ▼
Evaluate
   │
   ▼
Dose
   │
   ▼
Mix
   │
   ▼
Wait
   │
   ▼
Measure Again
```

### Wer schreibt

Du.

### Status

⬜ offen

---

## LE 5.5 – Regulation Engine Orchestrierung

### Lernziel

Mehrere Berechnungen und Schritte zu einem Ablauf verbinden.

Reihenfolge:

```text
Volume
   ↓
Water Correction
   ↓
Measurement
   ↓
EC Correction
   ↓
Measurement
   ↓
pH Correction
```

### Wer schreibt

Du.

### Status

⬜ offen

---

# Phase 6 – Regulation Runs und Historie

Ziel:

Vollständige Regelvorgänge speichern und nachvollziehbar machen.

---

## LE 6.1 – RegulationRun

### Lernziel

Einen vollständigen Regelvorgang persistieren.

Felder:

- Tank
- StartedAt
- FinishedAt
- Mode
- Status

### Wer schreibt

Du.

### Status

⬜ offen

---

## LE 6.2 – RegulationAction

### Lernziel

Einzelne Aktionen eines Regelvorgangs speichern.

Beispiele:

- Wasser hinzufügen
- Dünger dosieren
- pH+ dosieren
- pH- dosieren
- Warnung
- Fehler

### Wer schreibt

Du.

### Status

⬜ offen

---

## LE 6.3 – Dry Run

### Lernziel

Berechnungen durchführen, ohne Aktionen auszuführen.

Beispiel:

```text
Planned Actions

+ 3 L Water
+ 25 ml Fertilizer A
+ 25 ml Fertilizer B
+ 33 ml Fertilizer C
```

### Wer schreibt

Du.

### Status

⬜ offen

---

## LE 6.4 – Sicherheitsgrenzen

### Lernziel

Automatisierung gegen fehlerhafte Berechnungen absichern.

Grenzen:

- maximale Wassermenge
- maximale Düngermenge
- maximale pH+-Menge
- maximale pH--Menge
- maximale Anzahl Korrekturversuche

### Wer schreibt

Du.

### Status

⬜ offen

---

# Phase 7 – Dockerisierung der vollständigen Anwendung

Ziel:

Die komplette Anwendung reproduzierbar starten.

---

## LE 7.1 – FastAPI Dockerfile

### Lernziel

Eine Python-Webanwendung containerisieren.

### Wer schreibt

Gemeinsam.

### Status

⬜ offen

---

## LE 7.2 – Docker Compose Gesamtumgebung

### Lernziel

Mehrere Services gemeinsam starten.

```text
Docker Compose
│
├── API
│
└── PostgreSQL
```

Später:

```text
├── MQTT
└── Scheduler
```

### Wer schreibt

Gemeinsam.

### Status

⬜ offen

---

# Phase 8 – Hardware und MQTT

Diese Phase wird detailliert, sobald die vorherigen Phasen stabil funktionieren.

Geplante Themen:

- MQTT Grundlagen
- MQTT Client in Python
- MQTT Topics
- ESP32 Sensoren
- Sensorwerte empfangen
- Aktoren ansteuern
- Dosierpumpen
- Fehlerbehandlung
- automatische Regulation

Mögliche Architektur:

```text
ESP32 Sensor
      │
      ▼
MQTT Broker
      │
      ▼
Nutrient Solution Manager
      │
      ▼
Regulation Engine
      │
      ▼
MQTT
      │
      ▼
ESP32 Aktor
```

---

# 7. Lernstrategie

Der Schwerpunkt liegt nicht darauf, möglichst schnell eine große Anwendung fertigzustellen.

Der Schwerpunkt liegt darauf, die wichtigsten Konzepte mehrfach praktisch anzuwenden.

Das Muster lautet:

```text
1. Konzept verstehen
        ↓
2. Kleines Beispiel entwickeln
        ↓
3. Selbst implementieren
        ↓
4. Tests schreiben
        ↓
5. Code Review
        ↓
6. Nächstes Konzept
```

Dadurch wird verhindert, dass große Teile des Projekts entstehen, ohne dass die verwendeten Technologien verstanden werden.

---

# 8. Aktueller nächster Schritt

Stand 2026-09-15, LE 2.4 abgeschlossen, LE 2.5 begonnen.

## Abgeschlossen

- **LE 1.1–1.7** – Phase 1 (Projekt, FastAPI, Pydantic, Docker/Postgres, SQLAlchemy, Alembic, pytest)
- **LE 2.1** – Fertilizer-Model, Revision `b2741119ca18`
- **LE 2.2** – Schemas `FertilizerCreate` / `FertilizerUpdate` / `FertilizerResponse`; `id: int`; `from_attributes=True`; Tests in `tests/unit/test_fertilizer_schema.py`. Primärschlüssel INTEGER Auto-Increment, Revision `626c042a758a`. Commit `d5d3917`
- **LE 2.3** – `FertilizerService` (`app/services/fertilizer.py`): `create`, `get`, `get_all`, `update`, `delete`. Session im Konstruktor. Fehlende Id → `LookupError`. Update: `model_dump(exclude_unset=True)`. Commit `6022bdf`
- **LE 2.4** – Fertilizer API CRUD: `app/api/dependencies.py` (`get_db` mit `yield`), `app/api/routers/fertilizers.py` (POST 201, GET Liste, GET Detail, PUT, DELETE 204). `LookupError` → `HTTPException(404)` im Router. Dummy-`POST /fertilizers` in `app/main.py` entfernt, Router per `include_router` eingebunden. Verben außer POST vom Lernenden.
- Git-Arbeitsweise bewusst auf **Commits auf `main`** umgestellt (`docs/workflow.md`, Commit `aea9b37`)

## In Arbeit

**LE 2.5 – Fertilizer Tests** (🔶). Lernziel: Unit-, Integrations- und API-Tests unterscheiden (Service, Datenbank, HTTP). Bisher nur Schema-Unit-Tests in `tests/unit/`. Ordner `tests/integration/` und `tests/api/` existieren noch nicht.

## Nächster Schritt

Drei Testebenen kurz einordnen, dann **einen** ersten Test gemeinsam: Service-Test für fehlende Id (`get` → `LookupError`), noch ohne HTTP und ohne alle CRUD-Fälle.

Erst nach Bestätigung Code schreiben. Nicht alle drei Ebenen in einem Rutsch.

### Arbeitsweise (verbindlich)

LE 2.5 ist das **erste** Test-Muster für Service/API und darf gemeinsam entstehen. Danach weitere Fälle zunehmend der Lernende. Service nicht um HTTP erweitern. Ab Phase 3 wieder der Lernende.

**Nach jeder Lerneinheit** fragen: abschließen? committen? nächste LE beginnen?

## Hinweise aus den Sitzungen

- **Primärschlüssel:** INTEGER Auto-Increment, nicht UUID. Create ohne Id; DB vergibt sie; Response `id: int`. `DemoRecord` bleibt UUID.
- Service gibt ORM-`Fertilizer` zurück, nicht `FertilizerResponse`. FastAPI wandelt über `from_attributes` um.
- `LookupError` im Service, `HTTPException(404)` erst im Router. Decorator-`status_code` gilt nur im Erfolgsfall (POST 201, DELETE 204; GET/PUT bleiben 200).
- `get`/`update`/`delete`: fehlende Id über `self.get(...)` (ein Fehlerpfad).
- Pydantic-Update: `data.model_dump(exclude_unset=True)`, Variable z. B. `updates` — nicht `.items()` direkt auf dem Schema.
- FastAPI-`Depends(get_db)` für Fertilizer-Routen. Demo-Records dürfen `with SessionLocal()` behalten.
- Python, nicht C#: f-String `f"..."`, nicht `$"..."`; `if value is not None`, nicht `value not None`; Typen an der Funktion (`-> list[Fertilizer]`), nicht `list Fertilizer x =`. `except`, nicht `exept`. `try`/`except` einrücken. Methodenaufruf braucht `()`.
- Vor Reviews **speichern** (Editor und Platte liefen auseinander).
- **Git:** Arbeit auf `main`. `origin/main` ist `[gone]`. Nicht ungefragt pushen. Alte Branches (`le-1-6-alembic`, `le-2-2-fertilizer-schemas`, `le-2-3-fertilizer-service`, …) nicht weiterbenutzen.
- Parametrize bleibt zurückgestellt. Fixture: `.copy()`, dann ein Feld setzen.
- Alembic-Notiz des Lernenden: `notes/alembic-tabelle-fertilizers.md` (gitignored).
- Sitzungsende immer über `docs/kistart.md` Abschnitt „Sitzung beenden“.

## Nicht als Nächstes

- alle Service-, DB- und API-Tests in einem Rutsch
- Testcontainers (laut Lernpfad später)
- Demo-Records auf Service/`Depends` umbauen
- Plant CRUD (LE 3.1)
- Parametrize
- ungefragt pushen

