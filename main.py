"""
main.py
--------

A simple Pong game implemented using Pygame.

This module initializes the game, defines the player paddles (Strikers),
the ball, and handles game events such as movement, collisions,
and scoring.

Features
--------
- Two-player Pong game using keyboard controls.
- Smooth paddle and ball movement.
- Basic collision detection and scoring.
- Simple on-screen scoreboard and restart after point.

Controls
--------
Player 1 (Green): W (up), S (down)
Player 2 (Red):   UP (↑), DOWN (↓)
Press the close button to quit.
"""

import pygame

# ------------------------------------------------------------
# Initialization
# ------------------------------------------------------------
pygame.init()

# Font for text rendering
font20 = pygame.font.Font('freesansbold.ttf', 20)

# RGB color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (40, 40, 40)

# Screen setup
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🏓 Pong Game")

clock = pygame.time.Clock()
FPS = 60
# Game configuration
WINNING_SCORE = 5  # Number of points needed to win the match


# ------------------------------------------------------------
# Striker (Paddle) Class
# ------------------------------------------------------------
class Striker:
    """
    Represents a paddle (striker) controlled by a player.

    Attributes
    ----------
    pos_x, pos_y : int
        Current coordinates of the paddle.
    width, height : int
        Dimensions of the paddle.
    speed : int
        Speed of movement per frame.
    color : tuple[int, int, int]
        RGB color value.
    player_rect : pygame.Rect
        Used for positioning and collision detection.
    """

    def __init__(self, pos_x, pos_y, width, height, speed, color):
        """Initialize the paddle."""
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.player_rect = pygame.Rect(pos_x, pos_y, width, height)

    def display(self):
        """Draw the paddle on the screen."""
        pygame.draw.rect(screen, self.color, self.player_rect)

    def update(self, y_fac):
        """
        Update paddle position based on movement direction.

        Parameters
        ----------
        y_fac : int
            Direction factor (-1 for up, 1 for down, 0 for no movement).
        """
        self.pos_y += self.speed * y_fac

        # Restrict movement within screen boundaries
        self.pos_y = max(0, min(self.pos_y, HEIGHT - self.height))

        # Update paddle position
        self.player_rect = pygame.Rect(
            self.pos_x, self.pos_y, self.width, self.height
        )

    def display_score(self, text, score, x, y, color):
        """
        Display the player score.

        Parameters
        ----------
        text : str
            Label for the score.
        score : int
            Current score value.
        x, y : int
            Coordinates for score display.
        color : tuple[int, int, int]
            RGB color for text.
        """
        label = font20.render(f"{text}{score}", True, color)
        rect = label.get_rect(center=(x, y))
        screen.blit(label, rect)

    def get_rect(self):
        """Return the current paddle rectangle."""
        return self.player_rect


# ------------------------------------------------------------
# Ball Class
# ------------------------------------------------------------
class Ball:
    """
    Represents the game ball that bounces between paddles.

    Attributes
    ----------
    pos_x, pos_y : int
        Current position of the ball.
    radius : int
        Radius of the ball.
    speed : float
        Ball movement speed.
    color : tuple[int, int, int]
        RGB color of the ball.
    x_fac, y_fac : float
        Direction factors for movement along axes.
    """

    def __init__(self, pos_x, pos_y, radius, speed, color):
        """Initialize the ball."""
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.speed = speed * 0.5
        self.color = color
        self.x_fac = 1.0
        self.y_fac = -1.0
        self.first_time = True

    def display(self):
        """Draw the ball on the screen."""
        pygame.draw.circle(
            screen, self.color, (int(self.pos_x), int(self.pos_y)), self.radius
        )

    def update(self):
        """
        Move the ball and detect wall collisions.

        Returns
        -------
        int
            -1 if Player 1 scores, +1 if Player 2 scores, 0 otherwise.
        """
        self.pos_x += self.speed * self.x_fac
        self.pos_y += self.speed * self.y_fac

        # Reflect from top or bottom
        if self.pos_y - self.radius <= 0 or self.pos_y + self.radius >= HEIGHT:
            self.y_fac *= -1

        # Score detection
        if self.pos_x - self.radius <= 0 and self.first_time:
            self.first_time = False
            return 1  # Right player scores
        elif self.pos_x + self.radius >= WIDTH and self.first_time:
            self.first_time = False
            return -1  # Left player scores
        return 0

    def reset(self):
        """Reset the ball to the center and reverse direction."""
        self.pos_x = WIDTH // 2
        self.pos_y = HEIGHT // 2
        self.x_fac *= -1
        self.y_fac = -1 if self.y_fac > 0 else 1
        self.first_time = True

    def hit(self, paddle):
        """
        Reflect the ball when it hits a paddle.

        Parameters
        ----------
        paddle : Striker
            The paddle the ball has collided with.
        """
        # Calculate where on paddle the ball hit (-0.5 to 0.5)
        offset = ((self.pos_y - paddle.pos_y) / paddle.height) - 0.5
        self.y_fac = offset * 2  # vary vertical speed
        self.x_fac *= -1  # reverse horizontal direction

    def get_rect(self):
        """Return the current ball rectangle."""
        return pygame.Rect(
            int(self.pos_x) - self.radius,
            int(self.pos_y) - self.radius,
            2 * self.radius,
            2 * self.radius,
        )


# ---------- START SCREEN ------------------------
def start_screen():
    """Display a welcome screen until a key is pressed."""
    screen.fill(BLACK)
    title_font = pygame.font.Font('freesansbold.ttf', 50)
    title_text = title_font.render("Welcome to Pong!", True, WHITE)
    instruction_text = font20.render("Press any key to start", True, WHITE)

    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    screen.blit(title_text, title_rect)
    screen.blit(instruction_text, instruction_rect)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False


