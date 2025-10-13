import pygame
import math
import sys

# ------------------------------------------------------------
# Initialization and Constants
# ------------------------------------------------------------

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🏓 Pong Game")

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (40, 40, 40)

# Font
font20 = pygame.font.Font('freesansbold.ttf', 20)


# ------------------------------------------------------------
# Striker (Paddle) Class
# ------------------------------------------------------------

class Striker:
    """
    Represents a paddle (striker) controlled by a player.

    Attributes
    ----------
    pos_x : int
        Horizontal position of the paddle.
    pos_y : int
        Vertical position of the paddle.
    width : int
        Paddle width.
    height : int
        Paddle height.
    speed : int
        Movement speed per frame.
    color : tuple[int, int, int]
        RGB color of the paddle.
    player_rect : pygame.Rect
        Rectangle representing the paddle position and size.
    """

    def __init__(self, pos_x, pos_y, width, height, speed, color):
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

    def update(self, y_fac: int):
        """
        Update the paddle position.

        Parameters
        ----------
        y_fac : int
            Direction factor (-1 for up, 1 for down, 0 for no movement).
        """
        self.pos_y += self.speed * y_fac
        # Clamp within screen
        self.pos_y = max(0, min(self.pos_y, HEIGHT - self.height))
        self.player_rect.topleft = (self.pos_x, self.pos_y)

    def get_rect(self):
        """Return the paddle's rectangle for collision detection."""
        return self.player_rect


# ------------------------------------------------------------
# Ball Class
# ------------------------------------------------------------

class Ball:
    """
    Represents the pong ball.

    Attributes
    ----------
    pos_x : float
        Horizontal position of the ball.
    pos_y : float
        Vertical position of the ball.
    radius : int
        Radius of the ball.
    speed : float
        Movement speed of the ball.
    color : tuple[int, int, int]
        RGB color of the ball.
    x_fac : float
        Horizontal movement direction factor.
    y_fac : float
        Vertical movement direction factor.
    first_time : bool
        Flag for scoring detection.
    """

    def __init__(self, pos_x, pos_y, radius, speed, color):
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
        pygame.draw.circle(screen, self.color, (int(self.pos_x), int(self.pos_y)), self.radius)

    def update(self) -> int:
        """
        Update the ball's position and check for wall collisions.

        Returns
        -------
        int
            -1 if left player scores, 1 if right player scores, 0 otherwise.
        """
        self.pos_x += self.speed * self.x_fac
        self.pos_y += self.speed * self.y_fac

        # Bounce off top/bottom
        if self.pos_y - self.radius <= 0 or self.pos_y + self.radius >= HEIGHT:
            self.y_fac *= -1

        # Check scoring
        if self.pos_x - self.radius <= 0 and self.first_time:
            self.first_time = False
            return 1  # Right player scores
        elif self.pos_x + self.radius >= WIDTH and self.first_time:
            self.first_time = False
            return -1  # Left player scores
        return 0

    def reset(self):
        """Reset the ball position and direction after a score."""
        self.pos_x = WIDTH // 2
        self.pos_y = HEIGHT // 2
        self.x_fac *= -1
        self.y_fac = -1 if self.y_fac > 0 else 1
        self.first_time = True

    def hit(self, paddle: Striker):
        """
        Reflect the ball when it hits a paddle.

        Parameters
        ----------
        paddle : Striker
            The paddle the ball collided with.
        """
        offset = ((self.pos_y - paddle.pos_y) / paddle.height) - 0.5
        self.y_fac = offset * 2  # Adjust vertical speed
        self.x_fac *= -1  # Reverse horizontal direction

    def get_rect(self) -> pygame.Rect:
        """Return the bounding rectangle of the ball for collision detection."""
        return pygame.Rect(
            int(self.pos_x) - self.radius,
            int(self.pos_y) - self.radius,
            2 * self.radius,
            2 * self.radius,
        )


# ------------------------------------------------------------
# Utility Functions
# ------------------------------------------------------------

