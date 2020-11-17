import curses

def set_screen_layout_1(center_y, center_x):
    # Set screen layout that will be drawn by curses
    # At this screen we choose figure for game and turn order.
    # Coordinate y counts from top of screen and coordinate x counts from left of screen
    name = 'Tic Tac Toe'
    help_message = 'Choose figure X or O. O will move first. Use arrows up and down to move. [SPACE] Choose. [Q] Quit.'
    delim = "-" * len(help_message)
    start_cursor_point = [center_y + 1, center_x] #Coordinate of point where cursor will moved at start of layout drawing.
    return [start_cursor_point, name, delim, help_message, delim, "X", "O"]

def set_screen_layout_2(center_y, center_x):
    # Set screen layout that will be drawn by curses
    # It is main game screen
    # Coordinate y counts from top of screen and coordinate x counts from left of screen
    name = 'Tic Tac Toe'
    help_message = 'Use arrows to move, [SPACE] Draw, [Q] Quit, [R] Restart.'
    delim = "-" * len(help_message)
    board = """
   │   │   
───┼───┼───
   │   │   
───┼───┼───
   │   │   
"""
    start_cursor_point = [center_y, center_x - 4] #coordinates of point where cursor will moved at start of layout drawing.
    step = [2, 4] # y - is distance at vertical between board cells, x - is distance at gorizontal between board cells.
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


def choose_figure(stdscr, center_y, center_x):
    screen_layout = set_screen_layout_1(center_y, center_x)
    [start_y, start_x] = screen_layout.pop(0)
    print_screen_layout(screen_layout, stdscr, center_y, center_x)
    y = x = 0
    while True:
        stdscr.move(start_y + y, start_x + x)
        ch_input = stdscr.getch()
        if ch_input == curses.KEY_UP: y = max(0, y - 1)
        elif ch_input == curses.KEY_DOWN: y = min(1, y + 1)
        elif ch_input == ord('q') or ch_input == ord('Q'): break
        elif ch_input == ord(' '):
            # stdscr.getyx() gets coordinats (y,x) of point where cursor was
            # stdscr.inch(y, x) gets ascii code of character at point with coordinats (y,x)
            # chr converts ascii code to string character
            return chr(stdscr.inch(*stdscr.getyx()))


def check_victory_or_draw(A):
    for i in range(3):
        if A[i][0] and A[i][0] == A[i][1] and A[i][1] == A[i][2]:
            return A[i][0]
    for j in range(3):
        if A[0][j] and A[0][j] == A[1][j] and A[1][j] == A[2][j]:
            return A[0][j]
    if A[0][0] and A[0][0] == A[1][1] and A[1][1] == A[2][2]:
        return A[1][1]
    if A[2][0] and A[2][0] == A[1][1] and A[1][1] == A[0][2]:
        return A[1][1]
    if all([A[i][j] for i in range(3) for j in range(3)]):
        return "draw"
    return


def free_cells(cells):
    return [[i,j] for i in range(3) for j in range(3) if cells[i][j] == 0]

def alphabeta(state, computer_figure, player_figure, alpha=-2, beta=2, computer_turn=True):
    result = check_victory_or_draw(state)
    if result:
        if result == computer_figure: score = 1
        elif result == "draw": score = 0
        else: score = -1
        return [None, score]
    if computer_turn:
        score = -2 #non-possible score. Win, draw, loss will change this
        for [i, j] in free_cells(state):
            state_copy = [state[i].copy() for i in range(3)]
            state_copy[i][j] = computer_figure if computer_turn else player_figure
            [_, score_max] = alphabeta(state_copy, computer_figure, player_figure, alpha, beta, False)
            if score_max > score:
                score = score_max
                best_move = [i, j]
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return [best_move, score]
    else:
        score = 2 #non-possible score. Win, draw, loss will change this
        for [i, j] in free_cells(state):
            state_copy = [state[i].copy() for i in range(3)]
            state_copy[i][j] = computer_figure if computer_turn else player_figure
            [_, score_min] = alphabeta(state_copy, computer_figure, player_figure, alpha, beta, True)
            if score_min < score:
                score = score_min
                best_move = [i, j]
            beta = min(beta, score)
            if beta <= alpha:
                break
        return [best_move, score]


