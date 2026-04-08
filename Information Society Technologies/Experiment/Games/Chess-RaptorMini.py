import os
import sys
from copy import deepcopy

def fatal_error(msg):
    print(msg)
    sys.exit(1)

try:
    import pygame
except ImportError:
    fatal_error('Error: pygame is not installed in the Python environment.\nTo install: pip install pygame')

# Chess-RaptorMini.py
# Implemented according to GDD specs (setup, visuals, rules, course of game)

# Constants
WINDOW_W = 896
WINDOW_H = 576
PANEL_W = 256
PANEL_H = 512
MARGIN = 32
PANEL_GAP = 64
BOARD_SIZE = 512
SQUARE = 64
BOARD_X = MARGIN + PANEL_W + PANEL_GAP
BOARD_Y = MARGIN
FPS = 60

WHITE = (245, 235, 215)
BROWN = (166, 128, 95)
DARK_BROWN = (108, 65, 46)
UI_BG = (35, 38, 52)
TEXT_C = (255, 255, 255)
HIGHLIGHT = (255, 215, 0)
CHECK_RED = (200, 40, 40)
MOVE_CIRCLE = (255, 255, 0)
PAUSE_GRAY = (70, 70, 70)
BUTTON_BG = (60, 95, 180)
BUTTON_HOVER = (90, 130, 220)

PIECE_IMAGE_FILES = {
    'K': 'Pieces/WhiteKing.png',
    'Q': 'Pieces/WhiteQueen.png',
    'R': 'Pieces/WhiteRook.png',
    'B': 'Pieces/WhiteBishop.png',
    'N': 'Pieces/WhiteKnight.png',
    'P': 'Pieces/WhitePawn.png',
    'k': 'Pieces/BlackKing.png',
    'q': 'Pieces/BlackQueen.png',
    'r': 'Pieces/BlackRook.png',
    'b': 'Pieces/BlackBishop.png',
    'n': 'Pieces/BlackKnight.png',
    'p': 'Pieces/BlackPawn.png',
}

# Piece direction vectors
ROOK_DIRS = [(1,0),(-1,0),(0,1),(0,-1)]
BISHOP_DIRS = [(1,1),(1,-1),(-1,1),(-1,-1)]
QUEEN_DIRS = ROOK_DIRS + BISHOP_DIRS
KNIGHT_OFFSETS = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(-1,2),(1,-2),(-1,-2)]

# Global game state
board = None
selected = None
legal_moves = []
current_player = 'white'
move_number = 1
game_over = False
game_result = ''
status_message = ''
paused = False
draw_offer = None
promotion_pending = False
promotion_pos = None
repetition_counts = {}
fifty_move_clock = 0
en_passant_target = None
halfmove_clock = 0
history = []
last_move = None
moved_flags = {}

WHITE_TIME = 10 * 60
BLACK_TIME = 10 * 60
white_time = WHITE_TIME
black_time = BLACK_TIME
clock_running = False
last_clock_tick = 0
clock_started = False

# Initialize pygame and screen
pygame.init()
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption('Chess - Raptor mini')
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 18)
small_font = pygame.font.SysFont('Arial', 14)
large_font = pygame.font.SysFont('Arial', 26, bold=True)

# Load piece images
piece_images = {}
base_path = os.path.dirname(os.path.abspath(__file__))
for key, rel in PIECE_IMAGE_FILES.items():
    path = os.path.normpath(os.path.join(base_path, '..', rel))
    if not os.path.exists(path):
        fatal_error(f'Missing piece image: {path}')
    try:
        img = pygame.image.load(path).convert_alpha()
    except Exception as e:
        fatal_error(f'Failed to load image {path}: {e}')
    piece_images[key] = pygame.transform.smoothscale(img, (SQUARE, SQUARE))

# Buttons
buttons = {}

# UI layout constants for professional spacing
UI_LABEL_GAP = 8
UI_BUTTON_H = 24
UI_BUTTON_W = 94
UI_BUTTON_X_LEFT = MARGIN + 16
UI_BUTTON_X_RIGHT = MARGIN + PANEL_W - UI_BUTTON_X_LEFT - UI_BUTTON_W
UI_TURN_Y = MARGIN + 8
UI_SECTIONS_TOP = MARGIN + 44
UI_SECTION_HEIGHT = 108
UI_TIMER_OFFSET = 22
UI_BUTTON_Y_OFFSET = 52


