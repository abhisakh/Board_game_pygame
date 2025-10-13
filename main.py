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
    x_fac, y_fac : int
        Direction factors for movement along axes.
    """

    def __init__(self, pos_x, pos_y, radius, speed, color):
        """Initialize the ball."""
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.speed = speed * 0.5
        self.color = color
        self.x_fac = 1
        self.y_fac = -1
        self.first_time = True

    def display(self):
        """Draw the ball on the screen."""
        self.ball = pygame.draw.circle(
            screen, self.color, (self.pos_x, self.pos_y), self.radius
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
        if self.pos_y <= 0 or self.pos_y >= HEIGHT:
            self.y_fac *= -1

        # Score detection
        if self.pos_x <= 0 and self.first_time:
            self.first_time = False
            return 1  # Right player scores
        elif self.pos_x >= WIDTH and self.first_time:
            self.first_time = False
            return -1  # Left player scores
        return 0

    def reset(self):
        """Reset the ball to the center and reverse direction."""
        self.pos_x = WIDTH // 2
        self.pos_y = HEIGHT // 2
        self.x_fac *= -1
        self.first_time = True

    def hit(self, paddle):
        """
        Reflect the ball when it hits a paddle.

        Parameters
        ----------
        paddle : Striker
            The paddle the ball has collided with.
        """
        # Slight angle variation based on where it hit the paddle
        offset = (self.pos_y - paddle.pos_y) / paddle.height - 0.5
        self.y_fac = offset * 2
        self.x_fac *= -1

    def get_rect(self):
        """Return the current ball rectangle."""
        return pygame.Rect(
            self.pos_x - self.radius, self.pos_y - self.radius,
            2 * self.radius, 2 * self.radius
        )


# ------------------------------------------------------------
# Main Game Loop
# ------------------------------------------------------------
def main():
    """Run the Pong game."""
    running = True

    # Initialize paddles and ball
    green_player = Striker(20, HEIGHT // 2 - 50, 10, 100, 10, GREEN)
    red_player = Striker(WIDTH - 30, HEIGHT // 2 - 50, 10, 100, 10, RED)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 8, 8, WHITE)

    players = [green_player, red_player]

    green_score, red_score = 0, 0
    green_y_fac, red_y_fac = 0, 0

    # Game loop
    while running:
        screen.fill(BLACK)

        # Event handling
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

        # Collision detection
        for player in players:
            if pygame.Rect.colliderect(ball.get_rect(), player.get_rect()):
                ball.hit(player)

        # Update positions
        green_player.update(green_y_fac)
        red_player.update(red_y_fac)
        point = ball.update()

        # Update scores
        if point == -1:
            green_score += 1
        elif point == 1:
            red_score += 1

        # Reset after scoring
        if point:
            pygame.time.wait(700)
            ball.reset()

        # Draw score banner
        pygame.draw.rect(screen, GREY, (0, 0, WIDTH, 40))

        # Draw game objects
        green_player.display()
        red_player.display()
        ball.display()

        # Display scores
        green_player.display_score("Green: ", green_score, 100, 20, WHITE)
        red_player.display_score("Red: ", red_score, WIDTH - 100, 20, WHITE)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


# ------------------------------------------------------------
# Entry Point
# ------------------------------------------------------------
if __name__ == "__main__":
    main()
