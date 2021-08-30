import pygame
from random import randint
pygame.init() #dòng này cần phải có để sd các hàm của pygame,
# chỉ cần biết khi dùng pygame thì nhớ thêm dòng này vào :))
WIDTH, HEIGHT = 400,600
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #dòng này dùng để tạo cửa sổ game
# hai số trong tuple (400,600) là chiều dài và chiều rộng của cửa sổ
pygame.display.set_caption('Flappy Bird') # tiêu đề cửa sổ
running = True
GREEN = (0, 200, 0) #màu xanh trong hệ RGB
BLUE = (0, 0 ,255)
RED = (255,0,0)
BLACK = (0,0,0)
YEALLOW = (255, 255, 0)
BIRD_X = 50
bird_y = 400
BIRD_WIDTH = 35
BIRD_HEIGHT = 35
bird_drop_velocity = 0 #toc do roi cua chim
GRAVITY = 0.5
clock = pygame.time.Clock() #fps

TUBE_WIDTH = 50 #chiều rộng ống
tube1_x = 600 #tọa độ x ống 1
tube2_x = 800
tube3_x = 1000
tube1_height = randint(100,400) #chiều dài ống
tube2_height = randint(100,400)
tube3_height = randint(100,400)

tube_velocity = 3
TUBE_GAP = 150

score = 0
font = pygame.font.SysFont('sans', 20) #tạo font có sẵn trong systerm
tube1_pass = False # biến boolean check xem con chim đã qua tọa độ đầu tiên của ống chưa
tube2_pass = False
tube3_pass = False
pausing = False

background_image = pygame.image.load("bg4.jpg")
bird_image = pygame.image.load("fb21.png")

bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT)) # đưa ảnh về kích thước phù hợp với vật chủ được gán
while running:		#vòng lặp để vẽ liên tực các hình ảnh
	clock.tick(60)  #vẽ ảnh 60 lần/s
	screen.fill(GREEN) #màu nền của cửa sổ 
	screen.blit(background_image, (0,0))

	#ve ong
	tube1_rect = pygame.draw.rect(screen, BLUE, (tube1_x, 0, TUBE_WIDTH, tube1_height))
	tube2_rect = pygame.draw.rect(screen, BLUE, (tube2_x, 0, TUBE_WIDTH, tube2_height))
	tube3_rect = pygame.draw.rect(screen, BLUE, (tube3_x, 0, TUBE_WIDTH, tube3_height))
	#ve ong doi dien
	tube1_rect_invert = pygame.draw.rect(screen, BLUE, (tube1_x, tube1_height + TUBE_GAP, TUBE_WIDTH,HEIGHT - tube1_height - TUBE_GAP ))
	tube2_rect_invert = pygame.draw.rect(screen, BLUE, (tube2_x, tube2_height + TUBE_GAP, TUBE_WIDTH,HEIGHT - tube2_height - TUBE_GAP ))
	tube3_rect_invert = pygame.draw.rect(screen, BLUE, (tube3_x, tube3_height + TUBE_GAP, TUBE_WIDTH,HEIGHT - tube3_height - TUBE_GAP ))
	# ống chạy sang trái
	tube1_x = tube1_x - tube_velocity
	tube2_x = tube2_x - tube_velocity
	tube3_x = tube3_x - tube_velocity

	#vẽ đất
	land_rect = pygame.draw.rect(screen, YEALLOW, (0,550,400,50))

	#ve chim
	
	bird_rect = screen.blit(bird_image, (BIRD_X, bird_y)) #gán hình ảnh vào vật thể
	#chim rơi
	bird_y += bird_drop_velocity
	bird_drop_velocity += GRAVITY

	#tao ong moi
	if tube1_x < -TUBE_WIDTH:
		tube1_x = 550
		tube1_height = randint(100,400)
		tube1_pass = False #chua duoc tinh diem
	if tube2_x < -TUBE_WIDTH:
		tube2_x = 550
		tube2_height = randint(100,400)
		tube2_pass = False
	if tube3_x < -TUBE_WIDTH:
		tube3_x = 550
		tube3_height = randint(100,400)
		tube3_pass = False

	score_txt = font.render("Score: " + str(score), True, BLACK) #vẽ chữ
	screen.blit(score_txt, (5,5)) #vị trí của chữ

	# update điểm

	if (tube1_x + TUBE_WIDTH) <= BIRD_X and tube1_pass == False: #check xem con chim đã đi qua tọa độ đầu tiên của ống chưa, chưa đi qua thì tube1_pass = Flase, qua rồi thì đổi tube1_pass = True, tức là score + 1 và không cộng nữa 
	 	score +=1
	 	tube1_pass = True 
	if (tube2_x + TUBE_WIDTH) <= BIRD_X and tube2_pass == False: 
	 	score +=1
	 	tube2_pass = True
	if (tube3_x + TUBE_WIDTH) <= BIRD_X and tube3_pass == False:
	 	score +=1
	 	tube3_pass = True

	#check collision
	for tube in [tube1_rect, tube2_rect, tube3_rect, tube1_rect_invert, tube2_rect_invert, tube3_rect_invert, land_rect] :
		if bird_rect.colliderect(tube):
			pausing = True
			tube_velocity = 0 
			bird_drop_velocity = 0
			game_over_txt = font.render(("Game over, score: ") +str(score), True, BLACK)

			screen.blit(game_over_txt, (200,300))
			press_space_txt = font.render(("press Space to try again"), True, BLACK)
			screen.blit(press_space_txt,(200,400))

	for event in pygame.event.get(): #bắt sự kiện: khi ấn vào nút X
#trên cửa sổ thì kết thúc game và đóng cửa sổ lại : biến event trong 
#vòng for để lấy các sự kiện xảy ra, dòng if để kiểm tra xem sự kiện
#cso phải là "click nút X" hay không, 2 dòng tiếp để đóng chương trình
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN: #check khi nao ban ấn một nút bất kì trên bàn phím
			if event.key == pygame.K_SPACE: #code cho phím space
				#reset

				if pausing:

					bird_y = 400
					tube_velocity = 3
					tube1_x= 600
					tube2_x = 800
					tube3_x = 1000
					score = 0
					pausing = False

				bird_drop_velocity = 0 #reset lai toc do rơi sau khi ấn space, tức là con chim sẽ đứng yên một xíu tạo hiệu ứng giật giật
				bird_drop_velocity -= 8 #đi lên 

				
	pygame.display.flip() #phải có để tất cả những gì bạn vẽ lên cửa
	#sổ mới hiện lên màn hình được

pygame.quit()