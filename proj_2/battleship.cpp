#include <iostream>
#include <vector>
#include <string>
#include <cstdlib>
#include <ctime>
#include <iomanip>
#include <algorithm>
#include <limits>
#include <random>

using namespace std;

// ANSI color codes for terminal
namespace Color {
    const string RESET = "\033[0m";
    const string BOLD = "\033[1m";
    const string RED = "\033[31m";
    const string GREEN = "\033[32m";
    const string YELLOW = "\033[33m";
    const string BLUE = "\033[34m";
    const string MAGENTA = "\033[35m";
    const string CYAN = "\033[36m";
    const string WHITE = "\033[37m";
    const string BG_BLUE = "\033[44m";
    const string BG_RED = "\033[41m";
    const string BG_GREEN = "\033[42m";
}

const int BOARD_SIZE = 10;

// Cell states
enum CellState {
    EMPTY = 0,
    SHIP = 1,
    HIT = 2,
    MISS = 3,
    SUNK = 4
};

// Ship structure
struct Ship {
    string name;
    int size;
    int hits;
    bool sunk;
    vector<pair<int, int>> positions;
    
    Ship(string n, int s) : name(n), size(s), hits(0), sunk(false) {}
    
    bool isSunk() const {
        return hits >= size;
    }
};

class Board {
private:
    vector<vector<CellState>> grid;
    vector<Ship> ships;
    
public:
    Board() : grid(BOARD_SIZE, vector<CellState>(BOARD_SIZE, EMPTY)) {}
    
    void initializeShips() {
        ships.clear();
        ships.push_back(Ship("Carrier", 5));
        ships.push_back(Ship("Battleship", 4));
        ships.push_back(Ship("Cruiser", 3));
        ships.push_back(Ship("Submarine", 3));
        ships.push_back(Ship("Destroyer", 2));
    }
    
    vector<Ship>& getShips() {
        return ships;
    }
    
    bool canPlaceShip(int row, int col, int size, bool horizontal) {
        if (horizontal) {
            if (col + size > BOARD_SIZE) return false;
            for (int i = 0; i < size; i++) {
                if (grid[row][col + i] != EMPTY) return false;
            }
        } else {
            if (row + size > BOARD_SIZE) return false;
            for (int i = 0; i < size; i++) {
                if (grid[row + i][col] != EMPTY) return false;
            }
        }
        return true;
    }
    
    void placeShip(Ship& ship, int row, int col, bool horizontal) {
        ship.positions.clear();
        for (int i = 0; i < ship.size; i++) {
            int r = horizontal ? row : row + i;
            int c = horizontal ? col + i : col;
            grid[r][c] = SHIP;
            ship.positions.push_back({r, c});
        }
    }
    
    void placeShipsRandomly() {
        for (Ship& ship : ships) {
            bool placed = false;
            while (!placed) {
                int row = rand() % BOARD_SIZE;
                int col = rand() % BOARD_SIZE;
                bool horizontal = rand() % 2;
                
                if (canPlaceShip(row, col, ship.size, horizontal)) {
                    placeShip(ship, row, col, horizontal);
                    placed = true;
                }
            }
        }
    }
    
    // Returns: 0 = miss, 1 = hit, 2 = sunk, -1 = already attacked
    int receiveAttack(int row, int col, string& shipName) {
        if (row < 0 || row >= BOARD_SIZE || col < 0 || col >= BOARD_SIZE) {
            return -1;
        }
        
        if (grid[row][col] == HIT || grid[row][col] == MISS || grid[row][col] == SUNK) {
            return -1;
        }
        
        if (grid[row][col] == SHIP) {
            grid[row][col] = HIT;
            
            // Find which ship was hit
            for (Ship& ship : ships) {
                for (auto& pos : ship.positions) {
                    if (pos.first == row && pos.second == col) {
                        ship.hits++;
                        if (ship.isSunk()) {
                            ship.sunk = true;
                            shipName = ship.name;
                            // Mark all positions as sunk
                            for (auto& p : ship.positions) {
                                grid[p.first][p.second] = SUNK;
                            }
                            return 2;
                        }
                        return 1;
                    }
                }
            }
            return 1;
        }
        
        grid[row][col] = MISS;
        return 0;
    }
    
