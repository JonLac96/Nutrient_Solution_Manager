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

Stand 2026-10-01, Sitzung beendet.

## Abgeschlossen

- **LE 1.1–1.7** – Phase 1
- **LE 2.1–2.5** – Fertilizer durch alle Schichten inkl. Tests. Commits u. a. `cc86dd0`, `bc85ca4`
- **Datenbank:** SQLite `nsm.db` (gitignored). Commit `8015bff`
- **LE 3.1 – Plant** – Model `app/models/plant.py`, Revision `6966518b98df`, Schemas, `PlantService`, Router `/plants`. Tests: Unit leerer Name, Integration `get` → `LookupError`, API `POST /plants` → 201. Plant-CRUD-Code: Commit `2cd03a8`. Tests + Fixture-Umzug: Commit `507f7d3`
- **LE 3.2 Model + Migration + `relationship()`** — Commit `db07163`. Tabelle `growth_stages`, Revision `5b10439fdc69` (`down_revision = 6966518b98df`). `plant_id` bleibt, `relationship()` auf beiden Seiten. `sort_order` Pflichtfeld. EC/pH als `Float`
- **LE 3.2 Schemas + Service** — Commit `20a01ab`. `GrowthStageCreate`, `GrowthStageUpdate`, `GrowthStageResponse`; Service mit `create`, `get`, `get_all`, `update`, `delete`. `GrowthStageUpdate` hat **kein** `plant_id`
- **LE 3.2 Router** — `app/api/routers/growth_stages.py`, in `app/main.py` eingehängt. Commit `741b41f`
- **LE 3.2 Tests bis `get` und Session-Fixtures** — Commit `8e94b93` (auf `origin/main`). `tests/unit/test_growth_stage_schema.py` (leerer Name, negatives `ec_min`). Integration nur `get` → `LookupError`. Fixture `session` entfernt, `open_session` ist die einzige Session-Fixture
- **`open_session` erklärt** (2026-10-01). Nicht noch einmal als Einstieg erklären, außer der Lernende fragt
- **LE 3.2 Integration `create`** (2026-10-01, **noch nicht committet**) — `test_create_growth_stage` in `tests/integration/test_growth_stage_service.py`. Echte `plant_id` über `create_plant`, Payload per `model_copy`. Zurücklesen in einem zweiten `open_session()`, Assert `plant_id`. Review bestanden
- **LE 3.2 Integration `update`, fast fertig** (2026-10-01, **noch nicht committet**) — `test_update_growth_stage`. Drei Sessions: anlegen, `GrowthStageUpdate(name="Bluete")`, `get` in neuer Session, Assert `name`. Am Ende der Sitzung: `uv run pytest tests/unit/test_growth_stage_schema.py tests/integration/test_growth_stage_service.py` → 5 passed

## In Arbeit

**LE 3.2 – GrowthStage** (🔶). Model, Beziehung, Schemas, Service und Router sind fertig. Schema-Unit-Tests sind da. Integration: `get`, `create` und `update` (ohne die Prüfung, dass `plant_id` unverändert bleibt). `delete` und API-Tests fehlen.

```text
Plant  1 ──n  GrowthStage
```

## Erste Handlung der nächsten Session (verbindlich)

`open_session`, Router und `relationship()` nicht erneut erklären, außer der Lernende fragt. Nicht LE 3.3 anfangen. `create_plant` nicht wieder auf eine eigene Session umbauen.

1. `docs/kistart.md` lesen, dann **diesen gesamten Abschnitt**.
2. Kurz zusammenfassen, wo LE 3.2 steht (siehe „In Arbeit“).
3. Der Lernende ergänzt in `test_update_growth_stage` im dritten `with` die Zeile `assert growth_stage.plant_id == plant_id_1`. `plant_id_1` ist ein `int` und nach dem ersten `with` noch gültig. Danach Review. Erst dann `delete`.

### Tests, die noch offen sind

| Datei | Stand |
|---|---|
| `tests/unit/test_growth_stage_schema.py` | fertig (leerer Name, negatives `ec_min`) |
| `tests/integration/test_growth_stage_service.py` | `get` → `LookupError` fertig. `test_create_growth_stage` fertig. `test_update_growth_stage` prüft `name == "Bluete"` in einer frischen Session; es fehlt `plant_id` unverändert. Offen danach: `delete()` und anschließend `get()` wirft `LookupError` |
| `tests/api/test_growth_stages.py` | fehlt. `POST /growth-stages` → 201; `GET /growth-stages/{id}` mit unbekannter Id → 404 |

