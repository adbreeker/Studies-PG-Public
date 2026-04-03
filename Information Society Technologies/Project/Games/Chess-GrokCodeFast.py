import pygame
import sys
import time
from pygame.locals import *

# Constants
WIDTH = 896
HEIGHT = 576
BOARD_SIZE = 512
SQUARE_SIZE = 64
MARGIN = 32
UI_WIDTH = 256
SPACE = 64

# Colors
CREAM = (255, 248, 220)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)
LIGHT_GRAY = (220, 220, 220)

# Piece types
PIECE_NAMES = ['King', 'Queen', 'Rook', 'Bishop', 'Knight', 'Pawn']
PIECE_DIR = 'Pieces/'

# Load images
piece_images = {}
pygame.init()
for color in ['White', 'Black']:
    for piece in PIECE_NAMES:
        path = PIECE_DIR + color + piece + '.png'
        try:
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
            piece_images[color + piece] = img
        except:
            print(f"Could not load {path}")
            sys.exit(1)

# Font
font = pygame.font.SysFont(None, 24)
small_font = pygame.font.SysFont(None, 18)
big_font = pygame.font.SysFont(None, 48)

class Piece:
    def __init__(self, type, color, row, col):
        self.type = type
        self.color = color
        self.row = row
        self.col = col
        self.has_moved = False

# Initialize board
board = [[None for _ in range(8)] for _ in range(8)]
pieces_order = ['Rook', 'Knight', 'Bishop', 'Queen', 'King', 'Bishop', 'Knight', 'Rook']
for col in range(8):
    board[7][col] = Piece(pieces_order[col], 'White', 7, col)
    board[6][col] = Piece('Pawn', 'White', 6, col)
    board[0][col] = Piece(pieces_order[col], 'Black', 0, col)
    board[1][col] = Piece('Pawn', 'Black', 1, col)

# Game state
current_player = 'White'
turn_number = 1
timers = {'White': 600, 'Black': 600}  # 10 minutes
timer_started = False
last_move = None
selected_piece = None
possible_moves = []
game_state = 'playing'  # 'playing', 'checkmate', 'stalemate', 'draw', 'draw_proposal', 'paused', 'promotion'
winner = None
draw_proposer = None
promotion_piece = None
promotion_square = None

def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02}:{secs:02}"

def find_king(color):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece.type == 'King' and piece.color == color:
                return (row, col)
    return None

def get_pawn_moves(piece, board):
    moves = []
    direction = -1 if piece.color == 'White' else 1
    row, col = piece.row, piece.col
    # Move forward
    if 0 <= row + direction < 8 and board[row + direction][col] is None:
        moves.append((row + direction, col))
        if not piece.has_moved and 0 <= row + 2*direction < 8 and board[row + 2*direction][col] is None:
            moves.append((row + 2*direction, col))
    # Captures
    for dc in [-1, 1]:
        if 0 <= col + dc < 8:
            target_row = row + direction
            if 0 <= target_row < 8:
                target = board[target_row][col + dc]
                if target and target.color != piece.color:
                    moves.append((target_row, col + dc))
                # En passant
                if row == (3 if piece.color == 'White' else 4):
                    adjacent = board[row][col + dc]
                    if adjacent and adjacent.type == 'Pawn' and adjacent.color != piece.color and adjacent.has_moved and last_move and last_move[1] == (row, col + dc) and abs(last_move[0][0] - last_move[1][0]) == 2:
                        moves.append((target_row, col + dc))
    return moves

def get_sliding_moves(piece, board, directions):
    moves = []
    row, col = piece.row, piece.col
    for dr, dc in directions:
        r, c = row + dr, col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            target = board[r][c]
            if target:
                if target.color != piece.color:
                    moves.append((r, c))
                break
            moves.append((r, c))
            r += dr
            c += dc
    return moves

