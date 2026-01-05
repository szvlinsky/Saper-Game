import curses
import random
from dataclasses import dataclass
from enum import Enum, auto


class CellState(Enum):
    HIDDEN = auto()
    REVEALED = auto()
    FLAGGED = auto()


@dataclass
class Cell:
    is_mine: bool = False # czy pole zawiera minę
    neighbors: int = 0 # liczba min w sąsiedztwie
    state: CellState = CellState.HIDDEN


class Minesweeper:
    def __init__(self, size, mines):
        self.h = size
        self.w = size
        self.mines = mines

        # wypełnienie planszy 
        self.board = [[Cell() for _ in range(size)] for _ in range(size)]
        self.game_over = False
        self.win = False
        self._place_mines()
        self._compute_neighbors()

    def _place_mines(self):
        # losowanie unikalnej pozycji w postaci jednego indeksu
        for p in random.sample(range(self.h * self.w), self.mines):
            y, x = divmod(p, self.w) # zamiana indeksu 1D na 2D
            self.board[y][x].is_mine = True

    def _compute_neighbors(self):
        for y in range(self.h):
            for x in range(self.w):
                if self.board[y][x].is_mine:
                    continue

                # sumowanie dla każdej sąsiedniej miny
                self.board[y][x].neighbors = sum(
                    # sprawdzenie granic planszy
                    0 <= y + dy < self.h and
                    0 <= x + dx < self.w and
                    # czy sąsiednia komórka to mina
                    self.board[y + dy][x + dx].is_mine
                    for dy in (-1, 0, 1)
                    for dx in (-1, 0, 1)
                )

    def reveal(self, y, x):
        c = self.board[y][x]

        # nie odkrywamy ponownie ani flag
        if c.state != CellState.HIDDEN:
            return

        c.state = CellState.REVEALED

        if c.is_mine:
            self.game_over = True
            return

        # automatyczne odkrywanie pustych pól
        if c.neighbors == 0:
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < self.h and 0 <= nx < self.w:
                        self.reveal(ny, nx)

        self._check_win()

    def toggle_flag(self, y, x):
        c = self.board[y][x]
        # przełączanie stanu flagi na ukryte
        if c.state == CellState.HIDDEN:
            c.state = CellState.FLAGGED
        elif c.state == CellState.FLAGGED:
            c.state = CellState.HIDDEN

    def _check_win(self):
        # wygrana gdy wszystkie nieminne pola są odkryte
        for row in self.board:
            for c in row:
                if not c.is_mine and c.state != CellState.REVEALED:
                    return
        self.win = True
        self.game_over = True


def draw_game(stdscr, game, cy, cx):
    stdscr.clear()
    stdscr.addstr(0, 0, "STEROWANIE | Strzałki: poruszanie | Spacja: odkryj | F: flaga | Q: wyjście")

    for y in range(game.h):
        for x in range(game.w):
            c = game.board[y][x]
            ch = "■"

            if c.state == CellState.FLAGGED:
                ch = "⚑"
            elif c.state == CellState.REVEALED:
                ch = "*" if c.is_mine else str(c.neighbors) if c.neighbors else " " # mina, liczba sąsiadów albo puste pole

            sy = y + 2 # przesunięcie planszy o 2 wiersze w dół
            sx = x * 2 # rozstawienie kolumn dla czytelności

            if y == cy and x == cx:
                stdscr.addstr(sy, sx, f"[{ch}]")
            else:
                stdscr.addstr(sy, sx, f" {ch} ")

    if game.game_over:
        msg = "WYGRANA!" if game.win else "PRZEGRANA!"
        stdscr.addstr(game.h + 2, 0, msg + " | R: jeszcze raz | Q: menu")

    stdscr.refresh()


def menu(stdscr):
    options = [(6, 6), (8, 12), (10, 15)]
    idx = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # wyśrodkowanie tytułu
        stdscr.addstr(h // 2 - 3, w // 2 - 5, "SAPER")

        for i, (size, _) in enumerate(options):
            marker = ">" if i == idx else " "
            stdscr.addstr(h // 2 + i, w // 2 - 7,
                          f"{marker} {size} x {size}")

        stdscr.addstr(h // 2 + 4, w // 2 - 10,
                      "ENTER – start | Q – wyjście")
        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP:
            idx = (idx - 1) % len(options)
        elif key == curses.KEY_DOWN:
            idx = (idx + 1) % len(options)
        elif key in (ord("\n"), ord(" ")):
            return options[idx]
        elif key in (ord("q"), ord("Q")):
            return None


def main(stdscr):
    curses.curs_set(0) # ukrycie kursora
    stdscr.keypad(True) # obsługa klawiszy specjalnych

    while True:
        choice = menu(stdscr)
        if choice is None:
            break

        size, mines = choice
        game = Minesweeper(size, mines)
        cy = cx = 0

        while True:
            draw_game(stdscr, game, cy, cx)
            key = stdscr.getch()

            if key in (ord("q"), ord("Q")):
                break

            if game.game_over:
                if key in (ord("r"), ord("R")):
                    game = Minesweeper(size, mines)
                    cy = cx = 0
                continue

            if key == curses.KEY_UP:
                cy = max(0, cy - 1)
            elif key == curses.KEY_DOWN:
                cy = min(game.h - 1, cy + 1)
            elif key == curses.KEY_LEFT:
                cx = max(0, cx - 1)
            elif key == curses.KEY_RIGHT:
                cx = min(game.w - 1, cx + 1)
            elif key in (ord(" "), ord("\n")):
                game.reveal(cy, cx)
            elif key in (ord("f"), ord("F")):
                game.toggle_flag(cy, cx)


if __name__ == "__main__":
    curses.wrapper(main)
