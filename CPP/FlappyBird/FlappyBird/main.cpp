#include <SFML/Audio.hpp>
#include <SFML/Graphics.hpp>
#include <iostream>
#include <stdlib.h>
#include <time.h>
#include <vector>
#include <thread>
#include <chrono>

using namespace sf;
using namespace std;
using namespace std::this_thread;
using namespace std::chrono;

int window_width = 400;
int window_height = 800;
string app_name = "Flappy Bird";
bool isFirstTime = true;

RenderWindow window(VideoMode(window_width, window_height), app_name);

sf::Image icon;
sf::Music musicBG;

bool isMusicPlaying = true;

struct Sounds {
	SoundBuffer chingBuffer;
	SoundBuffer hopBuffer;
	SoundBuffer dishkBuffer;
	Sound ching;
	Sound hop;
	Sound dishk;
} sounds;

struct Textures {
	Texture flappy[3];
	Texture pipe;
	Texture background;
	Texture logo;
	Texture startBtn;
	Texture getReady;
	Texture gameover;
} textures;

enum GameState {
	loby,
	waiting,
	started,
	gameover
};

struct Game {
	int score = 0;
	int highscore = 0;
	int frames = 0;
	Sprite background;
	Sprite gameover;
	Sprite logo;
	Sprite start;
	Sprite getReady;
	Text pressC;
	Text scoreText;
	Text highscoreText;
	Font font;
	GameState gameState = loby;
} game;

struct Flappy {
	double v = 0;
	int frame = 0;
	Sprite sprite;
} flappy;

vector<Sprite> pipes;

// rect rect collision detection helper function
bool collides(float x1, float y1, float w1, float h1, float x2, float y2, float w2, float h2) {
	if (x1 + w1 >= x2 && x1 <= x2 + w2 && y1 + h1 >= y2 && y1 <= y2 + h2) {
		return true;
	}
	return false;
}

void init_app_icon() {
	if (!icon.loadFromFile("./resources/images/flappy3.png"))
	{
		// Error handling...
		printf("Can't load app icon.");
	}
	else {
		window.setIcon(icon.getSize().x, icon.getSize().y, icon.getPixelsPtr());
	}
}

void init_window() {
	// Create and Init. window
	window.setFramerateLimit(60);
	window.setKeyRepeatEnabled(false);
	srand(time(0));
}

void init_sound() {
	// load sounds
	sounds.chingBuffer.loadFromFile("./resources/audio/score.wav");
	sounds.hopBuffer.loadFromFile("./resources/audio/flap.wav");
	sounds.dishkBuffer.loadFromFile("./resources/audio/crash.wav");

	sounds.ching.setBuffer(sounds.chingBuffer);
	sounds.hop.setBuffer(sounds.hopBuffer);
	sounds.dishk.setBuffer(sounds.dishkBuffer);
}

void init_texture() {
	// load textures
	textures.flappy[0].loadFromFile("./resources/images/flappy1.png");
	textures.flappy[1].loadFromFile("./resources/images/flappy2.png");
	textures.flappy[2].loadFromFile("./resources/images/flappy3.png");
	textures.pipe.loadFromFile("./resources/images/pipe.png");
	textures.background.loadFromFile("./resources/images/background.png");
	textures.logo.loadFromFile("./resources/images/logo.png");
	textures.startBtn.loadFromFile("./resources/images/start.png");
	textures.getReady.loadFromFile("./resources/images/getReady.png");
	textures.gameover.loadFromFile("./resources/images/gameover.png");
}

void init_bird() {
	// initial position, scale
	flappy.sprite.setPosition(100, 400);
	flappy.sprite.setScale(2, 2);
}

