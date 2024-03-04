try:
    from PIL import Image, ImageDraw, ImageFont
except Exception:
    pass

from io import BytesIO
from random import choice


class TicTacToeAI:
    def __init__(self, player, opponent):
        self.player = player
        self.opponent = opponent

    def minimax(self, board, depth, is_maximizing):
        scores = {"X": -1, "O": 1, "Tie": 0}

        # winner = game.check_winner()
        # if winner:
        #     return scores[winner]

        if is_maximizing:
            max_eval = float("-inf")
            for i in range(3):
                for j in range(3):
                    if board[i][j] == " ":
                        board[i][j] = self.opponent
                        eval = self.minimax(board, depth + 1, False)
                        board[i][j] = " "
                        max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float("inf")
            for i in range(3):
                for j in range(3):
                    if board[i][j] == " ":
                        board[i][j] = self.player
                        eval = self.minimax(board, depth + 1, True)
                        board[i][j] = " "
                        min_eval = min(min_eval, eval)
            return min_eval

    def find_best_move(self, board):
        best_val = float("-inf")
        best_move = (-1, -1)

        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = self.opponent
                    move_val = self.minimax(board, 0, False)
                    board[i][j] = " "

                    if move_val > best_val:
                        best_move = (i, j)
                        best_val = move_val

        return best_move


class TicTacToeGame:
    def __init__(self):
        # اندازه تصویر و سلول‌ها
        self.image_size = 300
        self.cell_size = self.image_size // 3

        # ساخت تصویر
        self.image = Image.new("RGB", (self.image_size, self.image_size), "white")
        self.draw = ImageDraw.Draw(self.image)

        # اولین نمایش تصویر و خطوط
        self.draw_grid()

        # شماره‌گذاری سلول‌ها
        self.label_cells()

        # تخته بازی (ماتریس 3x3)
        self.board = [[" " for _ in range(3)] for _ in range(3)]

        # Set AI
        self.ai = TicTacToeAI(player="X", opponent="O")

    def draw_grid(self):
        for i in range(1, 3):
            x = i * self.cell_size
            self.draw.line([(x, 0), (x, self.image_size)], fill="black", width=4)
            self.draw.line([(0, x), (self.image_size, x)], fill="black", width=4)

    def draw_symbol(self, row, col, symbol, color):
        x = col * self.cell_size + self.cell_size // 2
        y = row * self.cell_size + self.cell_size // 2

        if symbol == "X":
            self.draw.line([(x - self.cell_size // 4, y - self.cell_size // 4),
                            (x + self.cell_size // 4, y + self.cell_size // 4)], fill=color, width=4)
            self.draw.line([(x + self.cell_size // 4, y - self.cell_size // 4),
                            (x - self.cell_size // 4, y + self.cell_size // 4)], fill=color, width=4)
        elif symbol == "O":
            self.draw.ellipse([(x - self.cell_size // 4, y - self.cell_size // 4),
                               (x + self.cell_size // 4, y + self.cell_size // 4)], outline=color, width=4)

    def label_cells(self):
        font_size = self.cell_size // 6  # اندازهٔ جدید فونت
        font = ImageFont.load_default(font_size)  # استفاده از فونت پیش‌فرض
        for i in range(3):
            for j in range(3):
                cell_number = i * 3 + j + 1
                x = j * self.cell_size + 3 * self.cell_size // 4
                y = i * self.cell_size + self.cell_size // 4
                # نمایش شماره بدون دایره
                text_size = self.draw.textbbox((0, 0), str(cell_number), font=font)
                text_position = (x - text_size[2] // 2, y - text_size[3] // 2)
                self.draw.text(text_position, str(cell_number), fill="black", font=font)

    def get_image(self):
        buffer = BytesIO()
        # ذخیره تصویر بازی
        self.image.save(buffer, format='PNG', quality=100, optimize=True)
        return buffer.getvalue()

    def display_board(self):
        # نمایش تصویر فعلی
        self.image.show()

    def save_board_image(self, file_name):
        # ذخیره تصویر فعلی
        self.image.save(file_name)

    def play_move(self, row, col, symbol):
        # انجام حرکت و رسم نماد در تصویر
        color = "red" if symbol == "X" else "blue"
        self.board[row][col] = symbol
        self.draw_symbol(row, col, symbol, color)

    def check_winner(self):
        # بررسی برنده بودن در سطرها و ستون‌ها
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != " ":
                return self.board[i][0]  # برنده در سطر
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != " ":
                return self.board[0][i]  # برنده در ستون

        # بررسی برنده بودن در قطرها
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            return self.board[0][0]  # برنده در قطر اصلی
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            return self.board[0][2]  # برنده در قطر فرعی

        return None  # برنده نداریم

# # شیء بازی Tic-Tac-Toe
# game = TicTacToeGame()

# # نمایش تصویر اولیه
# game.display_board()
# print(game.get_image())
# # بازی Tic-Tac-Toe با وارد کردن اعداد 1 تا 9
# for _ in range(9):
#     # ورود حرکت از کاربر
#     number = int(input("Enter a number (1 to 9): "))
#     symbol = "X" if _ % 2 == 0 else "O"
#     row = (number - 1) // 3
#     col = (number - 1) % 3
#     game.play_move(row, col, symbol)
#     # بررسی برنده بودن
#     winner = game.check_winner()
#     if winner:
#         print(f"Player '{winner}' wins!")
#         break

# # ذخیره تصویر نهایی
# game.save_board_image("tic_tac_toe_final.png")
