class UIBoard:
    def __init__(self, bcontrol, area, screen):
        self.b_controller = bcontrol
        self.rows, self.cols = bcontrol.get_rowcols()
        self.area = area
        self.width, self.height = area
        self.small_width = self.width * 14/16
        self.small_height = self.height * 14/16

        self.time = '0:00'
        self.moves = 0

        self.game = pygame
        self.screen = screen
        self.font_numbers = self.game.font.Font(None, 60)
        self.font_text = self.game.font.Font(None, 60)
        self.font_info = self.game.font.Font(None, 24)
        self.font_score = self.game.font.Font(None, 24)

        self.GRAY = (185, 173, 160)
        self.GRAY2 = (238, 228, 218)
        self.GRAY3 = (205, 196, 179)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.ORANGE = (242, 177, 121)
        self.ORANGE2 = (245, 149, 99)
        self.RED = (245, 124, 95)
        self.RED2 = (247, 94, 60)
        self.YELLOW = (236, 206, 115)
        self.YELLOW2 = (236, 200, 80)
        self.YELLOW3 = (237, 204, 97)
        self.YELLOW4 = (237, 197, 63)
        self.YELLOW5 = (238, 194, 46)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 128, 0)

        self.values2colorsPiece = {	0: self.GRAY3,      2: self.GRAY2,      4: self.GRAY2,
                                    8: self.ORANGE,     16: self.ORANGE2,   32: self.RED,
                                    64: self.RED2,      128: self.YELLOW,   256: self.YELLOW2,
                                    512: self.YELLOW3,  1024: self.YELLOW4, 2048: self.YELLOW5 }
        self.values2colorsNumber = {0: self.WHITE,      2: self.BLACK,      4: self.BLACK,
                                    8: self.WHITE,      16: self.WHITE,     32: self.WHITE,
                                    64: self.WHITE,     128: self.WHITE,    256: self.WHITE,
                                    512: self.WHITE,    1024: self.WHITE,   2048: self.WHITE }

    def set_time_moves(self, t, m):
        self.time = t
        self.moves = m

    def print_board_values(self):

        b_values = self.b_controller.get_board_values()
        print(np.matrix(b_values))

    def print_base_screen(self):
        board = self.b_controller.get_board_values()

        self.screen.fill(self.WHITE)
        white_borderx = self.width*1/16
        white_bordery = self.height*1/16
        self.game.draw.rect(self.screen, self.GRAY, (white_borderx, white_bordery,
                                                    self.small_width, self.small_height))

        miniborderx = 1/32*self.small_width
        minibordery = 1/32*self.small_height
        #there will be 5 miniborders
        rectanglex = self.small_width*(32-5)/32 / self.cols
        rectangley = self.small_height*(32-5)/32 / self.rows
        for ind_r, r in enumerate(board):
            for ind_c, c in enumerate(r):
                x_pos =  white_borderx + (ind_c+1) * miniborderx + ind_c * rectanglex
                y_pos =  white_bordery + (ind_r+1) * minibordery + ind_r * rectangley

                rr = self.game.draw.rect(self.screen, self.values2colorsPiece[c], (x_pos, y_pos, rectanglex, rectangley), border_radius=3)

                if c != 0:
                    text_o = self.font_numbers.render(str(c), 0, self.values2colorsNumber[c])

                    textRect = text_o.get_rect()
                    textRect.center = (x_pos + rectanglex/2, y_pos + rectangley/2)
                    self.screen.blit(text_o, textRect)


        #score
        score = self.b_controller.get_score()
        text_score = self.font_score.render('Score: {}'.format(score), 0, self.BLACK)
        textRect = text_score.get_rect()
        textRect.x = white_borderx
        textRect.centery = white_bordery/2
        self.screen.blit(text_score, textRect)

        #time
        text_score = self.font_score.render(self.time, 0, self.GRAY)
        textRect = text_score.get_rect()
        textRect.left = self.width - white_borderx*2
        textRect.centery = self.height - white_bordery/2
        self.screen.blit(text_score, textRect)

        #moves
        text_score = self.font_score.render("{} moves".format(self.moves), 0, self.GRAY)
        textRect = text_score.get_rect()
        textRect.x = white_borderx
        textRect.centery = self.height - white_bordery/2
        self.screen.blit(text_score, textRect)

        self.game.display.update()


    def new_piece(self, row, col):
        self.print_base_screen()

        value_p = self.b_controller.get_board().get_piece(row, col).get_value()


        white_borderx = self.width*1/16
        white_bordery = self.height*1/16
        miniborderx = 1/32*self.small_width
        minibordery = 1/32*self.small_height
        rectanglex = self.small_width*(32-5)/32 / self.cols
        rectangley = self.small_height*(32-5)/32 / self.rows

        x_pos =  white_borderx + (col+1) * miniborderx + col * rectanglex
        y_pos =  white_bordery + (row+1) * minibordery + row * rectangley

        rect_full = self.game.Rect(x_pos, y_pos, rectanglex, rectangley)
        rr = self.game.draw.rect(self.screen, self.values2colorsPiece[0], rect_full, border_radius=3)

        divisions = 20
        ms2wait = 5
        for i in range(divisions):
            rect_grow = self.game.Rect(x_pos, y_pos, rectanglex*i/divisions, rectangley*i/divisions)
            rect_grow.center = rect_full.center

            rr = self.game.draw.rect(self.screen, self.values2colorsPiece[value_p], rect_grow, border_radius=3)
            self.game.display.update()

            self.game.time.wait(ms2wait)


    def print_ending(self, text, color_text):
        self.print_base_screen()
        center_screen_x = self.width / 2
        center_screen_y = self.height / 2

        self.game.draw.rect(self.screen, self.WHITE,
                            (self.width / 4 - 1, self.height * 3 / 8 - 1, self.width / 2 + 2, self.height / 4 + 2))
        self.game.draw.rect(self.screen, self.BLACK,
                            (self.width / 4, self.height * 3 / 8, self.width / 2, self.height / 4))

        text_o = self.textOutline(self.font_text, text, color_text, self.WHITE)

        textRect = text_o.get_rect()
        textRect.center = (self.width / 2, self.height / 2)
        self.screen.blit(text_o, textRect)
        self.game.display.update()

    def print_win(self):
        text = 'YOU WIN !!'
        self.print_ending(text, self.GREEN)

    def print_loss(self):
        text = 'YOU LOSE ...'
        self.print_ending(text, self.BLUE)

    def textOutline(self, font, message, fontcolor, outlinecolor):
        base = font.render(message, 0, fontcolor)
        outline = self.textHollow(font, message, outlinecolor)
        img = self.game.Surface(outline.get_size(), 16)
        img.blit(base, (1, 1))
        img.blit(outline, (0, 0))
        img.set_colorkey(0)
        return img

    def textHollow(self, font, message, fontcolor):
        notcolor = [c ^ 0xFF for c in fontcolor]
        base = font.render(message, 0, fontcolor, notcolor)
        size = base.get_width() + 2, base.get_height() + 2
        img = self.game.Surface(size, 16)
        img.fill(notcolor)
        base.set_colorkey(0)
        img.blit(base, (0, 0))
        img.blit(base, (2, 0))
        img.blit(base, (0, 2))
        img.blit(base, (2, 2))
        base.set_colorkey(0)
        base.set_palette_at(1, notcolor)
        img.blit(base, (1, 1))
        img.set_colorkey(notcolor)
        return img