def get_knight_moves(piece, board):
    moves = []
    row, col = piece.row, piece.col
    deltas = [(1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]
    for dr, dc in deltas:
        nr, nc = row + dr, col + dc
        if 0 <= nr < 8 and 0 <= nc < 8:
            target = board[nr][nc]
            if not target or target.color != piece.color:
                moves.append((nr, nc))
    return moves

def get_king_moves(piece, board):
    moves = []
    row, col = piece.row, piece.col
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0: continue
            nr, nc = row + dr, col + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target = board[nr][nc]
                if not target or target.color != piece.color:
                    moves.append((nr, nc))
    # Castling
    if not piece.has_moved and not is_in_check(board, piece.color):
        # Kingside
        if board[row][7] and board[row][7].type == 'Rook' and board[row][7].color == piece.color and not board[row][7].has_moved:
            if all(board[row][c] is None for c in range(5, 7)):
                if not is_attacked(board, piece.color, (row, 5)) and not is_attacked(board, piece.color, (row, 6)):
                    moves.append((row, 6))
        # Queenside
        if board[row][0] and board[row][0].type == 'Rook' and board[row][0].color == piece.color and not board[row][0].has_moved:
            if all(board[row][c] is None for c in range(1, 4)):
                if not is_attacked(board, piece.color, (row, 2)) and not is_attacked(board, piece.color, (row, 3)):
                    moves.append((row, 2))
    return moves

def get_pawn_attacks(piece, board):
    attacks = []
    direction = -1 if piece.color == 'White' else 1
    row, col = piece.row, piece.col
    for dc in [-1, 1]:
        nr, nc = row + direction, col + dc
        if 0 <= nr < 8 and 0 <= nc < 8:
            attacks.append((nr, nc))
    return attacks

def get_king_attacks(piece, board):
    attacks = []
    row, col = piece.row, piece.col
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0: continue
            nr, nc = row + dr, col + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                attacks.append((nr, nc))
    return attacks

def is_attacked(board, color, pos):
    opp_color = 'Black' if color == 'White' else 'White'
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece.color == opp_color:
                if piece.type == 'Pawn':
                    attacks = get_pawn_attacks(piece, board)
                elif piece.type == 'King':
                    attacks = get_king_attacks(piece, board)
                else:
                    # For simplicity, use possible moves, but since they filter check, need to be careful
                    attacks = []
                    if piece.type == 'Rook':
                        attacks = get_sliding_moves(piece, board, [(0,1),(0,-1),(1,0),(-1,0)])
                    elif piece.type == 'Bishop':
                        attacks = get_sliding_moves(piece, board, [(1,1),(1,-1),(-1,1),(-1,-1)])
                    elif piece.type == 'Queen':
                        attacks = get_sliding_moves(piece, board, [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)])
                    elif piece.type == 'Knight':
                        attacks = get_knight_moves(piece, board)
                    elif piece.type == 'King':
                        attacks = get_king_attacks(piece, board)
                if pos in attacks:
                    return True
    return False

def is_in_check(board, color):
    king_pos = find_king(color)
    return is_attacked(board, color, king_pos)

def would_be_in_check(piece, move, board):
    orig_row, orig_col = piece.row, piece.col
    target_row, target_col = move
    captured = board[target_row][target_col]
    board[target_row][target_col] = piece
    board[orig_row][orig_col] = None
    piece.row, piece.col = target_row, target_col
    in_check = is_in_check(board, piece.color)
    board[orig_row][orig_col] = piece
    board[target_row][target_col] = captured
    piece.row, piece.col = orig_row, orig_col
    return in_check

def get_possible_moves(piece, board):
    if piece.type == 'Pawn':
        moves = get_pawn_moves(piece, board)
    elif piece.type == 'Rook':
        moves = get_sliding_moves(piece, board, [(0,1),(0,-1),(1,0),(-1,0)])
    elif piece.type == 'Bishop':
        moves = get_sliding_moves(piece, board, [(1,1),(1,-1),(-1,1),(-1,-1)])
    elif piece.type == 'Queen':
        moves = get_sliding_moves(piece, board, [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)])
    elif piece.type == 'Knight':
        moves = get_knight_moves(piece, board)
    elif piece.type == 'King':
        moves = get_king_moves(piece, board)
    valid_moves = []
    for move in moves:
        if not would_be_in_check(piece, move, board):
            valid_moves.append(move)
    return valid_moves

