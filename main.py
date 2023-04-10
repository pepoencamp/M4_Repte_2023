import numpy as np
import random
import pygame
import sys
import math

BLACK = (0,0,0)      # Definicio del color negre
GREY = (120,120,120) # Definicio del color gris
RED = (255,0,0)      # Definicio del color vermell
YELLOW = (255,255,0) # Definicio del color groc
GREEN = (0,128,0)    # Definicio del color verd
WHITE = (255,255,255)# Definicio del color blanc
BLUE = (0,0,255)     # Definicio del color blau

ROW_COUNT = 7 # Nombre de files
COLUMN_COUNT = 7 # Nombre de columnes

PLAYER = 0 # Torn del jugador humà 
AI = 1 # Torn del jugador màquina

EMPTY = 0 # Indicador de posició lliure
PLAYER_PIECE = 1 # Indicador de fitxa humà
AI_PIECE = 2 # Indicador de fitxa màquina
WALL = 4 # Indicador de mur


def crear_tauler(): # Genera un tauler per defecte
	board = np.array([[1, 0, 0, 0, 0, 0, 2],
					  [0, 0, 0, 0, 0, 0, 0],
					  [0, 0, 4, 0, 4, 0, 0],
					  [0, 0, 0, 0, 0, 0, 0],
					  [0, 0, 4, 0, 4, 0, 0],
					  [0, 0, 0, 0, 0, 0, 0],
					  [2, 0, 0, 0, 0, 0, 1]])
	return board


def recupera_posicions_valides(board, piece): # Avalua tots els moviments vàlids del tauler, per un jugador donat
	valid_locations = []
	for col in range(COLUMN_COUNT):
		for row in range(ROW_COUNT):
			if es_posicio_valida(board, row, col, piece):
				valid_locations.append([row,col])
	return valid_locations


def es_posicio_valida(board, row, col, piece): # Avalua segons l'estat, si el moviment del jugador indicat compleix les restriccions
	valid = False

	if (board[row][col] != EMPTY): 
		valid = False
		
	elif ((row < ROW_COUNT-1) and (row >= 0)) and (board[row+1][col] == piece):
		valid = True
	elif ((row <= ROW_COUNT-1) and (row > 0)) and (board[row-1][col] == piece):
		valid = True
		
	elif ((col < COLUMN_COUNT-1) and (col >= 0)) and (board[row][col+1] == piece):
		valid = True
	elif ((col <= COLUMN_COUNT-1) and (col > 0)) and (board[row][col-1] == piece):
		valid = True

	elif ((row <= ROW_COUNT-1) and (row > 0) and (col <= COLUMN_COUNT-1) and (col > 0)) and (board[row-1][col-1] == piece):
		valid = True
	elif ((row < ROW_COUNT-1) and (row >= 0) and (col <= COLUMN_COUNT-1) and (col > 0)) and (board[row+1][col-1] == piece):
		valid = True
	elif ((row <= ROW_COUNT-1) and (row > 0) and (col < COLUMN_COUNT-1) and (col >= 0)) and (board[row-1][col+1] == piece):
		valid = True #
	elif ((row < ROW_COUNT-1) and (row >= 0) and (col < COLUMN_COUNT-1) and (col >= 0)) and (board[row+1][col+1] == piece):
		valid = True

	return valid


def infecta(board, row, col, piece): # Segons tauler, posició i jugador actiu, infecta les posicions corresponents
	for c in range(col-1, col+2):
		for r in range(row-1, row+2):
			if (c >= 0 and r >= 0) and (c < COLUMN_COUNT and r < ROW_COUNT):
				if (board[r][c] != EMPTY and board[r][c] != WALL): # Posició ocupada per un jugador
					board[r][c] = piece
	board[row][col] = piece # Sempre és la posició lliure


def mostra_tauler(board): # Gira el tauler en el pla vertical
	print(np.flip(board, 0))


def jugada_guanyadora(board, piece): # Planteja el guany si perd el contrincant
	pl_score, ai_score = calcula_puntuacio(board, False) # Recupera puntuació tauler

	if piece == PLAYER_PIECE:
		aux_score = pl_score - ai_score
	else:
		aux_score = ai_score - pl_score # Si juga màquina i guanya, aux_score negatiu!
	
	if piece == PLAYER_PIECE and len(recupera_posicions_valides(board, AI_PIECE)) == 0 and aux_score > 0: # Fa darrera jugada
		winner = True
	elif piece == AI_PIECE and len(recupera_posicions_valides(board, PLAYER_PIECE)) == 0 and aux_score > 0:
		winner = True
	else:
		winner = False

	return winner