    bool allShipsSunk() const {
        for (const Ship& ship : ships) {
            if (!ship.sunk) return false;
        }
        return true;
    }
    
    CellState getCell(int row, int col) const {
        return grid[row][col];
    }
    
    void display(bool hideShips = false, [[maybe_unused]] bool isEnemy = false) const {
        cout << "\n";
        
        // Column headers
        cout << "    ";
        for (int i = 0; i < BOARD_SIZE; i++) {
            cout << Color::CYAN << setw(3) << i << Color::RESET;
        }
        cout << "\n";
        
        // Top border
        cout << "   " << Color::BLUE << "┌";
        for (int i = 0; i < BOARD_SIZE; i++) {
            cout << "───";
            if (i < BOARD_SIZE - 1) cout << "┬";
        }
        cout << "┐" << Color::RESET << "\n";
        
        for (int row = 0; row < BOARD_SIZE; row++) {
            cout << Color::CYAN << setw(2) << row << Color::RESET << " " << Color::BLUE << "│" << Color::RESET;
            
            for (int col = 0; col < BOARD_SIZE; col++) {
                string cell;
                CellState state = grid[row][col];
                
                switch (state) {
                    case EMPTY:
                        cell = Color::BLUE + " ~ " + Color::RESET;
                        break;
                    case SHIP:
                        if (hideShips) {
                            cell = Color::BLUE + " ~ " + Color::RESET;
                        } else {
                            cell = Color::GREEN + " ■ " + Color::RESET;
                        }
                        break;
                    case HIT:
                        cell = Color::RED + " ✖ " + Color::RESET;
                        break;
                    case MISS:
                        cell = Color::WHITE + " ○ " + Color::RESET;
                        break;
                    case SUNK:
                        cell = Color::MAGENTA + " ✖ " + Color::RESET;
                        break;
                }
                cout << cell;
                if (col < BOARD_SIZE - 1) cout << Color::BLUE << "│" << Color::RESET;
            }
            cout << Color::BLUE << "│" << Color::RESET << "\n";
            
            // Row separator
            if (row < BOARD_SIZE - 1) {
                cout << "   " << Color::BLUE << "├";
                for (int i = 0; i < BOARD_SIZE; i++) {
                    cout << "───";
                    if (i < BOARD_SIZE - 1) cout << "┼";
                }
                cout << "┤" << Color::RESET << "\n";
            }
        }
        
        // Bottom border
        cout << "   " << Color::BLUE << "└";
        for (int i = 0; i < BOARD_SIZE; i++) {
            cout << "───";
            if (i < BOARD_SIZE - 1) cout << "┴";
        }
        cout << "┘" << Color::RESET << "\n";
    }
};

class AI {
private:
    vector<pair<int, int>> huntTargets;
    vector<pair<int, int>> possibleTargets;
    bool hunting;
    int lastHitRow, lastHitCol;
    
public:
    AI() : hunting(false), lastHitRow(-1), lastHitCol(-1) {
        // Initialize all possible targets
        for (int r = 0; r < BOARD_SIZE; r++) {
            for (int c = 0; c < BOARD_SIZE; c++) {
                possibleTargets.push_back({r, c});
            }
        }
        // Shuffle for randomness
        random_device rd;
        mt19937 g(rd());
        shuffle(possibleTargets.begin(), possibleTargets.end(), g);
    }
    
    pair<int, int> getTarget() {
        // If we have hunt targets from a hit, prioritize those
        if (!huntTargets.empty()) {
            pair<int, int> target = huntTargets.back();
            huntTargets.pop_back();
            
            // Remove from possible targets
            possibleTargets.erase(
                remove(possibleTargets.begin(), possibleTargets.end(), target),
                possibleTargets.end()
            );
            
            return target;
        }
        
        // Otherwise pick from remaining possible targets
        if (!possibleTargets.empty()) {
            pair<int, int> target = possibleTargets.back();
            possibleTargets.pop_back();
            return target;
        }
        
        return {-1, -1};
    }
    
