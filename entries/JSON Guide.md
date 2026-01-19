# `entities.json` --- Server Configuration Guide

## 🎮 Player --- Fields Meaning

-   **startX** --- Absolute X spawn position\
-   **startYOffset** --- Vertical offset at spawn\
-   **type** --- Entity ID (1 = player in this project)\
-   **live** --- Starting lives / HP\
-   **collision.width/height** --- Hitbox size\
-   **velocity.vx/vy** --- Initial movement\
-   **shooter.cooldown** --- Seconds between shots\
-   **shooter.direction** --- 1 = right, -1 = left\
-   **shooter.weapon_level** --- Determines shot pattern\
-   **speed** --- Movement speed

### Practical effects

-   Higher **speed** = faster movement.\
-   Larger **collision** = easier to hit.

------------------------------------------------------------------------

## 👾 Enemies

Each key inside `enemies` defines a new enemy template.

### Example

``` json
"straight": {
  "type": 2,
  "live": 1,
  "collision": { "width": 40.0, "height": 40.0 },
  "velocity": { "vx": -4.0, "vy": 0.0 },
  "shooter": { "cooldown": 1.0, "direction": -1 },
  "ai": { "behavior": 0 },
  "spawn": { "x": 2000.0 }
}
```

### Common fields --- Meaning

-   **type** --- Entity ID (2 = enemy)\
-   **live** --- Hits required to destroy\
-   **collision** --- Hitbox size\
-   **velocity.vx** --- Horizontal speed (negative = moves left)\
-   **shooter** --- Optional shooting behavior\
-   **ai.behavior** --- AI type\
-   **spawn.x** --- X position where the enemy appears

### AI behaviors

-   **0 --- Straight movement**\
-   **1 --- Zigzag (amplitude, omega)**\
-   **2 --- Advanced/sniper (jitter + noise parameters)**

> If you set an AI behavior that is not implemented in code, it will
> simply be ignored.

------------------------------------------------------------------------

## 🚀 Missiles

``` json
"missiles": {
  "player": { "speed": 15.0, "collision": { "width": 20.0, "height": 10.0 } },
  "enemy": { "speed": 15.0, "collision": { "width": 20.0, "height": 10.0 } },
  "tripleShot": { "vy": [-3.0, 0.0, 3.0], "offsetY": 20.0, "offsetX": 40.0 }
}
```

### Field --- Meaning

-   **player.speed** --- Base projectile speed\
-   **enemy.speed** --- Enemy projectile speed\
-   **collision** --- Projectile hitbox\
-   **tripleShot.vy** --- Vertical velocities for multi-shot\
-   **offsetX/Y** --- Spawn offsets from shooter

> The actual missile type ID is assigned in Game.cpp.

------------------------------------------------------------------------

## ⚔️ enemySpawn (SURVIVAL mode)

``` json
"enemySpawn": {
  "periodStart": 3.0,
  "periodMin": 1.2,
  "decreaseFactor": 0.03,
  "decreasePerSeconds": 5.0
}
```

This controls how fast enemies spawn over time: - Starts slow
(**periodStart**)\
- Gradually speeds up\
- Never goes below **periodMin**

------------------------------------------------------------------------

## 🌊 Waves (WAVES mode)

Each wave lasts a fixed time and contains spawn groups.

### Example wave

``` json
{
  "duration": 20.0,
  "groups": [
    { "type": "straight", "period": 2.5, "count": 8 },
    { "type": "zigzag", "period": 4.0, "count": 0 }
  ]
}
```

### Group fields --- Meaning

-   **type** --- Must match an enemy name in `enemies`\
-   **period** --- Seconds between spawns\
-   **count** --- Total enemies to spawn (0 = disabled)

> Spawn Y is chosen randomly between `wavesSettings.yMin` and `yMax`.

------------------------------------------------------------------------

## ⚙️ wavesSettings

``` json
"wavesSettings": {
  "breakDuration": 5.0,
  "loop": true,
  "yMin": 60.0,
  "yMax": 540.0
}
```

### Field --- Meaning

-   **breakDuration** --- Pause between waves\
-   **loop** --- Restart from first wave if true\
-   **yMin/yMax** --- Vertical spawn range

------------------------------------------------------------------------

## 🗺️ Bounds

``` json
"bounds": { "xMin": -200.0, "xMax": 2000.0, "yMin": -200.0, "yMax": 1200.0 }
```

> Entities outside this area are automatically destroyed.

------------------------------------------------------------------------

## 🛡️ shieldVisualOffset

``` json
"shieldVisualOffset": { "x": -50.0, "y": -50.0 }
```

> Purely visual --- does not affect gameplay.

------------------------------------------------------------------------

# ➕ HOW TO ADD A NEW ENEMY (STEP-BY-STEP)

## Step 1 --- Add the enemy template

``` json
"kamikaze": {
  "type": 2,
  "live": 2,
  "collision": { "width": 36.0, "height": 36.0 },
  "velocity": { "vx": -6.0, "vy": 0.0 },
  "ai": { "behavior": 0 },
  "spawn": { "x": 2000.0 }
}
```

## Step 2 --- Add it to a wave

``` json
{
  "duration": 30.0,
  "groups": [
    { "type": "kamikaze", "period": 1.5, "count": 10 },
    { "type": "straight", "period": 2.0, "count": 8 }
  ]
}
```

## Step 3 --- Restart the server

Changes do not apply live.

------------------------------------------------------------------------

# ➕ HOW TO ADD OR MODIFY A WAVE

``` json
{
  "duration": 40.0,
  "groups": [
    { "type": "zigzag", "period": 2.0, "count": 12 },
    { "type": "kamikaze", "period": 1.2, "count": 20 }
  ]
}
```

### Rules

-   `type` must match an existing enemy.\
-   `count` controls how many spawn total.\
-   `period` controls spawn spacing.\
-   Spawn Y is random inside `wavesSettings.yMin/yMax`.

------------------------------------------------------------------------

## ✅ Best practices

-   Always validate JSON after editing.\
-   Restart the server after changes.\
-   Start with low counts and high periods when testing.\
-   Keep `spawn.x` off-screen (e.g., 2000.0).\
-   Don't invent new AI behaviors unless you code them in C++.

------------------------------------------------------------------------

## 🔍 How the code reads this file

``` cpp
Config::instance().load("src/server/config/entities.json");
```

### Examples

``` cpp
float speed = Config::instance().get<float>("/player/speed", 7.0f);

auto vy = Config::instance().getArrayFloat("/missiles/tripleShot/vy");
```
