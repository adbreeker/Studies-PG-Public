import pygame
import sys
import os
import copy
import time

pygame.init()
pygame.font.init()

# Visuals
WINDOW_WIDTH = 896
WINDOW_HEIGHT = 576
SQUARE_SIZE = 64
BOARD_MARGIN_X = 352
BOARD_MARGIN_Y = 32
UI_MARGIN_X = 32
UI_MARGIN_Y = 32

COLOR_LIGHT = (245, 222, 179)
COLOR_DARK = (139, 69, 19)
COLOR_BG = (40, 40, 40)
COLOR_PANEL = (60, 60, 60)
COLOR_TEXT = (255, 255, 255)
COLOR_BUTTON = (100, 100, 100)

FONT_LARGE = pygame.font.SysFont("Arial", 22, bold=True)
FONT_MEDIUM = pygame.font.SysFont("Arial", 16)
FONT_SMALL = pygame.font.SysFont("Arial", 12)

class ChessGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Chess - Gemini 3.1 Pro")
        self.clock = pygame.time.Clock()
        self.running = True
        self.load_images()
        self.reset_game()

    def reset_game(self):
        self.board = self.create_initial_board()
        self.turn = "white"
        self.turn_number = 1
        self.selected_square = None
        self.valid_moves = []
        self.last_move = None
        
        self.en_passant_target = None # (r, c)
        self.promotion_state = None # {"pos": (r, c), "color": color}
        
        self.white_time = 600.0
        self.black_time = 600.0
        self.timer_started = False
        self.last_time = time.time()
        self.game_over = False
        self.end_message = ""
        self.paused = False
        self.draw_proposal = None

    def load_images(self):
        self.pieces_images = {}
        pieces = ["WhiteKing", "BlackKing", "WhiteQueen", "BlackQueen",
                  "WhiteRook", "BlackRook", "WhiteBishop", "BlackBishop",
                  "WhiteKnight", "BlackKnight", "WhitePawn", "BlackPawn"]
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pieces_dir = os.path.join(base_dir, "Pieces")
        for piece in pieces:
            path = os.path.join(pieces_dir, piece + ".png")
            if os.path.exists(path):
                img = pygame.image.load(path)
                self.pieces_images[piece] = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
            else:
                surf = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                col = (255,255,255) if "White" in piece else (0,0,0)
                pygame.draw.circle(surf, col, (32, 32), 20)
                self.pieces_images[piece] = surf

    def create_initial_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]
        order = ["Rook", "Knight", "Bishop", "Queen", "King", "Bishop", "Knight", "Rook"]
        for c in range(8):
            board[0][c] = {"color": "black", "type": order[c], "has_moved": False}
            board[1][c] = {"color": "black", "type": "Pawn", "has_moved": False}
            board[6][c] = {"color": "white", "type": "Pawn", "has_moved": False}
            board[7][c] = {"color": "white", "type": order[c], "has_moved": False}
        return board

    def handle_click(self, pos):
        x, y = pos
        
        # Handle Promotion Selection
        if self.promotion_state:
            # Draw promotion options horizontally centered on the board
            px = BOARD_MARGIN_X + 128
            py = BOARD_MARGIN_Y + 256
            if py <= y <= py + SQUARE_SIZE:
                opts = ["Queen", "Rook", "Bishop", "Knight"]
                for i in range(4):
                    if px + i*SQUARE_SIZE <= x <= px + (i+1)*SQUARE_SIZE:
                        pr, pc = self.promotion_state["pos"]
                        self.board[pr][pc]["type"] = opts[i]
                        self.promotion_state = None
                        self.end_turn()
                        return
            return

        # Handle Draw Proposal
        if self.draw_proposal:
            if BOARD_MARGIN_X + 150 <= x <= BOARD_MARGIN_X + 250 and BOARD_MARGIN_Y + 280 <= y <= BOARD_MARGIN_Y + 310:
                self.game_over = True
                self.end_message = "Draw by agreement"
                self.draw_proposal = None
            elif BOARD_MARGIN_X + 260 <= x <= BOARD_MARGIN_X + 360 and BOARD_MARGIN_Y + 280 <= y <= BOARD_MARGIN_Y + 310:
                self.draw_proposal = None
            return

        # Handle Board Clicks
        if BOARD_MARGIN_X <= x < BOARD_MARGIN_X + 512 and BOARD_MARGIN_Y <= y < BOARD_MARGIN_Y + 512:
            if not self.game_over and not self.paused:
                col = (x - BOARD_MARGIN_X) // SQUARE_SIZE
                row = (y - BOARD_MARGIN_Y) // SQUARE_SIZE
                self.process_board_click(row, col)
                
        # Handle UI Clicks
        if UI_MARGIN_X <= x <= UI_MARGIN_X + 256:
            # UI symmetrically arranged: Top=Black, Mid=General, Bot=White
            # Black Box: 50 -> 130
            if y >= UI_MARGIN_Y + 80 and y <= UI_MARGIN_Y + 100:  # Black Draw
                if not self.game_over and not self.paused: self.draw_proposal = "black"
            if y >= UI_MARGIN_Y + 110 and y <= UI_MARGIN_Y + 130: # Black Resign
                if not self.game_over and not self.paused: 
                    self.game_over = True
                    self.end_message = "White wins by Resignation"
            
            # Gen Box: 200 -> 270
            if y >= UI_MARGIN_Y + 200 and y <= UI_MARGIN_Y + 230: # Pause
                if not self.game_over: self.paused = not self.paused
            if y >= UI_MARGIN_Y + 240 and y <= UI_MARGIN_Y + 270: # Reset
                self.reset_game()
                
            # White Box: 380 -> 460
            if y >= UI_MARGIN_Y + 410 and y <= UI_MARGIN_Y + 430: # White Draw
                if not self.game_over and not self.paused: self.draw_proposal = "white"
            if y >= UI_MARGIN_Y + 440 and y <= UI_MARGIN_Y + 460: # White Resign
                if not self.game_over and not self.paused: 
                    self.game_over = True
                    self.end_message = "Black wins by Resignation"

    def process_board_click(self, row, col):
        piece = self.board[row][col]
        if self.selected_square:
            if (row, col) in self.valid_moves:
                self.execute_move(self.selected_square, (row, col))
                self.selected_square = None
                self.valid_moves = []
            else:
                if piece and piece["color"] == self.turn:
                    self.selected_square = (row, col)
                    self.valid_moves = self.get_legal_moves(row, col)
                else:
                    self.selected_square = None
                    self.valid_moves = []
        else:
            if piece and piece["color"] == self.turn:
                self.selected_square = (row, col)
                self.valid_moves = self.get_legal_moves(row, col)

    def execute_move(self, start, end):
        r1, c1 = start
        r2, c2 = end
        moving_piece = self.board[r1][c1]
        
        # En passant execution
        if moving_piece["type"] == "Pawn" and c1 != c2 and self.board[r2][c2] is None:
            self.board[r1][c2] = None # capture the pawn
            
        # Castling execution
        if moving_piece["type"] == "King" and abs(c2 - c1) == 2:
            if c2 > c1: # Kingside
                rook = self.board[r1][7]
                self.board[r1][7] = None
                self.board[r1][c2-1] = rook
                rook["has_moved"] = True
            else: # Queenside
                rook = self.board[r1][0]
                self.board[r1][0] = None
                self.board[r1][c2+1] = rook
                rook["has_moved"] = True

        self.board[r2][c2] = moving_piece
        self.board[r1][c1] = None
        moving_piece["has_moved"] = True
        self.last_move = (start, end)
        
        # Set En Passant target
        self.en_passant_target = None
        if moving_piece["type"] == "Pawn" and abs(r2 - r1) == 2:
            self.en_passant_target = ((r1 + r2) // 2, c1)
            
        # Promotion Check
        if moving_piece["type"] == "Pawn" and (r2 == 0 or r2 == 7):
            self.promotion_state = {"pos": (r2, c2), "color": moving_piece["color"]}
            return # Delay turn switch until promotion resolved

        self.end_turn()
        
    def end_turn(self):
        if not self.timer_started and self.turn == "white":
            self.timer_started = True
            self.last_time = time.time()
            
        if self.timer_started:
            if self.turn == "white":
                self.white_time += 2.0
            else:
                self.black_time += 2.0
                
        if self.turn == "black":
            self.turn_number += 1
        
        self.turn = "black" if self.turn == "white" else "white"
        
        self.check_game_over()

    def check_game_over(self):
        # Determine if current player has any legal moves
        has_moves = False
        for r in range(8):
            for c in range(8):
                if self.board[r][c] and self.board[r][c]["color"] == self.turn:
                    if len(self.get_legal_moves(r, c)) > 0:
                        has_moves = True
                        break
            if has_moves: break
            
        if not has_moves:
            self.game_over = True
            if self.is_in_check(self.turn):
                winner = "Black" if self.turn == "white" else "White"
                self.end_message = f"{winner} wins by Checkmate!"
            else:
                self.end_message = "Draw by Stalemate"

    def is_in_check(self, color):
        king_pos = None
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p and p["type"] == "King" and p["color"] == color:
                    king_pos = (r, c)
                    break
            if king_pos: break
            
        if not king_pos: return False
        
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p and p["color"] != color:
                    moves = self.get_pseudo_legal_moves(r, c, ignore_castling=True)
                    if king_pos in moves:
                        return True
        return False

    def get_legal_moves(self, r, c):
        pseudo_moves = self.get_pseudo_legal_moves(r, c)
        legal_moves = []
        piece = self.board[r][c]
        color = piece["color"]
        
        for mr, mc in pseudo_moves:
            # Simulate
            target_piece = self.board[mr][mc]
            self.board[r][c] = None
            self.board[mr][mc] = piece
            
            ep_captured = None
            if piece["type"] == "Pawn" and c != mc and target_piece is None:
                ep_captured = self.board[r][mc]
                self.board[r][mc] = None
                
            in_check = self.is_in_check(color)
            
            # Undo
            self.board[r][c] = piece
            self.board[mr][mc] = target_piece
            if ep_captured:
                self.board[r][mc] = ep_captured
                
            if not in_check:
                legal_moves.append((mr, mc))
                
        # Add castling if King
        if piece["type"] == "King" and not piece.get("has_moved", False) and not self.is_in_check(color):
            # Kingside
            if self.board[r][7] and self.board[r][7]["type"] == "Rook" and not self.board[r][7].get("has_moved", False):
                if self.board[r][5] is None and self.board[r][6] is None:
                    # check path 
                    if (r, 5) in legal_moves: # if king can move to 5 legally
                        # Also check if moving to 6 is legal
                        self.board[r][c] = None
                        self.board[r][6] = piece
                        if not self.is_in_check(color):
                            legal_moves.append((r, c+2))
                        self.board[r][6] = None
                        self.board[r][c] = piece
                        
            # Queenside
            if self.board[r][0] and self.board[r][0]["type"] == "Rook" and not self.board[r][0].get("has_moved", False):
                if self.board[r][1] is None and self.board[r][2] is None and self.board[r][3] is None:
                    if (r, 3) in legal_moves:
                        self.board[r][c] = None
                        self.board[r][2] = piece
                        if not self.is_in_check(color):
                            legal_moves.append((r, c-2))
                        self.board[r][2] = None
                        self.board[r][c] = piece

        return legal_moves

    def get_pseudo_legal_moves(self, r, c, ignore_castling=False):
        moves = []
        piece = self.board[r][c]
        if not piece: return moves
        ptype = piece["type"]
        color = piece["color"]
        
        dirs = []
        if ptype in ["Rook", "Queen"]:
            dirs += [(0,1), (1,0), (0,-1), (-1,0)]
        if ptype in ["Bishop", "Queen"]:
            dirs += [(1,1), (1,-1), (-1,1), (-1,-1)]
            
        if ptype in ["Rook", "Bishop", "Queen"]:
            for dr, dc in dirs:
                nr, nc = r+dr, c+dc
                while 0<=nr<8 and 0<=nc<8:
                    if not self.board[nr][nc]:
                        moves.append((nr, nc))
                    elif self.board[nr][nc]["color"] != color:
                        moves.append((nr, nc))
                        break
                    else:
                        break
                    nr += dr
                    nc += dc
                    
        if ptype == "Knight":
            for dr, dc in [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]:
                nr, nc = r+dr, c+dc
                if 0<=nr<8 and 0<=nc<8:
                    if not self.board[nr][nc] or self.board[nr][nc]["color"] != color:
                        moves.append((nr, nc))
                        
        if ptype == "King":
            for dr in [-1,0,1]:
                for dc in [-1,0,1]:
                    if dr==0 and dc==0: continue
                    nr, nc = r+dr, c+dc
                    if 0<=nr<8 and 0<=nc<8:
                        if not self.board[nr][nc] or self.board[nr][nc]["color"] != color:
                            moves.append((nr, nc))
                            
        if ptype == "Pawn":
            dir_r = -1 if color == "white" else 1
            start_r = 6 if color == "white" else 1
            if 0 <= r+dir_r < 8 and not self.board[r+dir_r][c]:
                moves.append((r+dir_r, c))
                if r == start_r and not self.board[r+2*dir_r][c]:
                    moves.append((r+2*dir_r, c))
            for dc in [-1, 1]:
                if 0 <= r+dir_r < 8 and 0 <= c+dc < 8:
                    tgt = self.board[r+dir_r][c+dc]
                    if tgt and tgt["color"] != color:
                        moves.append((r+dir_r, c+dc))
                    elif self.en_passant_target == (r+dir_r, c+dc):
                        moves.append((r+dir_r, c+dc))
                        
        return moves

    def update(self):
        if self.timer_started and not self.game_over and not self.paused and self.promotion_state is None and self.draw_proposal is None:
            now = time.time()
            dt = now - self.last_time
            self.last_time = now
            if self.turn == "white":
                self.white_time -= dt
                if self.white_time <= 0:
                    self.white_time = 0
                    self.game_over = True
                    self.end_message = "Black wins on time!"
            else:
                self.black_time -= dt
                if self.black_time <= 0:
                    self.black_time = 0
                    self.game_over = True
                    self.end_message = "White wins on time!"
        else:
            self.last_time = time.time()

    def draw(self):
        self.screen.fill(COLOR_BG)
        self.draw_ui()
        self.draw_board()
        self.draw_overlays()
        pygame.display.flip()

    def draw_ui(self):
        pygame.draw.rect(self.screen, COLOR_PANEL, (UI_MARGIN_X, UI_MARGIN_Y, 256, 512))
        
        # Turn Text
        turn_text = FONT_LARGE.render(f"Turn {self.turn_number}: {self.turn.capitalize()}", True, COLOR_TEXT)
        self.screen.blit(turn_text, (UI_MARGIN_X + 10, UI_MARGIN_Y + 10))
        
        # Black UI (Top Half)
        b_time_str = f"{int(self.black_time)//60:02d}:{int(self.black_time)%60:02d}"
        self.screen.blit(FONT_MEDIUM.render(f"Black time: {b_time_str}", True, COLOR_TEXT), (UI_MARGIN_X + 10, UI_MARGIN_Y + 50))
        
        pygame.draw.rect(self.screen, COLOR_BUTTON, (UI_MARGIN_X + 10, UI_MARGIN_Y + 80, 100, 20))
        self.screen.blit(FONT_SMALL.render("Propose Draw", True, COLOR_TEXT), (UI_MARGIN_X + 15, UI_MARGIN_Y + 82))
        
        pygame.draw.rect(self.screen, COLOR_BUTTON, (UI_MARGIN_X + 10, UI_MARGIN_Y + 110, 100, 20))
        self.screen.blit(FONT_SMALL.render("Resign", True, COLOR_TEXT), (UI_MARGIN_X + 15, UI_MARGIN_Y + 112))
        
        # General Buttons (Middle)
        pygame.draw.rect(self.screen, COLOR_BUTTON, (UI_MARGIN_X + 10, UI_MARGIN_Y + 200, 100, 30))
        pts_txt = "Resume" if self.paused else "Pause"
        self.screen.blit(FONT_MEDIUM.render(pts_txt, True, COLOR_TEXT), (UI_MARGIN_X + 25, UI_MARGIN_Y + 205))
        
        pygame.draw.rect(self.screen, COLOR_BUTTON, (UI_MARGIN_X + 10, UI_MARGIN_Y + 240, 100, 30))
        self.screen.blit(FONT_MEDIUM.render("Reset", True, COLOR_TEXT), (UI_MARGIN_X + 25, UI_MARGIN_Y + 245))
        
        # White UI (Bottom Half)
        w_time_str = f"{int(self.white_time)//60:02d}:{int(self.white_time)%60:02d}"
        self.screen.blit(FONT_MEDIUM.render(f"White time: {w_time_str}", True, COLOR_TEXT), (UI_MARGIN_X + 10, UI_MARGIN_Y + 370))
        
        pygame.draw.rect(self.screen, COLOR_BUTTON, (UI_MARGIN_X + 10, UI_MARGIN_Y + 400, 100, 20))
        self.screen.blit(FONT_SMALL.render("Propose Draw", True, COLOR_TEXT), (UI_MARGIN_X + 15, UI_MARGIN_Y + 402))
        
        pygame.draw.rect(self.screen, COLOR_BUTTON, (UI_MARGIN_X + 10, UI_MARGIN_Y + 430, 100, 20))
        self.screen.blit(FONT_SMALL.render("Resign", True, COLOR_TEXT), (UI_MARGIN_X + 15, UI_MARGIN_Y + 432))
        
        # Footer
        self.screen.blit(FONT_SMALL.render("AI: Gemini 3.1 Pro", True, (150,150,150)), (UI_MARGIN_X + 5, UI_MARGIN_Y + 462))
        self.screen.blit(FONT_SMALL.render("Prompts: 3 | Tokens: 1123267", True, (150,150,150)), (UI_MARGIN_X + 5, UI_MARGIN_Y + 478))
        self.screen.blit(FONT_SMALL.render("@adbreeker 2026", True, (150,150,150)), (UI_MARGIN_X + 5, UI_MARGIN_Y + 494))

    def draw_board(self):
        in_check_pos = None
        if self.is_in_check(self.turn):
            for r in range(8):
                for c in range(8):
                    p = self.board[r][c]
                    if p and p["type"] == "King" and p["color"] == self.turn:
                        in_check_pos = (r, c)
                        break
                if in_check_pos: break

        for r in range(8):
            for c in range(8):
                rect = (BOARD_MARGIN_X + c * SQUARE_SIZE, BOARD_MARGIN_Y + r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                color = COLOR_LIGHT if (r + c) % 2 == 0 else COLOR_DARK
                pygame.draw.rect(self.screen, color, rect)
                
                if self.last_move and ((r,c) == self.last_move[0] or (r,c) == self.last_move[1]):
                    s = pygame.Surface((SQUARE_SIZE,SQUARE_SIZE), pygame.SRCALPHA)
                    s.fill((255, 255, 0, 100))
                    self.screen.blit(s, rect[:2])
                    
                if in_check_pos == (r, c):
                    s = pygame.Surface((SQUARE_SIZE,SQUARE_SIZE), pygame.SRCALPHA)
                    s.fill((255, 0, 0, 150))
                    self.screen.blit(s, rect[:2])
                
                piece = self.board[r][c]
                if piece:
                    name = piece["color"].capitalize() + piece["type"]
                    if name in self.pieces_images:
                        self.screen.blit(self.pieces_images[name], rect[:2])
                        
        if self.selected_square:
            sr, sc = self.selected_square
            s = pygame.Surface((SQUARE_SIZE,SQUARE_SIZE), pygame.SRCALPHA)
            s.fill((0, 255, 0, 100))
            self.screen.blit(s, (BOARD_MARGIN_X + sc * SQUARE_SIZE, BOARD_MARGIN_Y + sr * SQUARE_SIZE))
            
            for (vr, vc) in self.valid_moves:
                pygame.draw.circle(self.screen, (255, 255, 0, 200),
                                   (BOARD_MARGIN_X + vc * SQUARE_SIZE + 32, BOARD_MARGIN_Y + vr * SQUARE_SIZE + 32), 8)

    def draw_overlays(self):
        # Promotion overlay
        if self.promotion_state:
            px = BOARD_MARGIN_X + 128
            py = BOARD_MARGIN_Y + 256
            pygame.draw.rect(self.screen, COLOR_BG, (px, py, 4*SQUARE_SIZE, SQUARE_SIZE))
            color_prefix = self.promotion_state["color"].capitalize()
            opts = ["Queen", "Rook", "Bishop", "Knight"]
            for i, opt in enumerate(opts):
                p_img = self.pieces_images.get(color_prefix + opt)
                if p_img:
                    self.screen.blit(p_img, (px + i*SQUARE_SIZE, py))
            pygame.draw.rect(self.screen, (255,255,255), (px, py, 4*SQUARE_SIZE, SQUARE_SIZE), 2)
            
        elif self.game_over:
            txt = FONT_LARGE.render(self.end_message, True, (255,50,50))
            bg = pygame.Surface((txt.get_width()+20, txt.get_height()+20))
            bg.fill(COLOR_BG)
            bx, by = BOARD_MARGIN_X + 256 - txt.get_width()//2, BOARD_MARGIN_Y + 256
            self.screen.blit(bg, (bx-10, by-10))
            self.screen.blit(txt, (bx, by))
        elif self.draw_proposal:
            txt = FONT_LARGE.render(f"{self.draw_proposal.capitalize()} proposes draw!", True, (255,200,50))
            bx, by = BOARD_MARGIN_X + 256 - txt.get_width()//2, BOARD_MARGIN_Y + 230
            bg = pygame.Surface((300, 100))
            bg.fill(COLOR_BG)
            self.screen.blit(bg, (BOARD_MARGIN_X + 100, BOARD_MARGIN_Y + 220))
            self.screen.blit(txt, (bx, by))
            
            pygame.draw.rect(self.screen, (100,200,100), (BOARD_MARGIN_X + 150, BOARD_MARGIN_Y + 280, 100, 30))
            self.screen.blit(FONT_MEDIUM.render("Accept", True, COLOR_BG), (BOARD_MARGIN_X + 175, BOARD_MARGIN_Y + 285))
            pygame.draw.rect(self.screen, (200,100,100), (BOARD_MARGIN_X + 260, BOARD_MARGIN_Y + 280, 100, 30))
            self.screen.blit(FONT_MEDIUM.render("Refuse", True, COLOR_BG), (BOARD_MARGIN_X + 285, BOARD_MARGIN_Y + 285))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)
            self.update()
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    ChessGame().run()
    pygame.quit()
    sys.exit()
