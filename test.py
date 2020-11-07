import curses

def set_screen_layout_1(center_y, center_x):
    # Set screen layout that will be drawn by curses
    # At this screen we choose figure for game and turn order.
    # Coordinate of point where cursor will moved at start of layout drawing.
    # Coordinate y counts from top of screen and coordinate x counts from left of screen
    name = 'Tic Tac Toe'
    help_message = 'Choose figure. Move cursor by up and down keys. Push space key for choose. "O" will move first.'
    delim = "-" * len(help_message)
    start_cursor_point = [center_y + 1, center_x]
    return [start_cursor_point, name, delim, help_message, delim, "X", "O"]

def set_screen_layout_2(center_y, center_x):
    # Set screen layout that will be drawn by curses
    # It is main game screen
    # Coordinate of point where cursor will moved at start of layout drawing.
    # Coordinate y counts from top of screen and coordinate x counts from left of screen
    name = 'Tic Tac Toe'
    help_message = 'Use arrows to move,  [SPACE] Draw,  [Q] Quit'
    delim = "-" * len(help_message)
    board = """
   │   │   
───┼───┼───
   │   │   
───┼───┼───
   │   │   
"""
    start_cursor_point = [center_y + 2, center_x]
    return [start_cursor_point, name, delim, help_message, delim] + board.split("\n")

def print_screen_layout(screen_layout, stdscr, center_y, center_x):
    # draws screen layout at center
    y_offset = center_y - len(screen_layout) // 2
    for row in screen_layout:
        stdscr.addstr(y_offset, center_x - len(row) // 2, row)
        y_offset +=1

def get_center_coordinates(stdscr):
    # calculates coordinates of central point of screen
    # Coordinate y counts from top of screen and coordinate x counts from left of screen
    maxy, maxx = stdscr.getmaxyx()
    return maxy // 2, maxx // 2

def print_players(stdscr, player_id):
    message = "Player " + CH_P1
    stdscr.addstr(Y_OFFSET + 6, 0, 'Player {}'.format(CH_P1),
                  curses.A_BOLD if player_id == 0 else 0)
    stdscr.addstr(Y_OFFSET + 7, 0, 'Player {}'.format(CH_P2),
                  curses.A_BOLD if player_id == 1 else 0)

def choose_figure(stdscr, center_y, center_x):
    screen_layout = set_screen_layout_1(center_y, center_x)
    [start_y, start_x] = screen_layout.pop(0)
    print_screen_layout(screen_layout, stdscr, center_y, center_x)
    y = x = 0
    while True:
        stdscr.move(start_y + y, start_x + x)
        c = stdscr.getch()
        if c == curses.KEY_UP:
            y = max(0, y - 1)
        elif c == curses.KEY_DOWN:
            y = min(1, y + 1)
        elif c == ord('q') or c == ord('Q'):
            break
        elif c == ord(' '):
            # stdscr.getyx() gets coordinats (y,x) of point where cursor was
            # stdscr.inch(y, x) gets ascii code of character at point with coordinats (y,x)
            # chr converts ascii code to string character
            return chr(stdscr.inch(*stdscr.getyx()))


stdscr = curses.initscr()
# curses.noecho()
# curses.cbreak()
# stdscr.keypad(True)

def main(stdscr):
    center_y, center_x = get_center_coordinates(stdscr)
    # Clear screen
    stdscr.clear()
    #screen_layout = set_screen_layout()
    figure = choose_figure(stdscr, center_y, center_x)
    message = ["Figure is: " + figure]
    #print_screen_layout(stdscr, screen_layout)
    stdscr.refresh()
    stdscr.clear()
    print_screen_layout(message, stdscr, center_y, center_x)
    stdscr.getkey()


if __name__ == '__main__':
    curses.wrapper(main)