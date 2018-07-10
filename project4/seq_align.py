#! /usr/bin/env python

import sys, time, random
import pygame

e_aplh = "abcdefghijklmnopqrstuvwxyz"
dna_alph = "ACGT"

# generate random string drawn from the given alphabet and of a given length
def gen_random_string(alphabet, length):
    a_len = len(alphabet)
    ret = ""
    for n in range(length):
        ret += alphabet[random.randint(0, a_len-1)]
    return ret

# print gen_random_string(e_aplh, 5)

SPACE_CHAR = '_'
SPACE_PENALTY = -1

# the scoring function
def s(x, y):
    if x == SPACE_CHAR or y == SPACE_CHAR:
        return SPACE_PENALTY
    elif x == y:
        return 2
    else:
        return -2

TILE_SIZE = 40
tile_color = (255, 255, 255)
highlight_color = (120, 129, 250)

def init_board(m, n):
    screen = pygame.display.set_mode(((m+2)*TILE_SIZE, (n+2)*TILE_SIZE))
    screen.fill((0, 0, 0))
    pygame.display.set_caption('Dot Board')
    pygame.font.init()
    font = pygame.font.Font(None, 15)
    return screen, font

def create_tile(font, text, color):
    tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
    tile.fill(color)
    b1 = font.render(text, 1, (0, 0, 0))
    tile.blit(b1, (TILE_SIZE/2, TILE_SIZE/2))
    return tile

def render_board(board, font, s1, s2, F):
    for i in range(len(s1)):
        tile = create_tile(font, s1[i], tile_color)
        board.blit(tile, ((i+2)*TILE_SIZE, 0))
    tile = create_tile(font, '', tile_color); board.blit(tile, (0, 0))
    tile = create_tile(font, '', tile_color); board.blit(tile, (TILE_SIZE, 0))
    for j in range(len(s2)):
        tile = create_tile(font, s2[j], tile_color)
        board.blit(tile, (0, (j+2)*TILE_SIZE))
    tile = create_tile(font, '', tile_color); board.blit(tile, (0, TILE_SIZE))
    for (x,y) in sorted(F.keys()):
        tile = create_tile(font, str(F[(x,y)]), tile_color)
        board.blit(tile, ((x+1)*TILE_SIZE, (y+1)*TILE_SIZE))
    
def seq_align(s1, s2, enable_graphics=True):
    
    s1 = '_' + s1
    s2 = '_' + s2



    matrix = [[0 for x in range(len(s2))] for x in range(len(s1))]

    for i in range(0, len(s1)):
    	for j in range(0, len(s2)):
    		if i == 0 and j == 0:
    			pass
    		elif i == 0:
    			matrix[i][j] = SPACE_PENALTY + matrix[i][j - 1]
    		elif j == 0:
    			matrix[i][j] = SPACE_PENALTY + matrix[i - 1][j]
    		else:
    			matrix[i][j] = max(
    				s(s1[i],s2[j]) + matrix[i - 1][j - 1], 
    				SPACE_PENALTY + matrix[i - 1][j], 
    				SPACE_PENALTY + matrix[i][j - 1])

    #for row in matrix:
    	#print row


    i = len(s1) - 1
    j = len(s2) - 1

    answer1 = ""
    answer2 = ""

    while i > 0 and j > 0:
    	if s(s1[i], s2[j]) + matrix[i - 1][j - 1] == matrix[i][j]:
    		answer1 = s1[i] + answer1
    		answer2 = s2[j] + answer2
    		i -= 1
    		j -= 1
    	elif SPACE_PENALTY + matrix[i][j - 1] == matrix[i][j]:
    		answer1 = '_' + answer1
    		answer2 = s2[j] + answer2
    		j -= 1
    	elif SPACE_PENALTY + matrix[i - 1][j] == matrix[i][j]:
    		answer1 = s1[i] + answer1
    		answer2 = '_' + answer2
    		i -= 1

    if i > 0:
    	while i > 0:
    		answer1 = s1[i] + answer1
    		answer2 = '_' + answer2
    		i -= 1
    elif j > 0:
    	while j > 0:
    		answer1 = '_' + answer1
    		answer2 = s2[j] + answer2
    		j -= 1

    return (answer1, answer2)



def bestSoln(orig_a1, orig_a2, ret_a1, ret_a2, a1, a2):
    if len(ret_a1) != len(ret_a2):
        return False

    ansScore = 0
    for ctr in range(len(a1)):
        ansScore += s(a1[ctr], a2[ctr])

    retScore = 0
    for ctr in range(len(ret_a1)):
        retScore += s(ret_a1[ctr], ret_a2[ctr])

    if retScore > ansScore:
        return False

    orig_ctr = 0
    for ctr in range(len(ret_a1)):
        if ret_a1[ctr] != "_":
            if ret_a1[ctr] != orig_a1[orig_ctr]:
                return False
            orig_ctr += 1

    orig_ctr = 0
    for ctr in range(len(ret_a2)):
        if ret_a2[ctr] != "_":
            if ret_a2[ctr] != orig_a2[orig_ctr]:
                return False
            orig_ctr += 1
        
    return True

if len(sys.argv) == 2 and sys.argv[1] == 'test':
    f=open('tests.txt', 'r');tests= eval(f.read());f.close()
    cnt = 0; passed = True
    for ((s1, s2), (a1, a2)) in tests:
        (ret_a1, ret_a2) = seq_align(s1, s2, False)
        #if (ret_a1 != a1) or (ret_a2 != a2):
        if( not bestSoln(s1, s2, ret_a1, ret_a2, a1, a2) ):
            print s1, s2 
            print a1, a2
            print ret_a1, ret_a2
            print("test#" + str(cnt) + " failed...")
            passed = False
        cnt += 1
    if passed: print("All tests passed!")
elif len(sys.argv) == 2 and sys.argv[1] == 'gentests':
    tests = []
    for n in range(25):
        m = random.randint(8, 70); n = random.randint(8, 70)
        (s1, s2) = (gen_random_string(dna_alph, m), gen_random_string(dna_alph, n))
        (a1, a2) = seq_align(s1, s2, False)
        tests.append(((s1, s2), (a1, a2)))
    f=open('tests.txt', 'w');f.write(str(tests));f.close()
else:
    l = [('ACACACTA', 'AGCACACA'), ('IMISSMISSISSIPI', 'MYMISSISAHIPPIE')]
    #l = [('ATG', 'TAG')]
    enable_graphics = True
    if enable_graphics: pygame.init()
    for (s1, s2) in l:
        print 'sequences:'
        print (s1, s2)
        
        m = len(s1)
        n = len(s2)
        
        print 'alignment: '
        print seq_align(s1, s2, enable_graphics)
    
    if enable_graphics: pygame.quit()
