# Workflow – Git, Branches und Review

Dieser Ablauf gilt für das aktuelle Python-Projekt.

Ziel ist ein nachvollziehbarer Arbeitsstand: eine Lerneinheit nach der anderen, kleine Schritte, klarer Review, ein funktionierender `main`.

---

# 1. Quellen der Wahrheit

| Datei | Rolle |
|---|---|
| [`lernpfad.md`](lernpfad.md) | Nächster Schritt, Status der Lerneinheiten, technische Entscheidungen |
| [`projektkonzept.md`](projektkonzept.md) | Fachliches und technisches Zielbild |
| [`kistart.md`](kistart.md) | Einstieg für den Agenten zu Beginn einer Lektion |
| [`../AGENTS.md`](../AGENTS.md) | Arbeitsweise des Agenten |

Bei Widersprüchen zuerst den Lernenden fragen, dann bewusst Docs oder Code anpassen.

---

# 2. Branch-Modell

- `main` enthält nur einen funktionierenden Stand nach abgeschlossenen Schritten.
- Neue Arbeit entsteht auf einem eigenen Branch.
- Ein Branch gehört zu **einer** Lerneinheit oder zu **einem** kleinen Feature.

Namensbeispiele:

```text
le-1-1-projektstruktur
le-2-1-fertilizer-crud
feature/tank-messungen
fix/alembic-revision
```

Nicht mehrere Lerneinheiten in einem Branch mischen.

---

# 3. Ablauf einer Lerneinheit

```text
Aktuellen nächsten Schritt im Lernpfad lesen
        ↓
Branch von aktuellem main erstellen
        ↓
Kleinen Schritt umsetzen
        ↓
Ergebnis prüfen (Code, Tests, Lernziel)
        ↓
Checkpoint / Review
        ↓
Nächster Schritt erst nach Bestätigung
        ↓
Nach Abschluss: Status in lernpfad.md aktualisieren
        ↓
In main mergen
```

Der Agent wartet bei größeren neuen Schritten auf Bestätigung.

Wenn das Lernziel einer Lerneinheit erreicht ist, fragt der Agent **immer** zuerst:

1. Lerneinheit abschließen?
2. Committen?
3. Nächste Lerneinheit beginnen?

Ohne klare Antwort keines der drei tun.

---

# 4. Commits

- Ein Commit hat ein Thema.
- Die Nachricht erklärt das **Warum**, nicht die Dateiliste.
- Häufig committen ist besser als ein großer Sammelcommit am Ende.
- Nicht committen:
  - virtuelle Umgebungen (`.venv`)
  - `__pycache__`, `.pytest_cache`
  - `.env` und Geheimnisse
  - lokale IDE-Dateien, soweit nicht bewusst geteilt

---

# 5. Review

Vor dem Merge prüft der Agent bzw. der Lernende:

- Entspricht der Stand dem Lernziel der aktuellen Lerneinheit?
- Laufen die vorhandenen Tests?
- Bleibt Fachlogik von FastAPI, SQLAlchemy und MQTT getrennt, soweit das in diesem Schritt schon gilt?
- Wurde `lernpfad.md` aktualisiert, wenn sich Status oder Entscheidungen geändert haben?

Fachliche Kernlogik (Berechnungen, Regelkreise) schreibt der Lernende. Der Agent reviewed und erklärt.

---

# 6. Merge

- Nach erfolgreichem Checkpoint in `main` mergen.
- `main` nicht per Force-Push überschreiben.
- Nach dem Merge den Feature-Branch löschen, wenn er nicht mehr benötigt wird.

Pull Requests sind erlaubt und nützlich, aber für lokale Lernschritte nicht zwingend.

---

# 7. Was nicht gemacht wird

- stillschweigend vom Projektkonzept abweichen
- mehrere neue Konzepte in einem Schritt vollständig einführen
- Infrastruktur und Fachlogik in einem ungeprüften Block fertigstellen
- auf einen anderen Stack ausweichen als in `lernpfad.md` festgelegt