def has_legal_moves(color):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece.color == color:
                if get_possible_moves(piece, board):
                    return True
    return False

def move_piece(piece, move):
    global last_move, turn_number, current_player, timer_started
    orig_row, orig_col = piece.row, piece.col
    target_row, target_col = move
    captured = board[target_row][target_col]
    # Handle en passant
    if piece.type == 'Pawn' and abs(target_col - orig_col) == 1 and not captured:
        captured_row = orig_row
        captured = board[captured_row][target_col]
        board[captured_row][target_col] = None
    # Handle castling
    if piece.type == 'King' and abs(target_col - orig_col) == 2:
        if target_col > orig_col:  # Kingside
            rook = board[orig_row][7]
            board[orig_row][5] = rook
            board[orig_row][7] = None
            rook.col = 5
            rook.has_moved = True
        else:  # Queenside
            rook = board[orig_row][0]
            board[orig_row][3] = rook
            board[orig_row][0] = None
            rook.col = 3
            rook.has_moved = True
    # Move piece
    board[target_row][target_col] = piece
    board[orig_row][orig_col] = None
    piece.row, piece.col = target_row, target_col
    piece.has_moved = True
    last_move = ((orig_row, orig_col), (target_row, target_col))
    # Promotion
    if piece.type == 'Pawn' and (target_row == 0 or target_row == 7):
        global game_state, promotion_piece, promotion_square
        game_state = 'promotion'
        promotion_piece = piece
        promotion_square = (target_row, target_col)
        return  # Don't switch turn yet
    # Timer bonus for the player who moved
    timers[piece.color] = min(600, timers[piece.color] + 2)
    # Switch turn
    current_player = 'Black' if current_player == 'White' else 'White'
    turn_number += 1
    if not timer_started and turn_number == 2:
        timer_started = True

def check_game_end():
    global game_state, winner
    if is_in_check(board, current_player):
        if not has_legal_moves(current_player):
            game_state = 'checkmate'
            winner = 'Black' if current_player == 'White' else 'White'
        else:
            game_state = 'playing'  # Just check
    else:
        if not has_legal_moves(current_player):
            game_state = 'stalemate'
        else:
            game_state = 'playing'

def handle_button(btn):
    global game_state, draw_proposer, winner
    if btn in ['Pause', 'Resume']:
        if game_state in ['playing', 'paused']:
            game_state = 'paused' if game_state == 'playing' else 'playing'
    elif btn == 'Reset':
        reset_game()
    elif btn == 'White Draw' and current_player == 'White' and game_state == 'playing':
        game_state = 'draw_proposal'
        draw_proposer = 'White'
    elif btn == 'Black Draw' and current_player == 'Black' and game_state == 'playing':
        game_state = 'draw_proposal'
        draw_proposer = 'Black'
    elif btn == 'White Resign' and current_player == 'White' and game_state == 'playing':
        game_state = 'resign'
        winner = 'Black'
    elif btn == 'Black Resign' and current_player == 'Black' and game_state == 'playing':
        game_state = 'resign'
        winner = 'White'

def reset_game():
    global board, current_player, turn_number, timers, timer_started, last_move, selected_piece, possible_moves, game_state, winner, draw_proposer, promotion_piece, promotion_square
    board = [[None for _ in range(8)] for _ in range(8)]
    for col in range(8):
        board[7][col] = Piece(pieces_order[col], 'White', 7, col)
        board[6][col] = Piece('Pawn', 'White', 6, col)
        board[0][col] = Piece(pieces_order[col], 'Black', 0, col)
        board[1][col] = Piece('Pawn', 'Black', 1, col)
    current_player = 'White'
    turn_number = 1
    timers = {'White': 600, 'Black': 600}
    timer_started = False
    last_move = None
    selected_piece = None
    possible_moves = []
    game_state = 'playing'
    winner = None
    draw_proposer = None
    promotion_piece = None
    promotion_square = None

