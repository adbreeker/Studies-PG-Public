"""
Chess Game - Pygame Implementation
Based on GDD.md specifications
Window: 896x576px, Board: 8x8 (64x64px squares), UI Panel: 256x512px
"""

import pygame
import sys
from enum import Enum
from typing import List, Tuple, Optional, Set
from copy import deepcopy
import os

# Initialize Pygame
pygame.init()

# Constants from GDD
WINDOW_WIDTH = 896
WINDOW_HEIGHT = 576
SQUARE_SIZE = 64
BOARD_SIZE = 8
MARGIN = 32
UI_PANEL_WIDTH = 256
UI_PANEL_HEIGHT = 512
UI_BREAK_SPACE = 64
BOARD_START_X = UI_PANEL_WIDTH + UI_BREAK_SPACE + MARGIN
BOARD_START_Y = MARGIN

# Colors
CREAM = (240, 217, 181)
BROWN = (181, 136, 99)
RED = (220, 20, 60)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (200, 200, 200)
BLUE = (100, 149, 237)

# Time control (in seconds)
INITIAL_TIME = 600  # 10 minutes
TIME_BONUS = 2  # 2 seconds per move
MOVE_HIGHLIGHT_RADIUS = 8


class PieceType(Enum):
    """Piece types in chess"""
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6


class Color(Enum):
    """Piece colors"""
    WHITE = 1
    BLACK = 2


class Piece:
    """Represents a chess piece"""
    
    def __init__(self, piece_type: PieceType, color: Color):
        self.type = piece_type
        self.color = color
        self.has_moved = False
        self.image = None
        self.load_image()
    
    def load_image(self):
        """Load piece image from Pieces directory"""
        color_name = "White" if self.color == Color.WHITE else "Black"
        type_name = self.type.name.capitalize()
        
        # Map piece types to file names
        type_map = {
            PieceType.PAWN: "Pawn",
            PieceType.KNIGHT: "Knight",
            PieceType.BISHOP: "Bishop",
            PieceType.ROOK: "Rook",
            PieceType.QUEEN: "Queen",
            PieceType.KING: "King",
        }
        
        filename = f"{color_name}{type_map[self.type]}.png"
        filepath = os.path.join(os.path.dirname(__file__), "..", "Pieces", filename)
        
        try:
            self.image = pygame.image.load(filepath)
            self.image = pygame.transform.scale(self.image, (SQUARE_SIZE, SQUARE_SIZE))
        except pygame.error as e:
            print(f"Warning: Could not load {filepath}: {e}")
            # Create a placeholder surface
            self.image = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            self.image.fill(LIGHT_GRAY)
    
    def __repr__(self):
        color_str = "W" if self.color == Color.WHITE else "B"
        type_str = self.type.name[0]
        return f"{color_str}{type_str}"


