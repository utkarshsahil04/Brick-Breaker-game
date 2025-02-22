# Brick Breaker Game

A classic Brick Breaker game built using Python and Pygame. Control the paddle, break bricks, and progress through levels while aiming for a high score!

## Features
- Paddle movement using the mouse.
- Ball with realistic bounce mechanics.
- Multiple levels with increasing difficulty.
- High score tracking using JSON file storage.
- Lives system to make the game more challenging.
- Level progression when all bricks are cleared.

## Installation
### Prerequisites
Make sure you have Python installed on your system. You also need to install Pygame:
```bash
pip install -r requirements.txt
```

## How to Play
1. Run the game using:
   ```bash
   python brick_breaker.py
   ```
2. Press `SPACE` to start the game.
3. Move the paddle using your mouse to keep the ball in play.
4. Destroy all bricks to advance to the next level.
5. If you lose all lives, the game is over!

## Controls
- **Mouse Movement**: Move the paddle left and right.
- **SPACE**: Start the game or continue to the next level.
- **R**: Restart the game after winning all levels.
- **ESC / Quit Button**: Exit the game.

## Files and Structure
```
Brick-Breaker/
│── brick_breaker.py   # Main game logic
│── highscore.json     # Stores high score
│── requirements.txt   # Dependencies
│── README.md          # Documentation
```

## Future Improvements
- Add sound effects and background music.
- Introduce power-ups (larger paddle, multi-ball, etc.).
- Implement different brick types with unique behaviors.
- Enhance graphics and animations.

## License
This project is open-source and available under the MIT License.


---
Enjoy playing Brick Breaker! 🎮

