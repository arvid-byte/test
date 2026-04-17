#!/usr/bin/env python3
"""Et enkelt terminalbasert Sudoku-spill."""

from __future__ import annotations

from copy import deepcopy

Board = list[list[int]]

# 0 betyr tom celle.
DEFAULT_PUZZLE: Board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


class SudokuGame:
    def __init__(self, puzzle: Board) -> None:
        self.initial_board = deepcopy(puzzle)
        self.board = deepcopy(puzzle)

    def print_board(self) -> None:
        print("\n    1 2 3   4 5 6   7 8 9")
        print("   +-------+-------+-------+")
        for row_idx, row in enumerate(self.board, start=1):
            rendered = [str(n) if n != 0 else "." for n in row]
            print(
                f" {row_idx} | {' '.join(rendered[0:3])} | {' '.join(rendered[3:6])} | {' '.join(rendered[6:9])} |"
            )
            if row_idx % 3 == 0:
                print("   +-------+-------+-------+")

    def is_move_valid(self, row: int, col: int, num: int) -> bool:
        # Sjekk rad
        if any(self.board[row][c] == num for c in range(9) if c != col):
            return False

        # Sjekk kolonne
        if any(self.board[r][col] == num for r in range(9) if r != row):
            return False

        # Sjekk 3x3-boks
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if (r, c) != (row, col) and self.board[r][c] == num:
                    return False

        return True

    def place_number(self, row: int, col: int, num: int) -> tuple[bool, str]:
        if self.initial_board[row][col] != 0:
            return False, "Denne ruten er låst fra startpuslespillet."

        if num == 0:
            self.board[row][col] = 0
            return True, "Ruten ble tømt."

        if num < 1 or num > 9:
            return False, "Tall må være mellom 1 og 9 (eller 0 for å tømme)."

        old_val = self.board[row][col]
        self.board[row][col] = num
        if not self.is_move_valid(row, col, num):
            self.board[row][col] = old_val
            return False, "Ugyldig trekk: bryter Sudoku-reglene."

        return True, "Trekk registrert."

    def is_complete(self) -> bool:
        # Ingen tomme ruter
        if any(0 in row for row in self.board):
            return False

        # Alle celler må følge reglene
        for r in range(9):
            for c in range(9):
                num = self.board[r][c]
                if num == 0:
                    return False
                if not self.is_move_valid(r, c, num):
                    return False

        return True


def print_help() -> None:
    print(
        """
Kommandoer:
  sett R C N   -> sett tall N i rad R, kolonne C
                  (R, C, N mellom 1 og 9. Bruk N=0 for å tømme rute)
  vis          -> vis brettet
  hjelp        -> vis denne hjelpeteksten
  slutt        -> avslutt spillet
""".strip()
    )


def parse_set_command(parts: list[str]) -> tuple[bool, tuple[int, int, int] | str]:
    if len(parts) != 4:
        return False, "Bruk: sett <rad> <kolonne> <tall>."

    try:
        row = int(parts[1])
        col = int(parts[2])
        num = int(parts[3])
    except ValueError:
        return False, "Rad, kolonne og tall må være heltall."

    if not (1 <= row <= 9 and 1 <= col <= 9 and 0 <= num <= 9):
        return False, "Rad og kolonne må være 1-9. Tall må være 0-9."

    # Konverter til 0-indeks
    return True, (row - 1, col - 1, num)


def main() -> None:
    game = SudokuGame(DEFAULT_PUZZLE)

    print("Velkommen til Sudoku! 🎯")
    print_help()
    game.print_board()

    while True:
        cmd = input("\n> ").strip()
        if not cmd:
            continue

        parts = cmd.split()
        action = parts[0].lower()

        if action == "slutt":
            print("Takk for spillet!")
            break

        if action == "hjelp":
            print_help()
            continue

        if action == "vis":
            game.print_board()
            continue

        if action == "sett":
            ok, result = parse_set_command(parts)
            if not ok:
                print(result)
                continue

            row, col, num = result
            success, message = game.place_number(row, col, num)
            print(message)
            game.print_board()

            if success and game.is_complete():
                print("Gratulerer! Du løste Sudoku-brettet! 🥳")
                break
            continue

        print("Ukjent kommando. Skriv 'hjelp' for tilgjengelige kommandoer.")


if __name__ == "__main__":
    main()