def draw_exit_button(screen: pygame.Surface, running: bool) -> bool:
    """
    Draws an Exit button and checks for clicks to quit.

    Parameters
    ----------
    screen : pygame.Surface
        The screen to draw on.
    running : bool
        Current running state.

    Returns
    -------
    bool
        Updated running state (False if exit clicked).
    """
    width, height = screen.get_size()
    exit_rect = pygame.Rect(width - 100, 10, 80, 40)
    button_color = (200, 0, 0)
    button_hover_color = (255, 0, 0)
    button_text_color = WHITE
    font = pygame.font.Font(None, 30)

    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]

    if exit_rect.collidepoint(mouse_pos):
        color = button_hover_color
        if mouse_pressed:
            return False
    else:
        color = button_color

    pygame.draw.rect(screen, color, exit_rect)
    pygame.draw.rect(screen, GREEN, exit_rect.inflate(6, 6), 3)  # border

    text_surface = font.render("Exit", True, button_text_color)
    text_rect = text_surface.get_rect(center=exit_rect.center)
    screen.blit(text_surface, text_rect)

    return running


def draw_gradient(surface: pygame.Surface, time_val: float):
    """
    Draw a dynamic vertical gradient based on a sine wave for colors.

    Parameters
    ----------
    surface : pygame.Surface
        Surface to draw on.
    time_val : float
        Time value to animate colors.
    """
    height = surface.get_height()
    width = surface.get_width()

    for y in range(height):
        ratio = y / height
        # Sine wave color cycling
        r = int((1 + math.sin(time_val + ratio * 5)) * 127)
        g = int((1 + math.sin(time_val + ratio * 5 + 2)) * 127)
        b = int((1 + math.sin(time_val + ratio * 5 + 4)) * 127)
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))


def start_screen():
    """
    Display a colorful welcome screen with animated gradient background
    until the player presses any key.
    """
    running = True
    title_font = pygame.font.SysFont('freesansbold.ttf', 80)
    subtitle_font = pygame.font.SysFont('freesansbold.ttf', 30)
    small_font = pygame.font.SysFont('freesansbold.ttf', 20)

    while running:
        time_val = pygame.time.get_ticks() / 700  # slow color cycling
        draw_gradient(screen, time_val)

        # Render title text with shadow
        title_text = title_font.render("PONG GAME", True, WHITE)
        shadow_text = title_font.render("PONG GAME", True, BLACK)

        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        shadow_rect = shadow_text.get_rect(center=(WIDTH // 2 + 3, HEIGHT // 3 + 3))

        screen.blit(shadow_text, shadow_rect)
        screen.blit(title_text, title_rect)

        # Animated subtitle color
        r = int((1 + math.sin(time_val)) * 127)
        g = int((1 + math.sin(time_val + 2)) * 127)
        b = int((1 + math.sin(time_val + 4)) * 127)
        subtitle_color = (r, g, b)

        subtitle_text = subtitle_font.render("🏓 Two Player Pong Game 🏓", True, subtitle_color)
        subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(subtitle_text, subtitle_rect)

        instruction_text = small_font.render("Press any key to start", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        screen.blit(instruction_text, instruction_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                running = False


def game_over_screen(winner: str) -> bool:
    """
    Display the game over screen showing the winner.
    Wait for R to restart or Q to quit.

    Parameters
    ----------
    winner : str
        Winner name.

    Returns
    -------
    bool
        True if restarting, False if quitting.
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
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    return False


# ------------------------------------------------------------
# Main Game Loop
# ------------------------------------------------------------

def main():
    """
    Run the Pong game.
    """
    running = True
    WINNING_SCORE = 5  # Number of points needed to win

    # Initialize paddles and ball
    green_player = Striker(20, HEIGHT // 2 - 50, 10, 100, 10, GREEN)
    red_player = Striker(WIDTH - 30, HEIGHT // 2 - 50, 10, 100, 10, RED)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 8, 8, WHITE)

    players = [green_player, red_player]

    green_score, red_score = 0, 0

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

        # ------------------ SMOOTH PADDLE CONTROL ------------------
        keys = pygame.key.get_pressed()
        green_y_fac = -1 if keys[pygame.K_w] else 1 if keys[pygame.K_s] else 0
        red_y_fac = -1 if keys[pygame.K_UP] else 1 if keys[pygame.K_DOWN] else 0

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


if __name__ == "__main__":
    main()
