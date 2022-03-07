import pygame

class Button():
	def __init__(self, x, y, image, image_press, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.image_press = pygame.transform.scale(image_press, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			surface.blit(self.image_press, (self.rect.x, self.rect.y))
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True
		else:
			surface.blit(self.image, (self.rect.x, self.rect.y))

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		return action

class Loading():
	
	def __init__(self, x, y, image, scale, angle):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.x = x
		self.y = y
		self.angle = angle

	def draw(self, surf, vel):

		pos = (self.x, self.y)
		w, h = self.image.get_size()
		originPos = (w/2, h/2)
		# offset from pivot to center
		image_rect = self.image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
		offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

		# roatated offset from pivot to center
		rotated_offset = offset_center_to_pivot.rotate(-int(self.angle/vel))

		# roatetd image center
		rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

		# get a rotated image
		rotated_image = pygame.transform.rotate(self.image, int(self.angle/vel))
		rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

		# rotate and blit the image
		surf.blit(rotated_image, rotated_image_rect)


class Slider():
	def __init__(self, x, y, width, height):
		#Height and widht of the total slider, only vertical
		self.x = x
		self.y = y
		self.height = height
		self.width = width
		self.slider = pygame.Rect(self.x + self.width//4, self.y + int(self.height * 0.45), self.width//2, self.height//10)

	def draw(self, surface):
		action = False
		self.pos = pygame.mouse.get_pos()
		pygame.draw.rect(surface, (0,0,0), self.slider)
		pygame.draw.line(surface, (0,0,0), (self.x + self.width// 2, self.y),  (self.x + self.width// 2, self.y + self.height))

		slider_move = pygame.Rect(self.x + self.width//2, self.y, self.width//2, self.height)

		if slider_move.collidepoint(self.pos):
			if pygame.mouse.get_pressed()[0] == 1:
				action = True
				self.slider = pygame.Rect(self.x + self.width//4, self.pos[1], self.width//2, self.height//10)

		return action

	def volume(self):
		max_vol = self.y
		min_vol = self.y + self.height

		a = -1/(min_vol - max_vol)  #Regresion lineal para tener una escala entre 0 y 1
		b = -a * min_vol

		vol_scale = a * self.pos[1] + b

		return vol_scale
