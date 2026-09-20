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
| Datenbank | **SQLite** (Datei `nsm.db` im Projektroot) |
| Datenbankmigrationen | **Alembic** |
| Tests | **pytest** |
| HTTP/API-Tests | FastAPI TestClient bzw. httpx |
| Integrationstest-Datenbank | SQLite (Datei bzw. später Testdatei) |
| API-Dokumentation | Automatisch durch FastAPI (OpenAPI, Swagger UI und ReDoc) |
| Containerisierung | **Docker** später (Phase 7), kein Datenbank-Container |
| Architektur | API → Service → Fachlogik → Infrastruktur |
| Primärschlüssel | **INTEGER, Auto-Increment** (SQLite: `INTEGER PRIMARY KEY`) |
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
SQLite
```

Wichtig:

Die eigentliche Fachlogik soll möglichst unabhängig von FastAPI und der Datenbank bleiben.

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
- SQLite-Persistenz
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

Eine lauffähige Python-Anwendung mit FastAPI, SQLite, SQLAlchemy aufbauen.

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

## LE 1.4 – SQLite als lokale Datenbank

### Lernziel

Eine dateibasierte Datenbank verstehen und lokal betreiben.

Themen:

- SQLite
- Unterschied zu einem Datenbankserver
- Datenbankdatei im Projektroot
- Persistenz ohne Container

Ursprünglich Docker Compose + PostgreSQL. Am 2026-09-16 bewusst auf SQLite (`nsm.db`) umgestellt.

### Ergebnis

Die Datei `nsm.db` liegt im Projektroot. Alembic erzeugt die Tabellen.

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

Ein minimales SQLAlchemy-Modell kann mit SQLite verbunden werden.

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
SQLite
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

✅ abgeschlossen

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

✅ abgeschlossen

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

🔶 in Arbeit

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
- SQLite
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
└── API
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

Stand 2026-09-20.

## Abgeschlossen

- **LE 1.1–1.7** – Phase 1
- **LE 2.1–2.5** – Fertilizer durch alle Schichten inkl. Tests. Commits u. a. `cc86dd0`, `bc85ca4`
- **Datenbank:** SQLite `nsm.db`. Commit `8015bff`
- **LE 3.1 – Plant** – Model `app/models/plant.py`, Revision `6966518b98df`, Schemas, `PlantService`, Router `/plants`, Tests (Unit leer-Name, Integration get-fehlend, API POST 201). Fixtures in `tests/conftest.py`. Dummy-`GET /plants` und Demo-Record-Routen aus `main.py` entfernt. Commit folgt mit den Tests.

## In Arbeit

**LE 3.2 – GrowthStage** (🔶). Erste **1:n-Beziehung**. **Der Lernende schreibt.**

```text
Plant  1 ──n  GrowthStage
```

Felder laut Projektkonzept:

- Id (INTEGER Auto-Increment)
- PlantId (Foreign Key → `plants.id`)
- Name
- Order
- EcMin, EcTarget, EcMax
- PhMin, PhTarget, PhMax

Noch kein GrowthStage-Code. Recipe (LE 3.3) kommt danach.

## Nächster Schritt in der nächsten Sitzung

1. `docs/kistart.md` lesen, dann **diesen gesamten Abschnitt**.
2. Kurz: Was ist ein Foreign Key? (siehe Hinweise)
3. Lernender schreibt nur das SQLAlchemy-Model `GrowthStage` in `app/models/growth_stage.py`, Export in `__init__.py`.
4. Review, dann Alembic (`create growth_stages`).

Nicht in einem Rutsch: Relationship-Attribute, Schemas, Service, Router, Tests.

`order` ist in SQL ein Schlüsselwort. Spaltenname im Code: `sort_order` (Python/snake_case), Konzeptfeld bleibt „Order“.

### Arbeitsweise (verbindlich)

Ab Phase 3 schreibt der Lernende. Agent: Konzept, Review. Plant/Fertilizer sind Muster; Foreign Key ist neu – erst erklären, dann Model.

**Nach jeder Lerneinheit** fragen: abschließen? committen? nächste LE beginnen?

## Hinweise aus den Sitzungen

- **Datenbank:** SQLite, `nsm.db` (gitignored). `check_same_thread=False`. Alembic: `render_as_batch=True`.
- **Tests:** Unit ohne DB/HTTP. Integration: `LookupError`, nicht `None`. Persistenz: **zweite** Session. API: `TestClient`. Fixture-Ort: `tests/conftest.py` (gilt für unit/integration/api). `.copy()` vor Mutation. Testdateien vor pytest **speichern**.
- `include_router` braucht `router` aus dem Modul, nicht das Modul selbst.
- `exclude_unset=True` bei Updates, nicht `exclude_none`.
- `from_attributes=True` nur am Response-Schema (ORM → JSON).
- `LookupError` im Service, `HTTPException(404)` im Router.
- **Git:** `main`. `origin/main` ist `[gone]`. Nicht ungefragt pushen.
- Parametrize zurückgestellt.
- Sitzungsende: `docs/kistart.md` „Sitzung beenden“.

## Nicht als Nächstes

- Recipe / RecipeItem (LE 3.3+)
- GrowthStage-CRUD komplett in einem Schritt
- PostgreSQL / Docker Compose / Testcontainers
- Demo-Records wieder anbauen
- Parametrize
- ungefragt pushen

