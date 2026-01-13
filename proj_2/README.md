# Battleship

A classic naval combat game implemented in C++ with a colorful terminal interface.

## Features

- **10x10 game board** with coordinate-based targeting
- **5 ships** to place and sink:
  - Carrier (5 cells)
  - Battleship (4 cells)
  - Cruiser (3 cells)
  - Submarine (3 cells)
  - Destroyer (2 cells)
- **Smart AI opponent** that hunts adjacent cells after hits
- **Colorful terminal display** with Unicode characters
- **Manual or random ship placement**
- **Game statistics** tracking shots and accuracy

## Building

Using Make:
```bash
make
```

Or compile directly:
```bash
g++ -std=c++17 -Wall -O2 -o battleship battleship.cpp
```

## Running

```bash
./battleship
# or
make run
```

## How to Play

1. **Setup**: Choose to place ships manually or randomly
2. **Manual Placement**: Enter row and column (0-9), then direction (h/v)
3. **Attack**: Enter target coordinates as `row col` (e.g., `5 3`)
4. **Win**: Sink all enemy ships before they sink yours!

## Controls

- Enter coordinates as two numbers: `row col`
- Rows and columns are numbered 0-9
- For ship placement, use `h` for horizontal, `v` for vertical

## Display Legend

| Symbol | Meaning |
|--------|---------|
| `~` | Water |
| `■` | Your ship |
| `✖` (red) | Hit |
| `○` | Miss |
| `✖` (purple) | Sunk ship |

## Requirements

- C++17 compatible compiler (g++, clang++)
- Terminal with ANSI color support

## License

MIT License - Feel free to modify and share!
