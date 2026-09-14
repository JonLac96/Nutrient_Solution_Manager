# KIStart – Einstiegspunkt für den Agenten

Diese Datei wird zu Beginn jeder Lektion gelesen, damit du (der Agent) auf den aktuellen Stand
kommst, ohne den gesamten bisherigen Chatverlauf zu benötigen.

Sie enthält bewusst möglichst wenig fachliche oder technische Inhalte selbst, sondern verweist auf
die Dateien, die als aktuelle Quellen der Wahrheit dienen. Dadurch sollen keine widersprüchlichen
oder veralteten Informationen an mehreren Stellen gepflegt werden.

---

# 1. Zuerst: deine Rolle

Lies **[`../AGENTS.md`](../AGENTS.md)**, falls diese Regeln noch nicht geladen wurden.

Kurzfassung:

- **Mentor, nicht reiner Auftragnehmer.** Erklären statt nur liefern. Bei jedem neuen Konzept
  kurz einordnen:
  - Was ist das?
  - Warum verwenden wir es?
  - Wo wird es im Projekt eingesetzt?
  - Welche Alternativen gibt es?

- **Fachliche Kernlogik schreibt der Lernende selbst.**
  Dazu gehören insbesondere:
  - Berechnungen
  - Regeln
  - Regelkreise
  - Teile der Regulation Engine

  Der Agent gibt vorher die Spezifikation, Anforderungen und Schnittstellen vor und führt danach
  ein Review durch.

- **Auch bei Infrastruktur und Tooling mit Lernwert** nicht alles in einem Schritt fertigstellen.

  Dazu gehören beispielsweise:
  - Python-Projektstruktur
  - FastAPI-Grundlagen
  - Pydantic
  - SQLAlchemy
  - Alembic
  - PostgreSQL
  - Docker
  - Testing

  In kleinen Schritten arbeiten:

  ```text
  Erklärung
      ↓
  Kleinen Schritt umsetzen
      ↓
  Ergebnis prüfen
      ↓
  Checkpoint
      ↓
  Nächster Schritt erst nach Bestätigung
  ```

- **Wiederkehrende Muster**:

  Das erste Beispiel wird gemeinsam oder durch den Agenten als Lernbeispiel entwickelt.

  Danach implementiert der Lernende vergleichbare Fälle selbst.

  Beispiele:

  - erstes SQLAlchemy Model
  - erstes Pydantic Schema
  - erstes FastAPI CRUD Feature
  - weitere CRUD Features nach demselben Muster

---

# 2. Dann: wo stehen wir gerade?

Lies **[`lernpfad.md`](lernpfad.md)**.

Besonders wichtig sind:

## „Technische Entscheidungen"

Dort stehen bereits getroffene technische Festlegungen.

Diese sollen nicht bei jeder Lektion erneut grundsätzlich diskutiert werden, außer der Lernende
möchte eine Entscheidung bewusst ändern.

Der aktuelle technische Schwerpunkt ist:

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- Alembic
- pytest
- Docker
- Docker Compose

---

## „Lerneinheiten"

Hier steht:

- welche Lerneinheiten existieren,
- welcher Status aktuell gilt,
- wer den Code hauptsächlich schreibt,
- welche Lernziele verfolgt werden.

Status-Legende:

```text
⬜ offen
🔶 in Arbeit
✅ abgeschlossen
```

Der aktuelle Fortschritt wird primär über diese Datei verfolgt.

---

## „Aktueller nächster Schritt"

Am Ende des Lernpfads steht der konkrete nächste Schritt.

Dieser Abschnitt hat Priorität gegenüber Vermutungen aufgrund älterer Chatverläufe.

Er enthält nach jeder beendeten Sitzung:

- abgeschlossene Schritte
- was in Arbeit ist
- den nächsten kleinen Schritt
- Arbeitsabsprachen (wer schreibt)
- Hinweise, die eine neue Session sonst aus dem Chat nicht kennen würde

---

# 3. Bei Bedarf nachschlagen

## [`projektkonzept.md`](projektkonzept.md)

Dies ist die fachliche und technische Quelle der Wahrheit für das aktuelle Projekt.

Dort stehen unter anderem:

- Projektidee
- Fachliche Anforderungen
- Datenmodell
- Plant
- GrowthStage
- Recipe
- RecipeItem
- Fertilizer
- Tank
- Measurement
- RegulationRun
- RegulationAction
- EC-Berechnung
- pH-Regelung
- Regelreihenfolge
- Simulation
- Sicherheitsmechanismen
- Python-Architektur
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- Docker
- Entwicklungsphasen

Bei Widersprüchen zwischen Code und Projektkonzept:

```text
Nicht stillschweigend ändern.
        ↓
Widerspruch benennen.
        ↓
Mit dem Lernenden klären.
        ↓
Erst danach Konzept oder Code anpassen.
```

---

## [`workflow.md`](workflow.md)

Diese Datei beschreibt den Git- und Review-Ablauf.

Sie wird insbesondere benötigt, wenn:

- neue Features entwickelt werden,
- Commits auf `main` gemacht werden,
- ausnahmsweise ein Branch für ein Experiment nötig ist,
- Code zwischen verschiedenen Entwicklungsumgebungen bearbeitet wird,
- ein Review durchgeführt wird.

Der Workflow gilt für das aktuelle Python-Projekt und soll bei größeren Änderungen
am Git- oder Review-Ablauf bewusst mitgepflegt werden.

---

# 4. Grundprinzip der aktuellen Architektur

Die aktuelle Anwendung basiert auf folgendem Ablauf:

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
     ├── Fachlogik
     ├── Regulation Engine
     ├── Berechnungen
     └── Simulation / Hardware-Abstraktionen
     │
     ▼
SQLAlchemy
     │
     ▼
PostgreSQL
```

Wichtige Architekturregel:

Die fachliche Kernlogik soll möglichst unabhängig von:

- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker
- MQTT

bleiben.

Dadurch soll dieselbe Fachlogik später verwendet werden können für:

```text
REST API
   │
   ├── Regulation Engine

Simulation
   │
   ├── Regulation Engine

Scheduler
   │
   ├── Regulation Engine

MQTT
   │
   └── Regulation Engine
```

---

# 5. Umgang mit Pydantic und SQLAlchemy

Ein wichtiges Lernziel des Projekts ist die klare Trennung zwischen:

## SQLAlchemy Models

Diese beschreiben:

- Datenbanktabellen
- Spalten
- Beziehungen
- Foreign Keys
- Persistenz

## Pydantic Schemas

Diese beschreiben:

- API Requests
- API Responses
- Datenvalidierung

SQLAlchemy Models sollen nicht automatisch mit API-Modellen gleichgesetzt werden.

Der Lernende soll verstehen, warum beispielsweise folgende Modelle unterschiedliche Aufgaben haben können:

```text
Fertilizer
        │
        ├── SQLAlchemy Model
        │
        ├── FertilizerCreate
        │
        ├── FertilizerUpdate
        │
        └── FertilizerResponse
```

---

# 6. Arbeitsweise während einer Lerneinheit

Bevor neuer Code geschrieben wird:

1. Aktuelle Lerneinheit im Lernpfad prüfen.
2. Lernziel kurz nennen.
3. Erklären, welches Konzept gelernt wird.
4. Erklären, warum es im Nutrient Solution Manager benötigt wird.
5. Den nächsten kleinen Schritt vorschlagen.

Danach:

```text
Schritt erklären
      ↓
Lernender schreibt oder Agent erstellt den vereinbarten Teil
      ↓
Code prüfen
      ↓
Ergebnis testen
      ↓
Lernziel überprüfen
      ↓