Nächster Test nach der einen Assert-Zeile und dem Review: `delete()` in `tests/integration/test_growth_stage_service.py`. Muster: anlegen, in einer zweiten Session löschen, in einer dritten `get` und `pytest.raises(LookupError)`. Echte `plant_id` über `create_plant`.

### Arbeitsweise (verbindlich)

Ab Phase 3 schreibt der Lernende den Fachcode und die Tests. Agent: Konzept, Review, Debugging. Der `create`-Test wurde in dieser Sitzung auf Wunsch des Lernenden vom Agenten umgebaut (`model_copy`, Annotation `Callable[[Session, PlantCreate], int]`). `update` und `delete` schreibt der Lernende.

**Nach jeder Lerneinheit** fragen: abschließen? committen? nächste LE beginnen? LE 3.2 ist noch nicht abgeschlossen.

## Hinweise aus den Sitzungen

- **`open_session`:** einzige Session-Fixture. Signatur `Callable[[], AbstractContextManager[Session]]`. Aufruf `with open_session() as session`. Jeder Aufruf ist eine neue Session, der `with`-Block schließt sie. Persistenzprüfungen brauchen einen weiteren Aufruf (Identity Map). Die Fixture `session` ist gelöscht und bleibt gelöscht.
- **`create_plant` (bewusst so, 2026-10-01):** Signatur `Callable[[Session, PlantCreate], int]`. Der Test übergibt seine offene Session. Die Fixture öffnet keine eigene. `PlantService.create` committet **diese** Session; andere noch offene Änderungen in derselben Session werden mitgeschrieben. Die `int`-Id wird innerhalb von `_make` gelesen, solange die Session des Aufrufers offen ist. Aufruf nur innerhalb von `with open_session() as session`.
- **`plant_create_1`:** ist seit 2026-10-01 eine Fixture (`@pytest.fixture`) und liefert ein `PlantCreate`. `grow_stage_create_1` ist eine Fixture mit festem `plant_id=1`. Das Schema prüft keinen Fremdschlüssel. Integration und API überschreiben die Id mit `model_copy(update={"plant_id": plant_id})` und einer echten Id von `create_plant`. Die Fixture selbst nicht per `grow_stage_create_1.plant_id = ...` verändern. `valid_growth_stage_payload` mit `"plant_id": 1` nur für Schema-Unit-Tests. `existing_plant_id` und `plant1` gibt es nicht.
- **`model_copy`:** Pydantic-Methode. Gibt ein neues Modell zurück und ersetzt nur die Felder in `update`. Das Fixture-Objekt bleibt unverändert.
- **`GrowthStageUpdate`:** kein `plant_id`. Ein Feld ohne Default ist bei Pydantic Pflicht; `plant_id: int | None` ohne `= None` würde jedes Update zu einem Pflicht-`plant_id` machen. Das wurde in dieser Sitzung ausprobiert und wieder entfernt. Ob ein Stadium die Pflanze wechseln darf, ist nicht entschieden. Der Update-Test ändert `name`.
- **`model_validate`:** Klassenmethode, Dict rein, Modell oder `ValidationError`. Keys müssen die Feldnamen exakt treffen. Ungültige Werte ins kopierte Dict legen. Assert auf dem Schema, das geprüft werden soll.
- **`plant_id` und `relationship()`:** Spalte bleibt. `relationship()` ist nur die Python-Navigation. Keine neue Alembic-Revision dafür.
- **Service-Fallen:** `get_all` ist `scalars(select(GrowthStage)).all()`. `update`/`delete` rufen `self.get(growth_stage_id)` auf. `commit()` mit Klammern. `delete` committet. In `update` kein extra `add`. `__init__(...) -> None`.
- **Import in `conftest.py`:** `GrowthStageCreate` kommt dort aus `app.services.growth_stage`, weil das Service-Modul die Schema-Klasse importiert. Der Test importiert sie aus `app.schemas.growth_stage`. Nicht im Vorbeigehen „aufräumen“, ohne den Import im Service zu prüfen.
- **Datenbank:** SQLite, `nsm.db`. Engine: `check_same_thread=False`. Alembic: `render_as_batch=True`. Autogenerate braucht Model-Import in `app/models/__init__.py`. Bei `no such table: ...`: `uv run alembic upgrade head`. Details: `docs/alembic.md`.
- **`uv` fehlt oder Befehle nicht gefunden:** Neues Terminal öffnen. `uv.exe` liegt unter `C:\Users\Jonas\AppData\Local\Microsoft\WinGet\Packages\astral-sh.uv_Microsoft.Winget.Source_8wekyb3d8bbwe`.
- **`.venv\Scripts\Activate.ps1` und ExecutionPolicy:** `CurrentUser` steht auf `RemoteSigned`. Falls `PSSecurityException`: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`.
- **Editor-Puffer vs. Datei auf Platte:** Ungespeicherte Tabs können leer oder alt sein. Zuerst die Datei auf der Platte prüfen.
- **`DemoRecord`:** Model `app/models/demo.py` und Export in `__init__.py` behalten. Demo-Routen bleiben weg.
- **`sort_order`:** Pflichtfeld. `from operator import gt` nicht für `Field(gt=0.0)` importieren.
- **Tests:** Unit ohne DB/HTTP. Integration: `LookupError`, nicht `None`. `get` gibt nie `None` zurück, `assert x is not None` danach ist wirkungslos. API: `TestClient`, Status 201/404/422. Testdateien speichern, sonst sammelt pytest sie nicht.
- **Factory-Fixture:** Der Aufruf steht im Funktionskörper. `def foo(create_plant(...))` ist ein Syntaxfehler.
- `include_router` bekommt den Router, nicht das Modul. Growth Stage: `from app.api.routers.growth_stages import router as router_growth_stage`.
- Update: `model_dump(exclude_unset=True)`. `from_attributes=True` nur am Response-Schema. `LookupError` im Service, `HTTPException(404)` im Router. Die Prüfung eines Updates steht in einer Session nach dem `update`, per `get`, nicht auf dem Rückgabewert derselben Session.
- **Git:** `main`, gleichauf mit `origin/main` bei `8e94b93`. Uncommittet nach dieser Sitzung: `tests/conftest.py` (`create_plant` nimmt eine Session, `plant_create_1` ist Fixture), `tests/integration/test_growth_stage_service.py` (`create` und `update`), `docs/lernpfad.md` (dieser Abschnitt). `nsm.db` nicht committen. Nicht ungefragt committen oder pushen.
- **Offen, nicht entschieden:** Soll `docs/alembic.md` in `kistart.md` und/oder `workflow.md` verlinkt werden? In dieser Sitzung gefragt, keine Antwort. Nicht stillschweigend verlinken und nicht als Einstieg der nächsten Sitzung noch einmal fragen.
- Parametrize zurückgestellt.
- SQLite-Inhalt lokal z. B. Extension **SQLite Viewer** (`qwtel.sqlite-viewer`).
- Cursor Tab bleibt aus (`cursor.tabCompletion: false` in den User-`settings.json`). Nicht ohne Nachfrage wieder einschalten.
- Sitzungsende immer über `docs/kistart.md` Abschnitt „Sitzung beenden“.

## Nicht als Nächstes

- `open_session` noch einmal erklären
- `create_plant` wieder eine eigene Session öffnen lassen
- Die Fixture `session` wieder anlegen
- `plant_id` auf `GrowthStageUpdate` setzen, nur damit der Update-Test ein Feld hat
- Router oder `relationship()` noch einmal als Einstieg erklären
- Neue Alembic-Revision
- `plant_id` aus dem Model entfernen
- EC/pH-Reihenfolge (`min <= target <= max`) zusammen mit den restlichen Tests
- `ec_min = 0.0` als Pflicht-Test nachziehen
- Recipe / RecipeItem (LE 3.3+)
- PostgreSQL / Docker Compose / Testcontainers
- Demo-Records-API oder `drop_table('demo_records')`
- Parametrize
- `plant_create_1` oder `grow_stage_create_1` stillschweigend löschen
- ungefragt committen, pushen oder LE 3.2 abschließen

