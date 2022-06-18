import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIDTH2= 700
FRAME = pygame.display.set_mode((WIDTH2 , WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (139,71,93)
GREEN = (34,139,34)
BLUE = (51,161,201)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
DARKBLUE=(16,78,139)
PINK=(238,18,137)
OLIVE=(142,142,56)
BLUE1=(162,181,205)
BLUE2=(110,123,139)

button1= pygame.image.load('Reset.png').convert_alpha()
button2=pygame.image.load('Visualize.png').convert_alpha()


class Button:
	def __init__(self,x,y, image, scale_x,scale_y):

		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale_x), int(height * scale_y)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self):
		action = False
		position = pygame.mouse.get_pos()

		if self.rect.collidepoint(position):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action= True


		if pygame.mouse.get_pressed()[0]==0:
			self.clicked= False



		FRAME.blit(self.image, (self.rect.x, self.rect.y))

		return action


reset_button= Button(100,710,button1,0.5,0.5)
visualize_button= Button(400,710,button2,0.4,0.3)
rectangle = pygame.rect.Rect(14, 141, 14, 14)
rectangle_end = pygame.rect.Rect(140, 420, 14, 14)
bottom_rectangle= pygame.rect.Rect(0,702,700,98)


class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = BLUE1
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == OLIVE

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = BLUE1

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = OLIVE

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = BLUE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False




def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()





def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	pygame.draw.line(win, BLACK, (0, 700), (700, 700), width=2)
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i*gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw_start(win):
	pass



def draw(win, grid, rows, width):
	win.fill(BLUE2)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.draw.rect(win, DARKBLUE, bottom_rectangle)
	reset_button.draw()
	visualize_button.draw()
	pygame.draw.rect(win, PINK, rectangle)

	pygame.draw.rect(win, TURQUOISE, rectangle_end)
	pygame.display.flip()


def get_clicked_pos(pos, rows, width):
	gap = width // rows

	y, x = pos

	row = y // gap
	col = x // gap

	return row, col



def main(win, width,width2):

	FPS=30
	pygame.init()


	rectangle_draging = False
	rectangle_end_draging= False
	adjust=False
	clock = pygame.time.Clock()

	ROWS = 50
	gap2=width2//50
	grid = make_grid(ROWS, width2)


	row_start = int(rectangle.x / gap2)
	col_start = int(rectangle.y / gap2)
	row_end = int(rectangle_end.x / gap2)
	col_end = int(rectangle_end.y / gap2)
	start = grid[row_start][col_start]
	end = end = grid[row_end][col_end]
	run = True
	while run:
		draw(win, grid, ROWS, width2)
		# pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if rectangle.collidepoint(event.pos):
						rectangle_draging = True
					elif rectangle_end.collidepoint(event.pos):
						rectangle_end_draging = True


			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:

					rectangle_draging = False
					rectangle_end_draging= False


			if event.type == pygame.MOUSEMOTION:
				if rectangle_draging:
					pos = pygame.mouse.get_pos()
					row, col = get_clicked_pos(pos, ROWS, width2)

					if col<ROWS:
						#
						rectangle.x = row * gap2
						rectangle.y = col * gap2
						row_start = int(rectangle.x / gap2)
						col_start = int(rectangle.y / gap2)
						start = grid[row_start][col_start]

				elif rectangle_end_draging:
					pos = pygame.mouse.get_pos()
					row2, col2 = get_clicked_pos(pos, ROWS, width2)

					if col2<ROWS:
						rectangle_end.x = row2 * gap2
						rectangle_end.y = col2 * gap2
						row_end = int(rectangle_end.x / gap2)
						col_end = int(rectangle_end.y / gap2)
						end = grid[row_end][col_end]



			clock.tick(FPS)


			if pygame.mouse.get_pressed()[0] and (rectangle_draging == False and rectangle_end_draging== False): # LEFT

					pos = pygame.mouse.get_pos()
					row, col = get_clicked_pos(pos, ROWS, width2)

					if col<ROWS:

						# row_start=int(rectangle.x/gap2)
						# col_start=int(rectangle.y/gap2)
						spot = grid[row][col]
						if ((row !=row_start and col!=col_start) or (row!= row_end and col!=col_end)
								or (row!= row_start and col!=col_end)or (row!= row_end and col!=col_start)):
							spot.make_barrier()




			if pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width2)
				if col < ROWS:
					spot = grid[row][col]
					spot.reset()
					if spot == start:
						start = None
					elif spot == end:
						end = None

			if reset_button.draw():
				for row in range(ROWS):
					for col in range(ROWS):

						spot= grid[row][col]
						if spot.color == BLACK or spot.color == OLIVE or spot.color==GREEN or spot.color==BLUE:
							spot.reset()
						# if spot == start:
						# 	start = None
						# elif spot == end:
						# 	end = None


			if visualize_button.draw():
				for row in grid:
					for spot in row:
						x=1
						spot.update_neighbors(grid)

				algorithm(lambda: draw(win, grid, ROWS, width2), grid, start, end)
				adjust=True

			if adjust==True and (rectangle_draging==True or rectangle_end_draging==True) :
				for row in range(ROWS):
					for col in range(ROWS):

						spot= grid[row][col]
						if spot.color == OLIVE or spot.color==GREEN or spot.color==BLUE or spot.color==TURQUOISE:
							spot.reset()





			if event.type == pygame.KEYDOWN:
				# if event.key == pygame.K_SPACE and start and end:
				# 	for row in grid:
				# 		for spot in row:
				# 			spot.update_neighbors(grid)
				#
				# 	algorithm(lambda: draw(win, grid, ROWS, width2), grid, start, end)

				if event.key == pygame.K_x:
					start = None
					end = None
					grid = make_grid(ROWS, width2)



	pygame.quit()

main(FRAME, WIDTH,WIDTH2)