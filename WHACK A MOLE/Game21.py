


import random
import sys
import os
import pygame

# setting
CURPATH = os.getcwd()
SCREENSIZE = (993, 477)
# hammer pic
HAMMER_IMAGEPATHS = [os.path.join(CURPATH, 'resources/images/hammer0.png'),
					 os.path.join(CURPATH, 'resources/images/hammer1.png')]
# start 
GAME_BEGIN_IMAGEPATHS = [os.path.join(CURPATH, 'resources/images/begin.png'),
						 os.path.join(CURPATH, 'resources/images/begin1.png')]

# replay 
GAME_AGAIN_IMAGEPATHS = [os.path.join(CURPATH, 'resources/images/again.png'),
						 os.path.join(CURPATH, 'resources/images/again2.png')]

# background
GAME_BG_IMAGEPATH = os.path.join(CURPATH, 'resources/images/background.png')

GAME_END_IMAGEPATH = os.path.join(CURPATH, 'resources/images/end.png')

MOLE_IMAGEPATHS = [os.path.join(CURPATH, 'resources/images/mole_1.png'), os.path.join(CURPATH, 'resources/images/mole_laugh1.png'),
                   os.path.join(CURPATH, 'resources/images/mole_laugh2.png'), os.path.join(CURPATH, 'resources/images/mole_laugh3.png')]
# hole position
HOLE_POSITIONS = [(90, -20), (405, -20), (720, -20), (90, 140), (405, 140), (720, 140), (90, 290), (405, 290), (720, 290)]
BGM_PATH = os.path.join(CURPATH,'resources/audios/bgm.mp3')

#countdown
COUNT_DOWN_SOUND_PATH = os.path.join(CURPATH,'resources/audios/count_down.wav')
HAMMERING_SOUND_PATH = os.path.join(CURPATH,'resources/audios/hammering.wav')

FONT_PATH = os.path.join(CURPATH,'resources/font/Gabriola.ttf')
BROWN = (150, 75, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
RECORD_PATH = os.path.join(CURPATH,'score.rec')

'''mole'''
class Mole(pygame.sprite.Sprite):
    def __init__(self, image_paths, position, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.transform.scale(pygame.image.load(image_paths[0]), (101, 103)),
                       pygame.transform.scale(pygame.image.load(image_paths[-1]), (101, 103))]

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.setPosition(position)

        self.is_mole= False

    '''position'''
    def setPosition(self, pos):
        self.rect.left, self.rect.top = pos

    '''hit'''
    def setBeHammered(self):
        self.is_mole = True
    def draw(self, screen):
        if self.is_mole:
            self.image = self.images[1]
        screen.blit(self.image, self.rect)
    '''reset'''
    def reset(self):
        self.image = self.images[0]
        self.is_mole = False

'''hammer'''
class Hammer(pygame.sprite.Sprite):
    def __init__(self, image_paths, position):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(image_paths[0]), pygame.image.load(image_paths[1])]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.images[1])
        self.rect.left, self.rect.top = position
        self.is_hammering = False
    def setPosition(self, pos):
        self.rect.centerx, self.rect.centery = pos
    def draw(self, screen):
        if self.is_hammering:
            self.image = self.images[1]
        else:
            self.image = self.images[0]
        screen.blit(self.image, self.rect)



def initGame():
	pygame.init()
	screen = pygame.display.set_mode(SCREENSIZE)
	pygame.display.set_caption('WHACK-A-MOLE')
	return screen


def startInterface(screen, begin_image_paths):
	begin_images = [pygame.image.load(begin_image_paths[0]), pygame.image.load(begin_image_paths[1])]
	begin_image = begin_images[0]
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEMOTION:
				mouse_pos = pygame.mouse.get_pos()
				if mouse_pos[0] in list(range(419, 574)) and mouse_pos[1] in list(range(374, 416)):
					begin_image = begin_images[1]
				else:
					begin_image = begin_images[0]
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1 and mouse_pos[0] in list(range(419, 574)) and mouse_pos[1] in list(range(374, 416)):
					return True
		screen.blit(begin_image, (0, 0))
		pygame.display.update()


