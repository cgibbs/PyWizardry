import pygame
import random
import time

SCREEN_WIDTH = SCREEN_HEIGHT = 800

# constants to draw backgrounds of walls and floors

LEFT_WALL  	= [(0,0), (0,600), (200,400), (200,0)]
RIGHT_WALL 	= [(800,0), (800,600), (600,400), (600,0)]
GROUND     	= [(0,600), (200,400), (600,400), (800,600)]
BACK		= [(200,0), (200,400), (600,400), (600,0)]

#constants to draw doors

LEFT_DOOR	= [(50,350), (50,550), (150,450), (150,250)]
RIGHT_DOOR	= [(650,250), (650,450), (750,550), (750,350)]
FRONT_DOOR	= [(300,200),	(300,400), (500,400), (500,200)]

# map constants
MAP_WIDTH = 20
MAP_HEIGHT = 20

map = []

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

# mode constants
EXPLORE = 0
BATTLE = 1

# colors

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0, 100)
BLUE = (0,0,255)

pygame.init()
text12 = pygame.font.Font("freesansbold.ttf", 12)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Player:
	def __init__(self, x, y, facing):
		self.x = x
		self.y = y
		self.facing = facing

	def turn_right(self):
		self.facing += 1
		if self.facing > 3:
			self.facing = 0

	def turn_left(self):
		self.facing -= 1
		if self.facing < 0:
			self.facing = 3

	def p_move(self, dir):
		(self.x, self.y) = move(self.x,self.y,dir)
		map[self.x][self.y].visited = True
		

player = Player(0,0,NORTH)

class Room:
	def __init__(self):
		self.open_edges = 4
		self.n_door = False
		self.e_door = False
		self.w_door = False
		self.s_door = False
		self.visited = False
		self.virgin = True # used for map generation

	def draw_room(self, facing):
		screen.fill((0,0,0))

		pygame.draw.polygon(screen, (100,100,100), LEFT_WALL)
		pygame.draw.polygon(screen, (100,100,100), RIGHT_WALL)
		pygame.draw.polygon(screen, (200,200,200), GROUND)
		pygame.draw.polygon(screen, (220,220,220), BACK)

		if facing == NORTH:
			if self.w_door:
				pygame.draw.polygon(screen, (160, 80, 42), LEFT_DOOR)
			if self.n_door:
				pygame.draw.polygon(screen, (160, 80, 42), FRONT_DOOR)
			if self.e_door:
				pygame.draw.polygon(screen, (160, 80, 42), RIGHT_DOOR)
		elif facing == EAST:
			if self.n_door:
				pygame.draw.polygon(screen, (160, 80, 42), LEFT_DOOR)
			if self.e_door:
				pygame.draw.polygon(screen, (160, 80, 42), FRONT_DOOR)
			if self.s_door:
				pygame.draw.polygon(screen, (160, 80, 42), RIGHT_DOOR)
		elif facing == SOUTH:
			if self.e_door:
				pygame.draw.polygon(screen, (160, 80, 42), LEFT_DOOR)
			if self.s_door:
				pygame.draw.polygon(screen, (160, 80, 42), FRONT_DOOR)
			if self.w_door:
				pygame.draw.polygon(screen, (160, 80, 42), RIGHT_DOOR)
		elif facing == WEST:
			if self.s_door:
				pygame.draw.polygon(screen, (160, 80, 42), LEFT_DOOR)
			if self.w_door:
				pygame.draw.polygon(screen, (160, 80, 42), FRONT_DOOR)
			if self.n_door:
				pygame.draw.polygon(screen, (160, 80, 42), RIGHT_DOOR)

def toggle_door(x,y,door):
	global map
	room = map[x][y]
	door_bool = False
	if door == NORTH and y > 0:
		door_bool = room.n_door = map[x][y-1].s_door = not room.n_door
	elif door == EAST and x < MAP_WIDTH - 1:
		door_bool = room.e_door = map[x+1][y].w_door = not room.e_door
	elif door == SOUTH and y < MAP_HEIGHT - 1:
		door_bool = room.s_door = map[x][y+1].n_door = not room.s_door
	elif door == WEST and x > 0:
		door_bool = room.w_door = map[x-1][y].e_door = not room.w_door

	room.open_edges += (-1)**door_bool # +1 or -1, depending on door_bool
	if room.virgin == True:
		room.virgin = False