def make_button(name, rect, text):
    buttons[name] = {'rect': pygame.Rect(rect), 'text': text}


def setup_buttons():
    buttons.clear()
    black_top = UI_SECTIONS_TOP
    general_top = UI_SECTIONS_TOP + UI_SECTION_HEIGHT
    white_top = general_top + UI_SECTION_HEIGHT

    black_buttons_y = black_top + UI_BUTTON_Y_OFFSET
    general_buttons_y = general_top + UI_BUTTON_Y_OFFSET
    white_buttons_y = white_top + UI_BUTTON_Y_OFFSET

    make_button('black_draw', (UI_BUTTON_X_LEFT, black_buttons_y, UI_BUTTON_W, UI_BUTTON_H), 'Draw')
    make_button('black_resign', (UI_BUTTON_X_RIGHT, black_buttons_y, UI_BUTTON_W, UI_BUTTON_H), 'Resign')
    make_button('pause', (UI_BUTTON_X_LEFT, general_buttons_y, UI_BUTTON_W, UI_BUTTON_H), 'Pause')
    make_button('reset', (UI_BUTTON_X_RIGHT, general_buttons_y, UI_BUTTON_W, UI_BUTTON_H), 'Reset')
    make_button('white_draw', (UI_BUTTON_X_LEFT, white_buttons_y, UI_BUTTON_W, UI_BUTTON_H), 'Draw')
    make_button('white_resign', (UI_BUTTON_X_RIGHT, white_buttons_y, UI_BUTTON_W, UI_BUTTON_H), 'Resign')


setup_buttons()

# Helpers

def in_bounds(r, c):
    return 0 <= r < 8 and 0 <= c < 8


def is_white(piece):
    return piece is not None and piece.isupper()


def is_black(piece):
    return piece is not None and piece.islower()


def opponent(color):
    return 'black' if color == 'white' else 'white'


def piece_color(piece):
    if piece is None:
        return None
    return 'white' if piece.isupper() else 'black'


def board_to_fen(bd):
    fen = []
    for r in range(8):
        count = 0
        row = ''
        for c in range(8):
            p = bd[r][c]
            if p is None:
                count += 1
            else:
                if count:
                    row += str(count)
                    count = 0
                row += p
        if count:
            row += str(count)
        fen.append(row)
    return '/'.join(fen)


def init_board():
    global board, current_player, move_number, game_over, game_result, status_message
    global paused, draw_offer, promotion_pending, promotion_pos, repetition_counts
    global fifty_move_clock, en_passant_target, halfmove_clock, history, last_move, moved_flags
    global white_time, black_time, clock_running, last_clock_tick, clock_started

    setup_buttons()

    board = [[None for _ in range(8)] for _ in range(8)]
    moved_flags = {
        'white_king': False,
        'white_rook_a': False,
        'white_rook_h': False,
        'black_king': False,
        'black_rook_a': False,
        'black_rook_h': False,
    }
    # White back rank
    board[7] = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    board[6] = ['P'] * 8
    # Black back rank
    board[0] = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
    board[1] = ['p'] * 8
    board[2] = [None] * 8
    board[3] = [None] * 8
    board[4] = [None] * 8
    board[5] = [None] * 8

    current_player = 'white'
    move_number = 1
    selected = None
    legal_moves.clear()
    game_over = False
    game_result = ''
    status_message = 'Game started. White moves.'
    paused = False
    draw_offer = None
    promotion_pending = False
    promotion_pos = None
    repetition_counts = {}
    fifty_move_clock = 0
    en_passant_target = None
    halfmove_clock = 0
    history = []
    last_move = None
    white_time = WHITE_TIME
    black_time = BLACK_TIME
    clock_running = False
    last_clock_tick = pygame.time.get_ticks()
    clock_started = False

    fen = board_to_fen(board)
    repetition_counts[fen] = 1


