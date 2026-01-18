# 📚 SFML Template Documentation

Complete guide to the SFML rendering and resource management system of the R-Type client.

---

## 📋 Table of Contents

1. [Overview](https://www.google.com/search?q=%23overview)
2. [ResourceManager](https://www.google.com/search?q=%23resourcemanager)
3. [SpriteRenderer](https://www.google.com/search?q=%23spriterenderer)
4. [TextRenderer](https://www.google.com/search?q=%23textrenderer)
5. [AnimationRenderer](https://www.google.com/search?q=%23animationrenderer)
6. [ButtonManager](https://www.google.com/search?q=%23buttonmanager)
7. [InputManager](https://www.google.com/search?q=%23inputmanager)
8. [AudioManager](https://www.google.com/search?q=%23audiomanager)

---

## Overview

The SFML template is a set of **managers** that bridge the gap between the ECS and SFML. They manage resources (textures, fonts, sounds) and rendering (sprites, texts, animations).

### Architecture

```text
┌─────────────────────────────────────────┐
│              ECS Components             │
│   (position, ui_text, sprite_component) │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│         Synchronization Systems         │
│     (sync_ui_text_to_renderer, etc.)    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│           Template Managers             │
│   (TextRenderer, SpriteRenderer, etc.)  │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│               SFML API                  │
│   (sf::Sprite, sf::Text, sf::Texture)   │
└─────────────────────────────────────────┘

```

---

## ResourceManager

**File**: `src/client/template/ressources/resource_manager.cpp`

Manages the loading and storage of resources (textures, fonts, sounds).

### Methods

#### Textures

```cpp
// Load a texture
void loadTexture(const std::string& id, const std::string& filepath);

// Get a texture
sf::Texture* getTexture(const std::string& id);
const sf::Texture* getTexture(const std::string& id) const;

// Check existence
bool hasTexture(const std::string& id) const;

```

#### Fonts

```cpp
// Load a font
void loadFont(const std::string& id, const std::string& filepath);

// Get a font
sf::Font* getFont(const std::string& id);
const sf::Font* getFont(const std::string& id) const;

// Check existence
bool hasFont(const std::string& id) const;

```

### Usage Example

```cpp
// In the scene
ResourceManager resources;

// Load a texture
resources.loadTexture("player", "src/client/assets/player.png");

// Load a font
resources.loadFont("main", "src/client/assets/RetroBiker.ttf");

// Get a texture
sf::Texture* tex = resources.getTexture("player");
if (tex) {
    // Use the texture
}

```

---

## SpriteRenderer

**File**: `src/client/template/sprites/sprite_renderer.cpp`

Manages the creation, modification, and rendering of SFML sprites.

### Data Structure

```cpp
struct SpriteData {
    std::string textureId;    // Texture ID
    sf::Vector2f position;    // Position (x, y)
    sf::Vector2f scale;       // Scale (sx, sy)
    int zIndex;               // Render order
    sf::IntRect textureRect;  // Texture rectangle (for animations)
    bool useTextureRect;      // Use textureRect or not
};

```

### Main Methods

#### Creation / Destruction

```cpp
// Create a sprite
void create(const std::string& id,
            const std::string& textureId,
            sf::Vector2f position,
            sf::Vector2f scale = {1.0f, 1.0f});

// Remove a sprite
void remove(const std::string& id);

// Remove everything
void clear();

```

#### Modification

```cpp
// Position
void setPosition(const std::string& id, sf::Vector2f position);

// Scale
void setScale(const std::string& id, sf::Vector2f scale);

// Z-Index (render order)
void setZIndex(const std::string& id, int zIndex);

// Texture Rect (for animations)
void setTextureRect(const std::string& id, sf::IntRect rect);

```

#### Access and Rendering

```cpp
// Get data
SpriteData* get(const std::string& id);

// Check existence
bool exists(const std::string& id) const;

// Draw all sprites (sorted by z-index)
void draw(sf::RenderWindow& window);

// Draw a specific sprite
void drawSingle(sf::RenderWindow& window, const std::string& id);

```

### Usage Example

```cpp
// Create a sprite
_sprites.create("player_sprite", "player_texture", {100.0f, 200.0f}, {2.0f, 2.0f});

// Modify position
_sprites.setPosition("player_sprite", {150.0f, 250.0f});

// Define a texture rectangle (for animation)
_sprites.setTextureRect("player_sprite", sf::IntRect(0, 0, 32, 32));

// Draw (in draw())
_sprites.draw(window);

```

---

## TextRenderer

**File**: `src/client/template/text/text_renderer.cpp`

Manages the creation, modification, and rendering of SFML texts.

### Data Structure

```cpp
struct TextData {
    std::string fontId;     // Font ID
    std::string content;    // Text content
    sf::Vector2f position;  // Position (x, y)
    unsigned int size;      // Font size
    sf::Color color;        // Color
    sf::Text::Style style;  // Style (Bold, Italic, etc.)
    int zIndex;             // Render order
};

```

### Main Methods

#### Creation / Destruction

```cpp
// Create a text
void create(const std::string& id,
            const std::string& fontId,
            const std::string& content,
            sf::Vector2f position,
            unsigned int size = 24);

// Remove a text
void remove(const std::string& id);

// Remove everything
void clear();

```

#### Modification

```cpp
// Content
void setText(const std::string& id, const std::string& content);

// Position
void setPosition(const std::string& id, sf::Vector2f position);

// Size
void setSize(const std::string& id, unsigned int size);

// Color
void setColor(const std::string& id, sf::Color color);

// Style (Bold, Italic, etc.)
void setStyle(const std::string& id, sf::Text::Style style);

// Z-Index
void setZIndex(const std::string& id, int zIndex);

```

#### Access and Rendering

```cpp
// Get data
TextData* get(const std::string& id);

// Check existence
bool exists(const std::string& id) const;

// Get bounds (for centering)
sf::FloatRect getBounds(const std::string& id) const;

// Draw all texts (sorted by z-index)
void draw(sf::RenderWindow& window);

// Draw a specific text
void drawSingle(sf::RenderWindow& window, const std::string& id);

```

### Usage Example

```cpp
// Create text
_texts.create("title", "main", "R-TYPE", {400.0f, 100.0f}, 48);

// Modify content
_texts.setText("title", "R-TYPE MENU");

// Change color
_texts.setColor("title", sf::Color(255, 215, 0));

// Bold style
_texts.setStyle("title", sf::Text::Bold);

// Draw (in draw())
_texts.draw(window);

```

---

## AnimationRenderer

**File**: `src/client/template/animations/animation_renderer.cpp`

Manages frame-based animations (spritesheets).

### Data Structure

```cpp
struct AnimationData {
    std::string spriteId;    // Associated sprite ID
    int frameWidth;          // Width of a frame
    int frameHeight;         // Height of a frame
    int frameCount;          // Total number of frames
    int currentFrame;        // Current frame
    float frameDuration;     // Duration of a frame (seconds)
    float elapsedTime;       // Time elapsed since last change
    bool loop;               // Loop or not
    bool playing;            // Playing or not
};

```

### Main Methods

```cpp
// Create an animation
void create(const std::string& id,
            const std::string& spriteId,
            int frameWidth,
            int frameHeight,
            int frameCount,
            float frameDuration,
            bool loop = true);

// Start
void play(const std::string& id);

// Stop
void stop(const std::string& id);

// Update (call in update())
void update(float deltaTime);

```

### Usage Example

```cpp
// Create a sprite for the animation
_sprites.create("player_anim", "player_spritesheet", {100.0f, 100.0f});

// Create the animation (spritesheet of 8 frames, 32x32 pixels each)
_animations.create("player_walk", "player_anim", 32, 32, 8, 0.1f, true);

// Start the animation
_animations.play("player_walk");

// In update()
_animations.update(deltaTime);

```

---

## ButtonManager

**File**: `src/client/template/button/button_manager.cpp`

**Note**: This manager is **deprecated** in the new ECS architecture. Use `ui_button` components with ECS systems instead.

---

## InputManager

**File**: `src/client/template/input/input_manager.cpp`

Manages text input fields.

### Methods

```cpp
// Handle events
void handleEvent(const sf::Event& event, sf::RenderWindow& window);

// Update
void update(float deltaTime);

// Draw
void draw(sf::RenderWindow& window);

```

**Note**: This manager is also largely replaced by `ui_input_field` in the ECS.

---

## AudioManager

**File**: `src/client/template/audio/audio_manager.cpp`

Manages music and sound effects.

### Main Methods

#### Music

```cpp
// Create/load music
void createMusic(const std::string& id, const std::string& filepath);

// Play
void playMusic(const std::string& id, bool loop = false);

// Stop
void stopMusic(const std::string& id);

// Pause
void pauseMusic(const std::string& id);

// Volume (0.0f to 100.0f)
void setMusicVolume(const std::string& id, float volume);
void setGlobalMusicVolume(float volume);
float getMusicVolume() const;

// Loop
void setMusicLoop(const std::string& id, bool loop);

```

#### Sounds (SFX)

```cpp
// Load a sound
void loadSound(const std::string& id, const std::string& filepath);

// Play a sound
void playSound(const std::string& id);

// Volume
void setSoundVolume(const std::string& id, float volume);

```

### Usage Example

```cpp
// Background music
_audio.createMusic("background_music", "src/client/assets/music.ogg");
_audio.setMusicLoop("background_music", true);
_audio.setMusicVolume("background_music", 50.0f);
_audio.playMusic("background_music");

// Sound effect
_audio.loadSound("shoot_sfx", "src/client/assets/shoot.wav");
_audio.playSound("shoot_sfx");

```

---

## 🎨 Best Practices

### ✅ DO

* **Load resources at startup** (in `main.cpp` or `onEnter()`).
* **Use unique IDs** for each sprite/text/sound.
* **Clean up resources** in `onExit()` using `.clear()`.
* **Use ECS systems** to synchronize data.
* **Use z-index** to control rendering order.

### ❌ DON'T

* **Do not load the same resources multiple times.**
* **Do not call `draw()` directly** → use the systems.
* **Do not forget to `clear()**` in `onExit()`.
* **Do not mix** the old system (ButtonManager) with the new one (ECS).

---

## 📁 Template Files

```text
src/client/template/
├── ressources/
│   ├── resource_manager.cpp       # Texture/font management
│   ├── fonts.cpp
│   ├── textures.cpp
│   └── sounds.cpp
├── sprites/
│   ├── sprite_renderer.cpp        # Sprite rendering
│   ├── sprite_basics.cpp
│   ├── sprite_acces.cpp
│   └── sprite_modifications.cpp
├── text/
│   ├── text_renderer.cpp          # Text rendering
│   ├── text_basics.cpp
│   ├── text_acces.cpp
│   └── text_modifications.cpp
├── animations/
│   └── animation_renderer.cpp     # Frame-based animations
├── audio/
│   ├── audio_manager.cpp          # Music and sounds
│   ├── music_manager.cpp
│   └── sound_manager.cpp
├── button/
│   └── button_manager.cpp         # [DEPRECATED] Use ECS
└── input/
    └── input_manager.cpp          # [DEPRECATED] Use ECS

```

---

## 🔗 See Also

* [R-Type Client Guide](https://meow-type-wiki.onrender.com/wiki/Client%20Guide)
* [Create a New Scene](https://meow-type-wiki.onrender.com/wiki/Create%20a%20new%20scene)