void init_text() {
	// load font, set positions, scales etc
	game.font.loadFromFile("./resources/fonts/flappy.ttf");
	game.background.setTexture(textures.background);
	game.background.setScale(2.0, 2.0);

	game.logo.setTexture(textures.logo);
	game.logo.setOrigin(192 / 2, 42 / 2);
	game.logo.setPosition(125, 350);
	game.logo.setScale(0.8, 0.8);

	game.start.setTexture(textures.startBtn);
	game.start.setOrigin(game.logo.getLocalBounds().width / 2, 0);
	game.start.setPosition(310, 425);

	game.gameover.setTexture(textures.gameover);
	game.gameover.setOrigin(192 / 2, 42 / 2);
	game.gameover.setPosition(200, 400);
	game.gameover.setScale(1, 1);

	game.getReady.setTexture(textures.getReady);
	game.getReady.setOrigin(192 / 2, 42 / 2);
	game.getReady.setPosition(90, 200);
	game.getReady.setScale(0.7, 0.7);

	game.pressC.setString("Press C to continue");
	game.pressC.setFont(game.font);
	game.pressC.setFillColor(Color::White);
	game.pressC.setCharacterSize(30);
	game.pressC.setOrigin(game.pressC.getLocalBounds().width / 2, 0);
	game.pressC.setPosition(200, 425);

	game.scoreText.setFont(game.font);
	game.scoreText.setFillColor(Color::White);
	game.scoreText.setCharacterSize(75);
	game.scoreText.move(30, 0);

	game.highscoreText.setFont(game.font);
	game.highscoreText.setFillColor(Color::White);
	game.highscoreText.setCharacterSize(20);
	game.highscoreText.move(30, 80);
}

void init_musicBG() {
	musicBG.openFromFile("./resources/audio/themesong.wav");
	musicBG.setLoop(true);
	musicBG.play();
}

void init(){
	init_app_icon();
	init_window();
	init_sound();
	init_texture();
	init_bird();
	init_text();
	init_musicBG();
}

void setGameEvent() {
	Event event;
	while (window.pollEvent(event)) {
		// Exit
		if (event.type == Event::Closed || (event.type == Event::KeyPressed &&
			event.key.code == Keyboard::Escape)) {
			window.close();
		}

		// flap
		else if (event.type == Event::KeyPressed &&
			event.key.code == Keyboard::Space) {
			if (game.gameState == waiting) {
				game.gameState = started;
			}

			if (game.gameState == started) {
				flappy.v = -8;
				sounds.hop.play();
			}
			// restart
		}
		//Continue
		else if (event.type == Event::KeyPressed &&
			event.key.code == Keyboard::C &&
			game.gameState == gameover) {
			game.gameState = loby;
			flappy.sprite.setPosition(100, 300);
			game.score = 0;
			pipes.clear();
		}
		//Start button listener
		else if (sf::Mouse::isButtonPressed(sf::Mouse::Left))
		{
			// transform the mouse position from window coordinates to world coordinates
			sf::Vector2f mouse = window.mapPixelToCoords(sf::Mouse::getPosition(window));

			// retrieve the bounding box of the sprite
			sf::FloatRect bounds = game.start.getGlobalBounds();

			// hit test
			if (bounds.contains(mouse))
			{
				// mouse is on sprite, show how to play
				musicBG.stop();
				isMusicPlaying = false;

				if (isFirstTime) {
					window.clear();
					window.draw(game.background);
					window.draw(game.getReady);
					window.display();

					sleep_for(5s);
					isFirstTime = !isFirstTime;
				}
				
				game.gameState = waiting;
				
			}
		}
	}
}

