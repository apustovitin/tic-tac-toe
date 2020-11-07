import curses


CH_P1 = 'X'
CH_P2 = 'O'
X_STEP = 4
Y_STEP = 2
X_OFFSET = 1
Y_OFFSET = 4


def set_game_screen():
    name = 'Tic Tac Toe'
    delim = "-" * 50
    help_message = 'Use arrows to move,  [SPACE] Draw,  [Q] Quit'
    game_screen = """
       │   │   
    ───┼───┼───
       │   │   
    ───┼───┼───
       │   │   
    """
    return name + "\n" + delim + "\n" + help_message + game_screen


def calculate_string_offset(string):
    return


def print_board(stdscr):
    rows, cols = stdscr.getmaxyx()
    stdscr.addstr(0, 0, 'Tic Tac Toe')
    stdscr.hline(1, 0, '-', 50)
    stdscr.addstr(2, 0, 'Use arrows to move,  [SPACE] Draw,  [Q] Quit')
    stdscr.addstr(Y_OFFSET    , X_OFFSET, '   │   │   ')
    stdscr.addstr(Y_OFFSET + 1, X_OFFSET, '───┼───┼───')
    stdscr.addstr(Y_OFFSET + 2, X_OFFSET, '   │   │   ')
    stdscr.addstr(Y_OFFSET + 3, X_OFFSET, '───┼───┼───')
    stdscr.addstr(Y_OFFSET + 4, X_OFFSET, '   │   │   ')


def print_players(stdscr, player_id):
    stdscr.addstr(Y_OFFSET + 6, 0, 'Player {}'.format(CH_P1),
                  curses.A_BOLD if player_id == 0 else 0)
    stdscr.addstr(Y_OFFSET + 7, 0, 'Player {}'.format(CH_P2),
                  curses.A_BOLD if player_id == 1 else 0)




def draw(y, x, stdscr, player_id):
    stdscr.addch(y, x, CH_P2 if player_id else CH_P1)


def check_victory(board, y, x):
    #check if previous move caused a win on horizontal line
    if board[0][x] == board[1][x] == board [2][x]:
        return True

    #check if previous move caused a win on vertical line
    if board[y][0] == board[y][1] == board [y][2]:
        return True

    #check if previous move was on the main diagonal and caused a win
    if x == y and board[0][0] == board[1][1] == board [2][2]:
        return True

    #check if previous move was on the secondary diagonal and caused a win
    if x + y == 2 and board[0][2] == board[1][1] == board [2][0]:
        return True

    return False


def main(stdscr):
    # Clear screen
    # stdscr.clear()

    print_board(stdscr)
    player_id = 0
    print_players(stdscr, player_id=player_id)

    x_pos = 1
    y_pos = 1
    board = [list('   ') for _ in range(3)]

    # This raises ZeroDivisionError when i == 10.
    while True:
        stdscr.move(Y_OFFSET + y_pos * Y_STEP, X_OFFSET + x_pos * X_STEP)

        c = stdscr.getch()
        if c == curses.KEY_UP:
            y_pos = max(0, y_pos - 1)
        elif c == curses.KEY_DOWN:
            y_pos = min(2, y_pos + 1)
        elif c == curses.KEY_LEFT:
            x_pos = max(0, x_pos - 1)
        elif c == curses.KEY_RIGHT:
            x_pos = min(2, x_pos + 1)
        elif c == ord('q') or c == ord('Q'):
            break
        elif c == ord(' '):
            # Update
            y, x = stdscr.getyx()
            if stdscr.inch(y, x) != ord(' '):
                continue

            draw(y, x, stdscr, player_id)
            board[y_pos][x_pos] = CH_P2 if player_id else CH_P1

            if check_victory(board, y_pos, x_pos):
                stdscr.addstr(Y_OFFSET + 9, 0, 'Player {} wins'.format(
                    CH_P2 if player_id else CH_P1))
                break

            # Switch player
            player_id = (player_id + 1) % 2
            print_players(stdscr, player_id)


    stdscr.refresh()
    stdscr.getkey()


if __name__ == '__main__':
    curses.wrapper(main)
