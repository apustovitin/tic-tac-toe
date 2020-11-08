import curses

def set_screen_layout_1(center_y, center_x):
    # Set screen layout that will be drawn by curses
    # At this screen we choose figure for game and turn order.
    # Coordinate of point where cursor will moved at start of layout drawing.
    # Coordinate y counts from top of screen and coordinate x counts from left of screen
    name = 'Tic Tac Toe'
    help_message = 'Choose figure X or O."O" will move first. Use arrows up and down to move. [SPACE] choose. [Q] Quit.'
    delim = "-" * len(help_message)
    start_cursor_point = [center_y + 1, center_x]
    return [start_cursor_point, name, delim, help_message, delim, "X", "O"]

def set_screen_layout_2(center_y, center_x):
    # Set screen layout that will be drawn by curses
    # It is main game screen
    # start_cursor_point: coordinates of point where cursor will moved at start of layout drawing.
    # Coordinate y counts from top of screen and coordinate x counts from left of screen
    # step: y - is distance at vertical between board cells, x - is distance at gorizontal between board cells.
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
    start_cursor_point = [center_y, center_x - 4]
    step = [2, 4]
    return [step, start_cursor_point, name, delim, help_message, delim] + board.split("\n")

def print_screen_layout(screen_layout, stdscr, center_y, center_x):
    # draws screen layout at center
    y_offset = center_y - len(screen_layout) // 2
    for row in screen_layout:
        stdscr.addstr(y_offset, center_x - len(row) // 2, row)
        y_offset += 1
    return center_y + len(screen_layout) // 2

def get_center_coordinates(stdscr):
    # calculates coordinates of central point of screen
    # Coordinate y counts from top of screen and coordinate x counts from left of screen
    maxy, maxx = stdscr.getmaxyx()
    return maxy // 2, maxx // 2

def print_players(stdscr, figure, end_of_print_y, center_x, player_id=0):
    figure2 = "X" if figure == "O" else "0"
    stdscr.addstr(end_of_print_y + 1, center_x - 4, f'Player {figure}',
                  curses.A_BOLD if player_id == 0 else 0)
    stdscr.addstr(end_of_print_y + 2, center_x - 4, f'Player {figure2}',
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


def check_victory_or_draw(cells):
    if all([cells[i][j] for i in range(3) for j in range(3)]):
        return "draw"
    for i in range(3):
        if all(cells[i]):
            winner = cells[i][0]
            return winner
    for j in range(3):
        if all([cells[i][j] for i in range(3)]):
            winner = cells[0][j]
            return winner
    if all([cells[i][i] for i in range(3)]):
        winner = cells[1][1]
        return winner
    if all([cells[2 - i][i] for i in range(3)]):
        winner = cells[1][1]
        return winner
    return

def player_move(stdscr, cells, figure, start_y, start_x, step_y, step_x):
    y_pos = x_pos = 1
    while True:
        stdscr.move(start_y + y_pos * step_y, start_x + x_pos * step_x)
        ch_input = stdscr.getch()
        if ch_input == curses.KEY_UP:
            y_pos = max(0, y_pos - 1)
        elif ch_input == curses.KEY_DOWN:
            y_pos = min(2, y_pos + 1)
        elif ch_input == curses.KEY_LEFT:
            x_pos = max(0, x_pos - 1)
        elif ch_input == curses.KEY_RIGHT:
            x_pos = min(2, x_pos + 1)
        elif ch_input == ord('q') or c == ord('Q'):
            break
        elif ch_input == ord(' '):
            y, x = stdscr.getyx()
            if stdscr.inch(y, x) != ord(' '):
                continue
            stdscr.addch(y, x, figure)
            cells[x_pos][y_pos] = figure
            winner = check_victory_or_draw(cells)
            return winner


def game_round(stdscr, figure, center_y, center_x):
    stdscr.clear()
    screen_layout = set_screen_layout_2(center_y, center_x)
    [step_y, step_x] = screen_layout.pop(0)
    [start_y, start_x] = screen_layout.pop(0)
    end_of_print_y = print_screen_layout(screen_layout, stdscr, center_y, center_x)
    print_players(stdscr, figure, end_of_print_y, center_x)
    cells = [[[0]*3] for i in range(3)]
    winner = ""
    while winner:
        winner = player_move(stdscr, cells, figure, start_y, start_x, step_y, step_x)
        # Switch player
        player_id = (player_id + 1) % 2
        print_players(stdscr, figure, end_of_print_y, center_x, player_id)
        winner = computer_move(stdscr, cells, figure, start_y, start_x, step_y, step_x)
        player_id = (player_id + 1) % 2
        print_players(stdscr, figure, end_of_print_y, center_x, player_id)
    return True


def game_loop(stdscr):
    center_y, center_x = get_center_coordinates(stdscr)
    while True:
        figure = choose_figure(stdscr, center_y, center_x)
        if not figure:
            break
        is_break = game_round(stdscr, figure, center_y, center_x)
        if is_break:
            break


# curses.noecho()
# curses.cbreak()
# stdscr.keypad(True)

def main(stdscr):
    # Clear screen
    stdscr.clear()
    # center_y, center_x = get_center_coordinates(stdscr)
    # figure = choose_figure(stdscr, center_y, center_x)
    #screen_layout = set_screen_layout_2(center_y, center_x)
    #print_screen_layout(stdscr, screen_layout)
    stdscr.refresh()
    stdscr.clear()
    #print_screen_layout(message, stdscr, center_y, center_x)
    game_loop(stdscr)
    stdscr.getkey()


if __name__ == '__main__':
    stdscr = curses.initscr()
    curses.wrapper(main)