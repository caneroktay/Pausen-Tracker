import sys
import os
import datetime
import threading
import tkinter as tk
from PIL import Image, ImageTk

# PyInstaller sonrası dosya yolunu doğru bulmak için yardımcı fonksiyon
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Stundenplan (Zeitintervalle und Status)
stundenplan = [
    ("08:30", "10:00", "Unterricht"),
    ("10:00", "10:30", "Pause"),
    ("10:30", "12:00", "Unterricht"),
    ("12:00", "13:00", "Pause"),
    ("13:00", "14:30", "Unterricht"),
    ("14:30", "15:00", "Pause"),
    ("15:00", "16:30", "Unterricht"),
]

def zeit_parsen(zeit_str):
    return datetime.datetime.strptime(zeit_str, "%H:%M").time()

def status_ermitteln(jetzt):
    for start_str, end_str, status in stundenplan:
        start = zeit_parsen(start_str)
        ende = zeit_parsen(end_str)
        if start <= jetzt <= ende:
            return status
    if stundenplan:
        last_scheduled_end_time = zeit_parsen(stundenplan[-1][1])
        if jetzt > last_scheduled_end_time:
            return "Feierabend"
    return "Außerhalb der Unterrichtszeit"

def naechster_zeitpunkt(jetzt, ziel_status):
    for start_str, _, status in stundenplan:
        if status == ziel_status:
            start = zeit_parsen(start_str)
            if start > jetzt:
                return start.strftime("%H:%M")
    return "Feierabend !!!  :)"

