import os
from dataclasses import dataclass

import pygame


WINDOW_WIDTH = 896
WINDOW_HEIGHT = 576
FPS = 60

MARGIN = 32
PANEL_WIDTH = 256
PANEL_HEIGHT = 512
BOARD_GAP = 64
BOARD_SIZE = 512
SQUARE_SIZE = 64

PANEL_X = MARGIN
PANEL_Y = MARGIN
BOARD_X = PANEL_X + PANEL_WIDTH + BOARD_GAP
BOARD_Y = MARGIN

WHITE = (245, 245, 238)
BLACK = (25, 25, 25)
BG_COLOR = (230, 223, 213)
PANEL_BG = (244, 240, 233)
PANEL_BORDER = (120, 110, 95)
BOARD_LIGHT = (240, 217, 181)
BOARD_DARK = (181, 136, 99)

YELLOW = (245, 210, 50)
CHECK_RED = (210, 60, 60)
BUTTON = (168, 140, 110)
BUTTON_DISABLED = (185, 175, 162)
BUTTON_TEXT = (250, 247, 242)
BUTTON_ALT = (112, 130, 145)
BUTTON_DANGER = (158, 80, 75)
OVERLAY = (0, 0, 0, 130)

START_TIME_SECONDS = 10 * 60
MOVE_INCREMENT_SECONDS = 2


@dataclass(frozen=True)
class Move:
	fr: int
	fc: int
	tr: int
	tc: int
	piece: str
	captured: str | None = None
	is_en_passant: bool = False
	is_castle: bool = False
	promotion: bool = False


