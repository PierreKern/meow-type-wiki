# 🎮 R-Type Client Guide

Complete guide to understanding and developing for the R-Type client.

---

## 📋 Table of Contents

1. [Overview](https://www.google.com/search?q=%23overview)
2. [Client Architecture](https://www.google.com/search?q=%23client-architecture)
3. [The 14 Scenes](https://www.google.com/search?q=%23the-14-scenes)
4. [ECS System](https://www.google.com/search?q=%23ecs-system)
5. [Network (UDP)](https://www.google.com/search?q=%23network-udp)
6. [Game Modes](https://www.google.com/search?q=%23game-modes)
7. [Build System](https://www.google.com/search?q=%23build-system)
8. [Asset Management](https://www.google.com/search?q=%23asset-management)
9. [Configuration and Settings](https://www.google.com/search?q=%23configuration-and-settings)
10. [Quick Start](https://www.google.com/search?q=%23quick-start)

---

## Overview

The R-Type client is a comprehensive graphical application built with:

* **SFML 2.6.1**: Graphics, Audio, Windowing
* **Asio 1.28.0**: UDP Network Communication
* **C++20**: Modern Standard
* **ECS (Entity-Component-System)**: Game Architecture
* **Scene Architecture**: UI/Game State Management

### Key Technologies

| Technology | Version | Usage |
| --- | --- | --- |
| SFML | 2.6.1 | Graphics rendering, audio, windowing |
| Asio | 1.28.0 | Asynchronous UDP network communication |
| C++ | 20 | Main language |
| CMake | 3.14+ | Build system |
| CPM | Latest | Dependency manager |

### Key Features

* **60 FPS** cap for fluidity
* **Responsive UI** with anchoring system
* **14 complete scenes** covering the entire game flow
* **Visual effects** (particles, screen shake, trails)
* **Wave system** (progressive difficulty)
* **Multiplayer mode** (in development)

---

## Client Architecture

### Folder Structure

```text
src/client/
├── include/                     # Headers (.hpp)
│   ├── Scene.hpp                # Base scene class
│   ├── SceneManager.hpp         # Scene manager
│   ├── network_client.hpp       # UDP Client
│   ├── player_config.hpp        # Player config
│   └── [14 scene headers]       # Specific scene headers
│
├── assets/                      # Resources
│   ├── *.png                    # Textures
│   ├── *.wav                    # Sounds
│   └── RetroBiker.ttf           # Fonts
│
├── game_scene/                  # Scene Implementations
│   ├── start/
│   ├── menu/
│   ├── game/
│   └── [11 other scenes]
│
├── template/                    # SFML Managers
│   ├── animations/              # AnimationRenderer
│   ├── audio/                   # AudioManager
│   ├── button/                  # ButtonManager
│   ├── input/                   # InputManager
│   ├── ressources/              # ResourceManager
│   ├── scenes/                  # SceneManager
│   ├── sprites/                 # SpriteRenderer
│   └── text/                    # TextRenderer
│
├── main.cpp                     # Entry point
└── CMakeLists.txt               # Build configuration

```

### Architecture Diagram

```text
┌──────────────────────────────────────────────────┐
│                   main.cpp                       │
│             (Main Loop 60 FPS)                   │
└──────────────┬───────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────┐
│                 SceneManager                     │
│        (Scene Transition Management)             │
└──────────────┬───────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────┐
│              Scenes (14 total)                   │
│   Start → Menu → GameMode → GameType → Game      │
└──────────────┬───────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────┐
│           Registry ECS + Managers                │
│   ECS: Components + Systems                      │
│   Managers: Sprites, Texts, Audio, Resources     │
└──────────────┬───────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────┐
│               SFML + Asio                        │
│      Graphics Rendering + UDP Network            │
└──────────────────────────────────────────────────┘

```

### Frame Lifecycle

1. Calculate deltaTime
2. Process events (keyboard, mouse, window)
3. Change scene if necessary
4. Update active scene (logic)
5. Calculate FPS (every 1 second)
6. Clear screen
7. Draw active scene (rendering)
8. Display FPS
9. Display window

---

## The 14 Scenes

### Complete Scene Flow

```text
┌─────────────────┐
│ EpilepsyWarning │  (4s auto)
└────────┬────────┘
         ▼
┌─────────────────┐
│      Start      │
└────────┬────────┘
         ▼
┌─────────────────┐
│    GameMode     │  (Solo/Multi/Versus)
└────────┬────────┘
         ▼
┌─────────────────┐
│    GameType     │  (Waves/Survival)
└────────┬────────┘
         ▼
┌─────────────────┐
│   LevelSelect   │
└────────┬────────┘
         ▼
┌─────────────────┐      ┌──────────────┐
│      Lobby      │◄─────┤  ChooseSkin  │
└────────┬────────┘      └──────────────┘
         ▼
┌─────────────────┐      ┌──────────────┐
│      Game       │◄────►│  InGameMenu  │
└────────┬────────┘      └──────────────┘
         ▼
┌─────────────────┐      ┌──────────────┐
│  WaveComplete   │────► │   GameOver   │
└────────┬────────┘      └──────┬───────┘
         │                      │
         ▼                      ▼
┌─────────────────┐      ┌──────────────┐
│       End       │      │    Credits   │
└─────────────────┘      └──────────────┘

```

### Scene Descriptions

| Scene | File | Description | Key Properties |
| --- | --- | --- | --- |
| **EpilepsyWarning** | `epilepsy_warning.hpp` | Epilepsy warning (4s) | `_displayTimer`, `_fadeAlpha` |
| **Start** | `start.hpp` | Home screen with animated plane | `_zigzagPlane`, `_zigzagTimer` |
| **Menu** | `menu.hpp` | Main menu with settings | `_isWaitingForKey`, `_actionToRebind` |
| **ChooseSkin** | `choose_skin_scene.hpp` | Skin selection (garage) | `_skins`, `_selectedIndex` |
| **GameMode** | `game_mode_scene.hpp` | Solo/Multi/Versus choice | `_selectedMode` |
| **GameType** | `game_type_scene.hpp` | Waves/Survival choice | `_selectedType` |
| **LevelSelect** | `level_select_scene.hpp` | Starting wave selection | `_levels`, `_selectedLevel` |
| **Lobby** | `lobby_scene.hpp` | Multiplayer lobby | `_players`, `_network_client` |
| **Game** | `game.hpp` | Main gameplay | 1000+ lines, full ECS |
| **InGameMenu** | `ingame_menu.hpp` | Pause menu | Resume/Quit buttons |
| **WaveComplete** | `wave_complete_scene.hpp` | Inter-wave transition | `_completedWave`, `_waveScore` |
| **GameOver** | `game_over.hpp` | Defeat screen | Stats + Retry |
| **Credits** | `credits_scene.hpp` | Rolling credits | `_scrollOffset`, `_creditLines` |
| **End** | `end.hpp` | Final victory screen | Celebration |

### Anatomy of a Scene

Every scene inherits from `Scene` and implements:

```cpp
class MyScene : public Scene {
public:
    // Constructor (receives all managers)
    MyScene(ResourceManager& resources,
            SpriteRenderer& sprites,
            TextRenderer& texts,
            AnimationRenderer& animations,
            ButtonManager& buttons,
            InputManager& inputs,
            AudioManager& audio);

    // Lifecycle
    void onEnter() override;       // Initialization
    void onExit() override;        // Cleanup
    void update(float dt) override;// Logic
    void draw(sf::RenderWindow& window) override;  // Rendering
    void handleEvents(const sf::Event& event, sf::RenderWindow& window) override;  // Events

private:
    // Internal variables
    // Helper methods
};

```

**File Organization**:

* `include/my_scene.hpp`: Header
* `game_scene/my_scene/create.cpp`: onEnter/onExit
* `game_scene/my_scene/update.cpp`: update
* `game_scene/my_scene/draw.cpp`: draw
* `game_scene/my_scene/events.cpp`: handleEvents

---

## ECS System

### What is ECS?

**Entity-Component-System** is an architectural pattern that separates:

* **Entity**: Simple numerical identifier (ID).
* **Component**: Pure data (position, velocity, sprite, etc.).
* **System**: Logic operating on components.

### Client ECS Architecture

**Key Files**:

* [Engine/Entity/Entity.hpp](https://www.google.com/search?q=../src/Engine/Entity/Entity.hpp): Entity
* [Engine/Entity/Registry.hpp](https://www.google.com/search?q=../src/Engine/Entity/Registry.hpp): Registry
* [Engine/Components/Components.hpp](https://www.google.com/search?q=../src/Engine/Components/Components.hpp): All Components

### Main Components

#### Gameplay Components

```cpp
struct position { float x, y; };
struct velocity { float vx, vy; };
struct collision { float width, height; };
struct controllable { bool is_controlled; };
struct type { uint8_t value; };  // PLAYER=1, MONSTER=2, etc.
struct live { int health, max_health; };
struct shooter { double cooldown; int weapon_level; };
struct score { int current_score; };

```

#### Graphics Components

```cpp
struct sprite_component { std::string sprite_id; };
struct renderable { bool visible; int z_index; };
struct spritesheet_animation {
    int current_frame, total_frames;
    float frame_duration, elapsed_time;
    bool loop;
    int frame_width, frame_height, columns, row_offset;
};
struct health_bar {
    std::string bar_bg_id, bar_fill_id;
    float offset_y, width, height;
};

```

#### UI Components

```cpp
struct ui_text {
    std::string content, font_id;
    unsigned int font_size;
    uint8_t r, g, b, a;
};
struct ui_button {
    float width, height;
    bool is_hovered, is_pressed, enabled;
    std::function<void()> onClick;
};
struct ui_anchor {
    AnchorH horizontal;   // LEFT, CENTER, RIGHT
    AnchorV vertical;     // TOP, MIDDLE, BOTTOM
    float offset_x, offset_y;
};

```

#### Visual Effects Components

```cpp
struct screen_shake {
    float duration, intensity, frequency, time_elapsed;
};
struct ship_trail_particle {
    float lifetime, max_lifetime, size;
    uint8_t r, g, b;
};
struct explosion_particle {
    float lifetime, max_lifetime;
    float velocity_x, velocity_y, size;
    uint8_t r, g, b;
};
struct star_particle {
    float speed, size;
    uint8_t r, g, b, a;
};

```

### Practical Usage

#### Creating an Entity

```cpp
// In onEnter()
Entity player = _registry.spawn_entity();

// Add components
_registry.add_component(player, position{100.0f, 200.0f});
_registry.add_component(player, velocity{0.0f, 0.0f});
_registry.add_component(player, sprite_component{"player_sprite"});
_registry.add_component(player, renderable{true, 10});

```

#### Applying a System

```cpp
// In update()
auto& positions = _registry.get_components<position>();
auto& velocities = _registry.get_components<velocity>();

// Movement system
for (size_t i = 0; i < positions.size(); ++i) {
    if (positions[i] && velocities[i]) {
        positions[i]->x += velocities[i]->vx * deltaTime;
        positions[i]->y += velocities[i]->vy * deltaTime;
    }
}

```

#### Destroying an Entity

```cpp
_registry.kill_entity(enemy);

```

### Important Systems

| System | File | Role |
| --- | --- | --- |
| **movement_system** | Systems/movement_system.cpp | Applies velocity to position |
| **animation_system** | Systems/animation_system.cpp | Updates animation frames |
| **collision_system** | Systems/collision_system.cpp | Detects collisions |
| **ui_layout_system** | Systems/LayoutSystem.cpp | Responsive positioning |
| **ui_button_click_system** | Systems/UISystemsHybrid.cpp | Button click management |
| **sync_ui_text_to_renderer** | Systems/UISystemsHybrid.cpp | Syncs ECS → TextRenderer |

---

## Network (UDP)

### Network Architecture

The client uses **Asio** for asynchronous UDP communication with the server.

**File**: [include/network_client.hpp](https://www.google.com/search?q=../src/client/include/network_client.hpp)

```cpp
class NetworkClient {
private:
    asio::io_context& _io_context;
    udp::socket _socket;
    udp::endpoint _server_endpoint;
    std::array<char, 1024> _recv_buffer;
    std::queue<ReceivedPacket> _incoming_packets;
    std::mutex _queue_mutex;
};

```

### Communication Protocol

#### Packet Structure

```text
┌──────────────┬──────────────┬──────────────────┐
│ MessageType  │  Packet Size │      Payload     │
│   (1 byte)   │  (2 bytes)   │     (variable)   │
└──────────────┴──────────────┴──────────────────┘

```

#### Main Message Types

```cpp
enum class MessageType {
    // Connection
    CLIENT_HELLO = 0x01,           // Client → Server: connection
    SERVER_WELCOME = 0x02,         // Server → Client: ID assignment
    CLIENT_DISCONNECT = 0x03,      // Disconnect

    // Gameplay
    INPUT = 0x10,                  // Client → Server: player input

    // Entity Management
    ENTITY_CREATE = 0x20,          // Server → Client: create entity
    ENTITY_UPDATE = 0x21,          // Server → Client: update position/state
    ENTITY_DESTROY = 0x22,         // Server → Client: destroy entity
    ENTITY_MOVE = 0x27,            // Movement with velocity
    ENTITY_DEATH = 0x28,           // Entity death
    ENTITY_SHOOT = 0x29,           // Projectile shot
    ENTITY_HIT = 0x25,             // Damage taken
    ENTITY_COLLISION = 0x26,       // Collision

    // Wave System
    GAME_TYPE_SELECT = 0x30,       // Client → Server: game type choice
    WAVE_STATUS = 0x31,            // Server → Client: wave status
    WAVE_COMPLETE = 0x32,          // Wave completed
    ALL_WAVES_COMPLETE = 0x33      // All waves completed
};

```

#### Entity Types

```cpp
enum class EntityType {
    PLAYER = 1,           // Player
    MONSTER = 2,          // Enemy
    PLAYER_MISSILE = 3,   // Player projectile
    ENEMY_MISSILE = 4,    // Enemy projectile
    OBSTACLE = 5,         // Obstacle
    POWERUP = 6           // Power-up
};

```

### Communication Flow

#### Connection

```text
Client                          Server
  │                                │
  ├──► CLIENT_HELLO                │
  │    (name, nonce)               │
  │                                │
  │              SERVER_WELCOME ◄──┤
  │         (playerId, entityId)   │
  │                                │
  │◄────► GAME_TYPE_SELECT         │
  │       (WAVES vs SURVIVAL)      │
  │                                │

```

#### Gameplay Loop

```text
Client                          Server
  │                                │
  ├──► INPUT                       │
  │    (move, shoot)               │
  │                                │
  │          ENTITY_CREATE/UPDATE ◄┤
  │          ENTITY_DESTROY        │
  │          WAVE_STATUS           │
  │                                │
  ├──► INPUT                       │
  │    ...                         │
  │                                │
  │          WAVE_COMPLETE        ◄┤
  │          (score, stats)        │
  │                                │

```

### Usage in GameScene

```cpp
// Connect
_network_client.connect("127.0.0.1", 4242);

// Send input
_network_client.send_to_server(MessageType::INPUT, inputData);

// Receive messages
_network_client.poll();  // Processes async callbacks
while (auto packet = _network_client.pop_message()) {
    handleServerMessage(packet);
}

```

### Deserialization

**File**: [server/include/Protocol.hpp](https://www.google.com/search?q=../src/server/include/Protocol.hpp)

```cpp
inline bool deserialize(const std::vector<char>& raw, EntityUpdate& msg) {
    // Big-endian binary extraction
    // ...
}

```

**Binary Format**:

* `u8`: 1 byte
* `u16`: 2 bytes big-endian
* `u32`: 4 bytes big-endian
* `string`: fixed-size char array (16 bytes for names)

---

## Game Modes

### Game Mode (Solo/Multiplayer/Versus)

**File**: [include/game_mode_scene.hpp](https://www.google.com/search?q=../src/client/include/game_mode_scene.hpp)

```cpp
enum class GameMode {
    SOLO,          // Local solo
    MULTIPLAYER,   // Co-op (in development)
    VERSUS         // PvP (in development)
};

```

**Current State**: Only **SOLO** is fully functional.

### Game Type (Waves/Survival)

**File**: [include/game_type_scene.hpp](https://www.google.com/search?q=../src/client/include/game_type_scene.hpp)

```cpp
enum class GameType {
    WAVES,     // 10+ progressive waves
    SURVIVAL   // Infinite endurance
};

```

#### Differences

| Aspect | WAVES | SURVIVAL |
| --- | --- | --- |
| **Enemies** | Fixed number per wave | Infinite |
| **Progression** | 10+ distinct waves | Continuous |
| **Colors** | Theme per wave | Single theme |
| **Statistics** | Per wave | Cumulative |
| **Difficulty** | Predetermined | Increasing |
| **Unlocks** | Unlockable waves | N/A |

### Wave System

**File**: [include/player_config.hpp](https://www.google.com/search?q=../src/client/include/player_config.hpp)

```cpp
class PlayerConfig {
private:
    int _selectedWaveNumber;        // Starting wave (1-10+)
    int _highestWaveUnlocked;       // Highest unlocked wave

public:
    void unlockNextWave();
    void setHighestWaveUnlocked(int wave);
};

```

#### Wave Flow

1. Wave selection (LevelSelectScene)
2. Send `GAME_TYPE_SELECT` to server
3. Wave start (GameScene)
4. Receive `WAVE_STATUS` (remaining enemies)
5. Enemies eliminated
6. Receive `WAVE_COMPLETE` (stats)
7. Display WaveCompleteScene
8. Next wave or End

#### Colors per Wave

**File**: [game_scene/game/wave_colors.cpp](https://www.google.com/search?q=../src/client/game_scene/game/wave_colors.cpp)

```cpp
void GameScene::applyWaveColorTheme(int waveNumber) {
    std::vector<sf::Color> waveColors = {
        sf::Color(30, 30, 60),    // Wave 1: Dark Blue
        sf::Color(40, 20, 50),    // Wave 2: Purple
        sf::Color(50, 30, 30),    // Wave 3: Dark Red
        // ... 10+ colors
    };
    RType::Client::g_backgroundColor = waveColors[waveNumber % waveColors.size()];
}

```

---

## Build System

### CMake Configuration

**Root File**: [CMakeLists.txt](https://www.google.com/search?q=../CMakeLists.txt)

```cmake
cmake_minimum_required(VERSION 3.14)
project(r-type)

# CPM for dependencies
file(DOWNLOAD https://github.com/cpm-cmake/CPM.cmake/...
             ${CMAKE_BINARY_DIR}/cmake/CPM.cmake)
include(${CMAKE_BINARY_DIR}/cmake/CPM.cmake)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Subprojects
add_subdirectory(src/Engine)
add_subdirectory(src/server)
add_subdirectory(src/client)

```

**Client**: [src/client/CMakeLists.txt](https://www.google.com/search?q=../src/client/CMakeLists.txt)

```cmake
# Dependencies
CPMAddPackage(NAME SFML GITHUB_REPOSITORY SFML/SFML GIT_TAG 2.6.1)
CPMAddPackage(NAME asio GITHUB_REPOSITORY chriskohlhoff/asio GIT_TAG asio-1-28-0)

# Sources
file(GLOB_RECURSE CLIENT_SOURCES
    "template/**/*.cpp"
    "game_scene/**/*.cpp"
)

# Executable
add_executable(rtype_client main.cpp ${CLIENT_SOURCES})

# Includes
target_include_directories(rtype_client PRIVATE
    include template
    ../Engine ../Engine/Entity ../Engine/Components ../Engine/Systems
    ${asio_SOURCE_DIR}/asio/include
)

# Linking
target_link_libraries(rtype_client PRIVATE
    rtype_engine
    sfml-graphics sfml-window sfml-system sfml-network sfml-audio
)

# Platform-specific
if(UNIX AND NOT APPLE)
    target_link_libraries(rtype_client PRIVATE X11 GL pthread)
endif()

```

### Compilation

```bash
# 1. Create build directory
mkdir -p build && cd build

# 2. Generate build files
cmake ..

# 3. Compile (4 parallel threads)
cmake --build . -j4

# 4. Generated executable
./src/client/rtype_client

```

### Launch Script

**File**: [run.sh](https://www.google.com/search?q=../run.sh)

```bash
#!/bin/bash

# Compile
cd build && cmake --build . -j4 && cd ..

# Kill old processes
pkill -f rtype_server
pkill -f rtype_client

# Launch server
./build/src/server/rtype_server 4242 > server.log 2>&1 &

# Launch client
./build/src/client/rtype_client

```

**Usage**:

```bash
chmod +x run.sh
./run.sh

```

---

## Asset Management

### Available Assets

**Directory**: [assets/](https://www.google.com/search?q=../src/client/assets/)

#### Textures (PNG)

| File | Size | Usage |
| --- | --- | --- |
| `airplane_cat.png` | 147 KB | Default player |
| `Agathe.png`, `Dexter.png`, etc. | ~100 KB | Alternative skins |
| `Eenemi_chien_hugo.png` | ~80 KB | Enemies |
| `Munition_chat.png` | 10 KB | Player projectiles |
| `projectils_ennemi.png` | 8 KB | Enemy projectiles |
| `explosions.png` | 50 KB | Explosion spritesheet |
| `nuages.png` | 200 KB | Scrolling background |
| `heart.png`, `powerup_heart.png` | 5 KB | UI/Powerups |

#### Audio (WAV)

| File | Size | Usage |
| --- | --- | --- |
| `meow.wav` | 12 MB | Background music |
| `tir.wav` | 240 KB | Shooting effect |

#### Fonts (TTF)

| File | Size | Usage |
| --- | --- | --- |
| `RetroBiker.ttf` | 162 KB | Main retro font |

### Loading Resources

#### In main.cpp

```cpp
// Load global font
resources.loadFont("main", "./src/client/assets/RetroBiker.ttf");

// Load music
audio.createMusic("background_music", "src/client/assets/meow.wav");
audio.setMusicLoop("background_music", true);
audio.playMusic("background_music");

```

#### In a Scene (onEnter)

```cpp
void MyScene::onEnter() {
    // Load a texture (lazy loading)
    if (!_resources.hasTexture("player")) {
        _resources.loadTexture("player", "src/client/assets/airplane_cat.png");
    }

    // Create a sprite
    _sprites.create("player_sprite", "player", {100.0f, 200.0f});
}

```

#### Cleanup (onExit)

```cpp
void MyScene::onExit() {
    _registry.clear();
    _texts.clear();
    _sprites.clear();
    // Resources remain cached in ResourceManager
}

```

---

## Configuration and Settings

### Window Configuration

**File**: [main.cpp](https://www.google.com/search?q=../src/client/main.cpp)

```cpp
sf::ContextSettings settings;
settings.depthBits = 24;
settings.stencilBits = 8;
settings.antialiasingLevel = 0;
settings.majorVersion = 2;
settings.minorVersion = 1;

sf::RenderWindow window(
    sf::VideoMode::getDesktopMode(),
    "R-Type - Scene System",
    sf::Style::Fullscreen,
    settings
);

window.setFramerateLimit(60);  // 60 FPS

```

### Game Settings

**File**: [Components/Components.hpp](https://www.google.com/search?q=../src/Engine/Components/Components.hpp)

```cpp
struct game_settings {
    bool camera_shake_enabled = true;       // Screen shake
    bool warnings_enabled = true;           // Enemy warnings
    bool particles_enabled = true;          // Particles
    bool trails_enabled = true;             // Ship trails
    bool explosions_enabled = true;         // Explosions
    bool health_bars_enabled = true;        // Enemy HP bars
    bool fps_display_enabled = false;       // FPS counter
    bool fullscreen_enabled = true;         // Fullscreen
    bool vsync_enabled = true;              // Vertical Sync
    int fog_quality = 1;                    // 0=Low, 1=Med, 2=High
};

```

**Global Access**:

```cpp
#include <globals.hpp>

RType::Client::g_settings.camera_shake_enabled = false;

```

### Player Config

**File**: [include/player_config.hpp](https://www.google.com/search?q=../src/client/include/player_config.hpp)

```cpp
class PlayerConfig {  // Singleton
private:
    std::string _playerName;
    std::string _selectedSkinId;
    std::string _selectedSkinTexture;
    std::string _gameType;          // "waves" or "survival"
    int _selectedWaveNumber;
    int _highestWaveUnlocked;
    int _currentScore;
    int _enemiesKilled;
    int _shotsFired;
    int _shotsHit;
    float _playTime;
};

// Usage
auto& config = PlayerConfig::getInstance();
config.setPlayerName("Player1");
config.setSelectedSkin("agathe", "Agathe");

```

### Keyboard Controls

**File**: [include/player_config.hpp](https://www.google.com/search?q=../src/client/include/player_config.hpp)

```cpp
enum class Action {
    UP, DOWN, LEFT, RIGHT, SHOOT, AUTO_FIRE
};

struct KeyBinding {
    sf::Keyboard::Key primary;
    sf::Keyboard::Key secondary;
};

std::map<Action, KeyBinding> controls = {
    {Action::UP,        {sf::Keyboard::Z,     sf::Keyboard::Up}},
    {Action::DOWN,      {sf::Keyboard::S,     sf::Keyboard::Down}},
    {Action::LEFT,      {sf::Keyboard::Q,     sf::Keyboard::Left}},
    {Action::RIGHT,     {sf::Keyboard::D,     sf::Keyboard::Right}},
    {Action::SHOOT,     {sf::Keyboard::Space, sf::Keyboard::Unknown}},
    {Action::AUTO_FIRE, {sf::Keyboard::F,     sf::Keyboard::Unknown}}
};

```

**Rebinding**: Managed in `MenuScene` via the GUI.

---

## Quick Start

### Prerequisites

* **C++20 Compiler** (GCC 10+, Clang 12+, MSVC 2019+)
* **CMake 3.14+**
* **Git**
* **Internet Connection** (to download dependencies)

### Installation

```bash
# 1. Clone the repo
git clone <repo_url>
cd Rtype

# 2. Create build
mkdir build && cd build

# 3. Generate
cmake ..

# 4. Compile
cmake --build . -j4

# 5. Launch
cd ..
./build/src/client/rtype_client

```

### Development

#### Adding a New Scene

1. Create header `include/my_scene.hpp`
2. Create folder `game_scene/my_scene/`
3. Implement `create.cpp`, `update.cpp`, `draw.cpp`, `events.cpp`
4. Register in `main.cpp`:

```cpp
#include <my_scene.hpp>

auto myScene = std::make_unique<MyScene>(resources, sprites, texts, animations, buttons, inputs, audio);
sceneManager.addScene("my_scene", std::move(myScene));

```

5. Change scene:

```cpp
changeScene("my_scene");  // From another scene

```

#### Adding an ECS Component

1. Define in [Components/Components.hpp](https://www.google.com/search?q=../src/Engine/Components/Components.hpp):

```cpp
struct my_component {
    int value;
    float other_value;
};

```

2. Register in `onEnter()`:

```cpp
_registry.register_component<my_component>();

```

3. Use:

```cpp
Entity e = _registry.spawn_entity();
_registry.add_component(e, my_component{42, 3.14f});

auto& components = _registry.get_components<my_component>();
if (components[e]) {
    std::cout << components[e]->value << std::endl;
}

```

#### Adding an Asset

1. Place file in `src/client/assets/`
2. Load in `main.cpp` or `onEnter()`:

```cpp
_resources.loadTexture("my_asset", "src/client/assets/my_asset.png");

```

3. Use:

```cpp
_sprites.create("my_sprite", "my_asset", {x, y});

```

---

## 🔗 See Also

* [SFML Template Documentation](https://meow-type-wiki.onrender.com/wiki/)
* [Guide: Create a New Scene](https://meow-type-wiki.onrender.com/wiki/Accessibility)
* [Server Documentation](https://www.google.com/search?q=../../server/docs/) (if available)

---

## 📞 Support

* **Issues**: [GitHub Issues](https://github.com/EpitechPGE3-2025/G-CPP-500-NCY-5-2-rtype-2/issues)
* **Official SFML Documentation**: [https://www.sfml-dev.org/documentation/2.6.1/](https://www.sfml-dev.org/documentation/2.6.1/)
* **Asio Documentation**: [https://think-async.com/Asio/asio-1.28.0/doc/](https://think-async.com/Asio/asio-1.28.0/doc/)

---

**Version**: 1.0
**Last Updated**: 2025-01-17
**Author**: R-Type Team
