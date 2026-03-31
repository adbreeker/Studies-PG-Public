# Game Design Document

## Title: Chess
Chess is a board game for two players, played on a square board consisting of 64 squares arranged in an 8×8 grid. The players, referred to as "White" and "Black", each control sixteen pieces: one king, one queen, two rooks, two bishops, two knights, and eight pawns, with each piece type having a different pattern of movement. An enemy piece may be captured (removed from the board) by moving one's own piece onto the square it occupies. The object of the game is to "checkmate" (threaten with inescapable capture) the enemy king. There are also several ways a game can end in a draw.

## Setup
Chess sets come with pieces in two colors, referred to as white and black, regardless of their actual color; the players controlling the color sets are referred to as White and Black, respectively. Each set comes with at least the following 16 pieces in both colors: one king, one queen, two rooks, two bishops, two knights, and eight pawns.

The game is played on a square board of eight rows (called ranks) and eight columns (called files). Although it does not affect gameplay, by convention the 64 squares alternate in color and are referred to as light and dark squares.

To start the game, White's pieces are placed on the first rank in the following order, from left to right: rook, knight, bishop, queen, king, bishop, knight, rook. Pawns are placed on each square of the second rank. Black's position mirrors White's, with equivalent pieces on every file. The board is oriented so that the right-hand corner nearest each player is a light square; as a result the white queen always starts on a light square, while the black queen starts on a dark square. This may be remembered by the phrases "white on the right" and "queen on her color".

## Rules

### Movement

