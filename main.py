import random

MAX_LINES = 4
MAX_BET = 100
MIN_BET = 1

ROWS = 4
COLS = 4

symbol_count = {
    "A": 12,
    "B": 14,
    "C": 16,
    "D": 16,
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2,
}

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)
    return winnings, winning_lines



def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    """
    we create an empty list and fill the list with the symbols as many times as they can come acc to their count
    all_symbols = [A, A, B, B, B, B and so on...]
    """

    columns = []
    for _ in range(cols):                               # for every instance of column
        column = []                                     # define as empty column
        current_symbols = all_symbols[:]                # create a copy of the allsymbols list 
        for _ in range(rows):                           # for every instance of row (out of 3 currently)
            value = random.choice(current_symbols)      # append values from the copied list one by one randomly
            current_symbols.remove(value)               # remove that value after it is appended once so no repeat possible
            column.append(value)
        columns.append(column)                          # do for every row - in every column

    return columns                                      

    """
    here "columns" will look like [A D D] [A B D] [C D D] -> but these are the values that are possible for every row not every col
    so -> we have to transpose them as the slots work
    it should be something like =>
    [A | A | C]
    [D | B | D]
    [D | D | D]     => btw bingo
    """

def print_slot_machine(columns):                        # function for transposing and making it print correctly for user
    for row in range(len(columns[0])):                  # for first row in all columns (defined by len = no. of cols)
        for i, column in enumerate(columns):            # enumerate gives index and value so using 'i' for it.
            
            if i != len(columns) - 1:                   # so that we have to print 1 less pipe at the end
                print(column[row], end=" | ")          # end tells the print statement what to end the line with; by default end = \n
            else:
                print(column[row])

def deposit():
    while True:
        amount = input("What would you like to deposit? $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Amount must be greater than 0.")
        else:
            print("Please enter a valid number.")
    # print("Deposited amount is: ", amount, "$")
    return amount

def get_number_of_lines():
    while True:
        lines = input("Please enter number of lines to bet on (1-" + str(MAX_LINES) + ")? ")
        if lines.isdigit():
            lines = int(lines)
            if lines in range(1,MAX_LINES+1):
                break
            else:
                print("Enter a valid number of lines.")
        else:
            print("Please enter a valid number.")
    # print("Number of lines to play: ", lines)
    return lines

def get_bet():
    while True:
        amount = input("What would you like to bet on each line? $")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Amount must be between {MIN_BET} - {MAX_BET}.") # f automatically converts format, no need to tell
        else:
            print("Please enter a valid number.")
    return amount



def spin(balance):
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(f"You do not have enough to bet that amount, your current balance is ${balance}.")
        else:
            break

    print(f"\nYou are betting ${bet} on {lines} lines. Total bet is equal to ${total_bet}.")
    
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won ${winnings}.")
    if winning_lines != []:
        print(f"You won on lines:", *winning_lines)
    return winnings - total_bet


def main():
    balance = deposit()
    while True:
        print(f"Current balance is: ${balance}")
        answer = input("Press Enter to play (q to quit).")
        if answer == "q":
            break
        balance += spin(balance)

    print(f"You left with ${balance}")
main()