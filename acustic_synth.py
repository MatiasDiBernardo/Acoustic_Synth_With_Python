import pygame
import sound_stream
import sound_bank
import interactive
import keyboard
import sound_bank
pygame.font.init()

#Define the initial conditions and create presets
L = 0.66     #longitude  
d = 0.15     #distance
h =0.1       #height
b = 0.008    #stiffnes
gamma = 1    #damping

conditions_guit1 = [L, d, h, b, gamma]
conditions_guit2 = [0.66, 0.33, 0.1, 0.02, 4]
conditions_bell = [0.66, 0.33, 0.1, 0.5, 3]
conditions_bass = [1, 0.33, 0.2, 0.005, 0.6]
conditions_violin = [0.4, 0.15, 0.1, 0, 0.2]

presets = [conditions_guit1, conditions_guit2, conditions_bell, conditions_bass, conditions_violin]
presets_names = {'Guitar 1': conditions_guit1, 
				 'Guitar 2': conditions_guit2,
				 'Bell': conditions_bell,
				 'Bass':conditions_bass,
				 'Violin': conditions_violin,
				 }
instrument_index = 0

#Starting parameters
vol = 1
octav = 1
presicion = 25
time = 2

sound_synth = [conditions_guit1, vol, octav, presicion, time]  #Starting point

#Load all the images and buttons
WIDTH, HEIGHT = 350,200
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
WHITE = (255,255,255)
BLACK = (0,0,0)
WHITE_KEY_WIDTH = 25
WHITE_KEY_HEIGHT = 70
BLACK_KEY_WIDTH = 18
BLACK_KEY_HEIGHT = 40
KEYBOARD_POSITION = [20,110]
NUM_KEYS = 10  #White Keys

BACKGROUND = pygame.image.load('images/background.png')
BUTTON_IMAGE_UP = pygame.image.load('images/button_up.png').convert_alpha()
BUTTON_IMAGE_DOWN = pygame.image.load('images/button_down.png').convert_alpha()
BUTTON_IMAGE_UP_PRESS = pygame.image.load('images/button_up_press.png').convert_alpha()
BUTTON_IMAGE_DOWN_PRESS = pygame.image.load('images/button_down_press.png').convert_alpha()
LOADING_IMAGE = pygame.image.load('images/loading.png').convert_alpha()
UPDATE_IMAGE = pygame.image.load('images/button_upload.png').convert_alpha()
UPDATE_IMAGE_PRESS = pygame.image.load('images/button_upload_press.png').convert_alpha()
ICON = pygame.image.load('images/icon.png')

BUTTON_UP_1 = interactive.Button(82, 55, BUTTON_IMAGE_UP, BUTTON_IMAGE_UP_PRESS, 0.08)
BUTTON_UP_2 = interactive.Button(235, 55, BUTTON_IMAGE_UP, BUTTON_IMAGE_UP_PRESS, 0.08)

BUTTON_DOWN_1 = interactive.Button(82, 70, BUTTON_IMAGE_DOWN, BUTTON_IMAGE_DOWN_PRESS, 0.08)
BUTTON_DOWN_2 = interactive.Button(235, 70, BUTTON_IMAGE_DOWN, BUTTON_IMAGE_DOWN_PRESS, 0.08)

BUTTON_UPDATE = interactive.Button(310, 150, UPDATE_IMAGE, UPDATE_IMAGE_PRESS, 0.15) 

LOADING = interactive.Loading(330,180, LOADING_IMAGE,0.15, 0)

SLIDER = interactive.Slider(310,40, 30,70)

font = pygame.font.Font('images/Closeness.ttf', 16)
font2 = pygame.font.Font('images/Closeness.ttf', 12)

pygame.display.set_caption('Synth')
pygame.display.set_icon(ICON)

#Loading objects
sound_state = sound_stream.Load()  #Handle loading the sounds

sound_state.load_sound(sound_synth)  #Load the starting sound

playing = sound_stream.Play_Sounds(256, 0, 20000)  #Create object to play the sounds 