def endInterface(screen, end_image_path, score_info, font_path, font_colors, screensize):
	end_image = pygame.image.load(end_image_path)
	font = pygame.font.Font(font_path, 50)
	# SOCRE
	your_score_text = font.render('Your Score: %s' % score_info['your_score'], True, font_colors[0])
	your_score_rect = your_score_text.get_rect()
	your_score_rect.left, your_score_rect.top = (screensize[0] - your_score_rect.width) / 2, 215

	text = font.render('Game over' , True, font_colors[1])
	text_rect = text.get_rect()
	text_rect.left,text_rect.top = 415,370

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		screen.blit(end_image, (0, 0))
		screen.blit(your_score_text, your_score_rect)
		screen.blit(text,text_rect)
		pygame.display.update()

#MUSIC
def main():
	screen = initGame()
	pygame.mixer.init()
	pygame.mixer.music.load(BGM_PATH)
	pygame.mixer.music.play(-1)
	audios = {
				'count_down': pygame.mixer.Sound(COUNT_DOWN_SOUND_PATH),
				'hammering': pygame.mixer.Sound(HAMMERING_SOUND_PATH)
			}
	font = pygame.font.Font(FONT_PATH, 40)
	bg_img = pygame.image.load(GAME_BG_IMAGEPATH)
	# START SCENE
	startInterface(screen, GAME_BEGIN_IMAGEPATHS)

	# RANDOM MOLE POSITION
	hole_pos = random.choice(HOLE_POSITIONS)

	change_hole_event = pygame.USEREVENT
	pygame.time.set_timer(change_hole_event, 800)

	mole = Mole(MOLE_IMAGEPATHS, hole_pos)
	# # HAMMER
	hammer = Hammer(HAMMER_IMAGEPATHS, (500, 250))
	your_score = 0
	flag = False
	while True:
	# 	# TIME
		time_remain = round((61000 - pygame.time.get_ticks()) / 1000)
	# # 	# FASTER WITH TIME
		if time_remain == 40 and not flag:

			pygame.time.set_timer(change_hole_event, 650)
			flag = True
		elif time_remain == 20 and flag:
			pygame.time.set_timer(change_hole_event, 500)
			flag = False
		
		# --GAME OVER
		elif time_remain < 0:
			break
		count_down_text = font.render('Time: '+str(time_remain), True, WHITE)

	# 	# --BUTTON TEST
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			# MAKE MOUSE CONNECT WITH HAMMER
			elif event.type == pygame.MOUSEMOTION:
				mou_position = pygame.mouse.get_pos()
				hammer.setPosition(mou_position)
			# CLICK MOUSE
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					hammer.is_hammering = True
			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button ==1:
					hammer.is_hammering = False

			elif event.type == change_hole_event:
				hole_pos = random.choice(HOLE_POSITIONS)
				mole.reset()
				mole.setPosition(hole_pos)

		# # --HIT MOLE
		if hammer.is_hammering and not mole.is_mole:
			is_hammer = pygame.sprite.collide_mask(hammer, mole)
			if is_hammer:
				# HAMMER AUDIO
				audios['hammering'].play()
				mole.setBeHammered()
				your_score += 10
	# 	# --SCORE
		your_score_text = font.render('Score: '+str(your_score), True, BROWN)

		screen.blit(bg_img, (0, 0))
		# TIME COUNT
		screen.blit(count_down_text, (875, 8))
		# SCORE COUNT
		screen.blit(your_score_text, (800, 430))

		mole.draw(screen)
		hammer.draw(screen)
		pygame.display.flip()

	# # END SCENE
	score_info = {'your_score': your_score}
	endInterface(screen, GAME_END_IMAGEPATH,  score_info, FONT_PATH, [WHITE, RED],SCREENSIZE)


main()

