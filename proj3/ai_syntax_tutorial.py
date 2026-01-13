# =============================================================================
# CHUNK 1: Variables & Data Types
# =============================================================================
# WHY THIS MATTERS: Every program stores and manipulates data.
# Variables are named containers. Data types define what you can do with them.

# Integer (whole numbers) - used for counting, indexing, loops
age = 25
print("age =", age, "| type:", type(age))

# Float (decimals) - used for measurements, percentages, math
price = 19.99
print("price =", price, "| type:", type(price))

# String (text) - used for names, messages, file paths
name = "Python"
print("name =", name, "| type:", type(name))

# Boolean (True/False) - used for conditions, flags, filtering
is_valid = True
print("is_valid =", is_valid, "| type:", type(is_valid))


# =============================================================================
# CHUNK 2: String Operations
# =============================================================================
# WHY THIS MATTERS: Strings appear in almost every LeetCode problem.
# Slicing and manipulation are essential for parsing and transforming data.

text = "Hello, World!"

# INDEXING: Access single characters (0-indexed)
print("text[0] =", text[0])    # 'H' - first character
print("text[-1] =", text[-1])  # '!' - last character (negative = from end)

# SLICING: [start:end] - end is EXCLUSIVE
print("text[0:5] =", text[0:5])   # 'Hello' - chars 0,1,2,3,4
print("text[7:] =", text[7:])     # 'World!' - char 7 to end
print("text[:5] =", text[:5])     # 'Hello' - start to char 4

# F-STRINGS: Embed variables directly in strings (Python 3.6+)
name, age = "Alice", 25
print(f"{name} is {age} years old")  # "Alice is 25 years old"

# COMMON METHODS (used constantly in interviews)

# .split(separator) - Breaks a string into a LIST of substrings
# Default separator is whitespace (spaces, tabs, newlines)
# Think of it as: "chop this string wherever you see the separator"
sentence = "hello world python"
words = sentence.split()       # No argument = split on whitespace
print("split():", words)       # ['hello', 'world', 'python']

csv_data = "apple,banana,cherry"
fruits = csv_data.split(",")   # Split on comma
print("split(','):", fruits)   # ['apple', 'banana', 'cherry']

# .join(list) - OPPOSITE of split: combines a LIST into a single string
# Syntax: "separator".join(list_of_strings)
# Think of it as: "glue these pieces together with this separator"
words = ["hello", "world"]
joined = " ".join(words)       # Join with space
print("' '.join():", joined)   # 'hello world'

path_parts = ["Users", "griffen", "Desktop"]
path = "/".join(path_parts)    # Join with slash
print("'/'.join():", path)     # 'Users/griffen/Desktop'

# .strip() - Removes whitespace from BOTH ends (not the middle)
# .lstrip() = left only, .rstrip() = right only
# Essential for cleaning user input or file data
messy = "   trim me   "
print("strip():", messy.strip())    # 'trim me'
print("lstrip():", messy.lstrip())  # 'trim me   '
print("rstrip():", messy.rstrip())  # '   trim me'


# =============================================================================
# CHUNK 3: Operators & Comparisons
# =============================================================================
# WHY THIS MATTERS: Every if-statement, loop condition, and calculation uses these.
# Mastering operators is essential for writing any logic.