    void reportResult(int row, int col, int result) {
        if (result == 1) { // Hit but not sunk
            // Add adjacent cells to hunt targets
            vector<pair<int, int>> adjacent = {
                {row - 1, col}, {row + 1, col},
                {row, col - 1}, {row, col + 1}
            };
            
            for (auto& adj : adjacent) {
                if (adj.first >= 0 && adj.first < BOARD_SIZE &&
                    adj.second >= 0 && adj.second < BOARD_SIZE) {
                    // Check if it's still a possible target
                    if (find(possibleTargets.begin(), possibleTargets.end(), adj) != possibleTargets.end()) {
                        huntTargets.push_back(adj);
                    }
                }
            }
            hunting = true;
            lastHitRow = row;
            lastHitCol = col;
        } else if (result == 2) { // Sunk
            // Clear hunt targets for this ship
            huntTargets.clear();
            hunting = false;
        }
    }
};

class Game {
private:
    Board playerBoard;
    Board computerBoard;
    AI computerAI;
    int playerShots;
    int computerShots;
    int playerHits;
    int computerHits;
    
public:
    Game() : playerShots(0), computerShots(0), playerHits(0), computerHits(0) {}
    
    void clearScreen() {
        cout << "\033[2J\033[H";
    }
    
    void printTitle() {
        cout << Color::CYAN << Color::BOLD;
        cout << R"(
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║    ██████╗  █████╗ ████████╗████████╗██╗     ███████╗        ║
    ║    ██╔══██╗██╔══██╗╚══██╔══╝╚══██╔══╝██║     ██╔════╝        ║
    ║    ██████╔╝███████║   ██║      ██║   ██║     █████╗          ║
    ║    ██╔══██╗██╔══██║   ██║      ██║   ██║     ██╔══╝          ║
    ║    ██████╔╝██║  ██║   ██║      ██║   ███████╗███████╗        ║
    ║    ╚═════╝ ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚══════╝╚══════╝        ║
    ║                                                              ║
    ║        ███████╗██╗  ██╗██╗██████╗                            ║
    ║        ██╔════╝██║  ██║██║██╔══██╗                           ║
    ║        ███████╗███████║██║██████╔╝                           ║
    ║        ╚════██║██╔══██║██║██╔═══╝                            ║
    ║        ███████║██║  ██║██║██║                                ║
    ║        ╚══════╝╚═╝  ╚═╝╚═╝╚═╝                                ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
)" << Color::RESET << "\n";
    }
    
    void printLegend() {
        cout << "\n" << Color::BOLD << "  Legend:" << Color::RESET << "\n";
        cout << "  " << Color::BLUE << "~" << Color::RESET << " Water   ";
        cout << Color::GREEN << "■" << Color::RESET << " Ship   ";
        cout << Color::RED << "✖" << Color::RESET << " Hit   ";
        cout << Color::WHITE << "○" << Color::RESET << " Miss   ";
        cout << Color::MAGENTA << "✖" << Color::RESET << " Sunk\n";
    }
    
    void showShipStatus(Board& board, const string& title) {
        cout << "\n" << Color::BOLD << "  " << title << ":" << Color::RESET << "\n";
        for (const Ship& ship : board.getShips()) {
            cout << "  " << setw(12) << left << ship.name << " [";
            for (int i = 0; i < ship.size; i++) {
                if (i < ship.hits) {
                    cout << Color::RED << "X" << Color::RESET;
                } else {
                    cout << Color::GREEN << "O" << Color::RESET;
                }
            }
            cout << "] ";
            if (ship.sunk) {
                cout << Color::RED << "SUNK!" << Color::RESET;
            }
            cout << "\n";
        }
    }
    
    bool getPlayerInput(int& row, int& col) {
        string input;
        cout << "\n" << Color::YELLOW << "  Enter target (row col): " << Color::RESET;
        
        if (!(cin >> row >> col)) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            return false;
        }
        
        if (row < 0 || row >= BOARD_SIZE || col < 0 || col >= BOARD_SIZE) {
            return false;
        }
        
        return true;
    }
    
    void placePlayerShips() {
        clearScreen();
        printTitle();
        cout << "\n" << Color::BOLD << "  SHIP PLACEMENT" << Color::RESET << "\n";
        cout << "  Place your ships on the board.\n";
        
        playerBoard.initializeShips();
        
        for (Ship& ship : playerBoard.getShips()) {
            bool placed = false;
            
            while (!placed) {
                clearScreen();
                printTitle();
                cout << "\n" << Color::BOLD << "  Placing: " << Color::CYAN << ship.name 
                     << Color::RESET << " (Size: " << ship.size << ")\n";
                playerBoard.display(false, false);
                printLegend();
                
                int row, col;
                char dir;
                
                cout << "\n  Enter starting position (row col): ";
                if (!(cin >> row >> col)) {
                    cin.clear();
                    cin.ignore(numeric_limits<streamsize>::max(), '\n');
                    cout << Color::RED << "  Invalid input! Try again." << Color::RESET << "\n";
                    continue;
                }
                
                cout << "  Direction (h=horizontal, v=vertical): ";
                cin >> dir;
                
                bool horizontal = (dir == 'h' || dir == 'H');
                
                if (playerBoard.canPlaceShip(row, col, ship.size, horizontal)) {
                    playerBoard.placeShip(ship, row, col, horizontal);
                    placed = true;
                } else {
                    cout << Color::RED << "\n  Cannot place ship there! Try again." << Color::RESET << "\n";
                    cin.ignore(numeric_limits<streamsize>::max(), '\n');
                }
            }
        }
    }
    
    void placeShipsRandomlyForPlayer() {
        playerBoard.initializeShips();
        playerBoard.placeShipsRandomly();
    }
    
    void setupGame() {
        clearScreen();
        printTitle();
        
        cout << "\n" << Color::BOLD << "  GAME SETUP" << Color::RESET << "\n\n";
        cout << "  How would you like to place your ships?\n";
        cout << "  " << Color::CYAN << "1" << Color::RESET << ") Place manually\n";
        cout << "  " << Color::CYAN << "2" << Color::RESET << ") Random placement\n\n";
        cout << "  Choice: ";
        
        int choice;
        cin >> choice;
        
        if (choice == 1) {
            placePlayerShips();
        } else {
            placeShipsRandomlyForPlayer();
        }
        
        // Computer places ships randomly
        computerBoard.initializeShips();
        computerBoard.placeShipsRandomly();
    }
    
    void playerTurn() {
        bool validShot = false;
        
        while (!validShot) {
            int row, col;
            
            if (!getPlayerInput(row, col)) {
                cout << Color::RED << "  Invalid coordinates! Use numbers 0-9." << Color::RESET << "\n";
                continue;
            }
            
            string shipName;
            int result = computerBoard.receiveAttack(row, col, shipName);
            
            if (result == -1) {
                cout << Color::RED << "  Already attacked there! Try again." << Color::RESET << "\n";
                continue;
            }
            
            playerShots++;
            validShot = true;
            
            cout << "\n";
            if (result == 0) {
                cout << Color::WHITE << "  ○ MISS! ○" << Color::RESET << "\n";
            } else if (result == 1) {
                cout << Color::RED << "  ✖ HIT! ✖" << Color::RESET << "\n";
                playerHits++;
            } else if (result == 2) {
                cout << Color::MAGENTA << Color::BOLD << "  ★ You sunk the " << shipName << "! ★" << Color::RESET << "\n";
                playerHits++;
            }
        }
    }
    
    void computerTurn() {
        pair<int, int> target = computerAI.getTarget();
        
        if (target.first == -1) return;
        
        string shipName;
        int result = playerBoard.receiveAttack(target.first, target.second, shipName);
        
        computerShots++;
        computerAI.reportResult(target.first, target.second, result);
        
        cout << "\n  Computer fires at (" << target.first << ", " << target.second << "): ";
        
        if (result == 0) {
            cout << Color::WHITE << "MISS" << Color::RESET << "\n";
        } else if (result == 1) {
            cout << Color::RED << "HIT!" << Color::RESET << "\n";
            computerHits++;
        } else if (result == 2) {
            cout << Color::MAGENTA << "SUNK your " << shipName << "!" << Color::RESET << "\n";
            computerHits++;
        }
    }
    
    void displayBoards() {
        cout << "\n" << Color::BOLD << "  ═══════════════ YOUR BOARD ═══════════════" << Color::RESET;
        playerBoard.display(false, false);
        
        cout << "\n" << Color::BOLD << "  ════════════ ENEMY WATERS ════════════" << Color::RESET;
        computerBoard.display(true, true);
    }
    
    void displayStats() {
        cout << "\n" << Color::BOLD << "  ══════════════ STATISTICS ══════════════" << Color::RESET << "\n";
        cout << "  Your shots: " << playerShots << " | Hits: " << playerHits;
        if (playerShots > 0) {
            cout << " | Accuracy: " << fixed << setprecision(1) 
                 << (100.0 * playerHits / playerShots) << "%";
        }
        cout << "\n";
        cout << "  Enemy shots: " << computerShots << " | Hits: " << computerHits;
        if (computerShots > 0) {
            cout << " | Accuracy: " << fixed << setprecision(1) 
                 << (100.0 * computerHits / computerShots) << "%";
        }
        cout << "\n";
    }
    
    void play() {
        setupGame();
        
        bool gameOver = false;
        
        while (!gameOver) {
            clearScreen();
            printTitle();
            displayBoards();
            showShipStatus(playerBoard, "Your Fleet");
            showShipStatus(computerBoard, "Enemy Fleet");
            printLegend();
            displayStats();
            
            // Player turn
            cout << "\n" << Color::BOLD << Color::YELLOW << "  ═══════════ YOUR TURN ═══════════" << Color::RESET << "\n";
            playerTurn();
            
            if (computerBoard.allShipsSunk()) {
                gameOver = true;
                clearScreen();
                printTitle();
                displayBoards();
                displayStats();
                cout << "\n" << Color::GREEN << Color::BOLD;
                cout << R"(
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║      ██╗   ██╗ ██████╗ ██╗   ██╗    ██╗    ██╗██╗███╗   ██╗║
    ║      ╚██╗ ██╔╝██╔═══██╗██║   ██║    ██║    ██║██║████╗  ██║║
    ║       ╚████╔╝ ██║   ██║██║   ██║    ██║ █╗ ██║██║██╔██╗ ██║║
    ║        ╚██╔╝  ██║   ██║██║   ██║    ██║███╗██║██║██║╚██╗██║║
    ║         ██║   ╚██████╔╝╚██████╔╝    ╚███╔███╔╝██║██║ ╚████║║
    ║         ╚═╝    ╚═════╝  ╚═════╝      ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝║
    ║                                                           ║
    ║              CONGRATULATIONS, ADMIRAL!                    ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
)" << Color::RESET << "\n";
                break;
            }
            
            // Computer turn
            cout << "\n" << Color::BOLD << Color::RED << "  ═══════════ ENEMY TURN ═══════════" << Color::RESET << "\n";
            computerTurn();
            
            if (playerBoard.allShipsSunk()) {
                gameOver = true;
                clearScreen();
                printTitle();
                displayBoards();
                displayStats();
                cout << "\n" << Color::RED << Color::BOLD;
                cout << R"(
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║      ██████╗ ███████╗███████╗███████╗ █████╗ ████████╗    ║
    ║      ██╔══██╗██╔════╝██╔════╝██╔════╝██╔══██╗╚══██╔══╝    ║
    ║      ██║  ██║█████╗  █████╗  █████╗  ███████║   ██║       ║
    ║      ██║  ██║██╔══╝  ██╔══╝  ██╔══╝  ██╔══██║   ██║       ║
    ║      ██████╔╝███████╗██║     ███████╗██║  ██║   ██║       ║
    ║      ╚═════╝ ╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝       ║
    ║                                                           ║
    ║            YOUR FLEET HAS BEEN DESTROYED!                 ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
)" << Color::RESET << "\n";
                break;
            }
            
            cout << "\n  Press Enter to continue...";
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cin.get();
        }
    }
};

int main() {
    srand(static_cast<unsigned>(time(nullptr)));
    
    Game game;
    game.play();
    
    cout << "\n  Thanks for playing Battleship!\n\n";
    
    return 0;
}