void updateGameComponent() {
	// update score
	flappy.sprite.setTexture(textures.flappy[1]);
	game.scoreText.setString(to_string(game.score));
	game.highscoreText.setString("Best Score: " + to_string(game.highscore));

	// update flappy
	float fx = flappy.sprite.getPosition().x;
	float fy = flappy.sprite.getPosition().y;
	float fw = 34 * flappy.sprite.getScale().x;
	float fh = 24 * flappy.sprite.getScale().y;

	// flap the wings if playing
	if (game.gameState == waiting || game.gameState == started) {
		// change the texture once in 6 frames
		if (game.frames % 6 == 0) {
			flappy.frame += 1;
		}
		if (flappy.frame == 3) {
			flappy.frame = 0;
		}
	}

	flappy.sprite.setTexture(textures.flappy[flappy.frame]);

	// move flappy
	if (game.gameState == started) {
		flappy.sprite.move(0, flappy.v);
		flappy.v += 0.5;
	}

	// if hits ceiling, stop ascending
	// if out of screen, game over
	if (game.gameState == started) {
		if (fy < 0) {
			flappy.sprite.setPosition(100, 0);
			flappy.v = 0;
		}
		else if (fy > window_height) {
			flappy.v = 0;
			game.gameState = gameover;
			sounds.dishk.play();
		}
	}

	// count the score
	for (vector<Sprite>::iterator itr = pipes.begin(); itr != pipes.end(); itr++) {
		if (game.gameState == started && (*itr).getPosition().x == 100) {
			game.score++;
			sounds.ching.play();

			if (game.score > game.highscore) {
				game.highscore = game.score;
			}

			break;
		}
	}

	// generate pipes
	if (game.gameState == started && game.frames % 150 == 0) {
		int r = rand() % 475 + 75;
		int gap = 150;

		// lower pipe
		Sprite pipeL;
		pipeL.setTexture(textures.pipe);
		pipeL.setPosition(400, r + gap);
		pipeL.setScale(2, 2);

		// upper pipe
		Sprite pipeU;
		pipeU.setTexture(textures.pipe);
		pipeU.setPosition(400.0, r);
		pipeU.setScale(2, -2);

		// push to the array
		pipes.push_back(pipeL);
		pipes.push_back(pipeU);
	}

	// move pipes
	if (game.gameState == started) {
		for (vector<Sprite>::iterator itr = pipes.begin(); itr != pipes.end(); itr++) {
			(*itr).move(-3, 0);
		}
	}

	// remove pipes if offscreen
	if (game.frames % 100 == 0) {
		vector<Sprite>::iterator startitr = pipes.begin();
		vector<Sprite>::iterator enditr = pipes.begin();

		for (; enditr != pipes.end(); enditr++) {
			if ((*enditr).getPosition().x > -104) {
				break;
			}
		}

		pipes.erase(startitr, enditr);
	}

	// collision detection
	if (game.gameState == started) {
		for (vector<Sprite>::iterator itr = pipes.begin(); itr != pipes.end(); itr++) {
			float px, py, pw, ph;
			if ((*itr).getScale().y > 0) {
				px = (*itr).getPosition().x;
				py = (*itr).getPosition().y;
				pw = 52 * (*itr).getScale().x;
				ph = 320 * (*itr).getScale().y;
			}
			else {
				pw = 52 * (*itr).getScale().x;
				ph = -320 * (*itr).getScale().y;
				px = (*itr).getPosition().x;
				py = (*itr).getPosition().y - ph;
			}

			if (collides(fx, fy, fw, fh, px, py, pw, ph)) {
				game.gameState = gameover;
				sounds.dishk.play();
			}
		}
	}
}

int main() {
	init();

	// main loop
	while (window.isOpen()) {
		if (game.gameState != loby) {
			updateGameComponent();
		}

		// events
		setGameEvent();

		// clear, draw, display
		window.clear();
		window.draw(game.background);

		if (game.gameState == loby) {
			if (!isMusicPlaying) {
				musicBG.play();
				isMusicPlaying = true;
			}
			//show Flappy Bird logo & Button Start
			window.draw(game.logo);
			window.draw(game.start);
		}
		else {
			window.draw(flappy.sprite);
		}

		// draw pipes
		for (vector<Sprite>::iterator itr = pipes.begin(); itr != pipes.end(); itr++) {
			window.draw(*itr);
		}

		// draw scores
		if (game.gameState != loby) {
			window.draw(game.scoreText);
			window.draw(game.highscoreText);
		}

		// gameover. press c to continue
		if (game.gameState == gameover) {
			window.draw(game.gameover);

			if (game.frames % 60 < 30) {
				window.draw(game.pressC);
			}
		}
		window.display();

		// dont forget to update total frames
		game.frames++;
	}

	return 0;
}