# --------- EXIT BUTTON ---------------------------------
def draw_exit_button(screen, running):
    """
    Draw an always-active Exit button on the screen.
    Check for mouse click on the button to quit the game.

    Parameters
    ----------
    screen : pygame.Surface
        The main game screen to draw the button on.
    running : bool
        The current game loop state; returns False if exit clicked.

    Returns
    -------
    bool
        Updated running state (False if exit clicked, else unchanged).
    """

    # Button properties
    width, height = screen.get_size()
    exit_button_rect = pygame.Rect(width - 100, 10, 80, 40)  # Position & size
    button_color = (200, 0, 0)
    button_hover_color = (255, 0, 0)
    button_text_color = (255, 255, 255)
    font = pygame.font.Font(None, 30)

    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    # Change color on hover and check click
    if exit_button_rect.collidepoint(mouse_pos):
        color = button_hover_color
        if mouse_clicked:
            running = False
    else:
        color = button_color

    # Draw button rectangle and text
    pygame.draw.rect(screen, color, exit_button_rect)
    text_surface = font.render("Exit", True, button_text_color)
    text_rect = text_surface.get_rect(center=exit_button_rect.center)
    screen.blit(text_surface, text_rect)

        # Draw outer border
    border_color = (0, 255, 0)  # Green
    border_thickness = 3
    border_rect = exit_button_rect.inflate(border_thickness * 2, border_thickness * 2)
    pygame.draw.rect(screen, border_color, border_rect)

    # Draw button rectangle and text
    pygame.draw.rect(screen, color, exit_button_rect)
    text_surface = font.render("Exit", True, button_text_color)
    text_rect = text_surface.get_rect(center=exit_button_rect.center)
    screen.blit(text_surface, text_rect)

    return running


def game_over_screen(winner):
    """
    Display the game over screen showing the winner.
    Waits for player to press R (restart) or Q (quit).

    Parameters:
    -----------
    winner : str
        The name or color of the winning player.

    Returns:
    --------
    bool
        True if the player wants to restart, False to quit.
    """
    screen.fill(BLACK)
    large_font = pygame.font.Font('freesansbold.ttf', 60)
    small_font = pygame.font.Font('freesansbold.ttf', 30)

    winner_text = large_font.render(f"{winner} Wins!", True, WHITE)
    restart_text = small_font.render("Press R to Restart or Q to Quit", True, WHITE)

    winner_rect = winner_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    screen.blit(winner_text, winner_rect)
    screen.blit(restart_text, restart_rect)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Restart
                elif event.key == pygame.K_q:
                    return False  # Quit


# ------------------------------------------------------------
# Main Game Loop
# ------------------------------------------------------------
def main():
    """Run the Pong game."""
    running = True
    WINNING_SCORE = 5  # Number of points needed to win

    # Initialize paddles and ball
    green_player = Striker(20, HEIGHT // 2 - 50, 10, 100, 10, GREEN)
    red_player = Striker(WIDTH - 30, HEIGHT // 2 - 50, 10, 100, 10, RED)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 8, 8, WHITE)

    players = [green_player, red_player]

    green_score, red_score = 0, 0
    green_y_fac, red_y_fac = 0, 0

    start_screen()

    # ------------------ MAIN LOOP ------------------
    while running:
        screen.fill(BLACK)

        # Draw center dividing line
        for y in range(0, HEIGHT, 30):
            pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 5, y, 10, 20))

        # ------------------ EVENT HANDLING ------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Movement keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    red_y_fac = -1
                elif event.key == pygame.K_DOWN:
                    red_y_fac = 1
                elif event.key == pygame.K_w:
                    green_y_fac = -1
                elif event.key == pygame.K_s:
                    green_y_fac = 1

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    red_y_fac = 0
                if event.key in (pygame.K_w, pygame.K_s):
                    green_y_fac = 0

        # ------------------ COLLISIONS ------------------
        for player in players:
            if pygame.Rect.colliderect(ball.get_rect(), player.get_rect()):
                ball.hit(player)

        # ------------------ UPDATE OBJECTS ------------------
        green_player.update(green_y_fac)
        red_player.update(red_y_fac)
        point = ball.update()

        # ------------------ SCORE LOGIC ------------------
        if point == -1:
            green_score += 1
        elif point == 1:
            red_score += 1

        if point:
            pygame.time.wait(700)
            ball.reset()

        # ------------------ CHECK WIN CONDITION ------------------
        if green_score >= WINNING_SCORE or red_score >= WINNING_SCORE:
            winner = "Green Player" if green_score >= WINNING_SCORE else "Red Player"
            restart = game_over_screen(winner)
            if restart:
                green_score, red_score = 0, 0
                ball.reset()
                green_y_fac, red_y_fac = 0, 0
                continue
            else:
                running = False

        # ------------------ DRAW ELEMENTS ------------------
        pygame.draw.rect(screen, GREY, (0, 0, WIDTH, 40))
        green_player.display()
        red_player.display()
        ball.display()

        # Display scores
        green_score_text = font20.render(str(green_score), True, WHITE)
        red_score_text = font20.render(str(red_score), True, WHITE)
        screen.blit(green_score_text, (WIDTH // 4, 10))
        screen.blit(red_score_text, (3 * WIDTH // 4, 10))

        # 🟩 Exit button drawn LAST so it stays visible
        running = draw_exit_button(screen, running)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()



# ------------------------------------------------------------
# Entry Point
# ------------------------------------------------------------
if __name__ == "__main__":
    main()