def draw_board_squares(screen):
    for row in range(8):
        for col in range(8):
            color = CREAM if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(screen, color, (MARGIN + UI_WIDTH + SPACE + col * SQUARE_SIZE, MARGIN + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_highlights(screen):
    # Highlight last move
    if last_move:
        for pos in last_move:
            r, c = pos
            pygame.draw.rect(screen, YELLOW, (MARGIN + UI_WIDTH + SPACE + c * SQUARE_SIZE, MARGIN + r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
    # Highlight check
    if game_state == 'playing' and is_in_check(board, current_player):
        king_pos = find_king(current_player)
        if king_pos:
            r, c = king_pos
            pygame.draw.rect(screen, RED, (MARGIN + UI_WIDTH + SPACE + c * SQUARE_SIZE, MARGIN + r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
    # Highlight possible moves
    for move in possible_moves:
        r, c = move
        center = (MARGIN + UI_WIDTH + SPACE + c * SQUARE_SIZE + SQUARE_SIZE//2, MARGIN + r * SQUARE_SIZE + SQUARE_SIZE//2)
        pygame.draw.circle(screen, YELLOW, center, 8)

def draw_pieces(screen):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                img = piece_images[piece.color + piece.type]
                screen.blit(img, (MARGIN + UI_WIDTH + SPACE + col * SQUARE_SIZE, MARGIN + row * SQUARE_SIZE))

def draw_ui(screen):
    # UI Panel background
    ui_x = MARGIN
    ui_y = MARGIN
    ui_w = UI_WIDTH
    ui_h = HEIGHT - 2 * MARGIN
    pygame.draw.rect(screen, LIGHT_GRAY, (ui_x, ui_y, ui_w, ui_h))
    pygame.draw.rect(screen, BLACK, (ui_x, ui_y, ui_w, ui_h), 2)
    
    # Turn
    turn_text = f"Turn {turn_number}: {current_player}"
    screen.blit(font.render(turn_text, True, BLACK), (MARGIN + 10, MARGIN + 10))
    # Timers
    white_time = format_time(timers['White'])
    black_time = format_time(timers['Black'])
    screen.blit(font.render(f"White: {white_time}", True, BLACK), (MARGIN + 10, MARGIN + 50))
    screen.blit(font.render(f"Black: {black_time}", True, BLACK), (MARGIN + 10, MARGIN + 100))
    # Buttons
    buttons = {}
    if current_player == 'White':
        buttons['White Draw'] = (MARGIN + 10, MARGIN + 150, 110, 35)
        buttons['White Resign'] = (MARGIN + 130, MARGIN + 150, 110, 35)
    else:
        buttons['Black Draw'] = (MARGIN + 10, MARGIN + 200, 110, 35)
        buttons['Black Resign'] = (MARGIN + 130, MARGIN + 200, 110, 35)
    pause_text = 'Resume' if game_state == 'paused' else 'Pause'
    buttons[pause_text] = (MARGIN + 10, MARGIN + 250, 110, 35)
    buttons['Reset'] = (MARGIN + 130, MARGIN + 250, 110, 35)
    for btn, (x, y, w, h) in buttons.items():
        pygame.draw.rect(screen, LIGHT_BLUE, (x, y, w, h))
        pygame.draw.rect(screen, DARK_BLUE, (x, y, w, h), 2)
        text_surf = small_font.render(btn, True, BLACK)
        text_rect = text_surf.get_rect(center=(x + w//2, y + h//2))
        screen.blit(text_surf, text_rect)
    # Footer
    footer_lines = ["Grok Code Fast 1", "Prompts: 6, Tokens: 3 430 780", "@adbreeker 2026"]
    for i, line in enumerate(footer_lines):
        screen.blit(small_font.render(line, True, BLACK), (MARGIN + 10, HEIGHT - MARGIN - 20 * (len(footer_lines) - i)))
    # Game state messages
    if game_state in ['checkmate', 'stalemate', 'draw', 'resign', 'timeout']:
        msg = ""
        if game_state == 'checkmate':
            msg = f"Checkmate! {winner} wins!"
        elif game_state == 'stalemate':
            msg = "Stalemate! It's a draw."
        elif game_state == 'draw':
            msg = "Draw!"
        elif game_state == 'resign':
            msg = f"{winner} wins by resignation!"
        elif game_state == 'timeout':
            msg = f"Time out! {winner} wins!"
        text_surf = big_font.render(msg, True, BLACK)
        text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
        # Background
        bg_rect = pygame.Rect(text_rect.left - 30, text_rect.top - 20, text_rect.width + 60, text_rect.height + 40)
        pygame.draw.rect(screen, LIGHT_BLUE, bg_rect)
        pygame.draw.rect(screen, DARK_BLUE, bg_rect, 3)
        screen.blit(text_surf, text_rect)
    elif game_state == 'draw_proposal':
        msg = f"{draw_proposer} proposes a draw."
        text_surf = big_font.render(msg, True, BLACK)
        text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        # Background
        bg_rect = pygame.Rect(text_rect.left - 30, text_rect.top - 20, text_rect.width + 60, text_rect.height + 40)
        pygame.draw.rect(screen, LIGHT_BLUE, bg_rect)
        pygame.draw.rect(screen, DARK_BLUE, bg_rect, 3)
        screen.blit(text_surf, text_rect)
        # Accept/Refuse buttons
        btn_width = 120
        btn_height = 45
        accept_x = WIDTH//2 - 130
        refuse_x = WIDTH//2 + 10
        btn_y = HEIGHT//2
        pygame.draw.rect(screen, LIGHT_BLUE, (accept_x, btn_y, btn_width, btn_height))
        pygame.draw.rect(screen, DARK_BLUE, (accept_x, btn_y, btn_width, btn_height), 2)
        text_surf = font.render("Accept", True, BLACK)
        text_rect = text_surf.get_rect(center=(accept_x + btn_width//2, btn_y + btn_height//2))
        screen.blit(text_surf, text_rect)
        pygame.draw.rect(screen, LIGHT_BLUE, (refuse_x, btn_y, btn_width, btn_height))
        pygame.draw.rect(screen, DARK_BLUE, (refuse_x, btn_y, btn_width, btn_height), 2)
        text_surf = font.render("Refuse", True, BLACK)
        text_rect = text_surf.get_rect(center=(refuse_x + btn_width//2, btn_y + btn_height//2))
        screen.blit(text_surf, text_rect)
    elif game_state == 'promotion':
        msg = "Choose promotion piece:"
        text_surf = big_font.render(msg, True, BLACK)
        text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
        # Background
        bg_rect = pygame.Rect(text_rect.left - 30, text_rect.top - 20, text_rect.width + 60, text_rect.height + 40)
        pygame.draw.rect(screen, LIGHT_BLUE, bg_rect)
        pygame.draw.rect(screen, DARK_BLUE, bg_rect, 3)
        screen.blit(text_surf, text_rect)
        # Promotion buttons
        prom_buttons = ['Queen', 'Rook', 'Bishop', 'Knight']
        btn_width = 100
        btn_height = 45
        gap = 35
        total_width = 4 * btn_width + 3 * gap
        start_x = WIDTH // 2 - total_width // 2
        for i, piece in enumerate(prom_buttons):
            x = start_x + i * (btn_width + gap)
            y = HEIGHT//2 - 50
            pygame.draw.rect(screen, LIGHT_BLUE, (x, y, btn_width, btn_height))
            pygame.draw.rect(screen, DARK_BLUE, (x, y, btn_width, btn_height), 2)
            text_surf = font.render(piece, True, BLACK)
            text_rect = text_surf.get_rect(center=(x + btn_width//2, y + btn_height//2))
            screen.blit(text_surf, text_rect)

# Main loop
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess - Grok Code Fast")
clock = pygame.time.Clock()
running = True
last_timer_update = time.time()

while running:
    dt = clock.tick(60)
    current_time = time.time()
    if timer_started and game_state == 'playing':
        timers[current_player] -= current_time - last_timer_update
        if timers[current_player] <= 0:
            game_state = 'timeout'
            winner = 'Black' if current_player == 'White' else 'White'
    last_timer_update = current_time

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            x, y = event.pos
            if game_state == 'playing':
                board_x = MARGIN + UI_WIDTH + SPACE
                board_y = MARGIN
                if board_x <= x < board_x + BOARD_SIZE and board_y <= y < board_y + BOARD_SIZE:
                    col = (x - board_x) // SQUARE_SIZE
                    row = (y - board_y) // SQUARE_SIZE
                    piece = board[row][col]
                    if selected_piece:
                        if (row, col) in possible_moves:
                            move_piece(selected_piece, (row, col))
                            selected_piece = None
                            possible_moves = []
                            if game_state != 'promotion':  # Only check end if not promoting
                                check_game_end()
                        elif piece and piece.color == current_player:
                            selected_piece = piece
                            possible_moves = get_possible_moves(piece, board)
                        else:
                            selected_piece = None
                            possible_moves = []
                    elif piece and piece.color == current_player:
                        selected_piece = piece
                        possible_moves = get_possible_moves(piece, board)
            # Buttons - allow when not playing for reset and pause
            buttons = {}
            if current_player == 'White':
                buttons['White Draw'] = (MARGIN + 10, MARGIN + 150, 110, 35)
                buttons['White Resign'] = (MARGIN + 130, MARGIN + 150, 110, 35)
            else:
                buttons['Black Draw'] = (MARGIN + 10, MARGIN + 200, 110, 35)
                buttons['Black Resign'] = (MARGIN + 130, MARGIN + 200, 110, 35)
            pause_text = 'Resume' if game_state == 'paused' else 'Pause'
            buttons[pause_text] = (MARGIN + 10, MARGIN + 250, 110, 35)
            buttons['Reset'] = (MARGIN + 130, MARGIN + 250, 110, 35)
            for btn, (bx, by, bw, bh) in buttons.items():
                if bx <= x < bx + bw and by <= y < by + bh:
                    if game_state == 'playing' or btn in ['Reset', pause_text]:
                        handle_button(btn)
            # Draw proposal buttons
            if game_state == 'draw_proposal':
                btn_width = 120
                accept_x = WIDTH//2 - 130
                refuse_x = WIDTH//2 + 10
                btn_y = HEIGHT//2
                if accept_x <= x < accept_x + btn_width and btn_y <= y < btn_y + 45:
                    game_state = 'draw'
                elif refuse_x <= x < refuse_x + btn_width and btn_y <= y < btn_y + 45:
                    game_state = 'playing'
                    draw_proposer = None
            # Promotion buttons
            elif game_state == 'promotion':
                prom_buttons = ['Queen', 'Rook', 'Bishop', 'Knight']
                btn_width = 100
                gap = 35
                total_width = 4 * btn_width + 3 * gap
                start_x = WIDTH // 2 - total_width // 2
                for i, piece_type in enumerate(prom_buttons):
                    bx = start_x + i * (btn_width + gap)
                    by = HEIGHT//2 - 50
                    if bx <= x < bx + btn_width and by <= y < by + 45:
                        promotion_piece.type = piece_type
                        game_state = 'playing'
                        # Timer bonus for the player who promoted
                        timers[promotion_piece.color] = min(600, timers[promotion_piece.color] + 2)
                        # Now switch turn
                        current_player = 'Black' if current_player == 'White' else 'White'
                        turn_number += 1
                        if not timer_started and turn_number == 2:
                            timer_started = True
                        check_game_end()
                        promotion_piece = None
                        promotion_square = None

    screen.fill(WHITE)
    draw_board_squares(screen)
    draw_pieces(screen)
    draw_highlights(screen)
    draw_ui(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()