"""def list_avail_doors(x,y):
	doors = []
	if y > 0 and map[x][y].n_door == False:
		doors.append(NORTH)
	if x < MAP_WIDTH - 1 and map[x][y].e_door == False:
		doors.append(EAST)
	if y < MAP_HEIGHT - 1 and map[x][y].s_door == False:
		doors.append(SOUTH)
	if x > 0 and map[x][y].w_door == False:
		doors.append(WEST)
	return doors"""

def list_avail_doors(x,y):
	doors = []
	if y > 0 and map[x][y-1].virgin == True:
		doors.append(NORTH)
	if x < MAP_WIDTH - 1 and map[x+1][y].virgin == True:
		doors.append(EAST)
	if y < MAP_HEIGHT - 1 and map[x][y+1].virgin == True:
		doors.append(SOUTH)
	if x > 0 and map[x-1][y].virgin == True:
		doors.append(WEST)
	return doors

def move(x,y,dir):
	if dir % 2 == 0:
		y += (dir - 1)
	else:
		x -= (dir - 2)
	return (x,y)

def make_map():
	# "drunken" depth-first search 
	global map, player
	map = [[Room() for y in range(MAP_HEIGHT) ] for x in range(MAP_WIDTH) ]
	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			if x == 0 or x == MAP_WIDTH:
				map[x][y].open_edges -= 1
			if y == 0 or y == MAP_HEIGHT:
				map[x][y].open_edges -= 1

	stk = []

	x = random.randint(0, MAP_WIDTH - 1)
	y = random.randint(0, MAP_HEIGHT - 1)
	pick = 0

	toggle_door(x,y,NORTH)
	print map[x][y-1].virgin

	player.x = x
	player.y = y
	player.facing = NORTH
	map[x][y].visited = True

	x2 = y2 = 0

	print (x,y)

	i = 0

	stk.append((x,y))

	#while True:
	while len(stk) != 0:
		i += 1

		doors = list_avail_doors(x,y)
		if len(doors) > 1:
			pick = random.choice(doors)
		else:
			if len(stk) != 0:
				(x,y) = stk.pop()
				#print "stack popped, new coords:", (x,y)
				continue
			else:
				break

		(x2,y2) = move(x,y,pick)

		if len(list_avail_doors(x2,y2)) != 0:
			while map[x2][y2].virgin != True:
				if len(doors) > 1:
					doors.remove(pick)
					pick = random.choice(doors)
					(x2,y2) = move(x,y,pick)
				else:
				#	print "breaking, len(doors) > 1, coords:", (x,y)
					if len(stk) != 0:
						(x,y) = stk.pop()
						continue# need to skip back to top of main while
					else:
						return
					break

			if len(doors) > 1:
				#print "toggling door, coords:", (x,y,pick)
				toggle_door(x,y,pick)
				(x,y) = (x2, y2) #tabbed in

		else:
			if len(stk) != 0:
				(x,y) = stk.pop()
				#print "popping stack, new coords:", (x,y)
			else:
				#print "stack empty, finishing"
				break

		if len(doors) > 1:
			#print "appending to stack:", (x2,y2)
			stk.append((x2,y2))
	print i

