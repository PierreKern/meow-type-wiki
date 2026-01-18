Here is the complete translation of the "Guide: Create a New Graphical Scene" into English.

# 🎬 Guide: Creating a New Graphical Scene

Complete guide to creating a new scene in the R-Type client.

---

## 📋 Table of Contents

1. [Overview](https://www.google.com/search?q=%23overview)
2. [File Structure](https://www.google.com/search?q=%23file-structure)
3. [Step 1: Create the Header](https://www.google.com/search?q=%23step-1-create-the-header)
4. [Step 2: Implement create.cpp](https://www.google.com/search?q=%23step-2-implement-createcpp)
5. [Step 3: Implement update.cpp](https://www.google.com/search?q=%23step-3-implement-updatecpp)
6. [Step 4: Implement draw.cpp](https://www.google.com/search?q=%23step-4-implement-drawcpp)
7. [Step 5: Implement events.cpp](https://www.google.com/search?q=%23step-5-implement-eventscpp)
8. [Step 6: Integrate into SceneManager](https://www.google.com/search?q=%23step-6-integrate-into-scenemanager)
9. [Best Practices](https://www.google.com/search?q=%23best-practices)
10. [Complete Examples](https://www.google.com/search?q=%23complete-examples)

---

## Overview

A **scene** in R-Type is a class that inherits from `Scene` and represents a complete state of the application (menu, game, lobby, etc.).

### Scene Architecture

```text
┌─────────────────────────────────────────┐
│              SceneManager               │
│      (manages scene transitions)        │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│        My Scene (inherits Scene)        │
│                                         │
│  onEnter()  ──► Initialization          │
│  update()   ──► Logic                   │
│  draw()     ──► Rendering               │
│  events()   ──► Event Handling          │
│  onExit()   ──► Cleanup                 │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│     Registry ECS + Template Managers    │
│    (components, systems, renderers)     │
└─────────────────────────────────────────┘

```

### Lifecycle

1. **Scene Change** → `SceneManager::changeScene()`
2. **onExit()** of the old scene → Cleanup
3. **onEnter()** of the new scene → Initialization
4. **Loop**:
* `events()` → Event handling
* `update(deltaTime)` → Logic update
* `draw(window)` → Graphic rendering


5. **Scene Change** → Return to step 1

---

## File Structure

To create a new scene called `my_scene`, create the following files:

```text
src/client/
├── include/
│   └── my_scene.hpp                     # Scene Header
└── game_scene/
    └── my_scene/
        ├── create.cpp                   # Initialization (onEnter/onExit)
        ├── update.cpp                   # Logic (update)
        ├── draw.cpp                     # Rendering (draw)
        └── events.cpp                   # Events (handleEvents)

```

---

## Step 1: Create the Header

**File**: `src/client/include/my_scene.hpp`

```cpp
/*
** EPITECH PROJECT, 2025
** R-Type
** File description:
** My Scene Header
*/

#pragma once

#include <Scene.hpp>
#include <SceneManager.hpp>

namespace RType {
namespace Client {

    class MyScene : public Scene {
    public:
        // Constructor (inherited from Scene)
        MyScene(ResourceManager& resources,
                SpriteRenderer& sprites,
                TextRenderer& texts,
                AnimationRenderer& animations,
                ButtonManager& buttons,
                InputManager& inputs,
                AudioManager& audio);

        // Scene Lifecycle
        void onEnter() override;
        void onExit() override;
        void update(float deltaTime) override;
        void draw(sf::RenderWindow& window) override;
        void handleEvents(const sf::Event& event, sf::RenderWindow& window) override;

    private:
        // Private scene variables
        float _timer;
        bool _someFlag;

        // Helper methods (optional)
        void setupUI();
        void handleButtonClick(const std::string& buttonId);
    };

} // namespace Client
} // namespace RType

```

---

## Step 2: Implement create.cpp

**File**: `src/client/game_scene/my_scene/create.cpp`

```cpp
/*
** EPITECH PROJECT, 2025
** R-Type
** File description:
** My Scene - Create
*/

#include <my_scene.hpp>
#include <Components.hpp>
#include <iostream>

namespace RType {
namespace Client {

    MyScene::MyScene(ResourceManager& resources, SpriteRenderer& sprites, TextRenderer& texts, AnimationRenderer& animations, ButtonManager& buttons, InputManager& inputs, AudioManager& audio)
        : Scene(resources, sprites, texts, animations, buttons, inputs, audio)
        , _timer(0.0f)
        , _someFlag(false)
    {}

    void MyScene::onEnter()
    {
        // 1. Reset variables
        _timer = 0.0f;
        _someFlag = false;

        // 2. Register necessary ECS components
        _registry.register_component<position>();
        _registry.register_component<ui_text>();
        _registry.register_component<ui_button>();
        _registry.register_component<ui_anchor>();
        _registry.register_component<renderable>();
        _registry.register_component<sprite_component>();

        // 3. Load resources (if not already done in main.cpp)
        // _resources.loadTexture("my_texture", "src/client/assets/my_texture.png");
        // _resources.loadFont("main", "src/client/assets/RetroBiker.ttf");

        // 4. Create UI entities
        setupUI();

        // 5. Start music (optional)
        // _audio.playMusic("my_music", true);
    }

    void MyScene::onExit()
    {
        // 1. Clear the ECS registry
        _registry.clear();

        // 2. Clear renderers
        _texts.clear();
        _sprites.clear();

        // 3. Stop music (optional)
        // _audio.stopMusic("my_music");
    }

    void MyScene::setupUI()
    {
        // Create a title
        createAnchoredText(
            "My Title",
            "main",
            AnchorH::CENTER, AnchorV::TOP,
            0.0f, 100.0f,
            48,
            255, 215, 0, 255,
            100
        );

        // Create a button
        createAnchoredButton(
            "my_button",
            "main",
            "Click me!",
            AnchorH::CENTER, AnchorV::MIDDLE,
            0.0f, 0.0f,
            24,
            255, 255, 255, 255,
            100, 200, 255, 255,
            100
        );
    }

} // namespace Client
} // namespace RType

```

---

## Step 3: Implement update.cpp

**File**: `src/client/game_scene/my_scene/update.cpp`

```cpp
/*
** EPITECH PROJECT, 2025
** R-Type
** File description:
** My Scene - Update
*/

#include <my_scene.hpp>
#include <UISystemsHybrid.hpp>
#include <iostream>

namespace RType {
namespace Client {

    void MyScene::update(float deltaTime)
    {
        // 1. Update timer
        _timer += deltaTime;

        // 2. Get necessary components
        auto& positions = _registry.get_components<position>();
        auto& ui_buttons = _registry.get_components<ui_button>();
        auto& ui_texts = _registry.get_components<ui_text>();

        // 3. Apply ECS systems
        // (e.g., button hover system)
        // ui_button_hover_system(_registry, positions, ui_buttons, sf::Mouse::getPosition(window));

        // 4. Game logic (example: change scene after 5 seconds)
        if (_timer > 5.0f && _someFlag == false) {
            _someFlag = true;
            std::cout << "Timer reached 5 seconds!" << std::endl;
            // changeScene("other_scene");
        }

        // 5. Update animations (if applicable)
        _animations.update(deltaTime);
    }

} // namespace Client
} // namespace RType

```

---

## Step 4: Implement draw.cpp

**File**: `src/client/game_scene/my_scene/draw.cpp`

```cpp
/*
** EPITECH PROJECT, 2025
** R-Type
** File description:
** My Scene - Draw
*/

#include <my_scene.hpp>
#include <UISystemsHybrid.hpp>
#include <LayoutSystem.hpp>

namespace RType {
namespace Client {

    void MyScene::draw(sf::RenderWindow& window)
    {
        // 1. Background (color or sprite)
        window.clear(sf::Color(20, 20, 40));

        // 2. Get ECS components
        auto& positions = _registry.get_components<position>();
        auto& ui_texts = _registry.get_components<ui_text>();
        auto& ui_buttons = _registry.get_components<ui_button>();
        auto& ui_anchors = _registry.get_components<ui_anchor>();
        auto& renderables = _registry.get_components<renderable>();
        auto& ui_inputs = _registry.get_components<ui_input_field>();

        // 3. Apply responsive layout system
        ui_layout_system(_registry, positions, ui_anchors, window.getSize());

        // 4. Sync ECS texts → TextRenderer
        sync_ui_text_to_renderer(_registry, positions, ui_texts, ui_anchors, renderables, ui_inputs, _texts);

        // 5. Sync ECS buttons → TextRenderer
        sync_ui_button_to_renderer(_registry, positions, ui_buttons, ui_anchors, renderables, _texts);

        // 6. Draw sprites (if applicable)
        _sprites.draw(window);

        // 7. Draw texts
        _texts.draw(window);
    }

} // namespace Client
} // namespace RType

```

---

## Step 5: Implement events.cpp

**File**: `src/client/game_scene/my_scene/events.cpp`

```cpp
/*
** EPITECH PROJECT, 2025
** R-Type
** File description:
** My Scene - Events
*/

#include <my_scene.hpp>
#include <UISystemsHybrid.hpp>
#include <iostream>

namespace RType {
namespace Client {

    void MyScene::handleEvents(const sf::Event& event, sf::RenderWindow& window)
    {
        // 1. Get necessary components
        auto& positions = _registry.get_components<position>();
        auto& ui_buttons = _registry.get_components<ui_button>();

        // 2. Handle button clicks
        ui_button_click_system(_registry, positions, ui_buttons, event, window, [this](const std::string& buttonId) {
            handleButtonClick(buttonId);
        });

        // 3. Handle specific events
        if (event.type == sf::Event::KeyPressed) {
            if (event.key.code == sf::Keyboard::Escape) {
                // Return to main menu
                changeScene("menu");
            }
            else if (event.key.code == sf::Keyboard::Space) {
                std::cout << "Space pressed!" << std::endl;
                // Custom action
            }
        }

        // 4. Handle input fields (if applicable)
        // auto& ui_inputs = _registry.get_components<ui_input_field>();
        // ui_input_field_event_system(_registry, positions, ui_inputs, event, window);
    }

    void MyScene::handleButtonClick(const std::string& buttonId)
    {
        std::cout << "Button clicked: " << buttonId << std::endl;

        if (buttonId == "my_button") {
            // Play sound
            _audio.playSound("click_sfx");

            // Change scene
            changeScene("other_scene");
        }
    }

} // namespace Client
} // namespace RType

```

---

## Step 6: Integrate into SceneManager

### 6.1 Add Include

**File**: `src/client/main.cpp`

```cpp
#include <my_scene.hpp>

```

### 6.2 Register the Scene

**In** `main.cpp`, **after** creating the managers:

```cpp
// Create the scene
auto myScene = std::make_unique<MyScene>(resources, sprites, texts, animations, buttons, inputs, audio);

// Add it to the SceneManager
sceneManager.addScene("my_scene", std::move(myScene));

```

### 6.3 Start on This Scene (Optional)

```cpp
sceneManager.changeScene("my_scene");

```

---

## Best Practices

### ✅ DO

* **Always** register ECS components in `onEnter()`.
* **Always** clean up in `onExit()` using `_registry.clear()`, `_texts.clear()`, `_sprites.clear()`.
* **Use** ECS systems to synchronize data.
* **Prefer** `createAnchoredText()` and `createAnchoredButton()` for responsive UI.
* **Separate** logic into distinct files (create, update, draw, events).
* **Use** `changeScene()` to switch scenes.
* **Play** sounds with `_audio.playSound()` for feedback.

### ❌ DON'T

* **Do not** manipulate SFML directly (`sf::Text`, `sf::Sprite`) → go through the renderers.
* **Do not** forget to `clear()` in `onExit()` → risk of memory leaks.
* **Do not** load resources in every `onEnter()` → do it once in `main.cpp`.
* **Do not** use fixed positions → use the responsive anchor system.
* **Do not** mix the old system (direct ButtonManager) with the new one (ECS).

---

## Complete Examples

### Example 1: Minimalist Scene

**Scene that displays text and changes after 3 seconds**

```cpp
// my_scene.hpp
class MyScene : public Scene {
public:
    MyScene(ResourceManager& resources, SpriteRenderer& sprites, TextRenderer& texts, AnimationRenderer& animations, ButtonManager& buttons, InputManager& inputs, AudioManager& audio);
    void onEnter() override;
    void onExit() override;
    void update(float deltaTime) override;
    void draw(sf::RenderWindow& window) override;
    void handleEvents(const sf::Event& event, sf::RenderWindow& window) override;
private:
    float _timer;
};

// create.cpp
void MyScene::onEnter() {
    _timer = 0.0f;
    _registry.register_component<position>();
    _registry.register_component<ui_text>();
    _registry.register_component<ui_anchor>();
    _registry.register_component<renderable>();
    createAnchoredText("Loading...", "main", AnchorH::CENTER, AnchorV::MIDDLE, 0.0f, 0.0f, 36, 255, 255, 255, 255, 100);
}

void MyScene::onExit() {
    _registry.clear();
    _texts.clear();
}

// update.cpp
void MyScene::update(float deltaTime) {
    _timer += deltaTime;
    if (_timer > 3.0f) {
        changeScene("menu");
    }
}

// draw.cpp
void MyScene::draw(sf::RenderWindow& window) {
    window.clear(sf::Color::Black);
    auto& positions = _registry.get_components<position>();
    auto& ui_texts = _registry.get_components<ui_text>();
    auto& ui_anchors = _registry.get_components<ui_anchor>();
    auto& renderables = _registry.get_components<renderable>();
    auto& ui_inputs = _registry.get_components<ui_input_field>();
    ui_layout_system(_registry, positions, ui_anchors, window.getSize());
    sync_ui_text_to_renderer(_registry, positions, ui_texts, ui_anchors, renderables, ui_inputs, _texts);
    _texts.draw(window);
}

// events.cpp
void MyScene::handleEvents(const sf::Event& event, sf::RenderWindow& window) {
    // Nothing to do
}

```

### Example 2: Scene with Buttons

**Scene with 2 buttons: Play and Quit**

```cpp
// onEnter()
void MyScene::onEnter() {
    _registry.register_component<position>();
    _registry.register_component<ui_text>();
    _registry.register_component<ui_button>();
    _registry.register_component<ui_anchor>();
    _registry.register_component<renderable>();

    // Title
    createAnchoredText("My Menu", "main", AnchorH::CENTER, AnchorV::TOP, 0.0f, 100.0f, 48, 255, 215, 0, 255, 100);

    // Play Button
    createAnchoredButton("play_button", "main", "PLAY", AnchorH::CENTER, AnchorV::MIDDLE, 0.0f, -50.0f, 32, 255, 255, 255, 255, 100, 200, 255, 255, 100);

    // Quit Button
    createAnchoredButton("quit_button", "main", "QUIT", AnchorH::CENTER, AnchorV::MIDDLE, 0.0f, 50.0f, 32, 255, 255, 255, 255, 100, 200, 255, 255, 100);
}

// events.cpp
void MyScene::handleEvents(const sf::Event& event, sf::RenderWindow& window) {
    auto& positions = _registry.get_components<position>();
    auto& ui_buttons = _registry.get_components<ui_button>();

    ui_button_click_system(_registry, positions, ui_buttons, event, window, [this](const std::string& buttonId) {
        if (buttonId == "play_button") {
            _audio.playSound("click_sfx");
            changeScene("game");
        } else if (buttonId == "quit_button") {
            _audio.playSound("click_sfx");
            exit(0);
        }
    });
}

```

---

## 🔗 See Also

* [SFML Template Documentation](https://https://meow-type-wiki.onrender.com//TEMPLATE_SFML.md)
* [R-Type Client Guide](https://www.google.com/search?q=./CLIENT_GUIDE.md)