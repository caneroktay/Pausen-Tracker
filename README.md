<img src="./assets/pause_icon.png" alt="GFN-Pause" width="320">


# GFN-Pausen-Tracker

Bu basit Python uygulaması, okul saatlerine göre güncel durumu (Unterricht, Pause, Feierabend) gösteren bir saat ve durum takipçisidir. Program, belirtilen saat aralıklarına göre geçerli durumu kullanıcıya görsel ve yazılı olarak iletir.

---

## Özellikler

- Güncel saat ve durum gösterimi (`Unterricht`, `Pause`, `Feierabend`, `Außerhalb der Unterrichtszeit`).
- Duruma göre arka plan rengi değişimi ve görsel bildirim.
- Otomatik olarak duruma göre bilgilendirme metni güncellemesi.
- Dinamik olarak pencere boyutuna göre yazı tipi boyutunu ayarlar.
- Durum değişiminde sesli uyarı (Windows ortamında).

---

## Gereksinimler

- Python 3.x
- [Pillow](https://pillow.readthedocs.io/en/stable/) kütüphanesi (resim işlemleri için)

### Gereksinimlerin Kurulumu

-  **Python Kurulumu:** [BURADAN] sisteminize uyumlu versiyonu indirip kurun.

  [BURADAN]: https://www.python.org/downloads/

- **Pillow Kurulumu**
  ```bash
  pip install pillow
  ```

## Kurulum
- Depoyu klonlayın veya dosyaları indirin.
- GFNpause.py, pause_icon.png ve mein_icon.ico dosyalarının aynı klasörde olduğundan emin olun.
- Komut satırından programın bulunduğu klasöre gidin.
- Programı çalıştırmak için:
   ```bash
  python GFNpause.py
  ```
  *Pencere açılacak ve güncel saat ile durum bilgisi gösterilecektir.*

## EXE Dosyası Oluşturma (İsteğe Bağlı)

Windows için .exe dosyası oluşturmak istiyorsanız, PyInstaller kullanabilirsiniz:
  ```bash
  pyinstaller --onefile --noconsole --icon=mein_icon.ico --add-data "pause_icon.png;." GFNpause.py
   ```
Bu komut, tüm bağımlılıkları tek bir dosyada paketler ve belirtilen ikon ile exe dosyasını oluşturur.

  
