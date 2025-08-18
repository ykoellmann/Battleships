Project Guidelines
General Principles

Schreibe objektorientierten und sauberen Code (Clean Code).

Halte Verantwortlichkeiten klar getrennt (Spiel-Logik, UI/View, Datenstrukturen).

Änderungen am UI dürfen ausschließlich über View- und UI-Klassen erfolgen, niemals direkt aus der Game-/Logikschicht heraus.

Jede Klasse und Methode muss mit einem aussagekräftigen Docstring dokumentiert werden (Beschreibung der Aufgabe, Parameter, Rückgabewerte).

Project Structure

Game Layer
Enthält die Spiellogik (Phasen, Spieler, Schiffe, Board, Regeln).
Keine direkte UI-Logik.

View Layer
Enthält alle UI-bezogenen Klassen (z. B. GameView, BoardView).
Nimmt Input entgegen und ruft passende Methoden der Game Layer auf.
Ist für visuelles Feedback und Updates verantwortlich (z. B. Schiff markieren, Boards deaktivieren).

Phases
Jede Phase ist eine eigene Klasse, die von einer abstrakten GamePhase erbt.

Beispiel: PlacementPhase, ShipSelectionPhase, ShootingPhase.

Jede Phase definiert ihr Verhalten und wann sie endet.

Phasenwechsel läuft über die zentrale abstrakte Methode change_phase(next_phase) in der GameView.

Coding Standards

Docstrings:

Methoden: Kurzbeschreibung, Parameter, Rückgabewert.

Klassen: Zweck der Klasse, wichtige Attribute, Interaktion mit anderen Klassen.

Naming:

Klassen: PascalCase (GamePhase, ShipSelectionPhase).

Methoden/Attribute: snake_case (process_shot_result, change_phase).

Separation of Concerns:

Logik in Game-/Phase-Klassen.

Darstellung in View-/UI-Klassen.

Kein Mischen von Verantwortlichkeiten.