class Board:
    """Represents the chess board and game state"""
    
    def __init__(self):
        self.squares: List[List[Optional[Piece]]] = [[None for _ in range(8)] for _ in range(8)]
        self.setup_initial_position()
        self.move_history = []
        self.en_passant_target = None
    
    def setup_initial_position(self):
        """Set up pieces in starting positions"""
        # Back rank setup: rook, knight, bishop, queen, king, bishop, knight, rook
        back_rank_order = [
            PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP, PieceType.QUEEN,
            PieceType.KING, PieceType.BISHOP, PieceType.KNIGHT, PieceType.ROOK
        ]
        
        # White pieces (row 7 and 6)
        for col, piece_type in enumerate(back_rank_order):
            self.squares[7][col] = Piece(piece_type, Color.WHITE)
        for col in range(8):
            self.squares[6][col] = Piece(PieceType.PAWN, Color.WHITE)
        
        # Black pieces (row 0 and 1)
        for col, piece_type in enumerate(back_rank_order):
            self.squares[0][col] = Piece(piece_type, Color.BLACK)
        for col in range(8):
            self.squares[1][col] = Piece(PieceType.PAWN, Color.BLACK)
    
    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        """Get piece at position"""
        if 0 <= row < 8 and 0 <= col < 8:
            return self.squares[row][col]
        return None
    
    def set_piece(self, row: int, col: int, piece: Optional[Piece]):
        """Set piece at position"""
        if 0 <= row < 8 and 0 <= col < 8:
            self.squares[row][col] = piece
    
    def is_white_on_bottom(self) -> bool:
        """White pieces on bottom (row 7), black on top (row 0)"""
        return True
    
    def get_all_moves(self, color: Color) -> Set[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get all legal moves for a color"""
        moves = set()
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece.color == color:
                    piece_moves = self.get_legal_moves((row, col))
                    for target in piece_moves:
                        moves.add(((row, col), target))
        return moves
    
    def get_legal_moves(self, pos: Tuple[int, int]) -> Set[Tuple[int, int]]:
        """Get legal moves for piece at position (accounts for check)"""
        pseudo_legal = self.get_pseudo_legal_moves(pos)
        legal_moves = set()
        
        piece = self.get_piece(pos[0], pos[1])
        if not piece:
            return legal_moves
        
        # Filter out moves that leave/put king in check
        for target in pseudo_legal:
            # Try the move
            captured = self.get_piece(target[0], target[1])
            self.set_piece(pos[0], pos[1], None)
            self.set_piece(target[0], target[1], piece)
            
            # Check if king is in check
            if not self.is_king_in_check(piece.color):
                legal_moves.add(target)
            
            # Undo the move
            self.set_piece(pos[0], pos[1], piece)
            self.set_piece(target[0], target[1], captured)
        
        return legal_moves
    
    def get_pseudo_legal_moves(self, pos: Tuple[int, int], include_castling: bool = True) -> Set[Tuple[int, int]]:
        """Get pseudo-legal moves (not accounting for check)"""
        row, col = pos
        piece = self.get_piece(row, col)
        
        if not piece:
            return set()
        
        moves = set()
        
        if piece.type == PieceType.PAWN:
            moves = self.get_pawn_moves(row, col, piece.color)
        elif piece.type == PieceType.KNIGHT:
            moves = self.get_knight_moves(row, col, piece.color)
        elif piece.type == PieceType.BISHOP:
            moves = self.get_diagonal_moves(row, col, piece.color)
        elif piece.type == PieceType.ROOK:
            moves = self.get_orthogonal_moves(row, col, piece.color)
        elif piece.type == PieceType.QUEEN:
            moves = self.get_orthogonal_moves(row, col, piece.color)
            moves.update(self.get_diagonal_moves(row, col, piece.color))
        elif piece.type == PieceType.KING:
            moves = self.get_king_moves(row, col, piece.color, include_castling=include_castling)
        
        return moves
    
    def get_pawn_moves(self, row: int, col: int, color: Color) -> Set[Tuple[int, int]]:
        """Get pawn moves"""
        moves = set()
        direction = 1 if color == Color.BLACK else -1  # Black moves down (increasing row), White moves up (decreasing row)
        start_row = 1 if color == Color.BLACK else 6
        
        # Forward move
        new_row = row + direction
        if 0 <= new_row < 8 and not self.get_piece(new_row, col):
            moves.add((new_row, col))
            
            # Double move from start
            if row == start_row:
                double_row = row + 2 * direction
                if not self.get_piece(double_row, col):
                    moves.add((double_row, col))
        
        # Captures
        for dc in [-1, 1]:
            new_col = col + dc
            new_row = row + direction
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.get_piece(new_row, new_col)
                if target and target.color != color:
                    moves.add((new_row, new_col))
        
        # En passant
        if self.en_passant_target:
            # Pawn can move diagonally to en passant target
            for dc in [-1, 1]:
                if (row + direction, col + dc) == self.en_passant_target:
                    moves.add(self.en_passant_target)
        
        return moves
    
    def get_knight_moves(self, row: int, col: int, color: Color) -> Set[Tuple[int, int]]:
        """Get knight moves"""
        moves = set()
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.get_piece(new_row, new_col)
                if not target or target.color != color:
                    moves.add((new_row, new_col))
        
        return moves
    
    def get_diagonal_moves(self, row: int, col: int, color: Color) -> Set[Tuple[int, int]]:
        """Get diagonal moves (for bishop/queen)"""
        moves = set()
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.get_piece(new_row, new_col)
                if not target:
                    moves.add((new_row, new_col))
                else:
                    if target.color != color:
                        moves.add((new_row, new_col))
                    break
                new_row += dr
                new_col += dc
        
        return moves
    
    def get_orthogonal_moves(self, row: int, col: int, color: Color) -> Set[Tuple[int, int]]:
        """Get orthogonal moves (for rook/queen)"""
        moves = set()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.get_piece(new_row, new_col)
                if not target:
                    moves.add((new_row, new_col))
                else:
                    if target.color != color:
                        moves.add((new_row, new_col))
                    break
                new_row += dr
                new_col += dc
        
        return moves
    
    def get_king_moves(self, row: int, col: int, color: Color, include_castling: bool = True) -> Set[Tuple[int, int]]:
        """Get king moves including castling"""
        moves = set()
        
        # Regular king moves
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = self.get_piece(new_row, new_col)
                    if not target or target.color != color:
                        moves.add((new_row, new_col))
        
        # Castling (only when calculating legal moves, not when checking attacks)
        if include_castling:
            castling_moves = self.get_castling_moves(row, col, color)
            moves.update(castling_moves)
        
        return moves
    
    def get_castling_moves(self, row: int, col: int, color: Color) -> Set[Tuple[int, int]]:
        """Get castling moves"""
        moves = set()
        king = self.get_piece(row, col)
        
        if not king or king.type != PieceType.KING or king.has_moved:
            return moves
        
        # King must not be in check
        if self.is_king_in_check(color):
            return moves
        
        # Check both sides
        for rook_col, direction in [(0, -1), (7, 1)]:
            rook = self.get_piece(row, rook_col)
            
            # Rook must not have moved
            if not rook or rook.type != PieceType.ROOK or rook.has_moved:
                continue
            
            # Check squares between king and rook
            start_col = min(col, rook_col) + 1
            end_col = max(col, rook_col)
            blocked = False
            
            for c in range(start_col, end_col):
                if self.get_piece(row, c):
                    blocked = True
                    break
            
            if blocked:
                continue
            
            # King can't pass through check
            king_target_col = col + 2 * direction
            temp_col = col + direction
            
            # Check if king passes through attacked square
            king_safe = True
            for check_col in [temp_col, king_target_col]:
                if self.is_square_attacked(row, check_col, color):
                    king_safe = False
                    break
            
            if king_safe:
                moves.add((row, king_target_col))
        
        return moves
    
    def is_king_in_check(self, color: Color) -> bool:
        """Check if king of given color is in check"""
        # Find king
        king_pos = None
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece.type == PieceType.KING and piece.color == color:
                    king_pos = (row, col)
                    break
        
        if not king_pos:
            return False
        
        return self.is_square_attacked(king_pos[0], king_pos[1], color)
    
    def is_square_attacked(self, row: int, col: int, by_color: Color) -> bool:
        """Check if square is attacked by given color"""
        enemy_color = Color.BLACK if by_color == Color.WHITE else Color.WHITE
        
        # Check all enemy pieces (don't include castling to avoid infinite recursion)
        for r in range(8):
            for c in range(8):
                piece = self.get_piece(r, c)
                if piece and piece.color == enemy_color:
                    moves = self.get_pseudo_legal_moves((r, c), include_castling=False)
                    if (row, col) in moves:
                        return True
        
        return False
    
    def is_checkmate(self, color: Color) -> bool:
        """Check if position is checkmate"""
        if not self.is_king_in_check(color):
            return False
        
        return len(self.get_all_moves(color)) == 0
    
    def is_stalemate(self, color: Color) -> bool:
        """Check if position is stalemate"""
        if self.is_king_in_check(color):
            return False
        
        return len(self.get_all_moves(color)) == 0
    
    def is_dead_position(self) -> bool:
        """Check for dead position (insufficient material)"""
        pieces = []
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece.type != PieceType.KING:
                    pieces.append(piece.type)
        
        # Only kings left
        if len(pieces) == 0:
            return True
        
        # King + Knight vs King
        if len(pieces) == 1 and pieces[0] == PieceType.KNIGHT:
            return True
        
        # King + Bishop vs King
        if len(pieces) == 1 and pieces[0] == PieceType.BISHOP:
            return True
        
        return False
    
    def make_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], 
                  promotion_piece: Optional[PieceType] = None):
        """Make a move on the board"""
        piece = self.get_piece(from_pos[0], from_pos[1])
        if not piece:
            return False
        
        captured = self.get_piece(to_pos[0], to_pos[1])
        
        # Handle en passant
        if piece.type == PieceType.PAWN and self.en_passant_target:
            if to_pos == self.en_passant_target:
                direction = 1 if piece.color == Color.BLACK else -1
                ep_captured = self.get_piece(to_pos[0] - direction, to_pos[1])
                self.set_piece(to_pos[0] - direction, to_pos[1], None)
        
        # Update en passant target
        self.en_passant_target = None
        if piece.type == PieceType.PAWN:
            if abs(from_pos[0] - to_pos[0]) == 2:
                # Set en passant target
                ep_row = (from_pos[0] + to_pos[0]) // 2
                self.en_passant_target = (ep_row, to_pos[1])
        
        # Handle castling
        if piece.type == PieceType.KING and abs(from_pos[1] - to_pos[1]) == 2:
            # Move rook
            rook_col = 7 if to_pos[1] > from_pos[1] else 0
            rook_target_col = 5 if to_pos[1] > from_pos[1] else 3
            rook = self.get_piece(from_pos[0], rook_col)
            self.set_piece(from_pos[0], rook_col, None)
            self.set_piece(from_pos[0], rook_target_col, rook)
            if rook:
                rook.has_moved = True
        
        # Move piece
        self.set_piece(from_pos[0], from_pos[1], None)
        self.set_piece(to_pos[0], to_pos[1], piece)
        piece.has_moved = True
        
        # Handle pawn promotion
        if piece.type == PieceType.PAWN:
            if (piece.color == Color.WHITE and to_pos[0] == 0) or \
               (piece.color == Color.BLACK and to_pos[0] == 7):
                if promotion_piece:
                    promoted = Piece(promotion_piece, piece.color)
                    promoted.has_moved = True
                    self.set_piece(to_pos[0], to_pos[1], promoted)
        
        # Record move
        self.move_history.append({
            'from': from_pos,
            'to': to_pos,
            'piece': piece,
            'captured': captured
        })
        
        return True


class GameState(Enum):
    """Game states"""
    PLAYING = 1
    WHITE_WIN = 2
    BLACK_WIN = 3
    DRAW = 4
    DRAW_PROPOSAL = 5
    PAUSED = 6


class ChessGame:
    """Main chess game class"""
    
    def __init__(self):
        self.board = Board()
        self.current_player = Color.WHITE
        self.current_state = GameState.PLAYING
        self.white_time = INITIAL_TIME
        self.black_time = INITIAL_TIME
        self.turn_number = 0
        self.last_move = None
        self.selected_piece = None
        self.legal_moves = set()
        self.promotion_pending = False
        self.promotion_pos = None
        self.games_played = 0
        self.total_prompts = 9
        self.total_tokens = 7947344
        self.draw_proposer = None
        self.paused = False
        self.pause_time = 0
        self.promotion_from_pos = None
        
        # Setup display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Chess - Claude Haiku")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
    
    def handle_click(self, pos: Tuple[int, int]):
        """Handle mouse click"""
        # Don't allow moves if game is not playing
        if self.current_state != GameState.PLAYING:
            # Still allow UI clicks (resign, reset, etc)
            if self.handle_ui_click(pos):
                return
            return
        
        # Check UI buttons first
        if self.handle_ui_click(pos):
            return
        
        # Check board click
        if not self.is_click_on_board(pos):
            return
        
        board_pos = self.screen_to_board_pos(pos)
        if board_pos is None:
            return
        
        piece = self.board.get_piece(board_pos[0], board_pos[1])
        
        # If clicking on legal move
        if self.selected_piece and board_pos in self.legal_moves:
            self.make_move(self.selected_piece, board_pos)
            self.selected_piece = None
            self.legal_moves = set()
            return
        
        # Select piece
        if piece and piece.color == self.current_player:
            self.selected_piece = board_pos
            self.legal_moves = self.board.get_legal_moves(board_pos)
        else:
            self.selected_piece = None
            self.legal_moves = set()
    
    def handle_ui_click(self, pos: Tuple[int, int]) -> bool:
        """Handle UI button clicks, returns True if UI was clicked"""
        button_width = UI_PANEL_WIDTH - 2 * MARGIN - 20
        button_height = 35
        button_x = MARGIN + 10
        
        # Calculate button positions to match draw_ui_panel
        y_offset = MARGIN + 10  # Turn info
        y_offset += 80  # Black player UI
        y_offset += 80  # Buttons start here
        
        buttons = [
            ("Resign", 0),
            ("Draw", 1),
            ("Pause" if not self.paused else "Resume", 2),
        ]
        
        for label, idx in buttons:
            button_y = y_offset + idx * 40
            if button_x < pos[0] < button_x + button_width and \
               button_y < pos[1] < button_y + button_height:
                
                if label == "Resign":
                    self.handle_resign()
                elif label == "Draw":
                    self.handle_draw_proposal()
                elif "Pause" in label or "Resume" in label:
                    # Only allow pause if game is currently playing
                    if self.current_state == GameState.PLAYING:
                        self.paused = not self.paused
                        if self.paused:
                            self.pause_time = pygame.time.get_ticks()
                        else:
                            # Resume: update last_time to prevent time jump
                            self.last_time = pygame.time.get_ticks()
                
                return True
        
        # Reset button (after the 3 main buttons and spacing)
        reset_button_y = y_offset + 130
        if button_x < pos[0] < button_x + button_width and \
           reset_button_y < pos[1] < reset_button_y + button_height:
            self.reset_game()
            return True
        
        # Draw response buttons (if draw proposed)
        if self.current_state == GameState.DRAW_PROPOSAL:
            box_width = 350
            box_height = 150
            box_x = (WINDOW_WIDTH - box_width) // 2
            box_y = (WINDOW_HEIGHT - box_height) // 2
            button_y = box_y + 80
            button_height = 40
            button_width = 100
            
            accept_rect = pygame.Rect(box_x + 30, button_y, button_width, button_height)
            reject_rect = pygame.Rect(box_x + 220, button_y, button_width, button_height)
            
            if accept_rect.collidepoint(pos):
                self.end_game(GameState.DRAW)
                return True
            elif reject_rect.collidepoint(pos):
                self.current_state = GameState.PLAYING
                self.draw_proposer = None
                return True
        
        return False
    
    def screen_to_board_pos(self, screen_pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """Convert screen position to board position"""
        x, y = screen_pos
        
        if x < BOARD_START_X or x > BOARD_START_X + SQUARE_SIZE * 8:
            return None
        if y < BOARD_START_Y or y > BOARD_START_Y + SQUARE_SIZE * 8:
            return None
        
        col = (x - BOARD_START_X) // SQUARE_SIZE
        row = (y - BOARD_START_Y) // SQUARE_SIZE
        
        return (row, col)
    
    def is_click_on_board(self, pos: Tuple[int, int]) -> bool:
        """Check if click is on board"""
        x, y = pos
        return BOARD_START_X <= x <= BOARD_START_X + SQUARE_SIZE * 8 and \
               BOARD_START_Y <= y <= BOARD_START_Y + SQUARE_SIZE * 8
    
    def make_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]):
        """Make a move"""
        piece = self.board.get_piece(from_pos[0], from_pos[1])
        
        if not piece:
            return
        
        # Check for pawn promotion
        if piece.type == PieceType.PAWN:
            if (piece.color == Color.WHITE and to_pos[0] == 0) or \
               (piece.color == Color.BLACK and to_pos[0] == 7):
                self.promotion_pending = True
                self.promotion_from_pos = from_pos
                self.promotion_pos = to_pos
                self.selected_piece = None
                self.legal_moves = set()
                # Move the pawn first, then wait for promotion selection
                self.board.make_move(from_pos, to_pos)
                self.last_move = (from_pos, to_pos)
                return
        
        # Make the move
        self.board.make_move(from_pos, to_pos)
        
        # Add time bonus
        if self.current_player == Color.WHITE:
            self.white_time += TIME_BONUS
        else:
            self.black_time += TIME_BONUS
        
        self.last_move = (from_pos, to_pos)
        
        # Check game state
        self.check_game_state()
        
        # Switch player if game continues
        if self.current_state == GameState.PLAYING:
            self.current_player = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE
            self.turn_number += 1
    
    def check_game_state(self):
        """Check for win/draw conditions"""
        # Check opponent (who is about to move next) for checkmate/stalemate
        opponent = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE
        if self.board.is_checkmate(opponent):
            if opponent == Color.WHITE:
                self.end_game(GameState.BLACK_WIN)
            else:
                self.end_game(GameState.WHITE_WIN)
        elif self.board.is_stalemate(opponent):
            self.end_game(GameState.DRAW)
        elif self.board.is_dead_position():
            self.end_game(GameState.DRAW)
    
    def handle_resign(self):
        """Handle resignation"""
        if self.current_state == GameState.PLAYING:
            if self.current_player == Color.WHITE:
                self.end_game(GameState.BLACK_WIN)
            else:
                self.end_game(GameState.WHITE_WIN)
    
    def handle_draw_proposal(self):
        """Handle draw proposal"""
        if self.current_state == GameState.PLAYING:
            self.current_state = GameState.DRAW_PROPOSAL
            self.draw_proposer = self.current_player
    
    def end_game(self, state: GameState):
        """End the game"""
        self.current_state = state
        self.games_played += 1
        # Reset last_time to prevent time consumption during end-game dialogs
        if hasattr(self, 'last_time'):
            self.last_time = pygame.time.get_ticks()
    
    def reset_game(self):
        """Reset the game"""
        self.board = Board()
        self.current_player = Color.WHITE
        self.current_state = GameState.PLAYING
        self.white_time = INITIAL_TIME
        self.black_time = INITIAL_TIME
        self.turn_number = 0
        self.last_move = None
        self.selected_piece = None
        self.legal_moves = set()
        self.promotion_pending = False
        self.promotion_from_pos = None
        self.promotion_pos = None
        self.draw_proposer = None
        self.paused = False
        # Reset last_time so update_time reinitializes it properly
        if hasattr(self, 'last_time'):
            delattr(self, 'last_time')
    
    def update_time(self):
        """Update game timers"""
        if self.paused or self.current_state != GameState.PLAYING:
            return
        
        if not hasattr(self, 'last_time'):
            self.last_time = pygame.time.get_ticks()
            return
        
        current_time = pygame.time.get_ticks()
        elapsed = (current_time - self.last_time) / 1000.0
        self.last_time = current_time
        
        if self.current_player == Color.WHITE:
            self.white_time -= elapsed
        else:
            self.black_time -= elapsed
        
        # Check for timeout
        if self.white_time <= 0:
            self.end_game(GameState.BLACK_WIN)
        elif self.black_time <= 0:
            self.end_game(GameState.WHITE_WIN)
    
    def draw_board(self):
        """Draw the board"""
        for row in range(8):
            for col in range(8):
                color = CREAM if (row + col) % 2 == 0 else BROWN
                
                rect = pygame.Rect(
                    BOARD_START_X + col * SQUARE_SIZE,
                    BOARD_START_Y + row * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE
                )
                pygame.draw.rect(self.screen, color, rect)
                
                # Highlight last move
                if self.last_move:
                    if (row, col) == self.last_move[0] or (row, col) == self.last_move[1]:
                        pygame.draw.rect(self.screen, YELLOW, rect, 3)
                
                # Highlight check
                piece = self.board.get_piece(row, col)
                if piece and piece.type == PieceType.KING and \
                   self.board.is_king_in_check(piece.color):
                    pygame.draw.rect(self.screen, RED, rect, 3)
        
        # Draw pieces
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece:
                    self.screen.blit(
                        piece.image,
                        (BOARD_START_X + col * SQUARE_SIZE,
                         BOARD_START_Y + row * SQUARE_SIZE)
                    )
        
        # Draw legal moves
        if self.selected_piece:
            for move in self.legal_moves:
                center_x = BOARD_START_X + move[1] * SQUARE_SIZE + SQUARE_SIZE // 2
                center_y = BOARD_START_Y + move[0] * SQUARE_SIZE + SQUARE_SIZE // 2
                pygame.draw.circle(self.screen, YELLOW, (center_x, center_y), MOVE_HIGHLIGHT_RADIUS)
            
            # Highlight selected piece
            sel_row, sel_col = self.selected_piece
            sel_rect = pygame.Rect(
                BOARD_START_X + sel_col * SQUARE_SIZE,
                BOARD_START_Y + sel_row * SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE
            )
            pygame.draw.rect(self.screen, BLUE, sel_rect, 3)
    
    def draw_ui_panel(self):
        """Draw the UI panel"""
        # Background
        panel_rect = pygame.Rect(MARGIN, MARGIN, UI_PANEL_WIDTH - 2 * MARGIN, 
                                UI_PANEL_HEIGHT - 2 * MARGIN)
        pygame.draw.rect(self.screen, LIGHT_GRAY, panel_rect)
        pygame.draw.rect(self.screen, BLACK, panel_rect, 2)
        
        y_offset = MARGIN + 10
        
        # Turn info
        turn_text = f"Turn: {self.turn_number // 2 + 1}"
        player_text = "White" if self.current_player == Color.WHITE else "Black"
        
        turn_surf = self.font_medium.render(turn_text, True, BLACK)
        self.screen.blit(turn_surf, (MARGIN + 10, y_offset))
        
        player_surf = self.font_medium.render(f"Player: {player_text}", True, BLACK)
        self.screen.blit(player_surf, (MARGIN + 10, y_offset + 30))
        
        y_offset += 80
        
        # Black player UI
        black_label = self.font_medium.render("Black", True, BLACK)
        self.screen.blit(black_label, (MARGIN + 10, y_offset))
        
        black_time_str = self.format_time(self.black_time)
        black_time_surf = self.font_medium.render(black_time_str, True, BLACK)
        self.screen.blit(black_time_surf, (MARGIN + 10, y_offset + 30))
        
        y_offset += 80
        
        # Buttons
        button_width = UI_PANEL_WIDTH - 2 * MARGIN - 20
        button_height = 35
        button_x = MARGIN + 10
        
        buttons = ["Resign", "Draw", "Pause" if not self.paused else "Resume"]
        button_specs = [
            ("Resign", RED),
            ("Draw", YELLOW),
            ("Pause" if not self.paused else "Resume", BLUE)
        ]
        
        for i, (label, default_color) in enumerate(button_specs):
            button_y = y_offset + i * 40
            
            # Grey out buttons when game is not PLAYING
            if self.current_state != GameState.PLAYING:
                button_color = LIGHT_GRAY  # Greyed out
            else:
                button_color = default_color  # Normal color
            
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            pygame.draw.rect(self.screen, button_color, button_rect)
            pygame.draw.rect(self.screen, BLACK, button_rect, 2)
            
            button_text = self.font_small.render(label, True, BLACK)
            text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, text_rect)
        
        y_offset += 130
        
        # Reset button - use bright green to indicate it's always clickable
        reset_rect = pygame.Rect(button_x, y_offset, button_width, button_height)
        pygame.draw.rect(self.screen, (0, 200, 0), reset_rect)  # Bright green
        pygame.draw.rect(self.screen, BLACK, reset_rect, 2)
        reset_text = self.font_small.render("Reset", True, BLACK)
        reset_text_rect = reset_text.get_rect(center=reset_rect.center)
        self.screen.blit(reset_text, reset_text_rect)
        
        y_offset += 60
        
        # White player UI
        white_label = self.font_medium.render("White", True, BLACK)
        self.screen.blit(white_label, (MARGIN + 10, y_offset))
        
        white_time_str = self.format_time(self.white_time)
        white_time_surf = self.font_medium.render(white_time_str, True, BLACK)
        self.screen.blit(white_time_surf, (MARGIN + 10, y_offset + 30))
        
        # Footer
        footer_y = WINDOW_HEIGHT - MARGIN - 60
        footer_text = [
            "Claude Haiku 4.5",
            "Prompts: " + str(self.total_prompts),
            "Tokens: " + str(self.total_tokens),
            "@adbreeker © 2026"
        ]
        
        for i, text in enumerate(footer_text):
            footer_surf = self.font_small.render(text, True, BLACK)
            self.screen.blit(footer_surf, (MARGIN + 10, footer_y + i * 15))
    
    def format_time(self, seconds: float) -> str:
        """Format time in MM:SS"""
        minutes = int(seconds) // 60
        secs = int(seconds) % 60
        return f"{minutes:02d}:{secs:02d}"
    
    def draw_promotion_dialog(self):
        """Draw pawn promotion dialog"""
        if not self.promotion_pending or not self.promotion_pos:
            return
        
        dialog_width = 350
        dialog_height = 200
        dialog_x = (WINDOW_WIDTH - dialog_width) // 2
        dialog_y = (WINDOW_HEIGHT - dialog_height) // 2
        
        # Background
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
        pygame.draw.rect(self.screen, WHITE, dialog_rect)
        pygame.draw.rect(self.screen, BLACK, dialog_rect, 3)
        
        # Title
        title = self.font_medium.render("Promote Pawn to:", True, BLACK)
        self.screen.blit(title, (dialog_x + 20, dialog_y + 20))
        
        # Options
        options = [
            (PieceType.QUEEN, "Queen"),
            (PieceType.ROOK, "Rook"),
            (PieceType.BISHOP, "Bishop"),
            (PieceType.KNIGHT, "Knight"),
        ]
        
        option_width = 65
        option_height = 40
        total_width = option_width * 4 + 10 * 3  # 4 buttons + 3 gaps
        start_x = dialog_x + (dialog_width - total_width) // 2
        start_y = dialog_y + 80
        
        for i, (piece_type, label) in enumerate(options):
            option_x = start_x + i * (option_width + 10)
            option_rect = pygame.Rect(option_x, start_y, option_width, option_height)
            pygame.draw.rect(self.screen, BLUE, option_rect)
            pygame.draw.rect(self.screen, BLACK, option_rect, 2)
            
            option_text = self.font_small.render(label, True, BLACK)
            text_rect = option_text.get_rect(center=option_rect.center)
            self.screen.blit(option_text, text_rect)
    
    def handle_promotion_click(self, pos: Tuple[int, int]):
        """Handle click during promotion"""
        dialog_width = 350
        dialog_height = 200
        dialog_x = (WINDOW_WIDTH - dialog_width) // 2
        dialog_y = (WINDOW_HEIGHT - dialog_height) // 2
        
        options = [
            (PieceType.QUEEN, "Queen"),
            (PieceType.ROOK, "Rook"),
            (PieceType.BISHOP, "Bishop"),
            (PieceType.KNIGHT, "Knight"),
        ]
        
        option_width = 65
        option_height = 40
        total_width = option_width * 4 + 10 * 3  # 4 buttons + 3 gaps
        start_x = dialog_x + (dialog_width - total_width) // 2
        start_y = dialog_y + 80
        
        for i, (piece_type, label) in enumerate(options):
            option_x = start_x + i * (option_width + 10)
            option_rect = pygame.Rect(option_x, start_y, option_width, option_height)
            
            if option_rect.collidepoint(pos):
                # Get the pawn at the promotion square and replace it with promoted piece
                pawn = self.board.get_piece(self.promotion_pos[0], self.promotion_pos[1])
                if pawn:
                    promoted = Piece(piece_type, pawn.color)
                    promoted.has_moved = True
                    self.board.set_piece(self.promotion_pos[0], self.promotion_pos[1], promoted)
                    
                    # Add time bonus
                    if self.current_player == Color.WHITE:
                        self.white_time += TIME_BONUS
                    else:
                        self.black_time += TIME_BONUS
                    
                    # Check game state
                    self.check_game_state()
                    
                    # Switch player
                    if self.current_state == GameState.PLAYING:
                        self.current_player = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE
                        self.turn_number += 1
                
                self.promotion_pending = False
                self.promotion_pos = None
                self.promotion_from_pos = None
    
    def draw_game_over_screen(self):
        """Draw game over screen"""
        if self.current_state == GameState.PLAYING:
            return
        
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(DARK_GRAY)
        self.screen.blit(overlay, (0, 0))
        
        # Message box
        box_width = 400
        box_height = 150
        box_x = (WINDOW_WIDTH - box_width) // 2
        box_y = (WINDOW_HEIGHT - box_height) // 2
        
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(self.screen, WHITE, box_rect)
        pygame.draw.rect(self.screen, BLACK, box_rect, 3)
        
        # Game over message
        if self.current_state == GameState.WHITE_WIN:
            message = "White Wins!"
        elif self.current_state == GameState.BLACK_WIN:
            message = "Black Wins!"
        elif self.current_state == GameState.DRAW:
            message = "Draw!"
        elif self.current_state == GameState.DRAW_PROPOSAL:
            message = f"{self.draw_proposer.name} proposes draw"
        else:
            message = "Game Over"
        
        message_surf = self.font_large.render(message, True, BLACK)
        message_rect = message_surf.get_rect(
            center=(WINDOW_WIDTH // 2, box_y + 50)
        )
        self.screen.blit(message_surf, message_rect)
        
        # Instructions
        instr_text = "Click Reset button to play again"
        instr_surf = self.font_small.render(instr_text, True, BLACK)
        instr_rect = instr_surf.get_rect(
            center=(WINDOW_WIDTH // 2, box_y + 110)
        )
        self.screen.blit(instr_surf, instr_rect)
    
    def draw_draw_proposal_dialog(self):
        """Draw draw proposal dialog"""
        if self.current_state != GameState.DRAW_PROPOSAL:
            return
        
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(DARK_GRAY)
        self.screen.blit(overlay, (0, 0))
        
        # Dialog box
        box_width = 350
        box_height = 150
        box_x = (WINDOW_WIDTH - box_width) // 2
        box_y = (WINDOW_HEIGHT - box_height) // 2
        
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(self.screen, WHITE, box_rect)
        pygame.draw.rect(self.screen, BLACK, box_rect, 3)
        
        # Proposer name
        proposer_name = self.draw_proposer.name if self.draw_proposer else "Unknown"
        message = f"{proposer_name} proposes a draw"
        message_surf = self.font_medium.render(message, True, BLACK)
        self.screen.blit(message_surf, (box_x + 20, box_y + 30))
        
        # Buttons: Accept and Reject
        button_y = box_y + 80
        button_height = 40
        button_width = 100
        
        accept_rect = pygame.Rect(box_x + 30, button_y, button_width, button_height)
        pygame.draw.rect(self.screen, BLUE, accept_rect)
        pygame.draw.rect(self.screen, BLACK, accept_rect, 2)
        accept_text = self.font_small.render("Accept", True, BLACK)
        accept_text_rect = accept_text.get_rect(center=accept_rect.center)
        self.screen.blit(accept_text, accept_text_rect)
        
        reject_rect = pygame.Rect(box_x + 220, button_y, button_width, button_height)
        pygame.draw.rect(self.screen, RED, reject_rect)
        pygame.draw.rect(self.screen, BLACK, reject_rect, 2)
        reject_text = self.font_small.render("Reject", True, BLACK)
        reject_text_rect = reject_text.get_rect(center=reject_rect.center)
        self.screen.blit(reject_text, reject_text_rect)
    
    def draw(self):
        """Draw everything"""
        self.screen.fill(WHITE)
        
        # Draw board
        self.draw_board()
        
        # Draw promotion dialog if needed
        if self.promotion_pending:
            self.draw_promotion_dialog()
        
        # Draw game over screen
        self.draw_game_over_screen()
        
        # Draw draw proposal dialog
        self.draw_draw_proposal_dialog()
        
        # Draw UI panel LAST so it's always visible on top of overlays
        self.draw_ui_panel()
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.promotion_pending:
                        self.handle_promotion_click(event.pos)
                    elif self.current_state == GameState.DRAW_PROPOSAL:
                        self.handle_ui_click(event.pos)
                    else:
                        self.handle_click(event.pos)
            
            # Update
            self.update_time()
            
            # Draw
            self.draw()
            
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = ChessGame()
    game.run()