# ARITHMETIC OPERATORS - basic math
a, b = 10, 3
print("a + b =", a + b)   # 13  (addition)
print("a - b =", a - b)   # 7   (subtraction)
print("a * b =", a * b)   # 30  (multiplication)
print("a / b =", a / b)   # 3.333... (division - always returns float)
print("a // b =", a // b) # 3   (floor division - rounds DOWN to integer)
print("a % b =", a % b)   # 1   (modulo - remainder after division)
print("a ** b =", a ** b) # 1000 (exponent - 10 to the power of 3)

# COMPARISON OPERATORS - return True or False
x, y = 5, 10
print("x == y:", x == y)  # False (equal to)
print("x != y:", x != y)  # True  (not equal to)
print("x < y:", x < y)    # True  (less than)
print("x <= y:", x <= y)  # True  (less than or equal)
print("x > y:", x > y)    # False (greater than)
print("x >= y:", x >= y)  # False (greater than or equal)

# LOGICAL OPERATORS - combine True/False values
print("True and False:", True and False)  # False (both must be True)
print("True or False:", True or False)    # True  (at least one True)
print("not True:", not True)              # False (flips the value)


# =============================================================================
# CHUNK 4: Conditionals (if / elif / else)
# =============================================================================
# WHY THIS MATTERS: Control flow is the backbone of all algorithms.
# Every LeetCode problem uses conditionals to make decisions.

score = 85

# BASIC IF-ELSE: Two branches
if score >= 60:
    print("Pass")      # Runs if condition is True
else:
    print("Fail")      # Runs if condition is False

# IF-ELIF-ELSE: Multiple branches (first True wins)
grade = ""
if score >= 90:
    grade = "A"
elif score >= 80:      # "else if" - only checked if above was False
    grade = "B"
elif score >= 70:
    grade = "C"
else:                  # Catches everything else
    grade = "F"
print(f"Score {score} = Grade {grade}")  # "Score 85 = Grade B"

# TERNARY EXPRESSION: One-liner if-else (great for simple assignments)
# Syntax: value_if_true if condition else value_if_false
status = "adult" if age >= 18 else "minor"
print(f"Age {age}: {status}")

# COMBINING CONDITIONS with and/or
temp = 72
if temp >= 60 and temp <= 80:
    print("Nice weather!")


# =============================================================================
# CHUNK 5: For Loops
# =============================================================================
# WHY THIS MATTERS: Loops let you repeat code. for loops are used in almost
# every LeetCode problem to iterate through arrays, strings, and ranges.

# -----------------------------------------------------------------------------
# RANGE(): Generate a sequence of numbers to loop through
# -----------------------------------------------------------------------------
# range(stop)            → starts at 0, goes up to (but NOT including) stop
# range(start, stop)     → starts at start, goes up to (but NOT including) stop
# range(start, stop, step) → same, but increments by step instead of 1

# range(5) produces: 0, 1, 2, 3, 4 (five numbers, starting from 0)
for i in range(5):
    print(i, end=" ")   # end=" " prints a space instead of newline after each
print()                 # Empty print() adds a newline to end the line

# range(2, 6) produces: 2, 3, 4, 5 (starts at 2, stops BEFORE 6)
for i in range(2, 6):
    print(i, end=" ")
print()

# range(0, 10, 2) produces: 0, 2, 4, 6, 8 (starts at 0, increments by 2)
for i in range(0, 10, 2):
    print(i, end=" ")
print()

# -----------------------------------------------------------------------------
# ITERATING OVER SEQUENCES: Loop directly through items (no index needed)
# -----------------------------------------------------------------------------
# This works on lists, strings, tuples, and any "iterable"
fruits = ["apple", "banana", "cherry"]

# "fruit" is a variable that takes each value in the list, one at a time
# Loop 1: fruit = "apple"
# Loop 2: fruit = "banana"
# Loop 3: fruit = "cherry"
for fruit in fruits:
    print(f"I like {fruit}")

# -----------------------------------------------------------------------------
# ENUMERATE(): When you need BOTH the index AND the value
# -----------------------------------------------------------------------------
# enumerate(list) returns pairs of (index, value) on each iteration
# Use unpacking (idx, fruit) to grab both at once

for idx, fruit in enumerate(fruits):
    # idx = 0, 1, 2 (the position)
    # fruit = "apple", "banana", "cherry" (the value at that position)
    print(f"Index {idx}: {fruit}")


# =============================================================================
# CHUNK 6: While Loops
# =============================================================================
# WHY THIS MATTERS: while loops repeat code as long as a condition is True.
# Use them when you don't know in advance how many times you'll loop.
#
# FOR vs WHILE:
#   - for: "Do this for each item in a collection" (known iterations)
#   - while: "Keep doing this until something changes" (unknown iterations)

# -----------------------------------------------------------------------------
# BASIC WHILE: Keeps running as long as the condition is True
# -----------------------------------------------------------------------------
count = 0               # Initialize a counter BEFORE the loop

while count < 5:        # Check: is count still less than 5?
    print(count)        # If yes, run this code
    count += 1          # CRITICAL: change something so we eventually stop!
                        # Without this, the loop runs forever (infinite loop)
# Output: 0, 1, 2, 3, 4 (stops when count becomes 5, because 5 < 5 is False)

# -----------------------------------------------------------------------------
# BREAK: Exit the loop immediately, no matter the condition
# -----------------------------------------------------------------------------
# Use break when you find what you're looking for and don't need to continue
print("\nSearching for 'banana':")
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    if fruit == "banana":
        print("Found it!")
        break           # Exit the loop RIGHT NOW, skip "cherry" entirely
    print(f"Checking {fruit}...")
# Output: "Checking apple...", "Found it!" (never checks cherry)

# -----------------------------------------------------------------------------
# CONTINUE: Skip the rest of THIS iteration, jump to the next one
# -----------------------------------------------------------------------------
# Use continue when you want to skip certain items but keep looping
print("\nSkipping even numbers:")
for i in range(6):      # 0, 1, 2, 3, 4, 5
    if i % 2 == 0:      # If i is even (remainder when divided by 2 is 0)
        continue        # Skip the print below, go to next iteration
    print(i)            # Only runs for odd numbers
# Output: 1, 3, 5 (even numbers 0, 2, 4 are skipped)


# =============================================================================
# CHUNK 7: Lists I - Creation, Indexing, and Slicing
# =============================================================================
# WHY THIS MATTERS: Lists are Python's most-used data structure. Nearly every
# LeetCode problem involves lists (called "arrays" in other languages).
# Master these operations—you'll use them constantly.

# -----------------------------------------------------------------------------
# CREATING LISTS
# -----------------------------------------------------------------------------
# Lists are created with square brackets []
# They are ORDERED (items stay in the order you put them)
# They are MUTABLE (you can change them after creation)

empty_list = []                      # An empty list (length 0)
numbers = [1, 2, 3, 4, 5]            # A list of 5 integers
mixed = [1, "hello", 3.14, True]    # Lists can hold different types
nested = [[1, 2], [3, 4], [5, 6]]   # A list containing other lists (2D)

print("numbers:", numbers)
print("mixed:", mixed)
print("Length of numbers:", len(numbers))  # len() tells you how many items

# -----------------------------------------------------------------------------
# INDEXING: Accessing individual elements
# -----------------------------------------------------------------------------
# Index starts at 0 (first item is index 0, not 1!)
# Negative indices count from the end (-1 is the last item)

fruits = ["apple", "banana", "cherry", "date", "elderberry"]
#          [0]       [1]       [2]       [3]       [4]
#          [-5]      [-4]      [-3]      [-2]      [-1]

print("\n--- INDEXING ---")
print("fruits[0]:", fruits[0])    # "apple" - first element
print("fruits[2]:", fruits[2])    # "cherry" - third element
print("fruits[-1]:", fruits[-1])  # "elderberry" - last element
print("fruits[-2]:", fruits[-2])  # "date" - second to last

# -----------------------------------------------------------------------------
# SLICING: Getting a portion of the list
# -----------------------------------------------------------------------------
# Syntax: list[start:end] - gets items from start UP TO (not including) end
# Syntax: list[start:end:step] - with step (skip every N items)

print("\n--- SLICING ---")
print("fruits[1:4]:", fruits[1:4])   # ["banana", "cherry", "date"]
                                      # Starts at index 1, stops BEFORE index 4

print("fruits[:3]:", fruits[:3])     # ["apple", "banana", "cherry"]
                                      # Omit start = start from beginning

print("fruits[2:]:", fruits[2:])     # ["cherry", "date", "elderberry"]
                                      # Omit end = go to the end

print("fruits[::2]:", fruits[::2])   # ["apple", "cherry", "elderberry"]
                                      # Step of 2 = every other item

print("fruits[::-1]:", fruits[::-1]) # Reversed list!
                                      # Step of -1 = go backwards

# -----------------------------------------------------------------------------
# KEY DIFFERENCE: Lists are MUTABLE (unlike strings!)
# -----------------------------------------------------------------------------
# You can change a list after creating it

print("\n--- MUTABILITY ---")
fruits[0] = "apricot"                # Replace first element
print("After fruits[0] = 'apricot':", fruits)

# Compare to strings (this would ERROR):
# text = "hello"
# text[0] = "H"  # TypeError! Strings are immutable