def in_check(color, bd=None):
    if bd is None:
        bd = board
    king_chr = 'K' if color == 'white' else 'k'
    king_pos = None
    for r in range(8):
        for c in range(8):
            if bd[r][c] == king_chr:
                king_pos = (r,c)
                break
        if king_pos:
            break
    if not king_pos:
        return True

    kr, kc = king_pos

    def attacked_by(piece, pr, pc):
        if piece is None:
            return False
        pcolor = piece_color(piece)
        if pcolor == color:
            return False
        p = piece.lower()
        dr = kr - pr
        dc = kc - pc

        if p == 'p':
            direction = -1 if pcolor == 'white' else 1
            return (pr + direction == kr) and (abs(pc-kc) == 1)

        if p == 'n':
            return (abs(dr), abs(dc)) in [(1,2),(2,1)]

        if p in ['r','q']:
            if pr == kr:
                step = 1 if kc > pc else -1
                for x in range(pc+step, kc, step):
                    if bd[pr][x] is not None:
                        return False
                return True
            if pc == kc:
                step = 1 if kr > pr else -1
                for y in range(pr+step, kr, step):
                    if bd[y][pc] is not None:
                        return False
                return True

        if p in ['b','q']:
            if abs(kr-pr) == abs(kc-pc):
                step_r = 1 if kr>pr else -1
                step_c = 1 if kc>pc else -1
                r, c = pr+step_r, pc+step_c
                while (r,c) != (kr,kc):
                    if bd[r][c] is not None:
                        return False
                    r += step_r
                    c += step_c
                return True

        if p == 'k':
            return max(abs(dr), abs(dc)) == 1

        return False

    for r in range(8):
        for c in range(8):
            if attacked_by(bd[r][c], r, c):
                return True
    return False