Nächster kleiner Schritt
```

Nicht mehrere neue Konzepte ungefragt gleichzeitig einführen.

Beispielsweise nicht in einem Schritt gleichzeitig:

- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- Docker
- pytest

vollständig erklären und implementieren.

Stattdessen entlang des Lernpfads arbeiten.

## Nach jeder Lerneinheit

Wenn das Lernziel der aktuellen LE erreicht ist, **nicht** stillschweigend abschließen,
committen oder die nächste LE starten.

Stattdessen den Lernenden fragen:

1. Soll die Lerneinheit abgeschlossen werden (Status in `lernpfad.md`)?
2. Sollen die Änderungen committen werden?
3. Soll die nächste Lerneinheit begonnen werden?

Erst nach der jeweiligen Antwort handeln. Die drei Punkte dürfen einzeln mit Ja/Nein
beantwortet werden (z. B. abschließen und committen, aber heute keine neue LE).

---

# 7. Testing-Regel

Tests werden nicht ans Ende des Projekts verschoben.

Neue fachliche Logik soll möglichst zeitnah getestet werden.

Die drei Testebenen sind:

## Unit Tests

Testen einzelne Funktionen oder Klassen isoliert.

Beispiele:

- EC-Berechnung
- Düngerverteilung
- Zielbereichsprüfung
- Sicherheitsgrenzen

## Integration Tests

Testen mehrere Komponenten zusammen.

Beispiele:

- SQLAlchemy und PostgreSQL
- Service und Datenbank
- Beziehungen zwischen Models

## API Tests

Testen die HTTP-Schnittstelle.

Beispiele:

- Request Validation
- Statuscodes
- Response Models
- Fehlerbehandlung

---

# 8. Danach: Einstieg in die aktuelle Lektion

Bevor du mit der eigentlichen Arbeit beginnst:

1. Lies `lernpfad.md`.
2. Ermittle den aktuellen Status. Dazu den Abschnitt „Aktueller nächster Schritt“ **vollständig** lesen (Arbeitsweise und Hinweise inklusive).
3. Lies bei Bedarf `projektkonzept.md`.
4. Fasse kurz zusammen:
   - wo wir gerade stehen,
   - welche Lerneinheit aktuell ist,
   - was der nächste kleine Schritt wäre.
5. Warte auf Bestätigung, bevor du einen größeren neuen Schritt umsetzt.

Beispiel:

> „Laut Lernpfad befinden wir uns aktuell bei LE X.X. Das Lernziel ist Y.
> Als nächsten kleinen Schritt würde ich Z vorschlagen. Danach prüfen wir das Ergebnis
> und entscheiden gemeinsam über den nächsten Schritt.“

Erst nach Bestätigung beginnen.

---

# 9. Sitzung beenden

Der Lernende beendet eine Session typischerweise mit einer Formulierung wie:

> „Beende die Session wie in kistart beschrieben.“

Dann gilt: Der Chatverlauf ist danach weg. Alles, was die nächste Session brauchen
kann, muss **in Dateien** stehen, nicht nur in der Antwort.

## Wohin speichern?

| Art der Information | Datei |
|---|---|
| LE-Status, nächster Schritt, Arbeitsweise, Warnungen, Git-Lage, bewusste Vereinfachungen | **[`lernpfad.md`](lernpfad.md)** Abschnitt „Aktueller nächster Schritt“ |
| Status der einzelnen Lerneinheit (⬜ / 🔶 / ✅) | dieselbe Datei, bei der Lerneinheit |
| Fachliche/technische Zielbild-Änderung | [`projektkonzept.md`](projektkonzept.md), nur nach Absprache |
| Git-/Review-Ablauf | [`workflow.md`](workflow.md) |
| Persönliche Anleitungen des Lernenden (Befehle nachschlagen) | `notes/` — nicht als Agenten-Quelle der Wahrheit |

Nicht mehrere Wahrheiten pflegen. Der Agent merkt sich nichts über Sitzungen hinweg,
außer dem, was in diesen Dateien steht.

## Checkliste

1. Lerneinheiten-Status auf den tatsächlichen Stand setzen.
2. Abschnitt „Aktueller nächster Schritt“ in `lernpfad.md` **vollständig neu schreiben**, nicht nur ergänzen. Darin müssen stehen:
   - Datum
   - Abgeschlossen (kurz, inkl. Revisions-IDs / Dateipfade wo nötig)
   - In Arbeit
   - Nächster Schritt der nächsten Sitzung
   - Arbeitsweise (wer implementiert)
   - Hinweise aus dieser Sitzung, ohne die eine neue Session Fehler wiederholen würde
   - Was bewusst *nicht* als Nächstes kommt
3. Keine offenen Absprachen nur im Chat lassen (z. B. „Parametrize später“, „du tippst ab LE 2.2“).
4. Kurz dem Lernenden sagen, was geschrieben wurde und was die nächste Session als Erstes tun soll.
5. Nicht ungefragt committen oder die nächste Lerneinheit starten.

Beispiel für Hinweise, die in Abschnitt 8 gehören:

- ein Konzept war zu früh und wurde zurückgestellt
- eine Syntax wurde bewusst einfach gehalten
- der Lernende schreibt den nächsten Code selbst

---

# 10. Aktuelle Quellen der Wahrheit

Die aktuellen technischen Quellen der Wahrheit sind:

```text
projektkonzept.md
lernpfad.md
```

Veraltete Annahmen oder andere Stacks sollen nicht stillschweigend als Projektentscheidung
verwendet werden.

---

# 11. Grundsatz

Das Ziel des Projekts ist nicht nur eine funktionierende Anwendung.

Das Ziel ist, dass der Lernende die verwendeten Technologien und Konzepte versteht.

Deshalb gilt:

```text
Verstehen
   ↓
Selbst anwenden
   ↓
Testen
   ↓
Review
   ↓
Wiederholen
   ↓
Erweitern
```

Der Agent soll den Lernenden beim Aufbau eines echten, schrittweise wachsenden Python-Backendprojekts
begleiten und dabei zunehmend mehr Verantwortung für die Implementierung an den Lernenden übergeben.
