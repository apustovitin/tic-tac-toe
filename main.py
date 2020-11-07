import curses

empty_field = """
    1       2       3
        |       |
a   X   |   X   |   X  
 _______|_______|_______
        |       |
b   X   |   X   |   X  
 _______|_______|_______
        |       |
c   X   |   X   |   X  
        |       |       
"""
print(empty_field)

# determine the terminal type, send any required setup codes to the terminal,
# and create various internal data structures.
# If successful, initscr() returns a window object representing the entire screen
# stdscr = curses.initscr()

# turn off automatic echoing of keys to the screen, in order to be able to read keys
# and only display them under certain circumstances
#curses.noecho()

# Applications will also commonly need to react to keys instantly, without requiring
# the Enter key to be pressed; this is called cbreak mode, as opposed to the usual buffered input mode.
#curses.cbreak()

# Terminals usually return special keys, such as the cursor keys or navigation keys such as Page Up and Home,
# as a multibyte escape sequence. While you could write your application to expect such sequences and process
# them accordingly, curses can do it for you, returning a special value such as curses.KEY_LEFT.
# To get curses to do the job, you’ll have to enable keypad mode.
# stdscr.keypad(True)




# Terminating a curses application
# curses.nocbreak()
# stdscr.keypad(False)
# curses.echo()
# restore the terminal to its original operating mode.
# curses.endwin()

# The newwin() function creates a new window of a given size, returning the new window object.
# begin_x = 20; begin_y = 7
# height = 5; width = 40
# win = curses.newwin(height, width, begin_y, begin_x)

# Your application can determine the size of the screen by using the
# curses.LINES and curses.COLS variables to obtain the y and x sizes.
# Legal coordinates will then extend from (0,0) to (curses.LINES - 1, curses.COLS - 1).

# When you call a method to display or erase text, the effect doesn’t immediately show up on the display.
# Instead you must call the refresh() method of window objects to update the screen.
# be sure that the screen has been redrawn before pausing to wait for user input,
# by first calling stdscr.refresh() or the refresh() method of some other relevant window.

# There are two methods for getting input from a window:
#
# getch() refreshes the screen and then waits for the user to hit a key, displaying the key if echo() has been called
# earlier. You can optionally specify a coordinate to which the cursor should be moved before pausing.
#
# getkey() does the same thing but converts the integer to a string. Individual characters are returned as
# 1-character strings, and special keys such as function keys return
# longer strings containing a key name such as KEY_UP or ^G.


stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

def main(stdscr):
    # Clear screen
    #stdscr.clear()
    begin_x = 20; begin_y = 7
    height = 5; width = 40
    #win = curses.newwin(height, width, begin_y, begin_x)

    stdscr.addstr(0, 0, "Current mode: Typing mode", curses.A_REVERSE)

    # stdscr.refresh()
    # stdscr.getkey()
    while True:
        c = stdscr.getch()
        stdscr.refresh()
        if c == ord('p'):
            stdscr.addstr(10, 10, "Entered: p", curses.A_REVERSE)
            stdscr.refresh()
        elif c == ord('q'):
            break  # Exit the while loop
            stdscr.refresh()
        elif c == curses.KEY_LEFT:
            stdscr.addstr(20, 20, "Entered: XXX", curses.A_REVERSE)
            stdscr.refresh()
        stdscr.refresh()
        stdscr.getkey()

curses.wrapper(main)

main(stdscr)