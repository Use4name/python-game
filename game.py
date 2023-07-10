import pygame
import random as rnd



class Labyrinth:
    def __init__(self):
        pygame.init()
        self.load_pictures()
        self.new_game()

        self.clock = pygame.time.Clock()
        self.height = len(self.map)
        self.width = len(self.map)
        self.scale = 50
        screen_height = self.scale * self.height+50
        screen_width = (self.scale * self.width)*2-200
        #health of monster
        self.health = 3
        self.ball_radius = 8
        #We set this parameter to restrict shooting too many balls at once
        self.new_ball_interval = 10
        #This is the tick time it takes to randomly choose a direction for the monster
        self.new_direction_of_monster_interval = 20
        self.speed_of_monster = 10


        self.screen = pygame.display.set_mode((screen_width, screen_height + self.scale))
        self.font1 = pygame.font.SysFont("Arial", 24)
        self.font2 = pygame.font.SysFont("Arial", 20)
        pygame.display.set_caption("Labyrinth of monsters")
        self.changing_parameters()
        self.loop()

    def changing_parameters(self):
        #starting coordinate of the robot
        self.x = 50
        self.y = 50
        self.total_coins = 0
        self.total_monsters_killed = 0
        #This checks if the ball is currently moving
        self.ball_moving = False
        #This checks if the ball has been shot
        self.fire = False
        #Directions for the monsters
        self.down = False
        self.up = False
        self.left = False
        self.right = False
        #Position of the monster and its health. This list of dictionaries will be updated every frame
        self.starting_pos_of_monsters = [{"position": (50, 500), "health": self.health, "rnd_direction": "", "direction": False}, 
                                         {"position": (150, 300), "health": self.health, "rnd_direction": "", "direction": False},
                                         {"position": (150, 50), "health": self.health, "rnd_direction": "", "direction": False},
                                         {"position": (600, 150), "health": self.health,"rnd_direction": "", "direction": False},
                                         {"position": (850, 95), "health": self.health, "rnd_direction": "", "direction": False},
                                         {"position": (900, 250), "health": self.health, "rnd_direction": "", "direction": False},
                                         {"position": (400, 250), "health": self.health, "rnd_direction": "", "direction": False},
                                         {"position": (300, 450), "health": self.health, "rnd_direction": "", "direction": False},
                                         {"position": (500, 400), "health": self.health,"rnd_direction": "", "direction": False},
                                         {"position": (650, 445), "health": self.health, "rnd_direction": "", "direction": False},
                                         {"position": (900, 350), "health": self.health,"rnd_direction": "", "direction": False},
                                         {"position": (750, 250), "health": self.health,"rnd_direction": "","direction": False},
                                         {"position": (500, 250), "health": self.health, "rnd_direction": "", "direction": False}]



        #We start this from 11 so that we can start shooting immediately
        self.ball_frame_counter = 11
        self.monster_frame_counter = 0
        #Dictionary of all the currently moving balls and their direction updated to this dictionary
        self.balls = {"a_shot_L": [], "a_shot_R": [], "a_shot_U": [], "a_shot_D": []}
        #These are different input values. a_shot means a shot has been shot while the shoot means its constantly shooting and moving
        self.input_values = {"move_player_left": False,
                        "move_player_right": False,
                        "move_player_up": False,
                        "move_player_down": False,
                        "shoot_down": False,
                        "shoot_up": False,
                        "shoot_left": False,
                        "shoot_right": False,
                        "a_shot_L": False,
                        "a_shot_R": False,
                        "a_shot_U": False,
                        "a_shot_D": False,
                        "fire": False}
        
    #Loops the main code
    def loop(self):
        while True:
            self.draw_game()
            self.events()
            pygame.display.flip()
            pygame.display.update()
            self.clock.tick(60)

    #Loads the pictures
    def load_pictures(self):
        self.pictures = {}
        for i,name in enumerate(["lattia", "seina", "hirvio", "kolikko", "ovi", "robo"]):
            image_name = name + ".png"
            #Since no other pictures are allowed to use, this is done so that it does not load the floor and wall pictures
            #i dont know why provide a white rectangle with a picture of a robot. 
            # Would have been much better to crop out the robot from the white background but the pictures cant be altered unfortunately...
            if i > 1:
                self.pictures[i] = pygame.image.load(image_name)

    #Draws the map
    def new_game(self):
        #0 = floor, 1 = wall, 3 = coin, 4 = door
        self.map = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,0,1,0,0,0,0,0,3,1,0,0,0,0,1,3,0,0,0,1],
                    [1,0,1,0,3,1,1,1,0,0,0,0,1,0,0,1,0,0,0,1],
                    [1,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,1],
                    [1,3,1,0,0,1,0,0,0,1,4,3,0,0,0,0,1,3,0,1],
                    [1,0,0,0,1,3,0,1,1,1,1,1,1,1,1,0,1,1,1,1],
                    [1,0,1,0,0,0,0,1,3,1,1,0,0,0,1,0,0,0,0,1],
                    [1,0,1,1,1,1,0,1,0,0,0,0,1,0,1,1,1,1,0,1],
                    [1,0,0,0,1,0,0,0,1,1,0,1,1,0,0,0,0,1,0,1],
                    [1,0,1,0,0,3,1,0,0,0,0,0,0,0,0,1,3,0,0,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
    
    #initializes the game
    def draw_game(self):
        self.coordinates_of_walls = []
        self.coordinates_of_coins = []
        self.position_index_of_coins = []
        #We make a white background so the black walls are visible. 
        self.screen.fill((255,255,255))
        #By using enumerate, we can also find the corresponding index in the list
        for y,row in enumerate(self.map):
            for x,column in enumerate(row):
                if column == 3: #picture of the coin
                    #we add +10 because the coins picture is 10x10 pixels too short
                    self.coordinates_of_coins.append(((self.pictures[3].get_width()+10)*x, (self.pictures[3].get_height()+10)*y))
                    self.position_index_of_coins.append((x,y))
                    self.screen.blit(self.pictures[column], (x*self.scale, y*self.scale))

                if column == 4: #picture of the door
                    self.screen.blit(self.pictures[column], (x*self.scale, y*self.scale))

                if column == 1: #wall
                    #This is to add the coordinates of the walls
                    self.coordinates_of_walls.append((x*self.scale, y*self.scale))
                    #And here we draw the walls
                    pygame.draw.rect(self.screen, (0,0,0), (x*self.scale, y*self.scale, self.scale, self.scale))

        
        #And here we put the coin tracker text
        coins_text = self.font1.render(f"Coins: {self.total_coins}/10", True, (255,0,0))
        self.screen.blit(coins_text, (25, self.height * self.scale + 10))
        #And the monsters killed
        monsters_text = self.font1.render(f"Monsters killed: {self.total_monsters_killed}/13", True, (255,0,0))
        self.screen.blit(monsters_text, (200, self.height * self.scale + 10))
        #As well as the instructions
        instructions_text = self.font2.render(f"Use arrow keys to shoot. Collect all 10 coins and escape through the door to win", True, (255,0,0))
        self.screen.blit(instructions_text, (25, self.height * self.scale + 60))





    #This handles the events
    def events(self):
        key_mapping = {
            pygame.K_a: "move_player_left",
            pygame.K_d: "move_player_right",
            pygame.K_w: "move_player_up",
            pygame.K_s: "move_player_down",
            pygame.K_DOWN: "shoot_down",
            pygame.K_UP: "shoot_up",
            pygame.K_LEFT: "shoot_left",
            pygame.K_RIGHT: "shoot_right",
        }

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in key_mapping:
                    #Here we just turn the input values from the dictionary to True if the key is pressed
                    self.input_values[key_mapping[event.key]] = True
                    if key_mapping[event.key] == "shoot_up":
                        self.input_values["a_shot_U"] = True
                        self.ball_moving = True
                        self.fire = True
                    elif key_mapping[event.key] == "shoot_down":
                        self.input_values["a_shot_D"] = True
                        self.ball_moving = True
                        self.fire = True
                    elif key_mapping[event.key] == "shoot_left":
                        self.input_values["a_shot_L"] = True
                        self.ball_moving = True
                        self.fire = True
                    elif key_mapping[event.key] == "shoot_right":
                        self.input_values["a_shot_R"] = True
                        self.ball_moving = True
                        self.fire = True
            elif event.type == pygame.KEYUP:
                if event.key in key_mapping:
                    #idea in the first if-statement is that we do not want to turn the shoot values to False when key is released. 
                    # This ensures that the player is moving constantly because they stay True. 
                    # Otherwise the player could only be moved in increments
                    if not key_mapping[event.key].startswith("shoot_"):
                        self.input_values[key_mapping[event.key]] = False
                    if key_mapping[event.key] == "shoot_up":
                        self.input_values["a_shot_U"] = False
                        self.fire = False
                    elif key_mapping[event.key] == "shoot_down":
                        self.input_values["a_shot_D"] = False
                        self.fire = False
                    elif key_mapping[event.key] == "shoot_left":
                        self.input_values["a_shot_L"] = False
                        self.fire = False
                    elif key_mapping[event.key] == "shoot_right":
                        self.input_values["a_shot_R"] = False
                        self.fire = False
            if event.type == pygame.QUIT:
                exit()
        #run the functions that move the entitites
        self.movement_of_robot()
        self.movement_of_monsters()
        #if a shot has been fired we create a ball
        if self.fire == True:
            self.create_ball()
            #And then we turn it back to False
            self.fire = False
        #If the ball is moving, we keep updating its position
        if self.ball_moving == True:
            self.shoot_balls()

    
    def create_ball(self):
        #The ball starts from the middle of the player position
        new_ball = (self.x+self.scale//2, self.y+self.scale//2)
        #This for loop adds the ball to the corresponding direction
        for direction in self.input_values:
                if direction == "a_shot_U" and self.input_values[direction]:
                    #This if-statement restricts how many balls can be shot at once
                    if self.ball_frame_counter > self.new_ball_interval:
                        self.balls[direction].append(new_ball)
                        self.ball_frame_counter = 0
                if direction == "a_shot_D" and self.input_values[direction]:
                    if self.ball_frame_counter > self.new_ball_interval:
                        self.balls[direction].append(new_ball)
                        self.ball_frame_counter = 0
                if direction == "a_shot_L" and self.input_values[direction]:
                    if self.ball_frame_counter > self.new_ball_interval:
                        self.balls[direction].append(new_ball)
                        self.ball_frame_counter = 0
                if direction == "a_shot_R" and self.input_values[direction]:
                    if self.ball_frame_counter > self.new_ball_interval:
                        self.balls[direction].append(new_ball)
                        self.ball_frame_counter = 0


    def shoot_balls(self):
        ball_velocity = 5
        #We check all the directions where the ball has been shot and update each direction's ball's positions
        for direction in self.balls:
                if direction == "a_shot_U":
                    for i,ball in enumerate(self.balls[direction]):
                        #We update the coordinate of the ball
                        updated_y = ball[1] -1* ball_velocity 
                        #if collision, we delete the ball
                        if self.wall_collision_of_ball(ball[0], updated_y):
                            del self.balls[direction][i]
                            continue
                        #Here we check collision between ball and monster. We also want the index to know which monster was hit
                        collision_check, index = self.ball_monster_collision(ball[0], updated_y)
                        if collision_check:
                            #Loses 1 health point
                            self.starting_pos_of_monsters[index]["health"] -= 1
                            #Here if the health is 0 or less, the monster will be removed and also the ball
                            if self.starting_pos_of_monsters[index]["health"] <= 0:
                                del self.starting_pos_of_monsters[index]
                                del self.balls[direction][i]
                                self.total_monsters_killed += 1
                                continue
                            #We also delete the ball if it hits the monster but doesnt kill it
                            del self.balls[direction][i]
                            continue
                        #This updates the position of the ball
                        self.balls[direction][i] = (ball[0], updated_y)
                        pygame.draw.circle(self.screen, (255, 0, 0), (int(ball[0]), int(updated_y)), self.ball_radius)
                #Same logic is done for all the other directions
                if direction == "a_shot_D":
                    for i,ball in enumerate(self.balls[direction]):
                        updated_y = ball[1] + ball_velocity 
                        if self.wall_collision_of_ball(ball[0], updated_y):
                            del self.balls[direction][i]
                            continue
                        collision_check, index = self.ball_monster_collision(ball[0], updated_y)
                        if collision_check:
                            self.starting_pos_of_monsters[index]["health"] -= 1
                            if self.starting_pos_of_monsters[index]["health"] <= 0:
                                del self.starting_pos_of_monsters[index]
                                del self.balls[direction][i]
                                self.total_monsters_killed += 1
                                continue
                            del self.balls[direction][i]
                            continue
                        self.balls[direction][i] = (ball[0], updated_y)
                        pygame.draw.circle(self.screen, (255, 0, 0), (int(ball[0]), int(updated_y)), self.ball_radius)
                if direction == "a_shot_L":
                    for i,ball in enumerate(self.balls[direction]):
                        updated_x = ball[0] -1 * ball_velocity 
                        if self.wall_collision_of_ball(updated_x, ball[1]):
                            del self.balls[direction][i]
                            continue
                        collision_check, index = self.ball_monster_collision(updated_x, ball[1])
                        if collision_check:
                            self.starting_pos_of_monsters[index]["health"] -= 1
                            if self.starting_pos_of_monsters[index]["health"] <= 0:
                                del self.starting_pos_of_monsters[index]
                                del self.balls[direction][i]
                                self.total_monsters_killed += 1
                                continue
                            del self.balls[direction][i]
                            continue
                        self.balls[direction][i] = (updated_x, ball[1])
                        pygame.draw.circle(self.screen, (255, 0, 0), (int(updated_x), int(ball[1])), self.ball_radius)
                if direction == "a_shot_R":
                    for i,ball in enumerate(self.balls[direction]):
                        updated_x = ball[0] + ball_velocity 
                        if self.wall_collision_of_ball(updated_x, ball[1]):
                            del self.balls[direction][i]
                            continue
                        collision_check, index = self.ball_monster_collision(updated_x, ball[1])
                        if collision_check:
                            self.starting_pos_of_monsters[index]["health"] -= 1
                            if self.starting_pos_of_monsters[index]["health"] <= 0:
                                del self.starting_pos_of_monsters[index]
                                del self.balls[direction][i]
                                self.total_monsters_killed += 1
                                continue
                            del self.balls[direction][i]
                            continue
                        self.balls[direction][i] = (updated_x, ball[1])
                        pygame.draw.circle(self.screen, (255, 0, 0), (int(updated_x), int(ball[1])), self.ball_radius)

            
        #We want to have  the frame counter here so that way we can limit the amount of shots in a time period
        self.ball_frame_counter += 1

    
    #Here are all the collision check functions:

    #This function checks for collision between player and coin
    def coin_collision(self):
        #rectangular hitbox of the player
        player_rect = pygame.Rect(self.x, self.y, self.scale, self.scale)
        #Again we use enumerate to find the index of the coin
        for i, coord in enumerate(self.coordinates_of_coins):
            if player_rect.colliderect(pygame.Rect(*coord, self.scale, self.scale)):
                #Here we find the position index of the coin in the map
                the_coin = self.position_index_of_coins[i]
                #We update the map. The coin turns into a floor. In other words it turns into nothing, just white background
                self.map[the_coin[1]][the_coin[0]] = 0
                #Adds to the amount of coins collected
                self.total_coins += 1

    #This checks collision between ball and wall
    def wall_collision_of_ball(self, x,y):
        #we make the ball a rectangle. 
        ball_hitbox = pygame.Rect(x-self.ball_radius, y-self.ball_radius, self.ball_radius, self.ball_radius)
        #Idea here is we check for collision with any wall. This returns a boolean value
        wall_collision = any(ball_hitbox.colliderect(pygame.Rect(*coord, self.scale, self.scale)) for coord in self.coordinates_of_walls)
        return wall_collision
    
    #Collision between monster and wall
    def collision_of_monsters(self, x,y):
        monster_hitbox = pygame.Rect(x,y,self.scale,self.scale)
        return any(monster_hitbox.colliderect(pygame.Rect(*coord, self.scale, self.scale)) for coord in self.coordinates_of_walls)

    #Player monster collision
    def player_monster_collision(self, x, y):
        #We make an offset to have a more forgiving hitbox
        offset = 25
        monster_hitbox = pygame.Rect(x + offset, y + offset, self.scale-offset, self.scale-offset)
        robot_hitbox = pygame.Rect(self.x+15, self.y, self.scale//2, self.scale)
        return monster_hitbox.colliderect(robot_hitbox)
    
    #ball monster collision. We want to return the index so we know which monster was hit
    def ball_monster_collision(self, x, y):
        ball_hitbox = pygame.Rect(x-self.ball_radius, y-self.ball_radius, self.ball_radius, self.ball_radius)
        for i, coord in enumerate(self.starting_pos_of_monsters):
            if ball_hitbox.colliderect(pygame.Rect(*coord["position"], self.scale, self.scale)):
                return True, i
        return False, None

    def movement_of_robot(self):
        speed_of_robot = 5
        #We make the hitbox of the player a rectangle
        player_rect = pygame.Rect(self.x, self.y, self.scale, self.scale)

        #This checks if player is moving right
        if self.input_values["move_player_right"]:
            #This updates the coordinate
            player_rect.x += speed_of_robot
            #Checking for collision. Im not sure why but the if statements at the end help make the movement a little bit more smooth
            wall_collision_right = any(player_rect.colliderect(pygame.Rect(*coord, self.scale, self.scale)) for coord in self.coordinates_of_walls if coord[0] > player_rect.x)
            if not wall_collision_right:
                self.x = player_rect.x
        
        if self.input_values["move_player_left"]:
            player_rect.x -= speed_of_robot
            wall_collision_left = any(player_rect.colliderect(pygame.Rect(*coord, self.scale, self.scale)) for coord in self.coordinates_of_walls if coord[0] < player_rect.x)
            if not wall_collision_left:
                self.x = player_rect.x


        if self.input_values["move_player_down"]:
            player_rect.y += speed_of_robot
            wall_collision_down = any(player_rect.colliderect(pygame.Rect(*coord, self.scale, self.scale)) for coord in self.coordinates_of_walls if coord[1] > player_rect.y)
            if not wall_collision_down:
                self.y = player_rect.y

        if self.input_values["move_player_up"]:
            player_rect.y -= speed_of_robot
            wall_collision_up = any(player_rect.colliderect(pygame.Rect(*coord, self.scale, self.scale)) for coord in self.coordinates_of_walls if coord[1] < player_rect.y)
            if not wall_collision_up:
                self.y = player_rect.y
        
        

        #Here we check for coin collision            
        self.coin_collision()
        #And we display the robot with its updated coordinates
        self.screen.blit(self.pictures[5], (self.x, self.y))
        #Check for win
        if self.game_finished():
            self.winning_screen()


    #We make an algorithm for random movement of monsters. This is far from a good algorithm but it works just fine.
    def random_movement_of_monsters(self, x, y):
        different_directions = {"right": False, "left": False, "up": False, "down": False}
        list_of_possible_directions = []
        for i in range(len(self.starting_pos_of_monsters)):
            different_directions["right"] = self.collision_of_monsters(x + self.speed_of_monster, y)
            different_directions["down"] = self.collision_of_monsters(x, y + self.speed_of_monster)
            different_directions["left"] = self.collision_of_monsters(x - self.speed_of_monster, y)
            different_directions["up"] = self.collision_of_monsters(x, y - self.speed_of_monster)
        #Here we for loop the dictionary and add only the possible directions where there was no collision with a wall. so a False value
        for direction in different_directions:
            if not different_directions[direction]:
                list_of_possible_directions.append(direction)
        #We randomly choose the direction from the possible directions
        self.random_direction = rnd.choice(list_of_possible_directions)

    #There is probably a way shorter way to represent the if-statements in this function
    def movement_of_monsters(self):   
        #The order of the if-statements makes the movement of the monsters a little different
        #Right now the order is: right, down, left, up
        for i, monster in enumerate(self.starting_pos_of_monsters):
            intended_x = monster["position"][0]
            intended_y = monster["position"][1]
            #Idea here is to randomly choose a new direction every time the frame counter is dividable with the direction interval
            if self.monster_frame_counter % self.new_direction_of_monster_interval == 0:
                self.random_movement_of_monsters(monster["position"][0], monster["position"][1])
                monster["rnd_direction"] = self.random_direction


            #If monster hits the player
            if self.player_monster_collision(intended_x, intended_y):
                        self.game_over_screen()

            #If randomly chosen direction is right
            if monster["rnd_direction"] == "right":
                if not self.collision_of_monsters(monster["position"][0] + self.speed_of_monster, monster["position"][1] ) and not monster["direction"]: #left movement
                    intended_x += self.speed_of_monster
                    #Again if monster hits the player, game over
                    if self.player_monster_collision(intended_x, intended_y):
                        self.game_over_screen()
                    monster["direction"] = True #Right movement
                    #Here we update the position of the monster. Same logic for all the other directions
                    monster["position"] = (intended_x, intended_y)
                    self.starting_pos_of_monsters[i] = monster
                    self.screen.blit(self.pictures[2], (intended_x, intended_y))
                    continue
                #Idea here is that if a collision finally happens, the direction it was originally moving turns to False
                else:
                    monster["direction"]= False

            if monster["rnd_direction"] == "down":
                if not self.collision_of_monsters(monster["position"][0], monster["position"][1] + self.speed_of_monster) and not monster["direction"]:
                    intended_y += self.speed_of_monster
                    if self.player_monster_collision(intended_x, intended_y):
                        self.game_over_screen()
                    monster["direction"] = True #Down movement
                    monster["position"] = (intended_x, intended_y)
                    self.starting_pos_of_monsters[i] = monster
                    self.screen.blit(self.pictures[2], (intended_x, intended_y))
                    continue
                else:
                    monster["direction"] = False

            if monster["rnd_direction"] == "left":
                if not self.collision_of_monsters(monster["position"][0] - self.speed_of_monster, monster["position"][1]) and not monster["direction"]:
                        intended_x -= self.speed_of_monster
                        if self.player_monster_collision(intended_x, intended_y):
                            self.game_over_screen()
                        monster["direction"] = True #Left movement
                        monster["position"] = (intended_x, intended_y)
                        self.starting_pos_of_monsters[i] = monster
                        self.screen.blit(self.pictures[2], (intended_x, intended_y))
                        continue
                else:
                    monster["direction"] = False

            if monster["rnd_direction"] == "up":
                if not self.collision_of_monsters(monster["position"][0], monster["position"][1] - self.speed_of_monster) and not monster["direction"]:
                    intended_y -= self.speed_of_monster
                    if self.player_monster_collision(intended_x, intended_y):
                        self.game_over_screen()
                    monster["direction"] = True #Up movement
                    monster["position"] = (intended_x, intended_y)
                    self.starting_pos_of_monsters[i] = monster
                    self.screen.blit(self.pictures[2], (intended_x, intended_y))
                    continue
                else:
                    monster["direction"] = False
                
            monster["position"] = (intended_x, intended_y)
            self.starting_pos_of_monsters[i] = monster
            self.screen.blit(self.pictures[2], (intended_x, intended_y))
        #We remember to update the monster frame counter
        self.monster_frame_counter += 1
        #print(self.starting_pos_of_monsters)



    #game finished function. Requirements are 10 coins collected and collision with the door
    def game_finished(self):
        door_pos_x = 50*10
        door_pos_y = 50*5
        #We make the door hitbox smaller so that the robot is actually on top of the door image when the collision happens
        offset = 40
        robot_hitbox = pygame.Rect(self.x, self.y, self.scale, self.scale)
        door_hitbox = pygame.Rect(door_pos_x+offset, door_pos_y+offset, self.scale-2*offset, self.scale-2*offset)
        if self.total_coins == 10 and robot_hitbox.colliderect(door_hitbox):
            return True
        return False
    
    #Game over
    def game_over_screen(self):
        game_over_text = self.font1.render("Game Over", True, (255, 255, 255))
        instructions_text = self.font1.render("Press R to restart", True, (255, 255, 255))
        pygame.draw.rect(self.screen, (255,0,0), (400, 275, instructions_text.get_width(), 50))
        self.screen.blit(game_over_text, (400, 275))
        self.screen.blit(instructions_text, (400, 300))
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        #We reset all the parameters
                        self.reset_game_state()
                        return
                if event.type == pygame.QUIT:
                    exit()
    
    #This is done to reset the whole game. This includes the map and the parameters.
    def reset_game_state(self):
        self.changing_parameters()
        self.new_game()
        self.loop()
    
    #If victorious
    def winning_screen(self):
        win_text = self.font1.render("You escaped the labyrinth!", True, (255, 255, 255))
        again_text = self.font1.render("Press r if you want to play again", True, (255, 255, 255))
        pygame.draw.rect(self.screen, (255,0,0), (400, 275, again_text.get_width(), 50))
        self.screen.blit(win_text, (400, 275))
        self.screen.blit(again_text, (400, 300))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    #r resets the game
                    if event.key == pygame.K_r:
                        self.reset_game_state()
                        return
                if event.type == pygame.QUIT:
                    exit()
                


if __name__=="__main__":
    Labyrinth()