class App:
    def __init__(self, root):
        self.root = root
        root.title("GFN - Pausen-Tracker")
        root.geometry("320x280")
        root.resizable(True, True)

        self.font_min = 12
        self.font_max = 100
        self.root.bind("<Configure>", self.fenster_groesse_angepasst)

        self.label_zeit = tk.Label(root, text="", font=("Arial", 24))
        self.label_zeit.pack(pady=10)

        self.label_status = tk.Label(root, text="", font=("Arial", 20))
        self.label_status.pack(pady=5)

        self.bild_frame = tk.Frame(root, bg="#CCEECC")
        self.pause_bild = None
        self.label_bild = None
        self.label_naechste_info = None

        try:
            bild_pfad = resource_path("pause_icon.png")
            original_bild = Image.open(bild_pfad)
            skaliertes_bild = original_bild.resize((100, 100), Image.Resampling.LANCZOS)
            self.pause_bild = ImageTk.PhotoImage(skaliertes_bild)

            self.label_bild = tk.Label(self.bild_frame, image=self.pause_bild, bg="#CCEECC")
            self.label_bild.pack()

            self.label_naechste_info = tk.Label(self.bild_frame, text="", font=("Arial", 12), bg="#CCEECC")
            self.label_naechste_info.pack(pady=5)

            self.bild_frame.pack_forget()
        except FileNotFoundError:
            print("Warnung: 'pause_icon.png' nicht gefunden. Das Bild wird nicht angezeigt.")
        except Exception as e:
            print(f"Fehler beim Laden des Bildes: {e}")

        self.label_naechste_stunde_info = tk.Label(root, text="", font=("Arial", 5), fg="darkgray")
        self.label_naechste_stunde_info.pack(side="bottom", pady=2)

        self.vorheriger_status = None
        self.aktuelle_hintergrundfarbe = ""
        self.ist_am_blinken = False
        self.blink_timer_id = None
        self.update_timer_id = None
        self.blink_max_schaltungen = 10
        self.blink_intervall_ms = 500

        self.uhr_aktualisieren()

    def piep_abspielen(self):
        try:
            import winsound
            winsound.MessageBeep()
        except ImportError:
            print("Warnung: winsound Modul nicht gefunden. Piepton konnte nicht abgespielt werden.")
        except Exception as e:
            print(f"Fehler beim Abspielen des Pieptons: {e}")

    def hintergrundfarben_aktualisieren(self, farbe):
        self.root.config(bg=farbe)
        self.label_zeit.config(bg=farbe)
        self.label_status.config(bg=farbe)
        self.bild_frame.config(bg=farbe)
        if self.label_bild:
            self.label_bild.config(bg=farbe)
        if self.label_naechste_info:
            self.label_naechste_info.config(bg=farbe)
        if self.label_naechste_stunde_info:
            self.label_naechste_stunde_info.config(bg=farbe)

    def uhr_aktualisieren(self):
        if self.update_timer_id:
            self.root.after_cancel(self.update_timer_id)

        jetzt_dt = datetime.datetime.now()
        jetzt = jetzt_dt.time()
        status = status_ermitteln(jetzt)
        zeit_str = jetzt_dt.strftime("%H:%M:%S")

        self.label_zeit.config(text=zeit_str)
        self.label_status.config(text=status)

        self.fenster_groesse_angepasst()

        info_text = ""
        if status == "Feierabend":
            info_text = "Der Tag ist vorbei! Feierabend!"
            if self.bild_frame.winfo_ismapped():
                self.bild_frame.pack_forget()
        elif status == "Unterricht":
            naechste_pause = naechster_zeitpunkt(jetzt, "Pause")
            info_text = f"Nächste Pause: {naechste_pause}"
            if self.bild_frame.winfo_ismapped():
                self.bild_frame.pack_forget()
        elif status == "Pause":
            naechster_unterricht = naechster_zeitpunkt(jetzt, "Unterricht")
            info_text = f"Nächster Unterricht: {naechster_unterricht}"
            if not self.bild_frame.winfo_ismapped():
                self.bild_frame.pack(pady=5)
        else:
            if stundenplan:
                first_lesson_start_str = stundenplan[0][0]
                info_text = f"Unterricht beginnt um {first_lesson_start_str}"
            else:
                info_text = "Kein Stundenplan definiert."
            if self.bild_frame.winfo_ismapped():
                self.bild_frame.pack_forget()

        if self.label_naechste_stunde_info:
            self.label_naechste_stunde_info.config(text=info_text)

        ziel_farbe = ""
        if status == "Pause":
            ziel_farbe = "#CCEECC"
        elif status == "Unterricht":
            ziel_farbe = "#FF9999"
        elif status == "Feierabend":
            ziel_farbe = "#ADD8E6"
        else:
            ziel_farbe = "#F0F0F0"

        if status != self.vorheriger_status:
            threading.Thread(target=self.piep_abspielen).start()
            self.vorheriger_status = status

            if self.ist_am_blinken and self.blink_timer_id:
                self.root.after_cancel(self.blink_timer_id)
                self.ist_am_blinken = False

            self.blink_zaehler = 0
            self.blink_farben = [ziel_farbe, "#F0F0F0"]
            self.blink_sequenz_starten(ziel_farbe)
        elif not self.ist_am_blinken:
            if self.aktuelle_hintergrundfarbe != ziel_farbe:
                self.hintergrundfarben_aktualisieren(ziel_farbe)
                self.aktuelle_hintergrundfarbe = ziel_farbe
            self.update_timer_id = self.root.after(1000, self.uhr_aktualisieren)

    def blink_sequenz_starten(self, end_farbe):
        if self.blink_zaehler < self.blink_max_schaltungen:
            self.ist_am_blinken = True
            aktuelle_blink_farbe = self.blink_farben[self.blink_zaehler % 2]
            self.hintergrundfarben_aktualisieren(aktuelle_blink_farbe)
            self.aktuelle_hintergrundfarbe = aktuelle_blink_farbe
            self.blink_zaehler += 1
            self.blink_timer_id = self.root.after(self.blink_intervall_ms,
                                                  lambda: self.blink_sequenz_starten(end_farbe))
        else:
            self.ist_am_blinken = False
            self.hintergrundfarben_aktualisieren(end_farbe)
            self.aktuelle_hintergrundfarbe = end_farbe
            self.blink_timer_id = None
            self.update_timer_id = self.root.after(1000, self.uhr_aktualisieren)

    def fenster_groesse_angepasst(self, event=None):
        breite = self.root.winfo_width()
        base_font_size = max(self.font_min, min(self.font_max, int(breite / 10)))

        self.label_zeit.config(font=("Arial", base_font_size))
        self.label_status.config(font=("Arial", int(base_font_size * 0.8)))
        if self.label_naechste_info:
            self.label_naechste_info.config(font=("Arial", int(base_font_size * 0.5)))
        if self.label_naechste_stunde_info:
            self.label_naechste_stunde_info.config(font=("Arial", int(base_font_size * 0.6)))

if __name__ == "__main__":
    root = tk.Tk()

    # İkon PNG dosyasının yolunu al
    icon_path = resource_path("pause_icon.png")  # PNG dosyanın adı ve yolunu değiştirilebilir
    try:
        icon_img = ImageTk.PhotoImage(Image.open(icon_path))
        root.iconphoto(True, icon_img)
    except Exception as e:
        print(f"Icon yüklenemedi: {e}")

    app = App(root)
    root.mainloop()