def calcula_puntuacio(board, show): # Calcula i mostra la puntuació d'un estat
	player_counter = 0
	ai_counter = 0
	return player_counter, ai_counter


def avalua_tauler(board): # Calcula l'heurística d'un estat
	ai_counter = 0
	return ai_counter


def es_estat_terminal(board, locations): # Comprova si hi ha alguna jugada no guanyadora possible
	return jugada_guanyadora(board, PLAYER_PIECE) or jugada_guanyadora(board, AI_PIECE) or len(locations) == 0


def minimax(board, depth, alpha, beta, maximizingPlayer): # Recursivament, executa el mètode de minimax amb poda alpha/beta
	if maximizingPlayer:
		valid_locations = recupera_posicions_valides(board, AI_PIECE)
	else:
		valid_locations = recupera_posicions_valides(board, PLAYER_PIECE)
	
	terminal = es_estat_terminal(board, valid_locations)
	if depth == 0 or terminal:
		if terminal: # Cal ajustar els valors de retorn segons qui guanya, perd o empata la partida
			if jugada_guanyadora(board, AI_PIECE):
				return (None, None, 0)
			elif jugada_guanyadora(board, PLAYER_PIECE):
				return (None, None, 0)
			else: # Final del joc, no hi ha moviments possibles
				return (None, None, 0)
		else: # Assoleix la profunditat màxima permesa
			return (None, None, avalua_tauler(board))

	if maximizingPlayer: # Juga Max
		value = -math.inf
		position = random.choice(valid_locations)
		for pos in valid_locations:
			b_copy = board.copy()
			infecta(b_copy, pos[0], pos[1], AI_PIECE)
			temp = minimax(b_copy, depth-1, alpha, beta, False)
			new_score = temp[2]
			if new_score > value:
				value = new_score
				position = pos
		return position[0], position[1], value

	else: # Juga Min
		value = math.inf
		position = random.choice(valid_locations)
		for pos in valid_locations:
			b_copy = board.copy()
			infecta(b_copy, pos[0], pos[1], PLAYER_PIECE)
			temp = minimax(b_copy, depth-1, alpha, beta, True)
			new_score = temp[2]
			if new_score < value:
				value = new_score
				position = pos
		return position[0], position[1], value


def dibuixa_tauler(board): # Mostra el tauler del joc
	screen.fill(BLACK)
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, WHITE, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == PLAYER_PIECE:
				pygame.draw.circle(screen, GREEN, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == AI_PIECE: 
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == WALL:
				pygame.draw.rect(screen, GREY, (c*SQUARESIZE, r*SQUARESIZE, SQUARESIZE, SQUARESIZE))
	
	pygame.display.update()


"""
********************************
*     INFECTED DAYS GAME       *
********************************
"""
board = crear_tauler()
mostra_tauler(board)
game_over = False

pygame.init()

SQUARESIZE = 80

width = COLUMN_COUNT * SQUARESIZE
height = ROW_COUNT * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
dibuixa_tauler(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 60)
turn = PLAYER

while not game_over:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			
			if turn == PLAYER: # Juga humà
				posx = event.pos[0] # Recupera la posicio (columna) clicada
				posy = event.pos[1] # Recupera la posicio (fila) clicada
		
				row = int(math.floor((ROW_COUNT*SQUARESIZE-posy)/SQUARESIZE)) # Cal invertir el calcul d'y!
				col = int(math.floor(posx/SQUARESIZE))

				if es_posicio_valida(board, row, col, PLAYER_PIECE):
					infecta(board, row, col, PLAYER_PIECE)
					mostra_tauler(board)
					dibuixa_tauler(board)
					
					if jugada_guanyadora(board, AI_PIECE) or len(recupera_posicions_valides(board, AI_PIECE)) == 0:
						game_over = True
					
					turn += 1
					turn = turn % 2

	if turn == AI and not game_over: # Juga màquina		
		row, col, minimax_score = minimax(board, 3, -math.inf, math.inf, True) # Podem ajustar la profunditat màxima
		pygame.time.wait(500)
		infecta(board, row, col, AI_PIECE)
		mostra_tauler(board)
		dibuixa_tauler(board)
	
		# La doble condició evita obrir un minimax d'una posició que com que ja ha guanyat, no obtindrà
		if jugada_guanyadora(board, AI_PIECE) or len(recupera_posicions_valides(board, PLAYER_PIECE)) == 0:
			game_over = True
		
		turn += 1
		turn = turn % 2

	if game_over: # Final de partida
		pygame.time.wait(3000)