#### Player turn
White moves first, after which players alternate turns. One piece is moved per turn (except when castling, during which two pieces are moved). In the diagrams, dots mark the squares to which each type of piece can move if unoccupied by friendly pieces and there are no intervening piece(s) of either color (except the knight, which leaps over any intervening pieces). With the sole exception of en passant, a piece captures an enemy piece by moving to the square it occupies, removing it from play and taking its place. The pawn is the only piece that does not capture the way it moves, and it is the only piece that moves and captures in only one direction (forwards from the player's perspective). A piece is said to control empty squares on which it could capture, attack squares with enemy pieces it could capture, and defend squares with pieces of the same color on which it could recapture. Moving is compulsory; a player may not skip a turn, even when having to move is detrimental

#### Figures move patterns
- **King** moves one square in any direction. There is also a special move called castling which moves the king and a rook. The king is the most valuable piece—it is illegal to play any move that puts one's king under attack by an opponent piece. A move that attacks the king must be parried immediately; if this cannot be done, the game is lost. (See § Check and checkmate.)
    - **Castling:** Kings can castle once per game. Castling consists of moving the king two squares toward either rook of the same color, and then placing the rook on the square that the king crossed. Castling is possible only if the following conditions are met: Neither the king nor the rook has previously moved during the game. There are no pieces between the king and the rook. The king is not in check and does not pass through or finish on a square controlled by an enemy piece. Castling is still permitted if the rook is under attack, or if the rook crosses an attacked square. It is also still permitted if the king had been in check earlier in the game, provided that the check was resolved without moving the king.
- **Rook** can move any number of squares along a rank or file. A rook is involved in the king's castling move.
- **Bishop** can move any number of squares diagonally.
- **Queen** combines the power of a rook and bishop and can move any number of squares along a rank, file, or diagonal.
- **Knight** moves to any of the closest squares that are not on the same rank, file, or diagonal. (Thus the move forms an "L"-shape: two squares vertically and one square horizontally, or two squares horizontally and one square vertically.) The knight is the only piece that can leap over other pieces.
- **Pawn** can move forward to the unoccupied square immediately in front of it on the same file, or on its first move it can optionally advance two squares along the same file, provided both squares are unoccupied (diagram dots). A pawn can capture an opponent's piece on a square diagonally in front of it by moving to that square (diagram crosses). It cannot capture a piece while advancing along the same file, nor can it move to either square diagonally in front without capturing. Pawns have two special moves: the en passant capture and promotion.
    - **En passant capture:** when a pawn makes a two-square advance to the same rank as an opponent's pawn on an adjacent file, that pawn can capture it en passant ("in passing"), moving to one square behind the captured pawn. A pawn can only be captured en passant on the turn after it makes a two-square advance. In the animated diagram, the black pawn advances two squares from g7 to g5, and the white pawn on f5 takes it en passant, landing on g6.
    - **Promotion:** when a pawn advances to its last rank, it is promoted and replaced with the player's choice of a queen, rook, bishop, or knight. Usually, pawns are promoted to queens; choosing another piece is called underpromotion. In the animated diagram, the c7-pawn is advanced to c8 and promoted to a queen.

#### Check and checkmate
When a king is under immediate attack, it is in check. A move in response to a check is legal only if it results in a position in which the king is no longer in check. There are three ways to counter a check:
- Capture the checking piece.
- Interpose a piece between the checking piece and the king (possible only if the attacking piece is a queen, rook, or bishop and there is a square between it and the king).
- Move the king to a square where it is not under attack.

The object of the game is to checkmate the opponent; this occurs when the opponent's king is in check, and there is no legal way to get it out of check

### Time
Each player starts a game with 10 minutes. The time for each Player is counted only in their respective turns. Timer starts for the first time after initial move of white player.

After each move, the player that performed a move is awarded 2 seconds bonus to their current time.

### End of the game
Game can be finished in two ways: win or draw.

#### Win
A game can be won in the following ways:

- **Checkmate:** The opposing king is in check and no move can get it out of check. (See § Check and checkmate.)
- **Resignation:** A player may resign, conceding the game to the opponent. If, however, the opponent has no way of checkmating the resigned player, this is a draw under FIDE Laws. Most tournament players consider it good etiquette to resign in a hopeless position.
- **Win on time:** In games with a time control, a player wins if the opponent runs out of time, even if the opponent has a superior position, as long as the player has a theoretical possibility to checkmate the opponent were the game to continue.

#### Draw
There are several ways a game can end in a draw:

- **Stalemate:** If the player to move has no legal move, but is not in check, the position is a stalemate, and the game is drawn.
- **Dead position:** If neither player is able to checkmate the other by any legal sequence of moves, the game is drawn. For example, if only the kings are on the board, all other pieces having been captured, checkmate is impossible and the game is drawn by this rule. On the other hand, if each player still has a knight, there is a theoretical albeit highly unlikely possibility of checkmate, so this rule does not apply. The dead position rule supersedes an older rule that referred to "insufficient material", thereby extending it to include other positions in which checkmate is impossible, such as blocked pawn endings in which the pawns cannot be attacked.
- **Draw by agreement:** In tournament chess, draws are most commonly reached by mutual agreement between the players. The correct procedure is to make a move, to verbally offer the draw, and then to start the opponent's clock. If a draw is offered before making a move, the opponent has the right to ask the player to make a move before making their decision on whether or not to accept the draw offer. Traditionally, players were allowed to agree to a draw at any point in the game, occasionally even without having played a single move. Since the 2000s, efforts have been made to discourage early draws, for example by forbidding draw offers before a certain number of moves have been completed or even forbidding draw offers altogether.
- **Threefold repetition:** This most commonly occurs when neither side is able to avoid repeating moves without incurring a disadvantage. The three occurrences of the position need not occur on consecutive moves for a claim to be valid. The addition of the fivefold repetition rule in 2014 requires the arbiter to intervene immediately and declare the game a draw after five occurrences of the same position, consecutive or otherwise, without requiring a claim by either player. FIDE rules make no mention of perpetual check; this is merely a specific type of draw by threefold repetition.
- **Fifty-move rule:** If during the previous 50 moves no pawn has been moved and no capture has been made, either player can claim a draw. The addition of the seventy-five-move rule in 2014 requires the arbiter to intervene and immediately declare the game drawn after 75 moves without a pawn move or capture, without requiring a claim by either player. There are several known endgames in which it is possible to force a mate but it requires more than 50 moves before a pawn move or capture is made; examples include some endgames with two knights against a pawn and some pawnless endgames such as queen against two bishops. Historically, FIDE has sometimes revised the fifty-move rule to make exceptions for these endgames, but these exceptions have since been repealed. Some correspondence chess organizations do not enforce the fifty-move rule.

## Figures description

### King
1. **Icon:** ♔ / ♚
2. **Move pattern:** Diagonal and Orthogonal, 1 square
3. **Attack pattern:** Same as movement
4. **Special moves:** Castle
5. **Points worth:** infinity

### Queen
1. **Icon:** ♕ / ♛
2. **Move pattern:** Diagonal and Orthogonal, no limits
3. **Attack pattern:** Same as movement
4. **Special moves:** None
5. **Points worth:** 9

### Rook
1. **Icon:** ♖ / ♜
2. **Move pattern:** Orthogonal, no limits
3. **Attack pattern:** Same as movement
4. **Special moves:** Castle (if initiated by king)
5. **Points worth:** 5

### Bishop
1. **Icon:** ♗ / ♝
2. **Move pattern:** Diagonal, no limits
3. **Attack pattern:** Same as movement
4. **Special moves:** None
5. **Points worth:** 3

### Knight
1. **Icon:** ♘ / ♞
2. **Move pattern:** L shape, 2 + 1, cannot be blocked
3. **Attack pattern:** Same as movement
4. **Special moves:** None
5. **Points worth:** 3

### Pawn
1. **Icon:** ♙ / ♟
2. **Move pattern:** Orthogonally forward, 1 square or 2 square in first move
3. **Attack pattern:** Diagonally forward, 1 square
4. **Special moves:** En passant, Promotion
5. **Points worth:** 1

## Game vision
This version of chess game will be prepared based on this document, by AI agents only — no manual changes will be made in code. The goal is to create game of chess for two on-site player (no in-game AI included), as accurate as possible, with prompting only.

### Visuals
1. **Game window:** width-896p height-576p
2. **Board:** 8x8 creamy and brown squares, 64x64p per square
3. **Figures:** listed figures images (rescaled to 64x64p) from Project/Pieces/ directory, white bottom, black top

| Name | Icon | Path |
|------|------|------|
| White King | <img src="Pieces/WhiteKing.png" width="40"> | Pieces/WhiteKing.png |
| Black King | <img src="Pieces/BlackKing.png" width="40"> | Pieces/BlackKing.png |
| White Queen | <img src="Pieces/WhiteQueen.png" width="40"> | Pieces/WhiteQueen.png |
| Black Queen | <img src="Pieces/BlackQueen.png" width="40"> | Pieces/BlackQueen.png |
| White Rook | <img src="Pieces/WhiteRook.png" width="40"> | Pieces/WhiteRook.png |
| Black Rook | <img src="Pieces/BlackRook.png" width="40"> | Pieces/BlackRook.png |
| White Bishop | <img src="Pieces/WhiteBishop.png" width="40"> | Pieces/WhiteBishop.png |
| Black Bishop | <img src="Pieces/BlackBishop.png" width="40"> | Pieces/BlackBishop.png |
| White Knight | <img src="Pieces/WhiteKnight.png" width="40"> | Pieces/WhiteKnight.png |
| Black Knight | <img src="Pieces/BlackKnight.png" width="40"> | Pieces/BlackKnight.png |
| White Pawn | <img src="Pieces/WhitePawn.png" width="40"> | Pieces/WhitePawn.png |
| Black Pawn | <img src="Pieces/BlackPawn.png" width="40"> | Pieces/BlackPawn.png |

4. **Board UI:** possible movement marked with circles (yellow, 8p radius), check marked by highlighting checked square red, last movement marked by highlighting pre and post move squares yellow
5. **UI panel**: left of the board (with 64p break space), width-256p height-512p
6. **Margins:** 32p each side

### UI panel
1. **Turn:** turn number and who moves (white/black)
2. **Black Player UI:**
    - Timer
    - Draw and Resign button
3. **General UI:** pause/resume and reset buttons
4. **White Player UI:**
    - Timer
    - Draw and Resign button
5. **Footer:** with information in rows as follows:
    - AI model name and version used
    - Number of prompts and tokens used (only for manual updating at the end)
    - @adbreeker (linked to github.com/adbreeker) and current year (2026)

**Draw** requests should open an additional UI (announcing who is proposing and who is answering) to "Accept" or "Refuse" the draw.

Only one special state (Win, Draw, Draw proposal, or Resign) should be displayed at a time. All of these announcements should be centered relative to the Board, not the entire game window.

### Course of the game
Launching the application should open game window with UI on the left and set chess board with pieces on the right (as described in § Setup and § Visuals).

Then players take turns (with running time) making moves, consistent of:
1. Observe move of oponent (marked visuals of move and potential check),
2. Choose your figure to move,
3. See possible movement squares of the figure (including special moves, see § Movement),
4. Move or choose other figure,
5. Game should verify checks, check mates, promotions, etc. in the background,
6. Depending on background checks, game should act accordingly (announcing win, giving option for promotion, etc.),
7. If the game is not finished, turn should be ended, UI updated, and the player to move switched.

In the middle of turns, UI buttons for pausing, proposing draw, resigining and reseting the game should be fully accessible.