def draw_window(white_keys, black_keys,new_white, new_black, instrument, octave):
	WIN.blit(BACKGROUND, (0,0))

	#Draw the white keys
	for key in white_keys:
		pygame.draw.rect(WIN, WHITE, key)

	#Draw press white keys
	if len(new_white) != 0:
		for i in range(len(new_white)):
			pygame.draw.rect(WIN, (209, 209, 209), new_white[i])

	#Draw black keys
	for i in range(len(black_keys)):
		if i not in (2,6,9,12):  #Exception starting in do
			pygame.draw.rect(WIN, BLACK, black_keys[i])

	#Draw the borders
	pygame.draw.line(WIN, BLACK,KEYBOARD_POSITION, (KEYBOARD_POSITION[0] , KEYBOARD_POSITION[1] + WHITE_KEY_HEIGHT), width=2)
	pygame.draw.line(WIN, BLACK,(KEYBOARD_POSITION[0], KEYBOARD_POSITION[1] + WHITE_KEY_HEIGHT), (KEYBOARD_POSITION[0] + (WHITE_KEY_WIDTH * NUM_KEYS) , KEYBOARD_POSITION[1] + WHITE_KEY_HEIGHT), width=2)
	pygame.draw.line(WIN, BLACK,(KEYBOARD_POSITION[0] + (WHITE_KEY_WIDTH * NUM_KEYS), KEYBOARD_POSITION[1]), (KEYBOARD_POSITION[0] + (WHITE_KEY_WIDTH * NUM_KEYS) , KEYBOARD_POSITION[1] + WHITE_KEY_HEIGHT), width=2)
	for i in range(1,NUM_KEYS):
		pygame.draw.line(WIN, BLACK,(KEYBOARD_POSITION[0] + WHITE_KEY_WIDTH * i, KEYBOARD_POSITION[1]), (KEYBOARD_POSITION[0] + WHITE_KEY_WIDTH * i, KEYBOARD_POSITION[1] + WHITE_KEY_HEIGHT), width=2)

	#Draw press black key
	if len(new_black) != 0:
		for i in range(len(new_black)):
			pygame.draw.rect(WIN, (54, 54, 54), new_black[i])

	#Instrument selection
	actual_instrument = font.render(instrument, True, (255,255,255))
	WIN.blit(actual_instrument, (10,60))

	#Octave selection
	oct_name = font.render('Octave ' + str(octave), True, (255,255,255))
	WIN.blit(oct_name, (150,60))

	#Volume
	vol = font2.render('Volume', True, (255,255,255))
	WIN.blit(vol, (300,15))

def keys_press(keys_to_check):
	key_check = keys_to_check
	press = ''
	for key in key_check:
		if keyboard.is_pressed(key):
			press += key
	return press