class ChessGame:
	def __init__(self) -> None:
		pygame.init()
		self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption("Chess - GPT-5.3-Codex")
		self.clock = pygame.time.Clock()

		self.font_title = pygame.font.SysFont("georgia", 24, bold=True)
		self.font_header = pygame.font.SysFont("georgia", 20, bold=True)
		self.font_text = pygame.font.SysFont("georgia", 18)
		self.font_small = pygame.font.SysFont("georgia", 14)
		self.font_button = pygame.font.SysFont("georgia", 17, bold=True)

		self.board_rect = pygame.Rect(BOARD_X, BOARD_Y, BOARD_SIZE, BOARD_SIZE)
		self.panel_rect = pygame.Rect(PANEL_X, PANEL_Y, PANEL_WIDTH, PANEL_HEIGHT)

		self.black_draw_rect = pygame.Rect(PANEL_X + 16, PANEL_Y + 134, 108, 32)
		self.black_resign_rect = pygame.Rect(PANEL_X + 132, PANEL_Y + 134, 108, 32)
		self.pause_rect = pygame.Rect(PANEL_X + 16, PANEL_Y + 266, 108, 32)
		self.reset_rect = pygame.Rect(PANEL_X + 132, PANEL_Y + 266, 108, 32)
		self.white_draw_rect = pygame.Rect(PANEL_X + 16, PANEL_Y + 374, 108, 32)
		self.white_resign_rect = pygame.Rect(PANEL_X + 132, PANEL_Y + 374, 108, 32)

		self.piece_images = self.load_piece_images()
		self.reset_game()

	def reset_game(self) -> None:
		self.board = self.create_initial_board()
		self.turn = "w"
		self.fullmove_number = 1
		self.selected_square: tuple[int, int] | None = None
		self.selected_moves: list[Move] = []
		self.last_move: tuple[tuple[int, int], tuple[int, int]] | None = None

		self.en_passant_target: tuple[int, int] | None = None
		self.castling_rights = {"wK": True, "wQ": True, "bK": True, "bQ": True}
		self.halfmove_clock = 0
		self.repetition_counts: dict[str, int] = {}

		self.white_time = float(START_TIME_SECONDS)
		self.black_time = float(START_TIME_SECONDS)
		self.timer_started = False

		self.paused = False
		self.game_over: dict[str, str] | None = None
		self.draw_proposal: dict[str, str] | None = None
		self.promotion_pending: dict[str, int | str | bool] | None = None

		self.add_current_position_to_history()

	@staticmethod
	def create_initial_board() -> list[list[str | None]]:
		return [
			["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
			["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
			[None, None, None, None, None, None, None, None],
			[None, None, None, None, None, None, None, None],
			[None, None, None, None, None, None, None, None],
			[None, None, None, None, None, None, None, None],
			["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
			["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
		]

	@staticmethod
	def opposite(color: str) -> str:
		return "b" if color == "w" else "w"

	@staticmethod
	def in_bounds(row: int, col: int) -> bool:
		return 0 <= row < 8 and 0 <= col < 8

	def load_piece_images(self) -> dict[str, pygame.Surface]:
		base_dir = os.path.dirname(os.path.abspath(__file__))
		project_dir = os.path.dirname(base_dir)
		pieces_dir = os.path.join(project_dir, "Pieces")

		file_map = {
			"wK": "WhiteKing.png",
			"wQ": "WhiteQueen.png",
			"wR": "WhiteRook.png",
			"wB": "WhiteBishop.png",
			"wN": "WhiteKnight.png",
			"wP": "WhitePawn.png",
			"bK": "BlackKing.png",
			"bQ": "BlackQueen.png",
			"bR": "BlackRook.png",
			"bB": "BlackBishop.png",
			"bN": "BlackKnight.png",
			"bP": "BlackPawn.png",
		}

		images: dict[str, pygame.Surface] = {}
		for piece, file_name in file_map.items():
			path = os.path.join(pieces_dir, file_name)
			try:
				image = pygame.image.load(path).convert_alpha()
				images[piece] = pygame.transform.smoothscale(image, (SQUARE_SIZE, SQUARE_SIZE))
			except pygame.error:
				fallback = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
				text = self.font_header.render(piece, True, BLACK)
				fallback.fill((255, 255, 255, 0))
				fallback.blit(
					text,
					(
						(SQUARE_SIZE - text.get_width()) // 2,
						(SQUARE_SIZE - text.get_height()) // 2,
					),
				)
				images[piece] = fallback

		return images

	def square_to_screen(self, row: int, col: int) -> tuple[int, int]:
		return BOARD_X + col * SQUARE_SIZE, BOARD_Y + row * SQUARE_SIZE

	def mouse_to_square(self, pos: tuple[int, int]) -> tuple[int, int] | None:
		if not self.board_rect.collidepoint(pos):
			return None
		x, y = pos
		col = (x - BOARD_X) // SQUARE_SIZE
		row = (y - BOARD_Y) // SQUARE_SIZE
		return row, col

	@staticmethod
	def square_color(row: int, col: int) -> int:
		return (row + col) % 2

	def serialize_position(self) -> str:
		rows = []
		for row in self.board:
			rows.append("".join(piece if piece else ".." for piece in row))
		castling = ""
		castling += "K" if self.castling_rights["wK"] else ""
		castling += "Q" if self.castling_rights["wQ"] else ""
		castling += "k" if self.castling_rights["bK"] else ""
		castling += "q" if self.castling_rights["bQ"] else ""
		if not castling:
			castling = "-"
		ep = "-"
		if self.en_passant_target:
			ep = self.algebraic(self.en_passant_target[0], self.en_passant_target[1])
		return f"{'/'.join(rows)} {self.turn} {castling} {ep}"

	def add_current_position_to_history(self) -> None:
		key = self.serialize_position()
		self.repetition_counts[key] = self.repetition_counts.get(key, 0) + 1

	@staticmethod
	def algebraic(row: int, col: int) -> str:
		return f"{chr(ord('a') + col)}{8 - row}"

	def find_king(self, board: list[list[str | None]], color: str) -> tuple[int, int] | None:
		king_piece = color + "K"
		for r in range(8):
			for c in range(8):
				if board[r][c] == king_piece:
					return r, c
		return None

	def is_square_attacked(
		self, board: list[list[str | None]], row: int, col: int, by_color: str
	) -> bool:
		pawn_row = row + (1 if by_color == "w" else -1)
		for dc in (-1, 1):
			pc = col + dc
			if self.in_bounds(pawn_row, pc):
				piece = board[pawn_row][pc]
				if piece == by_color + "P":
					return True

		knight_offsets = [
			(-2, -1),
			(-2, 1),
			(-1, -2),
			(-1, 2),
			(1, -2),
			(1, 2),
			(2, -1),
			(2, 1),
		]
		for dr, dc in knight_offsets:
			rr, cc = row + dr, col + dc
			if self.in_bounds(rr, cc):
				piece = board[rr][cc]
				if piece == by_color + "N":
					return True

		straight_dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
		for dr, dc in straight_dirs:
			rr, cc = row + dr, col + dc
			while self.in_bounds(rr, cc):
				piece = board[rr][cc]
				if piece:
					if piece[0] == by_color and piece[1] in ("R", "Q"):
						return True
					break
				rr += dr
				cc += dc

		diagonal_dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
		for dr, dc in diagonal_dirs:
			rr, cc = row + dr, col + dc
			while self.in_bounds(rr, cc):
				piece = board[rr][cc]
				if piece:
					if piece[0] == by_color and piece[1] in ("B", "Q"):
						return True
					break
				rr += dr
				cc += dc

		for dr in (-1, 0, 1):
			for dc in (-1, 0, 1):
				if dr == 0 and dc == 0:
					continue
				rr, cc = row + dr, col + dc
				if self.in_bounds(rr, cc):
					piece = board[rr][cc]
					if piece == by_color + "K":
						return True

		return False

	def is_in_check(self, board: list[list[str | None]], color: str) -> bool:
		king_pos = self.find_king(board, color)
		if king_pos is None:
			return False
		return self.is_square_attacked(board, king_pos[0], king_pos[1], self.opposite(color))

	def generate_piece_pseudo_moves(self, row: int, col: int) -> list[Move]:
		piece = self.board[row][col]
		if not piece:
			return []
		color, ptype = piece[0], piece[1]
		moves: list[Move] = []

		if ptype == "P":
			direction = -1 if color == "w" else 1
			start_row = 6 if color == "w" else 1
			one_step = row + direction

			if self.in_bounds(one_step, col) and self.board[one_step][col] is None:
				promote = one_step in (0, 7)
				moves.append(Move(row, col, one_step, col, piece, promotion=promote))
				two_step = row + 2 * direction
				if row == start_row and self.board[two_step][col] is None:
					moves.append(Move(row, col, two_step, col, piece))

			for dc in (-1, 1):
				tc = col + dc
				tr = row + direction
				if not self.in_bounds(tr, tc):
					continue
				target = self.board[tr][tc]
				if target and target[0] != color:
					promote = tr in (0, 7)
					moves.append(Move(row, col, tr, tc, piece, captured=target, promotion=promote))

				if self.en_passant_target == (tr, tc):
					side_piece = self.board[row][tc]
					if side_piece and side_piece == self.opposite(color) + "P":
						moves.append(
							Move(
								row,
								col,
								tr,
								tc,
								piece,
								captured=side_piece,
								is_en_passant=True,
							)
						)

		elif ptype == "N":
			for dr, dc in [
				(-2, -1),
				(-2, 1),
				(-1, -2),
				(-1, 2),
				(1, -2),
				(1, 2),
				(2, -1),
				(2, 1),
			]:
				rr, cc = row + dr, col + dc
				if not self.in_bounds(rr, cc):
					continue
				target = self.board[rr][cc]
				if target is None or target[0] != color:
					moves.append(Move(row, col, rr, cc, piece, captured=target))

		elif ptype in ("B", "R", "Q"):
			directions: list[tuple[int, int]] = []
			if ptype in ("B", "Q"):
				directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
			if ptype in ("R", "Q"):
				directions += [(-1, 0), (1, 0), (0, -1), (0, 1)]

			for dr, dc in directions:
				rr, cc = row + dr, col + dc
				while self.in_bounds(rr, cc):
					target = self.board[rr][cc]
					if target is None:
						moves.append(Move(row, col, rr, cc, piece))
					else:
						if target[0] != color:
							moves.append(Move(row, col, rr, cc, piece, captured=target))
						break
					rr += dr
					cc += dc

		elif ptype == "K":
			for dr in (-1, 0, 1):
				for dc in (-1, 0, 1):
					if dr == 0 and dc == 0:
						continue
					rr, cc = row + dr, col + dc
					if not self.in_bounds(rr, cc):
						continue
					target = self.board[rr][cc]
					if target is None or target[0] != color:
						moves.append(Move(row, col, rr, cc, piece, captured=target))

			if self.can_castle_kingside(color):
				home_row = 7 if color == "w" else 0
				moves.append(Move(home_row, 4, home_row, 6, piece, is_castle=True))
			if self.can_castle_queenside(color):
				home_row = 7 if color == "w" else 0
				moves.append(Move(home_row, 4, home_row, 2, piece, is_castle=True))

		return moves

	def can_castle_kingside(self, color: str) -> bool:
		key = color + "K"
		if not self.castling_rights.get(key, False):
			return False
		row = 7 if color == "w" else 0
		if self.board[row][4] != color + "K" or self.board[row][7] != color + "R":
			return False
		if self.board[row][5] is not None or self.board[row][6] is not None:
			return False
		if self.is_in_check(self.board, color):
			return False
		enemy = self.opposite(color)
		if self.is_square_attacked(self.board, row, 5, enemy):
			return False
		if self.is_square_attacked(self.board, row, 6, enemy):
			return False
		return True

	def can_castle_queenside(self, color: str) -> bool:
		key = color + "Q"
		if not self.castling_rights.get(key, False):
			return False
		row = 7 if color == "w" else 0
		if self.board[row][4] != color + "K" or self.board[row][0] != color + "R":
			return False
		if self.board[row][1] is not None or self.board[row][2] is not None or self.board[row][3] is not None:
			return False
		if self.is_in_check(self.board, color):
			return False
		enemy = self.opposite(color)
		if self.is_square_attacked(self.board, row, 3, enemy):
			return False
		if self.is_square_attacked(self.board, row, 2, enemy):
			return False
		return True

	def apply_move_on_position(
		self,
		board: list[list[str | None]],
		move: Move,
		castling_rights: dict[str, bool],
		en_passant_target: tuple[int, int] | None,
		promotion_choice: str | None = None,
	) -> tuple[bool, bool, tuple[int, int] | None]:
		piece = board[move.fr][move.fc]
		if piece is None:
			return False, False, en_passant_target

		target_piece = board[move.tr][move.tc]
		was_capture = target_piece is not None

		board[move.fr][move.fc] = None

		if move.is_en_passant:
			capture_row = move.tr + (1 if piece[0] == "w" else -1)
			captured_piece = board[capture_row][move.tc]
			board[capture_row][move.tc] = None
			if captured_piece:
				was_capture = True

		if move.is_castle:
			if move.tc == 6:
				rook_from = 7
				rook_to = 5
			else:
				rook_from = 0
				rook_to = 3
			board[move.tr][rook_to] = board[move.tr][rook_from]
			board[move.tr][rook_from] = None

		moved_piece = piece
		if move.promotion and promotion_choice:
			moved_piece = piece[0] + promotion_choice
		board[move.tr][move.tc] = moved_piece

		color = piece[0]
		ptype = piece[1]
		if ptype == "K":
			castling_rights[color + "K"] = False
			castling_rights[color + "Q"] = False
		elif ptype == "R":
			home = 7 if color == "w" else 0
			if move.fr == home and move.fc == 0:
				castling_rights[color + "Q"] = False
			if move.fr == home and move.fc == 7:
				castling_rights[color + "K"] = False

		if target_piece and target_piece[1] == "R":
			captured_color = target_piece[0]
			home = 7 if captured_color == "w" else 0
			if move.tr == home and move.tc == 0:
				castling_rights[captured_color + "Q"] = False
			if move.tr == home and move.tc == 7:
				castling_rights[captured_color + "K"] = False

		new_ep_target = None
		if ptype == "P" and abs(move.tr - move.fr) == 2:
			new_ep_target = ((move.tr + move.fr) // 2, move.fc)

		return was_capture, ptype == "P", new_ep_target

	def is_move_legal(self, move: Move, color: str) -> bool:
		board_copy = [r[:] for r in self.board]
		rights_copy = self.castling_rights.copy()
		self.apply_move_on_position(board_copy, move, rights_copy, self.en_passant_target)
		return not self.is_in_check(board_copy, color)

	def generate_legal_moves_for_color(self, color: str) -> list[Move]:
		legal_moves: list[Move] = []
		for r in range(8):
			for c in range(8):
				piece = self.board[r][c]
				if piece and piece[0] == color:
					for move in self.generate_piece_pseudo_moves(r, c):
						if self.is_move_legal(move, color):
							legal_moves.append(move)
		return legal_moves

	def get_moves_for_square(self, row: int, col: int) -> list[Move]:
		legal_moves = self.generate_legal_moves_for_color(self.turn)
		return [m for m in legal_moves if m.fr == row and m.fc == col]

	def commit_move(self, move: Move) -> None:
		mover = self.turn
		was_capture, was_pawn_move, new_ep_target = self.apply_move_on_position(
			self.board,
			move,
			self.castling_rights,
			self.en_passant_target,
		)

		self.en_passant_target = new_ep_target
		self.last_move = ((move.fr, move.fc), (move.tr, move.tc))
		self.selected_square = None
		self.selected_moves = []

		if move.promotion:
			self.promotion_pending = {
				"row": move.tr,
				"col": move.tc,
				"color": mover,
				"mover": mover,
				"was_capture": was_capture,
				"was_pawn_move": was_pawn_move,
			}
			return

		self.finish_turn(mover, was_capture, was_pawn_move)

	def finish_turn(self, mover: str, was_capture: bool, was_pawn_move: bool) -> None:
		if was_capture or was_pawn_move:
			self.halfmove_clock = 0
		else:
			self.halfmove_clock += 1

		if mover == "w":
			self.white_time += MOVE_INCREMENT_SECONDS
			if not self.timer_started:
				self.timer_started = True
		else:
			self.black_time += MOVE_INCREMENT_SECONDS
			self.fullmove_number += 1

		self.turn = self.opposite(mover)
		self.add_current_position_to_history()
		self.evaluate_end_conditions()

	def complete_promotion(self, choice: str) -> None:
		if not self.promotion_pending:
			return

		row = int(self.promotion_pending["row"])
		col = int(self.promotion_pending["col"])
		color = str(self.promotion_pending["color"])
		mover = str(self.promotion_pending["mover"])
		was_capture = bool(self.promotion_pending["was_capture"])
		was_pawn_move = bool(self.promotion_pending["was_pawn_move"])

		self.board[row][col] = color + choice
		self.promotion_pending = None
		self.finish_turn(mover, was_capture, was_pawn_move)

	def evaluate_end_conditions(self) -> None:
		if self.game_over:
			return

		legal_moves = self.generate_legal_moves_for_color(self.turn)
		if not legal_moves:
			if self.is_in_check(self.board, self.turn):
				winner = self.opposite(self.turn)
				self.set_win(winner, "Checkmate")
			else:
				self.set_draw("Stalemate")
			return

		if self.is_dead_position():
			self.set_draw("Dead position")
			return

		current_count = self.repetition_counts.get(self.serialize_position(), 0)
		if current_count >= 3:
			self.set_draw("Threefold repetition")
			return

		if self.halfmove_clock >= 100:
			self.set_draw("Fifty-move rule")

	def is_dead_position(self) -> bool:
		non_king_pieces: list[tuple[str, int, int]] = []
		for r in range(8):
			for c in range(8):
				piece = self.board[r][c]
				if piece and piece[1] != "K":
					non_king_pieces.append((piece, r, c))

		if not non_king_pieces:
			return True

		if len(non_king_pieces) == 1:
			return non_king_pieces[0][0][1] in ("B", "N")

		if len(non_king_pieces) == 2:
			a, b = non_king_pieces
			pa, pb = a[0], b[0]
			if pa[1] == "N" and pb[1] == "N" and pa[0] == pb[0]:
				return True
			if pa[1] == "B" and pb[1] == "B" and pa[0] != pb[0]:
				same_color_square = self.square_color(a[1], a[2]) == self.square_color(b[1], b[2])
				if same_color_square:
					return True

		return False

	def side_has_mating_material(self, color: str) -> bool:
		own_types: list[str] = []
		opp_non_king = False
		opp = self.opposite(color)

		for r in range(8):
			for c in range(8):
				piece = self.board[r][c]
				if not piece:
					continue
				if piece[0] == color and piece[1] != "K":
					own_types.append(piece[1])
				if piece[0] == opp and piece[1] != "K":
					opp_non_king = True

		if not own_types:
			return False
		if any(pt in ("Q", "R", "P") for pt in own_types):
			return True

		bishops = own_types.count("B")
		knights = own_types.count("N")

		if bishops >= 2:
			return True
		if bishops >= 1 and knights >= 1:
			return True
		if knights >= 2 and opp_non_king:
			return True

		return False

	def set_win(self, winner: str, reason: str) -> None:
		winner_name = "White" if winner == "w" else "Black"
		self.game_over = {
			"kind": "win",
			"title": f"{winner_name} wins",
			"reason": reason,
		}
		self.draw_proposal = None

	def set_draw(self, reason: str) -> None:
		self.game_over = {
			"kind": "draw",
			"title": "Draw",
			"reason": reason,
		}
		self.draw_proposal = None

	def offer_draw(self, proposer: str) -> None:
		if self.game_over or self.draw_proposal or self.promotion_pending:
			return
		if proposer != self.turn:
			return
		self.draw_proposal = {
			"proposer": proposer,
			"responder": self.opposite(proposer),
		}

	def respond_draw_offer(self, accepted: bool) -> None:
		if not self.draw_proposal:
			return
		if accepted:
			self.set_draw("Draw by agreement")
		else:
			self.draw_proposal = None

	def resign(self, color: str) -> None:
		if self.game_over or self.promotion_pending:
			return
		winner = self.opposite(color)
		if self.side_has_mating_material(winner):
			self.set_win(winner, "Resignation")
		else:
			self.set_draw("Resignation with insufficient mating material")

	def update_timers(self, dt: float) -> None:
		if not self.timer_started:
			return
		if self.paused or self.game_over or self.draw_proposal or self.promotion_pending:
			return

		if self.turn == "w":
			self.white_time = max(0.0, self.white_time - dt)
			if self.white_time <= 0.0:
				self.handle_flag_fall("w")
		else:
			self.black_time = max(0.0, self.black_time - dt)
			if self.black_time <= 0.0:
				self.handle_flag_fall("b")

	def handle_flag_fall(self, loser: str) -> None:
		if self.game_over:
			return
		winner = self.opposite(loser)
		if self.side_has_mating_material(winner):
			self.set_win(winner, "Win on time")
		else:
			self.set_draw("Timeout with insufficient mating material")

	def handle_board_click(self, pos: tuple[int, int]) -> None:
		if self.game_over or self.paused or self.draw_proposal or self.promotion_pending:
			return

		square = self.mouse_to_square(pos)
		if square is None:
			return

		row, col = square
		piece = self.board[row][col]

		if self.selected_square is not None:
			for move in self.selected_moves:
				if move.tr == row and move.tc == col:
					self.commit_move(move)
					return

		if piece and piece[0] == self.turn:
			self.selected_square = (row, col)
			self.selected_moves = self.get_moves_for_square(row, col)
		else:
			self.selected_square = None
			self.selected_moves = []

	def promotion_dialog_buttons(self) -> list[tuple[str, pygame.Rect]]:
		dialog_w = 330
		dialog_h = 150
		x = BOARD_X + (BOARD_SIZE - dialog_w) // 2
		y = BOARD_Y + (BOARD_SIZE - dialog_h) // 2

		button_w = 70
		button_h = 34
		gap = 10
		labels = ["Q", "R", "B", "N"]
		row_width = len(labels) * button_w + (len(labels) - 1) * gap
		start_x = x + (dialog_w - row_width) // 2
		btn_y = y + 90
		buttons: list[tuple[str, pygame.Rect]] = []
		for i, label in enumerate(labels):
			rect = pygame.Rect(start_x + i * (button_w + gap), btn_y, button_w, button_h)
			buttons.append((label, rect))
		return buttons

	def draw_offer_buttons(self) -> tuple[pygame.Rect, pygame.Rect]:
		dialog_w = 360
		dialog_h = 160
		x = BOARD_X + (BOARD_SIZE - dialog_w) // 2
		y = BOARD_Y + (BOARD_SIZE - dialog_h) // 2
		accept = pygame.Rect(x + 40, y + 96, 120, 36)
		refuse = pygame.Rect(x + 200, y + 96, 120, 36)
		return accept, refuse

	def handle_click(self, pos: tuple[int, int]) -> None:
		if self.draw_proposal:
			accept_rect, refuse_rect = self.draw_offer_buttons()
			if accept_rect.collidepoint(pos):
				self.respond_draw_offer(True)
				return
			if refuse_rect.collidepoint(pos):
				self.respond_draw_offer(False)
				return

		if self.promotion_pending:
			for label, rect in self.promotion_dialog_buttons():
				if rect.collidepoint(pos):
					self.complete_promotion(label)
					return

		if self.black_draw_rect.collidepoint(pos):
			self.offer_draw("b")
			return
		if self.black_resign_rect.collidepoint(pos):
			self.resign("b")
			return
		if self.pause_rect.collidepoint(pos):
			if not self.game_over:
				self.paused = not self.paused
			return
		if self.reset_rect.collidepoint(pos):
			self.reset_game()
			return
		if self.white_draw_rect.collidepoint(pos):
			self.offer_draw("w")
			return
		if self.white_resign_rect.collidepoint(pos):
			self.resign("w")
			return

		self.handle_board_click(pos)

	def format_time(self, value: float) -> str:
		total = int(max(0, value))
		minutes = total // 60
		seconds = total % 60
		return f"{minutes:02d}:{seconds:02d}"

	def draw_button(
		self,
		rect: pygame.Rect,
		text: str,
		enabled: bool,
		style: str = "normal",
	) -> None:
		color = BUTTON
		if style == "alt":
			color = BUTTON_ALT
		elif style == "danger":
			color = BUTTON_DANGER
		if not enabled:
			color = BUTTON_DISABLED

		pygame.draw.rect(self.screen, color, rect, border_radius=6)
		pygame.draw.rect(self.screen, (90, 80, 70), rect, 1, border_radius=6)
		label = self.font_button.render(text, True, BUTTON_TEXT if enabled else (230, 225, 218))
		self.screen.blit(
			label,
			(rect.x + (rect.width - label.get_width()) // 2, rect.y + (rect.height - label.get_height()) // 2),
		)

	def draw_board(self) -> None:
		for r in range(8):
			for c in range(8):
				sq_rect = pygame.Rect(
					BOARD_X + c * SQUARE_SIZE,
					BOARD_Y + r * SQUARE_SIZE,
					SQUARE_SIZE,
					SQUARE_SIZE,
				)
				color = BOARD_LIGHT if (r + c) % 2 == 0 else BOARD_DARK
				pygame.draw.rect(self.screen, color, sq_rect)

		if self.last_move:
			mark = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
			mark.fill((235, 220, 85, 120))
			(fr, fc), (tr, tc) = self.last_move
			fx, fy = self.square_to_screen(fr, fc)
			tx, ty = self.square_to_screen(tr, tc)
			self.screen.blit(mark, (fx, fy))
			self.screen.blit(mark, (tx, ty))

		for color in ("w", "b"):
			if self.is_in_check(self.board, color):
				king_pos = self.find_king(self.board, color)
				if king_pos:
					kx, ky = self.square_to_screen(king_pos[0], king_pos[1])
					check_rect = pygame.Rect(kx, ky, SQUARE_SIZE, SQUARE_SIZE)
					marker = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
					marker.fill((CHECK_RED[0], CHECK_RED[1], CHECK_RED[2], 130))
					self.screen.blit(marker, check_rect.topleft)

		for r in range(8):
			for c in range(8):
				piece = self.board[r][c]
				if piece:
					px, py = self.square_to_screen(r, c)
					self.screen.blit(self.piece_images[piece], (px, py))

		if self.selected_square:
			sr, sc = self.selected_square
			sx, sy = self.square_to_screen(sr, sc)
			pygame.draw.rect(self.screen, (70, 90, 120), (sx, sy, SQUARE_SIZE, SQUARE_SIZE), 3)

			for move in self.selected_moves:
				cx, cy = self.square_to_screen(move.tr, move.tc)
				center = (cx + SQUARE_SIZE // 2, cy + SQUARE_SIZE // 2)
				if move.captured or move.is_en_passant:
					pygame.draw.circle(self.screen, YELLOW, center, 18, 4)
				else:
					pygame.draw.circle(self.screen, YELLOW, center, 8)

		pygame.draw.rect(self.screen, (70, 60, 50), self.board_rect, 2)

	def draw_panel(self) -> None:
		def fit_footer_text(text: str) -> str:
			max_width = PANEL_WIDTH - 24
			if self.font_small.size(text)[0] <= max_width:
				return text
			trimmed = text
			while len(trimmed) > 3 and self.font_small.size(trimmed + "...")[0] > max_width:
				trimmed = trimmed[:-1]
			return trimmed + "..."

		pygame.draw.rect(self.screen, PANEL_BG, self.panel_rect, border_radius=10)
		pygame.draw.rect(self.screen, PANEL_BORDER, self.panel_rect, 2, border_radius=10)

		title = self.font_title.render("Chess", True, (70, 56, 38))
		self.screen.blit(title, (PANEL_X + 16, PANEL_Y + 10))

		turn_side = "White" if self.turn == "w" else "Black"
		turn_text = self.font_text.render(f"Turn {self.fullmove_number} - {turn_side}", True, BLACK)
		self.screen.blit(turn_text, (PANEL_X + 16, PANEL_Y + 44))

		black_header = self.font_header.render("Black", True, BLACK)
		self.screen.blit(black_header, (PANEL_X + 16, PANEL_Y + 86))
		black_timer = self.font_text.render(self.format_time(self.black_time), True, BLACK)
		self.screen.blit(black_timer, (PANEL_X + 140, PANEL_Y + 88))

		white_header = self.font_header.render("White", True, BLACK)
		self.screen.blit(white_header, (PANEL_X + 16, PANEL_Y + 326))
		white_timer = self.font_text.render(self.format_time(self.white_time), True, BLACK)
		self.screen.blit(white_timer, (PANEL_X + 140, PANEL_Y + 328))

		draw_enabled = not self.game_over and not self.draw_proposal and not self.promotion_pending
		black_draw_enabled = draw_enabled and self.turn == "b"
		white_draw_enabled = draw_enabled and self.turn == "w"

		resign_enabled = not self.game_over and not self.promotion_pending
		pause_enabled = not self.game_over
		reset_enabled = True

		self.draw_button(self.black_draw_rect, "Draw", black_draw_enabled)
		self.draw_button(self.black_resign_rect, "Resign", resign_enabled, "danger")

		self.draw_button(self.pause_rect, "Resume" if self.paused else "Pause", pause_enabled, "alt")
		self.draw_button(self.reset_rect, "Reset", reset_enabled)

		self.draw_button(self.white_draw_rect, "Draw", white_draw_enabled)
		self.draw_button(self.white_resign_rect, "Resign", resign_enabled, "danger")

		footer_y = PANEL_Y + 450
		footer_lines = [
			"Model: GPT-5.3-Codex",
			"Prompts/Tokens: 2 / 900 157",
			"@adbreeker 2026",
		]
		for i, line in enumerate(footer_lines):
			text = self.font_small.render(fit_footer_text(line), True, (45, 45, 45))
			self.screen.blit(text, (PANEL_X + 12, footer_y + 18 * i))

	def draw_draw_offer_overlay(self) -> None:
		if not self.draw_proposal:
			return

		overlay = pygame.Surface((BOARD_SIZE, BOARD_SIZE), pygame.SRCALPHA)
		overlay.fill(OVERLAY)
		self.screen.blit(overlay, (BOARD_X, BOARD_Y))

		dialog_w = 360
		dialog_h = 160
		x = BOARD_X + (BOARD_SIZE - dialog_w) // 2
		y = BOARD_Y + (BOARD_SIZE - dialog_h) // 2
		dialog_rect = pygame.Rect(x, y, dialog_w, dialog_h)
		pygame.draw.rect(self.screen, (245, 238, 227), dialog_rect, border_radius=10)
		pygame.draw.rect(self.screen, (85, 75, 62), dialog_rect, 2, border_radius=10)

		proposer = "White" if self.draw_proposal["proposer"] == "w" else "Black"
		responder = "White" if self.draw_proposal["responder"] == "w" else "Black"
		title = self.font_header.render("Draw Proposal", True, BLACK)
		line = self.font_text.render(f"{proposer} proposes. {responder}: accept?", True, BLACK)
		self.screen.blit(title, (x + (dialog_w - title.get_width()) // 2, y + 20))
		self.screen.blit(line, (x + (dialog_w - line.get_width()) // 2, y + 56))

		accept_rect, refuse_rect = self.draw_offer_buttons()
		self.draw_button(accept_rect, "Accept", True)
		self.draw_button(refuse_rect, "Refuse", True, "danger")

	def draw_promotion_overlay(self) -> None:
		if not self.promotion_pending:
			return

		overlay = pygame.Surface((BOARD_SIZE, BOARD_SIZE), pygame.SRCALPHA)
		overlay.fill(OVERLAY)
		self.screen.blit(overlay, (BOARD_X, BOARD_Y))

		dialog_w = 330
		dialog_h = 150
		x = BOARD_X + (BOARD_SIZE - dialog_w) // 2
		y = BOARD_Y + (BOARD_SIZE - dialog_h) // 2
		dialog_rect = pygame.Rect(x, y, dialog_w, dialog_h)
		pygame.draw.rect(self.screen, (245, 238, 227), dialog_rect, border_radius=10)
		pygame.draw.rect(self.screen, (85, 75, 62), dialog_rect, 2, border_radius=10)

		color = str(self.promotion_pending["color"])
		side = "White" if color == "w" else "Black"
		title = self.font_header.render("Promotion", True, BLACK)
		line = self.font_text.render(f"{side} pawn promotes to:", True, BLACK)
		self.screen.blit(title, (x + (dialog_w - title.get_width()) // 2, y + 18))
		self.screen.blit(line, (x + (dialog_w - line.get_width()) // 2, y + 52))

		for label, rect in self.promotion_dialog_buttons():
			piece_name = {"Q": "Queen", "R": "Rook", "B": "Bishop", "N": "Knight"}[label]
			self.draw_button(rect, piece_name, True)

	def draw_game_over_overlay(self) -> None:
		if not self.game_over:
			return

		overlay = pygame.Surface((BOARD_SIZE, BOARD_SIZE), pygame.SRCALPHA)
		overlay.fill(OVERLAY)
		self.screen.blit(overlay, (BOARD_X, BOARD_Y))

		dialog_w = 360
		dialog_h = 170
		x = BOARD_X + (BOARD_SIZE - dialog_w) // 2
		y = BOARD_Y + (BOARD_SIZE - dialog_h) // 2
		dialog_rect = pygame.Rect(x, y, dialog_w, dialog_h)
		pygame.draw.rect(self.screen, (245, 238, 227), dialog_rect, border_radius=10)
		pygame.draw.rect(self.screen, (85, 75, 62), dialog_rect, 2, border_radius=10)

		title = self.font_header.render(self.game_over["title"], True, BLACK)
		reason = self.font_text.render(self.game_over["reason"], True, BLACK)
		hint = self.font_small.render("Press Reset to start a new game", True, (55, 55, 55))

		self.screen.blit(title, (x + (dialog_w - title.get_width()) // 2, y + 30))
		self.screen.blit(reason, (x + (dialog_w - reason.get_width()) // 2, y + 72))
		self.screen.blit(hint, (x + (dialog_w - hint.get_width()) // 2, y + 116))

	def draw_pause_overlay(self) -> None:
		if not self.paused or self.game_over:
			return
		overlay = pygame.Surface((BOARD_SIZE, BOARD_SIZE), pygame.SRCALPHA)
		overlay.fill((0, 0, 0, 80))
		self.screen.blit(overlay, (BOARD_X, BOARD_Y))
		text = self.font_header.render("Paused", True, WHITE)
		self.screen.blit(
			text,
			(BOARD_X + (BOARD_SIZE - text.get_width()) // 2, BOARD_Y + (BOARD_SIZE - text.get_height()) // 2),
		)

	def render(self) -> None:
		self.screen.fill(BG_COLOR)
		self.draw_panel()
		self.draw_board()

		self.draw_pause_overlay()

		if self.draw_proposal:
			self.draw_draw_offer_overlay()
		elif self.promotion_pending:
			self.draw_promotion_overlay()
		elif self.game_over:
			self.draw_game_over_overlay()

		pygame.display.flip()

	def run(self) -> None:
		running = True
		while running:
			dt = self.clock.tick(FPS) / 1000.0

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					self.handle_click(event.pos)

			self.update_timers(dt)
			self.render()

		pygame.quit()


if __name__ == "__main__":
	ChessGame().run()