def draw_map():
	# hard-coded for 800x800, 20x20 rooms for now
	pygame.draw.line(screen, WHITE, (0, 800), (200, 800))
	pygame.draw.line(screen, WHITE, (200, 600), (200, 800))
	for y in range(MAP_HEIGHT):
		pygame.draw.line(screen, WHITE, (0 + y*10, 600), (0 + y*10, 800))
		pygame.draw.line(screen, WHITE, (0, 600 + y*10), (200, 600 + y*10))

	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			if map[x][y].n_door == True:
				pygame.draw.line(screen, GREEN, (0 + x * 10 + 3, 600 + y * 10 + 1),
												(0 + x * 10 + 7, 600 + y * 10 + 1))
			if map[x][y].e_door == True:
				pygame.draw.line(screen, GREEN, (0 + (x + 1) * 10 - 1, 600 + y * 10 + 3),
												(0 + (x + 1) * 10 - 1, 600 + y * 10 + 7))
			if map[x][y].s_door == True:
				pygame.draw.line(screen, GREEN, (0 + x * 10 + 3, 600 + (y + 1) * 10 - 1),
												(0 + x * 10 + 7, 600 + (y + 1) * 10 - 1))
			if map[x][y].w_door == True:
				pygame.draw.line(screen, GREEN, (0 + x * 10 + 1, 600 + y * 10 + 3),
												(0 + x * 10 + 1, 600 + y * 10 + 7))
			if player.x == x and player.y == y:
				pygame.draw.rect(screen, (0,255,255), pygame.Rect((0 + x * 10 + 3, 600 + y * 10 + 3),
															(5,5)))

def draw_map_open_doors():
	# hard-coded for 800x800, 20x20 rooms for now
	pygame.draw.line(screen, WHITE, (0, 800), (200, 800))
	pygame.draw.line(screen, WHITE, (200, 600), (200, 800))
	for y in range(MAP_HEIGHT):
		pygame.draw.line(screen, WHITE, (0 + y*10, 600), (0 + y*10, 800))
		pygame.draw.line(screen, WHITE, (0, 600 + y*10), (200, 600 + y*10))

	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			if map[x][y].n_door == True:
				pygame.draw.line(screen, BLACK, (0 + x * 10 + 3, 600 + y * 10),
												(0 + x * 10 + 7, 600 + y * 10))
			if map[x][y].e_door == True:
				pygame.draw.line(screen, BLACK, (0 + (x + 1) * 10, 600 + y * 10 + 3),
												(0 + (x + 1) * 10, 600 + y * 10 + 7))
			if map[x][y].s_door == True:
				pygame.draw.line(screen, BLACK, (0 + x * 10 + 3, 600 + (y + 1) * 10),
												(0 + x * 10 + 7, 600 + (y + 1) * 10))
			if map[x][y].w_door == True:
				pygame.draw.line(screen, BLACK, (0 + x * 10, 600 + y * 10 + 3),
												(0 + x * 10, 600 + y * 10 + 7))
			if player.x == x and player.y == y:
				pygame.draw.rect(screen, (0,255,255), pygame.Rect((0 + x * 10 + 3, 600 + y * 10 + 3),
															(5,5)))

def draw_map_open_walls():
	# hard-coded for 800x800, 20x20 rooms for now
	pygame.draw.line(screen, WHITE, (0, 800), (200, 800))
	pygame.draw.line(screen, WHITE, (200, 600), (200, 800))
	for y in range(MAP_HEIGHT):
		pygame.draw.line(screen, WHITE, (0 + y*10, 600), (0 + y*10, 800))
		pygame.draw.line(screen, WHITE, (0, 600 + y*10), (200, 600 + y*10))

	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			# TODO: once everything's working, add a test for "room explored"
			#if map[x][y].virgin == True:
			#	pygame.draw.rect(screen, WHITE, (0 + x * 10 + 1, 600 + y * 10 + 1,9,9))
			if map[x][y].n_door == True:
				pygame.draw.line(screen, BLACK, (0 + x * 10 + 1, 600 + y * 10),
												(0 + x * 10 + 9, 600 + y * 10))
			if map[x][y].e_door == True:
				pygame.draw.line(screen, BLACK, (0 + (x + 1) * 10, 600 + y * 10 + 1),
												(0 + (x + 1) * 10, 600 + y * 10 + 9))
			if map[x][y].s_door == True:
				pygame.draw.line(screen, BLACK, (0 + x * 10 + 1, 600 + (y + 1) * 10),
												(0 + x * 10 + 9, 600 + (y + 1) * 10))
			if map[x][y].w_door == True:
				pygame.draw.line(screen, BLACK, (0 + x * 10, 600 + y * 10 + 1),
												(0 + x * 10, 600 + y * 10 + 9))
			if player.x == x and player.y == y:
				pygame.draw.rect(screen, (0,255,255), pygame.Rect((0 + x * 10 + 3, 600 + y * 10 + 3),
															(5,5)))

