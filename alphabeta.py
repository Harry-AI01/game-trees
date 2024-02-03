class OthelloGame:
    def __init__(self):
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        self.board[3][3] = self.board[4][4] = 'W'  # White pieces
        self.board[3][4] = self.board[4][3] = 'B'  # Black pieces
        self.player = 'B'  # Black starts the game
        self.directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def print_board(self):
        for row in self.board:
            print(' '.join(row))
        print()

    def flip_pieces(self, row, col, player):
        to_flip = []
        for d in self.directions:
            r, c = row + d[0], col + d[1]
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == ('W' if player == 'B' else 'B'):
                to_flip.append((r, c))
                r += d[0]
                c += d[1]
            if not (0 <= r < 8 and 0 <= c < 8) or self.board[r][c] != player:
                to_flip = []
            else:
                for fr, fc in to_flip:
                    self.board[fr][fc] = player
                self.board[row][col] = player
                return True  # Valid move
        return False

    def valid_moves(self, player):
        moves = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == '.' and self.flip_pieces(row, col, player, check_only=True):
                    moves.append((row, col))
        return moves

    def make_move(self, row, col, player):
        if self.flip_pieces(row, col, player):
            self.player = 'W' if self.player == 'B' else 'B'
            return True
        return False

    def has_moves(self, player):
        return bool(self.valid_moves(player))

    def game_over(self):
        return not self.has_moves('B') and not self.has_moves('W')

    def score(self, player):
        return sum(row.count(player) for row in self.board)

    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.game_over():
            return self.score(self.player) - self.score('W' if self.player == 'B' else 'B')
        
        if maximizing_player:
            max_eval = float('-inf')
            for move in self.valid_moves(self.player):
                self.make_move(*move, self.player)
                eval = self.minimax(depth - 1, alpha, beta, False)
                self.undo_move(move)  # Implement this method to revert move
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.valid_moves('W' if self.player == 'B' else 'B'):
                self.make_move(*move, 'W' if self.player == 'B' else 'B')
                eval = self.minimax(depth - 1, alpha, beta, True)
                self.undo_move(move)  # Implement this method to revert move
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def find_best_move(self, depth=3):
        best_eval = float('-inf')
        best_move = None
        for move in self.valid_moves(self.player):
            self.make_move(*move, self.player)
            eval = self.minimax(depth - 1, float('-inf'), float('inf'), False)
            self.undo_move(move)  # Implement this method to revert move
            if eval > best_eval:
                best_eval = eval
                best_move = move
        return best_move

# To play a game, you would instantiate an OthelloGame object and repeatedly call find_best
