# Enemy AI
 
## Table of contents
1. [Introduction](#introduction)  
2. [Spawning rules (random + ramp)](#spawning-rules-random--ramp)  
3. [Enemy types implemented in code](#enemy-types-implemented-in-code)  
4. [Server AI update (what the code does)](#server-ai-update-what-the-code-does)  
5. [Shooting behavior](#shooting-behavior)  
6. [How to add / tweak enemies (simple, with code)](#how-to-add--tweak-enemies-simple-with-code)  
7. [Notes & determinism](#notes--determinism)
 
---
 
## Introduction
 
This page documents the enemy spawning and simple AI actually implemented in the server sources (see `src/server/Game.cpp` and `src/Engine/Components/Components.hpp`). It is intentionally concise and sticks to the real code: no invented functions or workflows.
 
---
 
## Spawning rules (random + ramp)
 
- Spawns are driven in `Game::run()` using:
  - accumulators: `_enemy_spawn_accumulator` and `_time_seconds`.
  - a dynamic spawn period stored in `_enemy_spawn_period` and bounded by `_enemy_spawn_period_min`.
- The code gradually decreases the spawn period over time with:
  - `double decrease = 0.03 * (_time_seconds / 5.0);`
  - `_enemy_spawn_period = std::max(_enemy_spawn_period_min, 3.0 - decrease);`
  - Effect: spawn period starts near 3.0s and drops toward the configured minimum as `_time_seconds` grows.
- When `_enemy_spawn_accumulator >= _enemy_spawn_period` a spawn happens and `_enemy_spawn_accumulator` is reset.
- Spawn X is set off-screen to the right (`float spawnX = 2000.0f;`) and Y is chosen randomly on a discrete grid:
  - `float y = 60.0f + static_cast<float>((std::rand() % 24) * 40);`
- Occasionally, when the period is low (`_enemy_spawn_period < 1.6`) a second, rarer spawn may be created (`std::rand() % 10 == 0`).
 
---
 
## Enemy types implemented in code
 
Components and values from `Components.hpp` and `Game.cpp`:
 
- `enemy_ai` component:
  - `uint8_t behavior` — 0 = straight, 1 = zigzag
  - `float base_y` — stored but mainly used as reference
  - `float phase` — used to offset oscillation
- Two concrete spawners in `Game.cpp`:
  - `spawn_enemy_straight(float x, float y)`:
    - Creates an entity with `velocity{-4.0f, 0.0f}` (moves left).
    - Adds `enemy_ai{0, y, 0.0f}` (behavior 0).
    - Adds a `shooter` component (direction -1).
  - `spawn_enemy_zigzag(float x, float y, float phase)`:
    - Creates an entity with `velocity{-4.0f, 0.0f}` (base left).
    - Adds `enemy_ai{1, y, phase}` (behavior 1) and a `shooter` (slightly different cooldown).
 
There is also a generic `spawn_enemy()` that uses `std::default_random_engine` and spawns with randomized Y and speed, but the main periodic spawns in `run()` call the two specific spawners above.
 
---
 
## Server AI update (what the code does)
 
The server updates simple enemy behavior in `Game::enemy_ai_update(double current_time)`:
 
- Iterates entity arrays: `position`, `velocity`, `type`, `enemy_ai`, `shooter`.
- Filters only entities where `type->value == 2` (MONSTER).
- For every monster:
  - Ensures shooting direction is set to left: `shooters[i]->direction = -1;`
  - If `ai->behavior == 0` (straight):
    - `velocities[i]->vy = 0.0f;` (no vertical movement)
    - Shooting is triggered with a time check:
      - `if (std::fmod(current_time + ai->phase, shooters[i]->cooldown) < 0.02) shooters[i]->want_to_shoot = true;`
  - If `ai->behavior == 1` (zigzag):
    - Vertical velocity set to a sinusoid:
      - `velocities[i]->vy = amplitude * std::sin(omega * current_time + ai->phase);`
      - In code `amplitude = 3.0f`, `omega = 2.0f`.
    - Shooting uses the same `fmod`-based check as straight enemies.
  - If there is no `enemy_ai` component, a fallback sets `vel.y = 0.0f` and triggers shooting based on `current_time` and `cooldown`.
 
Notes about movement:
- Horizontal velocity is set on spawn (`-4.0f`) and remains the base forward speed for both types.
- Zigzag lateral movement is implemented by modifying `vy` every update using `sin(omega * current_time + phase)`; the phase comes from spawn (randomized for variety).
 
---
 
## Shooting behavior
 
- Shooting is driven by the `shooter` component:
  - `double cooldown` controls rate.
  - `bool want_to_shoot` is set by `enemy_ai_update()` when time condition matches.
- Actual projectile creation is done by `shooting_system(...)` in `src/server/Game.cpp`:
  - When `want_to_shoot` and enough time passed since `last_shot_time`, a missile entity is spawned.
  - Missile velocity and type depend on `shooter->direction` (`+1` player, `-1` enemy).
  - Player missiles are logged in magenta; server also collects created missiles for later broadcast.
 
Timing detail used by AI to request shots:
- The code uses `std::fmod(current_time + ai->phase, shooters[i]->cooldown) < 0.02` as a small time window to set `want_to_shoot`. The `shooting_system` itself enforces real cooldown using `last_shot_time`.
 
---
 
## How to add / tweak enemies (simple, with code)
 
Below are small, concrete code snippets you can drop into `src/server/Game.cpp` following the existing patterns. These snippets follow the same component usage already present in the codebase.
 
1) Add a new spawn function (copy the style of existing spawners):
 
```c++
// Example: spawn a faster straight enemy
void Game::spawn_enemy_fast(float x, float y)
{
    Entity enemy = _registry.spawn_entity();
    _registry.add_component(enemy, position{x, y});
    // Faster horizontal speed than default straight enemy
    _registry.add_component(enemy, velocity{-6.0f, 0.0f});
    _registry.add_component(enemy, type{2}); // MONSTER
    _registry.add_component(enemy, collision{40.0f, 40.0f});
    // shooter: last_shot_time=0, cooldown=1.0 (slower firing), want_to_shoot=false, direction=-1 (left)
    _registry.add_component(enemy, shooter{0.0, 1.0, false, -1});
    // Use behavior 0 (straight). base_y set to spawn y, phase 0
    _registry.add_component(enemy, enemy_ai{0 /*straight*/, y, 0.0f});
 
    broadcast_entity_creation(enemy);
}
```
 
2) If you want a new zigzag variant with different amplitude/frequency just set a different phase or store params in `base_y`/`phase` (simple approach):
 
```c++
// Example: spawn a wide zigzag enemy with larger phase offset
void Game::spawn_enemy_wide_zigzag(float x, float y, float phase)
{
    Entity enemy = _registry.spawn_entity();
    _registry.add_component(enemy, position{x, y});
    _registry.add_component(enemy, velocity{-4.0f, 0.0f});
    _registry.add_component(enemy, type{2});
    _registry.add_component(enemy, collision{40.0f, 40.0f});
    _registry.add_component(enemy, shooter{0.0, 1.2, false, -1});
    // Keep behavior==1 (zigzag), use base_y to store amplitude hint if needed and phase to offset
    _registry.add_component(enemy, enemy_ai{1 /*zigzag*/, y /*base_y*/, phase});
    broadcast_entity_creation(enemy);
}
```
 
3) To extend `enemy_ai_update()` to support a new behavior value, follow the exact same update pattern already used:
 
```c++
void Game::enemy_ai_update(double current_time)
{
    auto &positions = _registry.get_components<position>();
    auto &velocities = _registry.get_components<velocity>();
    auto &types = _registry.get_components<type>();
    auto &ais = _registry.get_components<enemy_ai>();
    auto &shooters = _registry.get_components<shooter>();
 
    for (size_t i = 0; i < positions.size(); ++i) {
        if (!(positions[i] && velocities[i] && types[i]))
            continue;
        if (types[i]->value != 2) // only MONSTER
            continue;
 
        if (i < shooters.size() && shooters[i])
            shooters[i]->direction = -1;
 
        if (i < ais.size() && ais[i]) {
            auto &ai = ais[i];
            if (ai->behavior == 0) {
                velocities[i]->vy = 0.0f;
                if (i < shooters.size() && shooters[i]) {
                    if (std::fmod(current_time + ai->phase, shooters[i]->cooldown) < 0.02)
                        shooters[i]->want_to_shoot = true;
                }
            } else if (ai->behavior == 1) {
                float amplitude = 3.0f;
                float omega = 2.0f;
                velocities[i]->vy = amplitude * std::sin(omega * current_time + ai->phase);
                if (i < shooters.size() && shooters[i]) {
                    if (std::fmod(current_time + ai->phase, shooters[i]->cooldown) < 0.02)
                        shooters[i]->want_to_shoot = true;
                }
            } else if (ai->behavior == 2) {
                // NEW: example behavior 2 = fast straight (no vertical movement)
                // Keep it simple and consistent with existing code
                velocities[i]->vy = 0.0f;
                // Optionally adjust horizontal speed if you want, but horizontal speed is set on spawn
                if (i < shooters.size() && shooters[i]) {
                    if (std::fmod(current_time + ai->phase, shooters[i]->cooldown) < 0.02)
                        shooters[i]->want_to_shoot = true;
                }
            }
        } else {
            // fallback
            velocities[i]->vy = 0.0f;
            if (i < shooters.size() && shooters[i]) {
                if (std::fmod(current_time, shooters[i]->cooldown) < 0.02)
                    shooters[i]->want_to_shoot = true;
            }
        }
    }
}
```
 
Important: the above `behavior == 2` branch is an example of how to extend the code; it follows the same structure and uses only functions/components present in the repository.
 
---
 
## Notes & determinism
 
- Randomness used in spawns:
  - `std::rand()` is used in `Game::run()` to pick Y and phase for zigzag spawns.
  - `spawn_enemy()` uses a `std::default_random_engine` seeded with `std::random_device{}`.
- If reproducible runs are required for debugging/replays, replace or seed RNGs deterministically (e.g., use a fixed seed for `std::default_random_engine` and avoid `std::rand()` or seed it).
- This document purposely mirrors the code: no extra abstractions are assumed. If you want a refactor (data-driven parameters, deterministic RNG), make changes in the codebase and update this doc accordingly.