def draw_map_od_fog():
	# hard-coded for 800x800, 20x20 rooms for now
	pygame.draw.line(screen, WHITE, (0, 800), (200, 800))
	pygame.draw.line(screen, WHITE, (200, 600), (200, 800))
	for y in range(MAP_HEIGHT):
		pygame.draw.line(screen, WHITE, (0 + y*10, 600), (0 + y*10, 800))
		pygame.draw.line(screen, WHITE, (0, 600 + y*10), (200, 600 + y*10))

	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			room = map[x][y]
			if room.visited == True:
				if room.n_door == True:
					pygame.draw.line(screen, BLACK, (0 + x * 10 + 3, 600 + y * 10),
													(0 + x * 10 + 7, 600 + y * 10))
				if room.e_door == True:
					pygame.draw.line(screen, BLACK, (0 + (x + 1) * 10, 600 + y * 10 + 3),
													(0 + (x + 1) * 10, 600 + y * 10 + 7))
				if room.s_door == True:
					pygame.draw.line(screen, BLACK, (0 + x * 10 + 3, 600 + (y + 1) * 10),
													(0 + x * 10 + 7, 600 + (y + 1) * 10))
				if room.w_door == True:
					pygame.draw.line(screen, BLACK, (0 + x * 10, 600 + y * 10 + 3),
													(0 + x * 10, 600 + y * 10 + 7))
				if player.x == x and player.y == y:
					pygame.draw.rect(screen, (0,255,255), pygame.Rect((0 + x * 10 + 3, 600 + y * 10 + 3),
																(5,5)))

def draw_map_ow_fog():
	# hard-coded for 800x800, 20x20 rooms for now
	pygame.draw.line(screen, WHITE, (0, 800), (200, 800))
	pygame.draw.line(screen, WHITE, (200, 600), (200, 800))
	for y in range(MAP_HEIGHT):
		pygame.draw.line(screen, WHITE, (0 + y*10, 600), (0 + y*10, 800))
		pygame.draw.line(screen, WHITE, (0, 600 + y*10), (200, 600 + y*10))

	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			room = map[x][y]
			if room.visited == True:
				if room.n_door == True:
					pygame.draw.line(screen, BLACK, (0 + x * 10 + 1, 600 + y * 10),
													(0 + x * 10 + 9, 600 + y * 10))
				if room.e_door == True:
					pygame.draw.line(screen, BLACK, (0 + (x + 1) * 10, 600 + y * 10 + 1),
													(0 + (x + 1) * 10, 600 + y * 10 + 9))
				if room.s_door == True:
					pygame.draw.line(screen, BLACK, (0 + x * 10 + 1, 600 + (y + 1) * 10),
													(0 + x * 10 + 9, 600 + (y + 1) * 10))
				if room.w_door == True:
					pygame.draw.line(screen, BLACK, (0 + x * 10, 600 + y * 10 + 1),
													(0 + x * 10, 600 + y * 10 + 9))
				if player.x == x and player.y == y:
					pygame.draw.rect(screen, (0,255,255), pygame.Rect((0 + x * 10 + 3, 600 + y * 10 + 3),
																(5,5)))

def draw_screen():
	map[player.x][player.y].draw_room(player.facing)
	# TODO: add code to show compass, messages, etc.

def main():
	make_map()
	#ake_map_steps()
	mode = EXPLORE

	while True:
		draw_screen()
		#draw_map()
		#draw_map_open_doors()
		draw_map_open_walls()
		#draw_map_od_fog()
		#draw_map_ow_fog()
		if mode == EXPLORE:
			pass # draw explore stuff
		elif mode == BATTLE:
			pass # draw battle stuff
		elif mode == INVENTORY:
			pass # draw inventory stuff

		pygame.display.flip()
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				return
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return

if __name__ == "__main__":
	main()
	pygame.quit()