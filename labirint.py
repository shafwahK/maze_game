from pygame import *
win_width = 700
win_height = 500
display.set_caption("MazeAw")
window = display.set_mode((win_width, win_height))
bluehehe = (95,158,160)

class GameSprite(sprite.Sprite): #membuat objaek image
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite): #membuat si player bisa gerakk
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    def update(self):
        if baik.rect.x <= win_width - 80 and baik.x_speed > 0 or baik.rect.x >= 0 and baik.x_speed < 0:
            self.rect.x += self.x_speed
        platform_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0: #bergerak ke kanan
            for p in platform_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0: #bergerak ke kiri
            for p in platform_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if baik.rect.y <= win_height-80 and baik.y_speed > 0 or baik.rect.y >= 0 and baik.y_speed < 0:
            self.rect.y += self.y_speed
        platform_touched = sprite.spritecollide(self, barriers, False)

        if self.y_speed > 0: #bergerak ke bawah
            for p in platform_touched:
                self.y_speed = 0
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0: #bergerak ke atas
            for p in platform_touched:
                self.y_speed = 0
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    def update(self):
        if self.rect.x <= 420:
            self.side = "right"
        if self.rect.x >= win_width - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
            
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width + 10:
            self.kill()

barriers = sprite.Group()
bullets = sprite.Group()
monster = sprite.Group()
jahat1 = GameSprite('platform2.png', win_width / 2 - win_width / 3, win_height / 2, 300, 50)
jahat2 = GameSprite('platform2_v.png', 370, 100, 50, 400)
barriers.add(jahat1)
barriers.add(jahat2)
baik = Player('teenager.png', 5, win_height - 80, 80, 80, 0, 0)
monster1 = Enemy('game-controller.png', win_width - 80, 150, 80, 80, 5)
monster2 = Enemy('chat.png', win_width - 80, 230, 80, 80, 5)
final_sprite = GameSprite('school.png', win_width-80, win_height-100, 80, 80)
monster.add(monster1)
monster.add(monster2)
finish = False
run = True

while run:
    time.delay(50) #looping nya ketrigger tiap 0.5 detik
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                baik.x_speed = -5
            elif e.key == K_RIGHT:
                baik.x_speed = 5
            elif e.key == K_UP:
                baik.y_speed = -5
            elif e.key == K_DOWN:
                baik.y_speed = 5
            elif e.key == K_SPACE: #buat nembak cuy
                baik.fire()
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                baik.x_speed = 0
            elif e.key == K_RIGHT:
                baik.x_speed = 0
            elif e.key == K_UP:
                baik.y_speed = 0
            elif e.key == K_DOWN:
                baik.y_speed = 0
                
    if not finish:
        window.fill(bluehehe)  
        baik.update()  
        bullets.update()  #tambahkan
        baik.reset()  
        bullets.draw(window)  #tambahkan
        barriers.draw(window)  
        final_sprite.reset() 
        sprite.groupcollide(monster, bullets, True, True) #tambahkan
        monster.update()  
        monster.draw(window) 
        sprite.groupcollide(bullets, barriers, True, False) #tambahkan
    if sprite.spritecollide(baik, monster, False):
        finish = True
        img = image.load('game-over_1.png')
        d = img.get_width() // img.get_height()
        window.fill((255, 255, 255))
        window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))
    if sprite.collide_rect(baik, final_sprite):
        finish = True
        img = image.load('thumb.jpg')
        window.fill((255, 255, 255))
        window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
    display.update()