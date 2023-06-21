import turtle
import math

wn = turtle.Screen()

wn.bgcolor("black")
wn.title("Collision Detection by @TokyoEdtech")
wn.tracer(0)

pen = turtle.Turtle()   
pen.speed(0)
pen.hideturtle()

pen.color("red")
pen.width(3)    # 펜 굵기와 색 지정




shapes = ["wizard.gif", "goblin.gif", "pacman.gif", "cherry.gif", "bar.gif", "ball.gif", "x.gif"]

for shape in shapes:
    wn.register_shape(shape)
    
class Sprite():
    
    ## 생성자: 스프라이트의 위치, 가로/세로 크기, 이미지 지정

    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

    ## 스프라이트 메서드

    # 지정된 위치로 스프라이트 이동 후 도장 찍기
    def render(self, pen):
        pen.goto(self.x, self.y)
        pen.shape(self.image)
        pen.stamp()

    # 충돌 감지 방법 1: 두 스프라이트의 중심이 일치할 때 충돌 발생
    def is_overlapping_collision(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    # 충돌 감지 방법 2: 두 스프라이트 사이의 거리가 두 객체의 너비의 평균값 보다 작을 때 충돌 발생
    def is_distance_collision(self, other):
        distance = (((self.x-other.x) ** 2) + ((self.y-other.y) ** 2)) ** 0.5
        if distance < (self.width + other.width)/2.0:
            return True
        else:
            return False

    # 충돌 감지 방법 3: 각각의 스프라이트를 둘러썬 경계상자가 겹칠 때 충돌 발생
    # aabb: Axis Aligned Bounding Box
    def is_aabb_collision(self, other):
        x_collision = (math.fabs(self.x - other.x) * 2) < (self.width + other.width)
        y_collision = (math.fabs(self.y - other.y) * 2) < (self.height + other.height)
        return (x_collision and y_collision)

class Character(Sprite):
    def __init__(self, x, y, width, height, image, move1=False):
        super().__init__(x, y, width, height, image)
        self.move1 = move1  # move1 값을 새로 지정
        self.w_velocity = 1    
        self.y_velocity = 2.5   
        self.x_velocity = 0.2   # 속도
        self.gravity = -0.005   # 중력값, -값으로 지정을 해주어서 공이 아래로 떨어지도록 함
        
    def movingball(self):
        if self.move1 == True:
            self.y += self.y_velocity
            self.y_velocity += self.gravity # 공이 자연스럽게 떨어지도록 함. 가속도를 일으킴
            self.x += self.x_velocity       # 공이 포물선을 그리며 떨어지도록 함
            if self.y > 400 :             # 공의 y좌표값이 400이상일때 공이 벽에 튕겨 다시 떨어지도록 if문을 사용함
                    self.y_velocity = -self.y_velocity 
                    self.x_velocity = -self.x_velocity # 공이 벽에 닿아 떨어질때 y,x값 모두 달라질수 있도록 구현, 포물선 모양으로 떨어짐. 제자리에서 반복하여 점프하는것을 방지
            if self.x > 500 or self.x < - 500 : # 공의 x좌표값이 500이상이 되거나, -500이하로 되지않도록 함(벽에 튕겨나오는 것을 구현)
                    self.x_velocity = -self.x_velocity 
                    self.y_velocity = -self.y_velocity 
    def images1(self):  # images1,2는 캐릭터가 x좌표축으로 움직이도록 함 (velocity값으로 이미지의 속도를 조절, if 문을 사용해 지정된 범위 내에서 움직이도록함 )
        self.x += self.x_velocity
        if self.x > 500 or self.x < - 500 :
                    self.x_velocity = -self.x_velocity
    def images2(self):
        self.x += self.w_velocity
        if self.x > 500 or self.x < - 500 :
                    self.w_velocity = -self.w_velocity  
	
wizard = Character(-128, 200, 128, 128, "wizard.gif")
goblin = Character(128, 200, 108, 128, "goblin.gif")

pacman = Character(-128, 0, 128, 128, "pacman.gif")
cherry = Character(128, 0, 128, 128, "cherry.gif")

bar = Character(0, -400, 128, 24, "bar.gif")
ball = Character(0,-300, 32, 32, "ball.gif", move1 = False)    # 이미지 기존의 좌표값을 변경. 모든 객체를 sprite클래스를 상속하고 있는 character 클래스로 통일. 
                                                                # move1 을 False 값으로 두어 space를 눌렀을 때에만 공이 움직이도록 함

# 스프라이트 모음 리스트
sprites = [wizard, goblin, pacman, cherry, bar, ball]

# bar 왼쪽으로 이동
def move_ball1():
    bar.x -= 96

# bar 오른쪽으로 이동
def move_ball2():
    bar.x += 96                # moveball1,2는 bar가 x축을 기준으로 +-96씩 움직일 수 있도록 값을 지정
def move_ball3():
    ball.move1 = True          # moveball3는 ball.move1 = True값으로 줌, space키를 눌렀을때 공이 움직이도록 함

# 이벤트 처리
wn.listen()
wn.onkeypress(move_ball1, "Left")  # 왼쪽 방향 화살표 입력
wn.onkeypress(move_ball2, "Right") # 오른쪽 방향 화살표 입력
wn.onkeypress(move_ball3, "space") # 스페이스 입력                각 키를 입력했을때 bar와 ball이 반응하도록 함

while True:
    
    # 각 스프라이트 위치 이동 및 도장 찍기
    for sprite in sprites:
        sprite.render(pen)
        
    # 충돌 여부 확인
        
    if ball.is_aabb_collision(cherry):
        cherry.image = "x.gif"
    if ball.is_aabb_collision(pacman):
        pacman.image = "x.gif"
    if ball.is_aabb_collision(wizard):
        wizard.image = "x.gif"
    if ball.is_aabb_collision(goblin):
        goblin.image = "x.gif"                            # 공에 bar가 아닌 이미지가 충돌했을 경우 x이미지로 변경/ is_aabb_collision 충돌로 함수를 통일해서 사용
        
    if bar.is_aabb_collision(ball):
        ball.y_velocity =  -ball.y_velocity              # bar와 공이 충돌했을 경우에는 튕겨져 나갈 수 있도록 수정
    ball.movingball()   # space를 누른후 공의 움직임이 반복될 수 있도록 movingball함수를 while문에 넣어둠 , render로 도장 찍기를 하여 자연스럽게 공이 움직이도록 함
    ball.render(pen)

    wizard.images1()
    wizard.render(pen)
    pacman.images2()
    pacman.render(pen)
    cherry.images1()
    cherry.render(pen)
    goblin.images2()
    goblin.render(pen)    # images1,2 함수를 사용해 캐릭터이미지가 움직일수 있도록 while문에 넣어둠, 함수에 따라 속도가 다르게 변화, render로 도장 찍기


    if  cherry.image == "x.gif" and pacman.image == "x.gif" and  wizard.image == "x.gif" and  goblin.image == "x.gif":
        break   # 모든 캐릭터개 x이미지로 바뀌면 게임 종료
    if ball.y < -600:
         break  # 공이 bar를 지나 떨어졌을 경우 게임 종료
        
    wn.update() # 화면 업데이트
    pen.clear() # 스프라이트 이동흔적 삭제

    pen.penup()       # 선을 그어 게임 공간을 표시함
    pen.goto(-500, 800)  
    pen.pendown()
    pen.goto(-500, -800)  
    pen.goto(500, -800)  
    pen.goto(500, 800)  
    pen.goto(-500, 800)  # 사각형 틀의 각각의 꼭짓점 좌표 입력, 사각형 틀을 만들어 맵의 크기를 눈으로 볼 수 있도록 표시
    pen.penup()             