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
 
This document describes enemy spawning and the simple AI implemented in the server sources (see `src/server/Game.cpp` and component definitions). It is intentionally concise and strictly mirrors what the code actually does.
---
 
## Spawning rules (random + ramp)
 
- Spawns are driven from `Game::run()` using:
  - accumulators: `_enemy_spawn_accumulator` and `_time_seconds`.
  - a dynamic spawn period: `_enemy_spawn_period` limited by `_enemy_spawn_period_min`.
- Spawn period ramps down over time with:
  - `double decrease = decreaseFactor * (_time_seconds / decreasePerSeconds);`
  - `_enemy_spawn_period = std::max(_enemy_spawn_period_min, 3.0 - decrease);`
  - Default config values: `decreaseFactor = 0.03`, `decreasePerSeconds = 5.0` (read from JSON).
  - Effect: period starts near 3.0s and decreases toward the configured minimum as time increases.
- When `_enemy_spawn_accumulator >= _enemy_spawn_period` a spawn occurs and the accumulator is reset.
- Spawn positions:
  - X is off-screen right (commonly `2000.0f`).
  - Y is chosen on a discrete grid: `y = 60.0f + ((std::rand() % 24) * 40)`.
- Rare extra spawn:
  - When `_enemy_spawn_period < 1.6` there is a 1-in-10 chance to spawn a second enemy.
- Waves mode:
  - If the game is in WAVES mode, `Game::update_waves_logic()` drives spawns from `/waves` in the JSON config, honoring wave duration, groups, counts and breaks.
 
---
 
## Enemy types implemented in code
 
Implemented enemy variants (components used: `enemy_ai`, `shooter`, etc.):
 
- Straight (behavior = 0)
  - Horizontal velocity left (e.g. -4.0f), `vy = 0`.
  - `enemy_ai{behavior=0, base_y, phase=0}` and a `shooter` component (direction = -1).
 
- Zigzag (behavior = 1)
  - Horizontal velocity left, vertical velocity set to `amplitude * sin(omega * t + phase)`.
  - amplitude and omega read from config (defaults: amplitude = 3.0, omega = 2.0).
  - `enemy_ai{behavior=1, base_y, phase}` plus a `shooter`.
 
- Sniper (behavior = 2)
  - Horizontal velocity uses a base plus jitter (`vxBase`, `vxJitterRange` from config).
  - Vertical velocity uses noise and smoothing (`vyNoiseRange`, `vySmooth`, `vyAlpha`).
  - When a player position is known, snipers aim projectiles at the player.
 
- Generic `spawn_enemy()` exists (random Y and speed) but periodic spawns in `run()` call `spawn_enemy_straight`, `spawn_enemy_zigzag`, or `spawn_enemy_sniper`.
 
All of the above are consistent with spawn functions: `spawn_enemy_straight`, `spawn_enemy_zigzag`, `spawn_enemy_sniper`.
 
---
 
## Server AI update (what the code does)
 
Main routine: `Game::enemy_ai_update(double current_time)`
 
- Iterates component arrays: `position`, `velocity`, `type`, `enemy_ai`, `shooter`.
- Only processes entities with `type->value == 2` (MONSTER).
- For each monster:
  - Force shooter direction left: `shooters[i]->direction = -1`.
  - If `enemy_ai` exists:
    - behavior == 0 (straight):
      - `velocities[i]->vy = 0.0f`
      - Request shoot when `std::fmod(current_time + ai->phase, shooters[i]->cooldown) < 0.02`
    - behavior == 1 (zigzag):
      - `velocities[i]->vy = amplitude * sin(omega * current_time + ai->phase)`
      - Request shoot with same fmod window
    - behavior == 2 (sniper):
      - Add small random jitter to vx: `velocities[i]->vx = vxBase + jitter`
      - Smooth vy toward random noise using `vySmooth` / `vyAlpha`
      - Request shoot with same fmod window; `shooting_system` handles aiming when possible
  - If no `enemy_ai`: fallback sets `vy = 0.0f` and uses `std::fmod(current_time, cooldown) < 0.02` to request shooting.
 