def generate_moves(r, c, bd=None, en_passant=None):
    if bd is None:
        bd = board
    p = bd[r][c]
    if p is None:
        return []
    color = piece_color(p)
    moves = []

    if p.lower() == 'p':
        direction = -1 if color == 'white' else 1
        start_rank = 6 if color == 'white' else 1
        one_step = (r + direction, c)
        if in_bounds(*one_step) and bd[one_step[0]][one_step[1]] is None:
            moves.append(one_step)
            if r == start_rank:
                two_step = (r + 2*direction, c)
                if bd[two_step[0]][two_step[1]] is None:
                    moves.append(two_step)
        for dc in (-1, 1):
            cap = (r + direction, c + dc)
            if in_bounds(*cap):
                target = bd[cap[0]][cap[1]]
                if target is not None and piece_color(target) != color:
                    moves.append(cap)
                elif en_passant is not None and cap == en_passant:
                    moves.append(cap)

    elif p.lower() == 'n':
        for dr, dc in KNIGHT_OFFSETS:
            nr, nc = r + dr, c + dc
            if in_bounds(nr, nc):
                t = bd[nr][nc]
                if t is None or piece_color(t) != color:
                    moves.append((nr,nc))

    elif p.lower() == 'b':
        for dr, dc in BISHOP_DIRS:
            nr, nc = r+dr, c+dc
            while in_bounds(nr,nc):
                t = bd[nr][nc]
                if t is None:
                    moves.append((nr,nc))
                else:
                    if piece_color(t) != color:
                        moves.append((nr,nc))
                    break
                nr += dr
                nc += dc

    elif p.lower() == 'r':
        for dr, dc in ROOK_DIRS:
            nr, nc = r+dr, c+dc
            while in_bounds(nr,nc):
                t = bd[nr][nc]
                if t is None:
                    moves.append((nr,nc))
                else:
                    if piece_color(t) != color:
                        moves.append((nr,nc))
                    break
                nr += dr
                nc += dc

    elif p.lower() == 'q':
        for dr, dc in QUEEN_DIRS:
            nr, nc = r+dr, c+dc
            while in_bounds(nr,nc):
                t = bd[nr][nc]
                if t is None:
                    moves.append((nr,nc))
                else:
                    if piece_color(t) != color:
                        moves.append((nr,nc))
                    break
                nr += dr
                nc += dc

    elif p.lower() == 'k':
        for dr in (-1,0,1):
            for dc in (-1,0,1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r+dr, c+dc
                if in_bounds(nr, nc):
                    t = bd[nr][nc]
                    if t is None or piece_color(t) != color:
                        moves.append((nr,nc))
        # Castling
        king_flag = f"{color}_king"
        if not moved_flags.get(king_flag, True):
            row = 7 if color == 'white' else 0
            # kingside
            rook = bd[row][7]
            rook_flag = f"{color}_rook_h"
            if rook is not None and rook.lower() == 'r' and not moved_flags.get(rook_flag, True):
                if bd[row][5] is None and bd[row][6] is None:
                    if not in_check(color, bd) and not square_under_attack(row,5,color,bd) and not square_under_attack(row,6,color,bd):
                        moves.append((row,6))
            # queenside
            rook = bd[row][0]
            rook_flag = f"{color}_rook_a"
            if rook is not None and rook.lower() == 'r' and not moved_flags.get(rook_flag, True):
                if bd[row][1] is None and bd[row][2] is None and bd[row][3] is None:
                    if not in_check(color, bd) and not square_under_attack(row,3,color,bd) and not square_under_attack(row,2,color,bd):
                        moves.append((row,2))

    return moves

# Because we don't store per-piece moved state except in external map, let's use a simple map
piece_moved = {}

def getattr_pv(piece, attr, default=None):
    return default


def square_under_attack(r, c, color, bd=None):
    if bd is None:
        bd = board
    # Temporarily place king there, test from opponent
    temp_king = 'K' if color=='white' else 'k'
    saved = bd[r][c]
    bd[r][c] = temp_king
    result = in_check(color, bd)
    bd[r][c] = saved
    return result


def legal_moves_for(r, c):
    moves = generate_moves(r,c,bd=board,en_passant=en_passant_target)
    legal = []
    for nr,nc in moves:
        new_board = deepcopy(board)
        p = new_board[r][c]
        target = new_board[nr][nc]
        if p.lower() == 'p' and en_passant_target == (nr,nc) and target is None and c != nc:
            # en passant capture
            if current_player == 'white':
                new_board[nr+1][nc] = None
            else:
                new_board[nr-1][nc] = None
        new_board[nr][nc] = p
        new_board[r][c] = None
        # castling rook move
        if p.lower() == 'k' and abs(nc - c) == 2:
            if nc > c:  # king side
                new_board[r][5] = new_board[r][7]
                new_board[r][7] = None
            else:
                new_board[r][3] = new_board[r][0]
                new_board[r][0] = None
        if not in_check(current_player, new_board):
            legal.append((nr,nc))
    return legal


def update_legal_moves():
    global legal_moves
    legal_moves = []
    if selected is None:
        return
    r,c = selected
    if board[r][c] is None or piece_color(board[r][c]) != current_player:
        return
    legal_moves = legal_moves_for(r,c)


def apply_move(src, dst):
    global board, selected, legal_moves, current_player, move_number, last_move, en_passant_target, fifty_move_clock, halfmove_clock
    global repetition_counts, game_over, game_result, status_message, clock_running, clock_started, moved_flags
    global white_time, black_time, promotion_pending, promotion_pos

    sr, sc = src
    dr, dc = dst
    piece = board[sr][sc]
    target = board[dr][dc]
    moved_piece = piece
    captured = target
    ep_capture = False
    castle_type = None
    promotion_piece = None

    # En passant capture
    if piece.lower() == 'p' and en_passant_target == (dr,dc) and target is None and sc != dc:
        ep_capture = True
        if current_player == 'white':
            captured = board[dr+1][dc]
            board[dr+1][dc] = None
        else:
            captured = board[dr-1][dc]
            board[dr-1][dc] = None

    # Castling rook move handled after king move
    # Move
    board[dr][dc] = piece
    board[sr][sc] = None

    # Castling
    if piece.lower() == 'k' and abs(dc-sc) == 2:
        if dc > sc:
            board[dr][5] = board[dr][7]
            board[dr][7] = None
            castle_type = 'king'
        else:
            board[dr][3] = board[dr][0]
            board[dr][0] = None
            castle_type = 'queen'

    # Update moved flags for king/rook
    if piece.lower() == 'k':
        moved_flags[f"{current_player}_king"] = True
        if castle_type == 'king':
            moved_flags[f"{current_player}_rook_h"] = True
        elif castle_type == 'queen':
            moved_flags[f"{current_player}_rook_a"] = True
    if piece.lower() == 'r':
        if (sr, sc) == (7, 0):
            moved_flags['white_rook_a'] = True
        elif (sr, sc) == (7, 7):
            moved_flags['white_rook_h'] = True
        elif (sr, sc) == (0, 0):
            moved_flags['black_rook_a'] = True
        elif (sr, sc) == (0, 7):
            moved_flags['black_rook_h'] = True

    # Promotion test
    if piece.lower() == 'p' and (dr == 0 or dr == 7):
        promotion_pending = True
        promotion_pos = (dr, dc)
        selected = None
        legal_moves = []
        # update fifty move and halfmove for pawn move
        fifty_move_clock = 0
        halfmove_clock += 1
        # bonus time now for move
        if current_player == 'white':
            white_time += 2
        else:
            black_time += 2
        # preserve move so promotion can happen later
        history.append({'src':src, 'dst':dst, 'piece':piece, 'captured':captured, 'ep':ep_capture, 'castle':castle_type, 'promo':None})
        last_move = (src, dst)
        status_message = f"{current_player.capitalize()} promotion pending"
        return

    # Update en passant target
    if piece.lower() == 'p' and abs(dr-sr) == 2:
        en_passant_target = ((sr+dr)//2, sc)
    else:
        en_passant_target = None

    # Update halfmove/50 move
    if piece.lower() == 'p' or captured is not None:
        fifty_move_clock = 0
    else:
        fifty_move_clock += 1
    halfmove_clock += 1

    # update repetition
    fen = board_to_fen(board)
    repetition_counts[fen] = repetition_counts.get(fen,0) + 1

    last_move = (src, dst)
    history.append({'src':src, 'dst':dst, 'piece':piece, 'captured':captured, 'ep':ep_capture, 'castle':castle_type, 'promo':None})

    # add time increment to player who just moved
    if current_player == 'white':
        white_time += 2
    else:
        black_time += 2

    # switch player
    if current_player == 'white':
        current_player = 'black'
    else:
        current_player = 'white'
        move_number += 1

    # set status
    status_message = f"{current_player.capitalize()} to move."

    # Start timer after first move
    if not clock_started:
        clock_started = True
        clock_running = True

    # check endpoints
    if not any(get_legal_moves_for_any_piece()):
        if in_check(current_player):
            game_over = True
            winner = opponent(current_player)
            game_result = f'{winner.capitalize()} wins by checkmate'
        else:
            game_over = True
            game_result = 'Draw by stalemate'
        status_message = game_result

    if repetition_counts.get(fen, 0) >= 3 and not game_over:
        game_over = True
        game_result = 'Draw by threefold repetition'
        status_message = game_result

    if fifty_move_clock >= 100 and not game_over:
        game_over = True
        game_result = 'Draw by fifty-move rule'
        status_message = game_result



def promote_pawn(new_type):
    global board, promotion_pending, promotion_pos, current_player, en_passant_target
    global move_number, last_move, repetition_counts, fifty_move_clock, halfmove_clock
    global draw_offer, game_over, game_result, status_message
    global selected, legal_moves

    if not promotion_pending or promotion_pos is None:
        return
    dr, dc = promotion_pos
    piece = board[dr][dc]
    pcolor = piece_color(piece)
    if pcolor == 'white':
        board[dr][dc] = new_type.upper()
    else:
        board[dr][dc] = new_type.lower()

    promotion_pending = False
    promotion_pos = None
    selected = None
    legal_moves = []

    # promotion is a move completion, switch player
    if current_player == 'white':
        current_player = 'black'
        prev_color = 'White'
    else:
        current_player = 'white'
        prev_color = 'Black'
        move_number += 1

    # update fifty move and repetition
    fifty_move_clock = 0
    fen = board_to_fen(board)
    repetition_counts[fen] = repetition_counts.get(fen,0) + 1

    last_move_in_history = history[-1] if history else None
    if last_move_in_history:
        last_move_in_history['promo'] = new_type

    status_message = f"{prev_color} promoted to {new_type.upper()}. {current_player.capitalize()} to move."

    if not any(get_legal_moves_for_any_piece()):
        if in_check(current_player):
            game_over = True
            winner = opponent(current_player)
            game_result = f'{winner.capitalize()} wins by checkmate'
        else:
            game_over = True
            game_result = 'Draw by stalemate'
        status_message = game_result


def get_legal_moves_for_any_piece():
    moves = []
    for r in range(8):
        for c in range(8):
            if board[r][c] is not None and piece_color(board[r][c]) == current_player:
                pls = legal_moves_for(r,c)
                if pls:
                    return pls
    return []


def get_promotion_option_rects():
    options = [('Q','Queen'),('R','Rook'),('B','Bishop'),('N','Knight')]
    size = 56
    spacing = 12
    panel_w = 320
    panel_h = 132
    panel_x = BOARD_X + (BOARD_SIZE-panel_w)//2
    panel_y = BOARD_Y + (BOARD_SIZE-panel_h)//2 - 12
    total_w = len(options)*size + (len(options)-1)*spacing
    start_x = panel_x + (panel_w-total_w)//2
    y = panel_y + panel_h - size - 18
    rects = []
    for i, (code, name) in enumerate(options):
        rect = pygame.Rect(start_x + i*(size + spacing), y, size, size)
        rects.append((rect, code, name))
    return rects


def to_time_str(sec):
    if sec < 0: sec = 0
    m = int(sec)//60
    s = int(sec)%60
    return f'{m:02}:{s:02}'


def draw_ui_panel():
    pygame.draw.rect(screen, UI_BG, (MARGIN, MARGIN, PANEL_W, PANEL_H))
    pygame.draw.rect(screen, (100,100,100), (MARGIN, MARGIN, PANEL_W, PANEL_H), 2)

    # Shared section grid - all labels, timers, separators and buttons align to this.
    black_top = UI_SECTIONS_TOP
    general_top = UI_SECTIONS_TOP + UI_SECTION_HEIGHT
    white_top = general_top + UI_SECTION_HEIGHT

    # Turn header
    screen.blit(large_font.render(f"Turn: {move_number} ({current_player.capitalize()})", True, TEXT_C), (MARGIN + 12, UI_TURN_Y))

    # Black section
    screen.blit(font.render('Black', True, TEXT_C), (MARGIN + 12, black_top))
    screen.blit(font.render('Timer: ' + to_time_str(black_time), True, TEXT_C), (MARGIN + 12, black_top + UI_TIMER_OFFSET))

    # General section
    pygame.draw.line(screen, (170,170,170), (MARGIN + 8, general_top - 12), (MARGIN + PANEL_W - 8, general_top - 12), 2)
    screen.blit(font.render('General', True, TEXT_C), (MARGIN + 12, general_top))

    # White section
    pygame.draw.line(screen, (170,170,170), (MARGIN + 8, white_top - 12), (MARGIN + PANEL_W - 8, white_top - 12), 2)
    screen.blit(font.render('White', True, TEXT_C), (MARGIN + 12, white_top))
    screen.blit(font.render('Timer: ' + to_time_str(white_time), True, TEXT_C), (MARGIN + 12, white_top + UI_TIMER_OFFSET))

    # Control buttons rendering (pre-positioned from setup_buttons)
    for key in ['black_draw', 'black_resign', 'pause', 'reset', 'white_draw', 'white_resign']:
        b = buttons[key]
        rect = b['rect']
        if key == 'reset':
            enabled = True
        elif key == 'pause':
            enabled = (not game_over) and draw_offer is None and (not promotion_pending)
        elif key == 'black_draw':
            enabled = (not game_over) and draw_offer is None and current_player == 'black'
        elif key == 'white_draw':
            enabled = (not game_over) and draw_offer is None and current_player == 'white'
        else:
            enabled = (not game_over) and draw_offer is None
        mx, my = pygame.mouse.get_pos()
        is_over = rect.collidepoint(mx, my)
        color = BUTTON_HOVER if is_over and enabled else (BUTTON_BG if enabled else PAUSE_GRAY)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (255,255,255), rect, 1)
        txt = small_font.render(b['text'], True, TEXT_C)
        screen.blit(txt, (rect.x + (rect.width - txt.get_width()) // 2, rect.y + (rect.height - txt.get_height()) // 2))

    # Footer (bottom fixed)
    footer_start = MARGIN + PANEL_H - 80
    screen.blit(small_font.render('Model: Raptor mini', True, TEXT_C), (MARGIN + 12, footer_start))
    screen.blit(small_font.render('Prompts/tokens: 20+ / 12 000 000+', True, TEXT_C), (MARGIN + 12, footer_start + 18))
    screen.blit(small_font.render('EXPERIMENT FAILED', True, TEXT_C), (MARGIN + 12, footer_start + 36))
    screen.blit(small_font.render('@adbreeker 2026', True, TEXT_C), (MARGIN + 12, footer_start + 54))




def draw_board():
    for r in range(8):
        for c in range(8):
            sq_color = WHITE if (r+c)%2==0 else BROWN
            pygame.draw.rect(screen, sq_color, (BOARD_X + c*SQUARE, BOARD_Y + r*SQUARE, SQUARE, SQUARE))

    # last move highlight
    if last_move is not None:
        (sr,sc), (dr,dc) = last_move
        pygame.draw.rect(screen, (255,255,150,100), (BOARD_X + sc*SQUARE, BOARD_Y + sr*SQUARE, SQUARE, SQUARE), 4)
        pygame.draw.rect(screen, (255,255,150,100), (BOARD_X + dc*SQUARE, BOARD_Y + dr*SQUARE, SQUARE, SQUARE), 4)

    # check highlight
    if in_check(current_player):
        king = 'K' if current_player=='white' else 'k'
        for r in range(8):
            for c in range(8):
                if board[r][c] == king:
                    pygame.draw.rect(screen, CHECK_RED, (BOARD_X + c*SQUARE, BOARD_Y + r*SQUARE, SQUARE, SQUARE), 4)
                    break

    # pieces
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p is not None:
                screen.blit(piece_images[p], (BOARD_X + c*SQUARE, BOARD_Y + r*SQUARE))

    # possible moves (draw on top of pieces)
    for (r,c) in legal_moves:
        cx = BOARD_X + c*SQUARE + SQUARE//2
        cy = BOARD_Y + r*SQUARE + SQUARE//2
        pygame.draw.circle(screen, MOVE_CIRCLE, (cx,cy), 8)

    # Draw proposal in center board if active
    if draw_offer and draw_offer.get('state') == 'proposed':
        mid_x = BOARD_X + BOARD_SIZE//2
        mid_y = BOARD_Y + BOARD_SIZE//2
        w, h = 320, 120
        rect = pygame.Rect(mid_x - w//2, mid_y - h//2, w, h)
        pygame.draw.rect(screen, (40,40,40), rect)
        pygame.draw.rect(screen, (255,255,255), rect, 2)
        text = large_font.render(f"{draw_offer['by'].capitalize()} offers draw", True, TEXT_C)
        screen.blit(text, (rect.x + (w - text.get_width())//2, rect.y + 14))
        yes_rect = pygame.Rect(rect.x + 30, rect.y + 50, 110, 32)
        no_rect = pygame.Rect(rect.x + w - 140, rect.y + 50, 110, 32)
        pygame.draw.rect(screen, BUTTON_BG, yes_rect)
        pygame.draw.rect(screen, BUTTON_BG, no_rect)
        pygame.draw.rect(screen, (255,255,255), yes_rect, 2)
        pygame.draw.rect(screen, (255,255,255), no_rect, 2)
        screen.blit(small_font.render('Accept', True, TEXT_C), (yes_rect.x + 20, yes_rect.y + 8))
        screen.blit(small_font.render('Refuse', True, TEXT_C), (no_rect.x + 20, no_rect.y + 8))
        draw_offer['yes_rect'] = yes_rect
        draw_offer['no_rect'] = no_rect

    # selected square border
    if selected is not None:
        r,c = selected
        pygame.draw.rect(screen, HIGHLIGHT, (BOARD_X + c*SQUARE, BOARD_Y + r*SQUARE, SQUARE, SQUARE), 3)


def handle_promotion_mouse(pos):
    global promotion_pending
    if not promotion_pending or promotion_pos is None:
        return
    px,py = pos
    for rect, code, name in get_promotion_option_rects():
        if rect.collidepoint(px,py):
            promote_pawn(code)
            return


def draw_promotion_panel():
    if not promotion_pending or promotion_pos is None:
        return
    panel_w = 340
    panel_h = 142
    panel_rect = pygame.Rect(BOARD_X + (BOARD_SIZE-panel_w)//2, BOARD_Y + (BOARD_SIZE-panel_h)//2 - 8, panel_w, panel_h)
    pygame.draw.rect(screen, (20,20,20), panel_rect)
    pygame.draw.rect(screen, (255,255,255), panel_rect, 2)

    txt = large_font.render('Promotion: choose piece', True, TEXT_C)
    screen.blit(txt, (panel_rect.x + (panel_w-txt.get_width())//2, panel_rect.y + 10))

    for rect, code, name in get_promotion_option_rects():
        pygame.draw.rect(screen, BUTTON_BG, rect)
        pygame.draw.rect(screen, TEXT_C, rect, 1)
        label = small_font.render(name, True, TEXT_C)
        screen.blit(label, (rect.x + (rect.width-label.get_width())//2, rect.y + (rect.height-label.get_height())//2))


def click_button(pos):
    global paused, game_over, game_result, draw_offer, status_message
    x,y = pos
    for key,b in buttons.items():
        if b['rect'].collidepoint(x,y):
            if key == 'pause':
                if not game_over and draw_offer is None and not promotion_pending:
                    paused = not paused
                    status_message = ('Paused' if paused else f'{current_player.capitalize()} to move')
            elif key == 'reset':
                init_board()
            elif key == 'black_draw':
                if current_player == 'black' and not game_over and not draw_offer:
                    draw_offer = {'by':'black', 'state':'proposed'}
            elif key == 'white_draw':
                if current_player == 'white' and not game_over and not draw_offer:
                    draw_offer = {'by':'white', 'state':'proposed'}
            elif key == 'black_resign':
                if not game_over:
                    game_over = True
                    game_result = 'White wins by resignation'
                    status_message = game_result
            elif key == 'white_resign':
                if not game_over:
                    game_over = True
                    game_result = 'Black wins by resignation'
                    status_message = game_result


def main_loop():
    global selected, legal_moves, current_player, game_over, game_result, status_message
    global white_time, black_time, last_clock_tick, clock_running, draw_offer
    running = True

    while running:
        dt = clock.tick(FPS)
        mx,my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if promotion_pending:
                    handle_promotion_mouse((mx,my))
                    continue
                if draw_offer and draw_offer.get('state') == 'proposed':
                    if draw_offer['yes_rect'].collidepoint(mx,my):
                        game_over = True
                        game_result = 'Draw by agreement'
                        status_message = game_result
                        draw_offer = None
                        continue
                    if draw_offer['no_rect'].collidepoint(mx,my):
                        draw_offer = None
                        status_message = f'{current_player.capitalize()} to move'
                        continue
                    # prevent any board actions while draw proposal is open
                    continue
                if BOARD_X <= mx < BOARD_X + BOARD_SIZE and BOARD_Y <= my < BOARD_Y + BOARD_SIZE and not game_over and not paused:
                    col = (mx - BOARD_X)//SQUARE
                    row = (my - BOARD_Y)//SQUARE
                    if selected is None:
                        if board[row][col] is not None and piece_color(board[row][col]) == current_player:
                            selected = (row, col)
                            update_legal_moves()
                    else:
                        if (row,col) in legal_moves:
                            apply_move(selected, (row,col))
                            selected = None
                            legal_moves = []
                        elif board[row][col] is not None and piece_color(board[row][col]) == current_player:
                            selected = (row, col)
                            update_legal_moves()
                        else:
                            selected = None
                            legal_moves = []
                else:
                    click_button((mx,my))

        if not paused and not game_over and clock_started:
            now = pygame.time.get_ticks()
            if clock_running and now - last_clock_tick >= 1000:
                last_clock_tick = now
                if current_player == 'white':
                    white_time -= 1
                    if white_time <= 0:
                        game_over = True
                        game_result = 'Black wins on time'
                        status_message = game_result
                else:
                    black_time -= 1
                    if black_time <= 0:
                        game_over = True
                        game_result = 'White wins on time'
                        status_message = game_result

        # Rendering
        screen.fill((30,30,30))
        draw_ui_panel()
        draw_board()
        draw_promotion_panel()

        if game_over:
            overlay = pygame.Surface((BOARD_SIZE, BOARD_SIZE), pygame.SRCALPHA)
            overlay.fill((0,0,0,180))
            screen.blit(overlay, (BOARD_X, BOARD_Y))
            message = game_result
            text = large_font.render(message, True, (255,255,255))
            screen.blit(text, (BOARD_X + (BOARD_SIZE-text.get_width())//2, BOARD_Y + (BOARD_SIZE-text.get_height())//2))

        status_bar = small_font.render(status_message, True, TEXT_C)
        screen.blit(status_bar, (BOARD_X, BOARD_Y + BOARD_SIZE + 8))

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    init_board()
    main_loop()
