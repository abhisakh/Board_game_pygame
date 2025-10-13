# 🏓 Pong Game – Pygame Edition

<img width="900" height="600" alt="welcome_screen_screenshot" src="https://github.com/user-attachments/assets/85bf2f28-8341-4198-9a1c-53dd978456f3" />

A retro-style two-player Pong game built using Python and Pygame.
Enjoy smooth paddle control, ball physics, score tracking, restart options, 
and a clean interface with start and game-over screens.

---

## 🌟 Features
```bash
| Feature                      | Description                                                       |
| ---------------------------- | ----------------------------------------------------------------- |
| 🎮 Two-Player Gameplay       | Play locally — one player on each side using keyboard controls.   |
| ⚡ Smooth Controls            | Real-time paddle movement and ball physics with bounce mechanics. |
| 🧠 Collision System          | Detects paddle and wall collisions accurately.                    |
| 🏁 Scoring System            | Automatically tracks and displays scores on the screen.           |
| 🏆 Game Over Screen          | Announces the winner and allows Restart (`R`) or Quit (`Q`).      |
| 🚪 Always-Active Exit Button | Quit the game anytime via a visible on-screen exit button.        |
| 🕹️ Start Screen              | Displays a “Press any key to start” intro before gameplay begins. |
| 🧩 Modular Code              | Easy to extend with new features (AI, sound effects, power-ups).  |

```

---

## 🗂 Project Structure
```bash
.
├── main.py               # Main game logic and entry point
├── requirements.txt       # Python dependencies (pygame)
├── README.md              # Project documentation
└── assets/                # (Optional) images, sounds, etc.

```
---

## ⚙️ Setup Instructions

#### 1. Clone the repository
```bash
git clone git@github.com:abhisakh/Board_game_pygame.git
cd <project-folder>

```
#### 2. Create and activate a virtual environment
```bash
python3 -m venv myproject-env
source myproject-env/bin/activate      # macOS/Linux
myproject-env\Scripts\activate         # Windows

```
#### 3. Install dependencies
```bash
pip install -r requirements.txt

```
#### 4. Run the game
```bash
python main.py

```
## 🕹️ Controls
```bash
| Action                 | Player 1 (Green)             | Player 2 (Red)     |
| ---------------------- | ---------------------------- | ------------------ |
| Move Up                | **W**                        | **↑ (Up Arrow)**   |
| Move Down              | **S**                        | **↓ (Down Arrow)** |
| Restart (on Game Over) | **R**                        | **R**              |
| Quit                   | **Q** or use **Exit Button** |                    |

```

## 🧩 Gameplay Flow
```bash
┌────────────────┐
│  Start Screen  │
│ "Press any key"│
└───────┬────────┘
        │
        ▼
┌────────────────────┐
│  Main Game Loop    │
│  Paddle, Ball, UI  │
└───────┬────────────┘
        │
        ▼
┌────────────────┐
│ Game Over Screen│
│  Winner + (R/Q) │
└────────────────┘

```
## 📸 Screenshots

##### [Start Screen]
<img width="900" height="600" alt="welcome_screen_screenshot" src="https://github.com/user-attachments/assets/207d43f7-78a0-4f62-a210-b59732be7d82" />

##### [Gameplay]
<img width="886" height="595" alt="Screenshot 2025-10-13 at 13 57 50" src="https://github.com/user-attachments/assets/c28127d2-9252-4faf-b678-79e9762f7645" />

##### [Game Over]
<img width="886" height="595" alt="Screenshot 2025-10-13 at 13 57 22" src="https://github.com/user-attachments/assets/ad3b0664-b12f-4fb8-bcbc-697f28a5ad1a" />

## 🧱 Next Planned Upgrades

- 🎵 Add background music and sound effects
- 🧠 Add AI opponent mode (single-player)
- 🌈 Improve UI with gradients and animations
- 💾 Save high scores to a file

## 🛠 Dependencies
Listed in requirements.txt:
```bash
pygame

```

### ✨ Acknowledgments
Masterschool
- For the Codio project.


## 🙋‍♂️ Author
**Abhisakh Sarma** 
GitHub: [https://github.com/abhisakh](https://github.com/abhisakh)

[Basic game received from the Instructor]
**Victor Miclovich** [ https://gist.github.com/miclovich/]
_Contributions and feedback are always welcome!_