Notes:
- The `fmod` check creates a small time window (< 0.02s) to set `want_to_shoot`. The actual firing rate is enforced by `shooting_system` via `last_shot_time` and real cooldown checks, preventing rapid-fire abuse from the request window.
 
---
 
## Shooting behavior
 
- Two-stage process:
  1. AI sets `shooter->want_to_shoot = true` when timing window hits.
  2. `shooting_system(...)` checks `(current_time - last_shot_time >= cooldown)` and spawns projectile entities; it then sets `last_shot_time = current_time` and clears `want_to_shoot`.
- Projectile types:
  - Player projectiles: `type == 3` (direction == +1).
  - Enemy projectiles: `type == 4` (direction == -1).
- Sniper behavior:
  - If sniper and server knows a player's last position, projectile velocity is calculated to aim at that player (normalized to missile speed).
- Triple shot:
  - Controlled by config `/missiles/tripleShot/vy` and weapon level; the code spawns three projectiles with the configured vertical velocities and offsets when appropriate.
 
---
 
## How to add / tweak enemies (simple, with code)
 
Follow the existing spawn patterns in `Game.cpp`: spawn entity, add `position`, `velocity`, `type`, `collision`, `shooter`, `enemy_ai`, then call `broadcast_entity_creation()`.
 
Example — fast straight enemy:
```c++
void Game::spawn_enemy_fast(float x, float y)
{
    Entity enemy = _registry.spawn_entity();
    _registry.add_component(enemy, position{x, y});
    _registry.add_component(enemy, velocity{-6.0f, 0.0f}); // faster
    _registry.add_component(enemy, type{2});
    _registry.add_component(enemy, collision{40.0f, 40.0f});
    shooter s{};
    s.last_shot_time = 0.0;
    s.cooldown = 1.0;
    s.want_to_shoot = false;
    s.direction = -1;
    s.weapon_level = 1;
    _registry.add_component(enemy, s);
    _registry.add_component(enemy, enemy_ai{0, y, 0.0f});
    broadcast_entity_creation(enemy);
}
```
 
Example — wider zigzag:
```c++
void Game::spawn_enemy_wide_zigzag(float x, float y, float phase)
{
    Entity enemy = _registry.spawn_entity();
    _registry.add_component(enemy, position{x, y});
    _registry.add_component(enemy, velocity{-4.0f, 0.0f});
    _registry.add_component(enemy, type{2});
    _registry.add_component(enemy, collision{40.0f, 40.0f});
    shooter s{};
    s.last_shot_time = 0.0;
    s.cooldown = 1.2;
    s.want_to_shoot = false;
    s.direction = -1;
    s.weapon_level = 1;
    _registry.add_component(enemy, s);
    _registry.add_component(enemy, enemy_ai{1, y, phase});
    broadcast_entity_creation(enemy);
}
```
 
To add a new behaviour in `enemy_ai_update()`, add another `else if (ai->behavior == N)` block following the same pattern (set velocities and shooting logic using the same fmod-based timing and existing components).
 
---
 
## Notes & determinism
 
- Randomness sources:
  - `std::rand()` used in `Game::run()` for grid Y and phases.
  - `spawn_enemy()` uses `std::default_random_engine` seeded with `std::random_device`.
- For reproducible runs (debugging / replays), seed RNGs deterministically or remove `std::rand()` usage.
- Many parameters are configurable in `src/server/config/entities.json` and read via `Config::get(...)`:
  - enemy velocities, collision sizes, shooter cooldowns, AI parameters (`amplitude`, `omega`, `vxBase`, `vxJitterRange`, `vyNoiseRange`, `vySmooth`, `vyAlpha`), wave settings, bounds, shield visual offsets, missile config, etc.
- The server reads the JSON at startup with `Config::instance().load("src/server/config/entities.json")`.
 
---