def computer_move(stdscr, cells, computer_figure, player_figure, start_y, start_x, step_y, step_x):
    if len(free_cells(cells)) == 8 and cells[1][1] == 0: x, y = 1, 1
    else: [x, y] = (alphabeta(cells, computer_figure, player_figure, -2, 2, True))[0]
    cells[x][y] = computer_figure
    stdscr.addch(start_y + y * step_y, start_x + x * step_x, computer_figure)
    winner = check_victory_or_draw(cells)
    return False, False, winner, cells

def player_move(stdscr, cells, figure, start_y, start_x, step_y, step_x):
    y_pos = x_pos = 1
    while True:
        stdscr.move(start_y + y_pos * step_y, start_x + x_pos * step_x)
        ch_input = stdscr.getch()
        if ch_input == curses.KEY_UP: y_pos = max(0, y_pos - 1)
        elif ch_input == curses.KEY_DOWN: y_pos = min(2, y_pos + 1)
        elif ch_input == curses.KEY_LEFT: x_pos = max(0, x_pos - 1)
        elif ch_input == curses.KEY_RIGHT: x_pos = min(2, x_pos + 1)
        elif ch_input == ord('q') or ch_input == ord('Q'): return True, False, None, cells
        elif ch_input == ord('r') or ch_input == ord('R'): return False, True, None, cells
        elif ch_input == ord(' '):
            y, x = stdscr.getyx()
            if stdscr.inch(y, x) != ord(' '):
                continue
            stdscr.addch(y, x, figure)
            cells[x_pos][y_pos] = figure
            winner = check_victory_or_draw(cells)
            return False, False, winner, cells


def print_players(stdscr, player_figure, computer_figure, end_of_print_y, center_x, computer_turn):
    stdscr.addstr(end_of_print_y + 1, center_x - 4, f'Player {player_figure}',
                  curses.A_BOLD if not computer_turn else 0)
    stdscr.addstr(end_of_print_y + 2, center_x - 4, f'Player {computer_figure}',
                  curses.A_BOLD if computer_turn else 0)


def win_action(stdscr, end_of_print_y, center_x, winner, computer_turn):
    if winner == "draw":
        stdscr.addstr(end_of_print_y + 3, center_x - 2, f'DRAW!')
    else:
        win = "COMPUTER" if computer_turn else "PLAYER"
        stdscr.addstr(end_of_print_y + 3, center_x - 8, f'{win} IS WIN!')
    while True:
        ch_input = stdscr.getch()
        if ch_input == ord('q') or ch_input == ord('Q'): return True, False
        elif ch_input == ord('r') or ch_input == ord('R'): return False, True


def game_round(stdscr, player_figure, center_y, center_x):
    stdscr.clear()
    screen_layout = set_screen_layout_2(center_y, center_x)
    [step_y, step_x] = screen_layout.pop(0)
    [start_y, start_x] = screen_layout.pop(0)
    end_of_print_y = print_screen_layout(screen_layout, stdscr, center_y, center_x)
    cells = [[0]*3 for i in range(3)]
    computer_figure = "O" if player_figure != "O" else "X"
    if computer_figure == "O":
        cells[1][1] = computer_figure
        stdscr.addch(start_y + 1 * step_y, start_x + 1 * step_x, computer_figure)
    print_players(stdscr, player_figure, computer_figure, end_of_print_y, center_x, False)
    while True:
        is_break, is_restart, winner, cells = player_move(stdscr, cells, player_figure, start_y, start_x, step_y, step_x)
        if is_break or is_restart: return is_break, is_restart
        if winner: return win_action(stdscr, end_of_print_y, center_x, winner, False)
        print_players(stdscr, player_figure, computer_figure, end_of_print_y, center_x, True)
        is_break, is_restart, winner, cells = computer_move(stdscr, cells, computer_figure, player_figure, start_y, start_x, step_y, step_x)
        if is_break or is_restart: return is_break, is_restart
        if winner: return win_action(stdscr, end_of_print_y, center_x, winner, True)
        print_players(stdscr, player_figure, computer_figure, end_of_print_y, center_x, False)


def game_loop(stdscr):
    center_y, center_x = get_center_coordinates(stdscr)
    is_break, is_restart = False, True
    while not is_break and is_restart:
        stdscr.clear()
        player_figure = choose_figure(stdscr, center_y, center_x)
        if not player_figure: break
        stdscr.refresh()
        is_break, is_restart = game_round(stdscr, player_figure, center_y, center_x)


def main():
    stdscr = curses.initscr()
    stdscr.clear()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    game_loop(stdscr)
    curses.endwin()


if __name__ == '__main__':
    main()
    #curses.wrapper(main())