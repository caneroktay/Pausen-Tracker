
# Pausen-Tracker

Diese einfache Python-Anwendung ist ein Uhr- und Status-Tracker, der den aktuellen Status (Unterricht, Pause, Feierabend) gemäß den Schulzeiten anzeigt. Das Programm informiert den Benutzer visuell und schriftlich über den aktuellen Status entsprechend der angegebenen Zeitintervalle.

---

## Funktionen

- Anzeige der aktuellen Uhrzeit und des Status (Unterricht, Pause, Feierabend).
- Änderung der Hintergrundfarbe und visuelle Benachrichtigung je nach Status.
- Automatische Aktualisierung des Informationstextes je nach Status.
- Dynamische Anpassung der Schriftgröße an die Fenstergröße.
- Akustische Benachrichtigung bei Statusänderungen (in Windows).

---

## Anforderungen

- Python 3.x
- [Pillow](https://pillow.readthedocs.io/en/stable/) Bibliothek (für Bildverarbeitung)

### Installation der Anforderungen

-  **Python-Installation:** Laden Sie die für Ihr System passende Version [HIER] herunter und installieren Sie sie.

  [HIER]: https://www.python.org/downloads/

- **Pillow-Installation**
  ```bash
  pip install pillow
  ```

## Einrichtung
- Klonen Sie das Repository oder laden Sie die Dateien herunter.
- Stellen Sie sicher, dass sich die Dateien GFNpause.py, pause_icon.png und mein_icon.ico im selben Ordner befinden.
- Navigieren Sie in der Befehlszeile zu dem Ordner, in dem sich das Programm befindet.
- Um das Programm auszuführen:
   ```bash
  python GFNpause.py
  ```
  *Ein Fenster öffnet sich und zeigt die aktuelle Uhrzeit und Statusinformationen an.*

## EXE-Datei erstellen (Optional)

Wenn Sie eine .exe-Datei für Windows erstellen möchten, können Sie PyInstaller verwenden:
  ```bash
  pyinstaller --onefile --noconsole --icon=mein_icon.ico --add-data "pause_icon.png;." GFNpause.py
   ```
Dieser Befehl packt alle Abhängigkeiten in eine einzige Datei und erstellt die exe-Datei mit dem angegebenen Symbol.





