# Workflow – Git und Review

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

# 2. Arbeitsmodell

Das Projekt wird **allein** entwickelt. Deshalb gilt seit 2026-09-14:

- Neue Arbeit entsteht **direkt auf `main`**.
- `main` soll trotzdem ein nachvollziehbarer Stand bleiben: lieber kleine, thematische Commits als ein Sammelcommit am Ende einer LE.
- Feature-Branches sind **optional** — nur bei Experimenten, riskanten Umbauten oder späterer Teamarbeit.

Früher galt „eine LE = ein Branch, danach mergen“. Das haben wir bewusst aufgegeben, weil der Extra-Schritt ohne Team wenig Nutzen hatte und `main` hinter den Feature-Branches zurückblieb.

---

# 3. Ablauf einer Lerneinheit

```text
Aktuellen nächsten Schritt im Lernpfad lesen
        ↓
Auf main arbeiten
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
Auf main committen (nur wenn der Lernende das will)
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

Vor dem Commit einer abgeschlossenen LE prüft der Agent bzw. der Lernende:

- Entspricht der Stand dem Lernziel der aktuellen Lerneinheit?
- Laufen die vorhandenen Tests?
- Bleibt Fachlogik von FastAPI, SQLAlchemy und MQTT getrennt, soweit das in diesem Schritt schon gilt?
- Wurde `lernpfad.md` aktualisiert, wenn sich Status oder Entscheidungen geändert haben?

Fachliche Kernlogik (Berechnungen, Regelkreise) schreibt der Lernende. Der Agent reviewed und erklärt.

---

# 6. Remote und optionale Branches

- `main` nicht per Force-Push überschreiben.
- Nicht ungefragt pushen.
- Pull Requests sind erlaubt, für lokale Lernschritte nicht nötig.
- Entsteht doch ein Branch: nach dem Checkpoint nach `main` mergen und den Branch löschen, wenn er nicht mehr gebraucht wird.

Alte LE-Branches (`le-1-6-alembic`, `le-2-2-fertilizer-schemas`, …) sind Historie. Neue Arbeit nicht darauf fortsetzen.

---

# 7. Was nicht gemacht wird

- stillschweigend vom Projektkonzept abweichen
- mehrere neue Konzepte in einem Schritt vollständig einführen
- Infrastruktur und Fachlogik in einem ungeprüften Block fertigstellen
- auf einen anderen Stack ausweichen als in `lernpfad.md` festgelegt
- ungefragt eine neue Feature-Branch-Serie für jede Lerneinheit anlegen
