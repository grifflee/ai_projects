CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2
TARGET = battleship
SRC = battleship.cpp

.PHONY: all clean run

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC)

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET)
