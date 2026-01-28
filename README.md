# 🧨 Saper w terminalu
Klasyczna gra **Saper** zaimplementowana w Pythonie przy użyciu biblioteki **curses**.  
Gra działa w terminalu i oferuje menu wyboru poziomu trudności, obsługę klawiatury oraz automatyczne odkrywanie pól.

## Funkcje gry

- interfejs w terminalu
- menu wyboru rozmiaru planszy
- obsługa flag
- automatyczne odkrywanie pustych obszarów
- wykrywanie wygranej i przegranej
- możliwość restartu gry bez wychodzenia z programu

## Uruchomienie gry
Najpierw należy pobrać repozytorium za pomocą .zip na github lub sklonować repozytorium za pomocą komendy:
```bash
git clone https://github.com/szvlinsky/Saper-Game.git
```
Następnie trzeba zainstalować bibliotekę curses:
```bash
pip install curses
```
Finalnie można odpalić (trzeba znajdować się w folderze, w którym jest plik saper_game.py)
```bash
py saper_game.py
```