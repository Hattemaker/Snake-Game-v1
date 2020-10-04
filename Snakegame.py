import pygame
import sys
import random
import pygame_gui

background_color = (255, 255, 255)
motion_dir = {pygame.K_LEFT: "left", pygame.K_RIGHT: "right", pygame.K_UP: "up", pygame.K_DOWN: "down"}
move_direction = "null"

screen = pygame.display.set_mode((800, 600))
screen.fill(background_color)
pygame.display.set_caption("Snake v1.0")

#gui_manager = pygame_gui.UIManager((800, 600))
#hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)), text="hello!",
 #                                           manager=gui_manager)
#hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)), text="Hello!", manager=gui_manager)


screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h
snake_size = 25
food_size = 25
movement_speed = 25
snake_position_list = []

snake_head_group = pygame.sprite.Group()
clock = pygame.time.Clock()


class SnakeHead(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((snake_size, snake_size))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.travel_direction = "none"
        self.old_position = (0, 0)

    def start_position(self):
        self.rect.x = (screen_width / 2)
        self.rect.y = (screen_height / 2)

    def update(self, direction):
        self.old_position = self.rect.center
        if move_direction == "left":
            self.travel_direction = move_direction
            if self.rect.x <= -snake_size:
                self.rect.x = screen_width
            else:
                self.rect.x -= movement_speed
        elif move_direction == "right":
            self.travel_direction = move_direction
            if self.rect.x >= screen_width + snake_size:
                self.rect.x = -snake_size
            else:
                self.rect.x += movement_speed
        elif move_direction == "up":
            self.travel_direction = move_direction
            if self.rect.y <= -snake_size:
                self.rect.y = screen_height
            else:
                self.rect.y -= movement_speed
        elif move_direction == "down":
            self.travel_direction = move_direction
            if self.rect.y >= screen_height + snake_size:
                self.rect.y = -snake_size
            else:
                self.rect.y += movement_speed


class Food(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((food_size, food_size))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.randomize_position()

    def randomize_position(self):
        self.rect.x = random.randrange(0, (screen_width - food_size)  + 1, 25)
        self.rect.y = random.randrange(0, (screen_height - food_size) + 1, 25)

    def detect_collision(self, left, right) -> bool:
        if pygame.sprite.collide_rect(left, right):
            self.randomize_position()
            return True
        return False


class SnakeBody(SnakeHead):
    def __init__(self):
        SnakeHead.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((snake_size, snake_size))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.parent_node = snake_position_list[-1]
        #self.travel_direction = parent_node.travel_direction
        self.rect.center = self.parent_node.old_position

    def update(self, direction):
        self.old_position = self.rect.center
        self.rect.center = self.parent_node.old_position

snake_head = SnakeHead()
snake_head.start_position()
snake_position_list.append(snake_head)
snake_head_group.add(snake_head)
snake_body_group = pygame.sprite.Group()
food = Food()
food_group = pygame.sprite.Group(food)


# Main screen loop
running = True
while running:
    time_delta = clock.tick(8)/1000.0 #antall FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in motion_dir:
                move_direction = motion_dir[event.key]
        gui_manager.process_events(event)

    gui_manager.update(time_delta)

    if food.detect_collision(food, snake_head):
        snake_body = SnakeBody()
        snake_position_list.append(snake_body)
        snake_body_group.add(snake_body)

    if pygame.sprite.spritecollide(snake_head, snake_body_group, False):
        sys.exit()

    while pygame.sprite.spritecollide(food, snake_body_group, False) or pygame.sprite.collide_rect(food, snake_head):
        food.randomize_position()

    gui_manager.draw_ui(screen)
    snake_head_group.update(move_direction)
    snake_body_group.update(move_direction)
    screen.fill(background_color)
    snake_body_group.draw(screen)
    food_group.draw(screen)
    snake_head_group.draw(screen)
    pygame.display.flip()



