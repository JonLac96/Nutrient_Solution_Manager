# Alembic – Datenbankmigrationen

Dieses Dokument ist eine praktische Referenz für die Alembic-Workflows in diesem Projekt.

Es beschreibt bewusst nicht die komplette Alembic-Theorie, sondern die Befehle, die im Nutrient Solution Manager tatsächlich gebraucht werden.

---

# 1. Was ist Alembic?

Alembic ist das Migrationswerkzeug von SQLAlchemy.

Eine **Migration** ist eine kleine, versionierte Änderung am Datenbankschema (z. B. „Tabelle `plants` anlegen“ oder „Spalte `sort_order` zu `growth_stages` hinzufügen").

Jede Migration hat:

- eine eindeutige **Revision-ID**
- eine Referenz auf die **vorherige Revision** (`down_revision`)
- eine `upgrade()`-Funktion (Schema vorwärts ändern)
- eine `downgrade()`-Funktion (Änderung zurücknehmen)

Damit ergibt sich eine Kette:

```text
5a5b99cdf83a (demo_records)
      ↓
b2741119ca18 (fertilizers)
      ↓
626c042a758a (fertilizers id autoincrement)
      ↓
6966518b98df (plants)
      ↓
5b10439fdc69 (growth_stages)
      ↓
... nächste Migration
```

---

# 2. Warum wir es in diesem Projekt verwenden

Ohne Alembic müsste man das Datenbankschema händisch per SQL ändern, auf jedem Rechner einzeln, ohne Historie und ohne Rückweg.

Mit Alembic gilt stattdessen:

- Die Schemahistorie steht als Code in `alembic/versions/`.
- Jeder, der das Repo klont, kann mit einem Befehl (`alembic upgrade head`) exakt denselben Datenbankstand herstellen.
- Änderungen an SQLAlchemy-Models werden automatisch mit dem tatsächlichen DB-Schema verglichen (**Autogenerate**).
- Man kann eine Migration im Zweifel auch wieder zurückrollen (`downgrade`).

Die Datenbankdatei `nsm.db` selbst liegt **nicht** in Git (siehe `.gitignore`). Nur die Migrationsdateien sind versioniert. Das heißt: Nach jedem `git pull` oder auf einem neuen Rechner ist `nsm.db` entweder leer oder existiert gar nicht — die Tabellen entstehen erst durch `alembic upgrade head`.

---

# 3. Wo Alembic im Projekt eingesetzt wird

| Datei/Ordner | Rolle |
|---|---|
| `alembic.ini` | Grundkonfiguration, u. a. wo `alembic/` liegt |
| `alembic/env.py` | Verbindet Alembic mit unserer SQLAlchemy-`Base` und der DB-URL aus `app/core/config.py`. Setzt `render_as_batch=True` (siehe Abschnitt 6) |
| `alembic/versions/*.py` | Die einzelnen Migrationsdateien, eine pro Schemaänderung |
| `app/models/__init__.py` | Muss **jedes** Model importieren, sonst sieht Autogenerate die Tabelle nicht |

---

# 4. Workflow A — Datenbank auf den neuesten Stand bringen

**Wann:** nach `git pull`, nach einem frischen `uv sync`, oder wenn Tests mit `no such table: ...` fehlschlagen.

```powershell
uv run alembic upgrade head
```

Das führt alle Migrationen aus, die auf dem aktuellen DB-Stand noch fehlen, bis zur neuesten Revision (`head`).

Mit aktivierter venv reicht auch:

```powershell
alembic upgrade head
```

---

# 5. Workflow B — Neue Migration nach einer Modelländerung erstellen

**Wann:** du hast ein SQLAlchemy-Model geändert oder neu angelegt (neue Tabelle, neue Spalte, geänderter Typ, …).

## Schritt 1 — Sicherstellen, dass das Model geladen wird

Neues Model in `app/models/__init__.py` exportieren/importieren. Ohne das findet Autogenerate die Tabelle nicht.

## Schritt 2 — Migration automatisch generieren lassen

```powershell
uv run alembic revision --autogenerate -m "kurze beschreibung der änderung"
```

Das erzeugt eine neue Datei in `alembic/versions/`, z. B. `a1b2c3d4e5f6_kurze_beschreibung_der_aenderung.py`, mit automatisch befüllten `upgrade()`/`downgrade()`-Funktionen.

## Schritt 3 — Migration prüfen (nicht blind vertrauen!)

Autogenerate ist ein Vorschlag, kein Garant. Vor dem Ausführen kontrollieren:

- Wird nur die gewollte Änderung vorgeschlagen? (Fehlt ein Model-Import, schlägt Alembic manchmal fälschlich `drop_table(...)` für bereits vorhandene Tabellen vor.)
- Stimmen Spaltentypen, `nullable`, Constraints?
- Ist `downgrade()` sinnvoll (macht `upgrade()` wieder rückgängig)?

## Schritt 4 — Migration anwenden

```powershell
uv run alembic upgrade head
```

## Schritt 5 — Committen

Die neue Datei unter `alembic/versions/` gehört ins Git-Repo (im Gegensatz zu `nsm.db` selbst).

---

# 6. Projektspezifische Besonderheit: SQLite und Batch-Migrationen

SQLite kann viele `ALTER TABLE`-Operationen nicht direkt (z. B. eine Spalte umbenennen oder einen Constraint ändern).

Deshalb ist in `alembic/env.py` `render_as_batch=True` gesetzt. Alembic baut dann bei solchen Änderungen intern eine neue Tabelle, kopiert die Daten um und tauscht sie aus — für uns unsichtbar, einfach so laufen lassen.

---

# 7. Weitere nützliche Befehle

| Befehl | Zweck |
|---|---|
| `uv run alembic current` | Zeigt, auf welcher Revision die aktuelle DB steht |
| `uv run alembic history` | Zeigt die komplette Migrationskette |
| `uv run alembic downgrade -1` | Nimmt die letzte Migration zurück (eine Revision zurück) |
| `uv run alembic downgrade <revision_id>` | Setzt die DB auf eine bestimmte ältere Revision zurück |
| `uv run alembic upgrade +1` | Wendet nur die nächste ausstehende Migration an |

---

# 8. Typische Fehler

| Fehlermeldung | Wahrscheinliche Ursache | Lösung |
|---|---|---|
| `sqlite3.OperationalError: no such table: ...` | `nsm.db` wurde nie migriert (neuer Rechner, frisches `uv sync`, `nsm.db` gelöscht) | `uv run alembic upgrade head` |
| Autogenerate schlägt `drop_table(...)` für eine existierende Tabelle vor | Model fehlt im Import in `app/models/__init__.py` | Model importieren, Migration neu generieren |
| Migration lässt sich nicht anwenden, weil `down_revision` nicht passt | Zwei Migrationen wurden parallel (z. B. auf verschiedenen Branches) mit demselben Vorgänger erzeugt | Mit `alembic history` die Kette prüfen, ggf. eine Migration händisch anpassen oder neu erzeugen |

---

# 9. Nicht Teil dieses Dokuments

- Alembic-Branching/Merge-Migrationen (mehrere parallele Köpfe) — bisher nicht gebraucht, da wir allein auf `main` arbeiten (siehe [`workflow.md`](workflow.md))
- PostgreSQL-spezifische Migrationsfunktionen — aktuell SQLite (siehe [`lernpfad.md`](lernpfad.md), Abschnitt „Technische Entscheidungen")