def main():
	global sound_synth
	global presets
	global presets_names
	global instrument_index
	global vol

	#Draw black and white keys
	white_keys = []
	white_keys_position = [KEYBOARD_POSITION[0] + i * WHITE_KEY_WIDTH for i in range(NUM_KEYS)]
	for i in range(NUM_KEYS):
		white_keys.append(pygame.Rect(white_keys_position[i], KEYBOARD_POSITION[1], WHITE_KEY_WIDTH, WHITE_KEY_HEIGHT))

	black_keys = []
	for i in range(NUM_KEYS - 1):
		black_keys.append(pygame.Rect(white_keys_position[i] + WHITE_KEY_WIDTH//1.5, KEYBOARD_POSITION[1], BLACK_KEY_WIDTH, BLACK_KEY_HEIGHT))

	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		#Draw black and white keys when pressed
		keys_white = keys_press(['a', 's','d','f','g','h','j','k','l',';'])  #ENG Keyboard
		press_white_key = []

		notes_ref = {
				'a':[0,'do'],
				's':[1,'re'],
				'd':[2,'mi'],
				'f':[3,'fa'],
				'g':[4,'sol'],
				'h':[5,'la'],
				'j':[6,'si'],
				'k':[7,'doh'],
				'l':[8,'reh'],
				';':[9,'mih']}

		if len(keys_white) != 0:
			if len(keys_white) == 1:
				new_white = pygame.Rect(white_keys_position[notes_ref[keys_white][0]], KEYBOARD_POSITION[1], WHITE_KEY_WIDTH, WHITE_KEY_HEIGHT)
				press_white_key.insert(0, new_white)
				
			else:
				for i in range(len(keys_white)):
					new_white = pygame.Rect(white_keys_position[notes_ref[keys_white[i]][0]], KEYBOARD_POSITION[1], WHITE_KEY_WIDTH, WHITE_KEY_HEIGHT)
					press_white_key.insert(i, new_white)

		keys_black = keys_press(['w', 'e','t','y','u','o','p'])
		press_black_key = []

		notes_ref_b = {
					'w':[0,'do#'],
					'e':[1,'re#'],
					't':[3,'fa#'],
					'y':[4,'sol#'],
					'u':[5,'sib'],
					'o':[7,'do#h'],
					'p':[8,'re#h']}

		if len(keys_black) != 0:
			if len(keys_black) == 1:
				new_black = pygame.Rect(white_keys_position[notes_ref_b[keys_black][0]] + WHITE_KEY_WIDTH//1.5,KEYBOARD_POSITION[1], BLACK_KEY_WIDTH, BLACK_KEY_HEIGHT)
				press_black_key.insert(0, new_black)
				
			else:
				for i in range(len(keys_black)):
					new_black = pygame.Rect(white_keys_position[notes_ref_b[keys_black[i]][0]] + WHITE_KEY_WIDTH//1.5, KEYBOARD_POSITION[1], BLACK_KEY_WIDTH, BLACK_KEY_HEIGHT)
					press_black_key.insert(0, new_black)

		#Draw current octave and preset
		octave = sound_synth[2]

		for name_preset in presets_names:
			if sound_synth[0] == presets_names[name_preset]:
				instrument = name_preset

		draw_window(white_keys, black_keys, press_white_key, press_black_key, instrument, octave)

		#Change sound preset
		if BUTTON_UP_1.draw(WIN):
			instrument_index += 1
			if instrument_index >= len(presets):
				instrument_index = 0
			sound_synth[0] = presets[instrument_index]

		if BUTTON_DOWN_1.draw(WIN):
			instrument_index -= 1
			if instrument_index == -(len(presets)):
				instrument_index = 0
			sound_synth[0] = presets[instrument_index]

		#Change octave
		if BUTTON_UP_2.draw(WIN):
			sound_synth[2] += 1
			if sound_synth[2] > 3:
				sound_synth[2] = 3

		if BUTTON_DOWN_2.draw(WIN):
			sound_synth[2] -= 1
			if sound_synth[2] < 0:
				sound_synth[2] = 0

		#Change volume
		if SLIDER.draw(WIN):
			sound_synth[1] = 2 * vol * SLIDER.volume()

		#Add the changes made by the user
		if not sound_state.loading():
			if BUTTON_UPDATE.draw(WIN):
				sound_state.load_sound(sound_synth)
			text = font2.render('Update', True, (255,255,255))
			WIN.blit(text, (300,170))

		detect = ['a','w','s', 'e','d','f','t','g','y','h','u','j','k','o','l','p',';']
		keys = keys_press(detect)

		#Show animation while loading sounds
		if sound_state.loading():
			keys = ''  #While loading can't access the sound part of the program
			LOADING.draw(WIN,3)
			LOADING.angle += 1

		pygame.display.update()

		#Detect key press and play the sound
		letter_to_note = {
					'a' : 0,
					'w' : 1,
					's' : 2,
					'e' : 3,
					'd' : 4,
					'f' : 5,
					't' : 6,
					'g' : 7,
					'y' : 8,
					'h' : 9,
					'u' : 10,
					'j' : 11,
					'k' : 12,
					'o' : 13,
					'l' : 14,
					'p' : 15,
					';' : 16}

		notes = []

		if len(keys) == 1:
			notes.insert(0,letter_to_note[keys])
			if len(keys) == 1:
				audio_new = playing.buffer_segmentation(sound_state.pluck_sounds, notes)
				playing.play(audio_new)
				playing.step += 1
				keys = keys_press(detect)

		elif len(keys) > 1:
			for i in range(len(keys)):
				notes.insert(i, letter_to_note[keys[i]])
			if len(keys) > 1:
				audio_new = playing.buffer_segmentation(sound_state.pluck_sounds, notes)
				playing.play(audio_new)
				playing.step += 1
				keys = keys_press(detect)
		else:
			playing.step = 0
		
	pygame.quit()

if __name__ == '__main__':
	main()
