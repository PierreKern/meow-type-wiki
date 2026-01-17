# 📝 R-Type Global Verification Protocol


## 🛠 1. Configuration & UI (Settings)
- [ ] **Menu Access:** Launch the client and enter "SETTINGS" without crashing.
- [ ] **Key Binding Display:** Verify that each action (Up, Down, Left, Right, Shoot, Auto-fire) displays two columns (Primary / Secondary).
- [ ] **Rebinding Procedure:**
    - [ ] Click a button -> Text should indicate "Waiting for input".
    - [ ] Press a keyboard key -> The button must update instantly with the new key name.
- [ ] **Volume Control:** - [ ] Click `+` and `-` buttons.
    - [ ] Verify that the percentage text updates and the actual audio volume changes.

## 🕹 2. Input System (Keyboard & Gamepad)
- [ ] **Double Mapping:** Move the ship using `ZQSD` (or `WASD`) AND the `Arrow Keys` simultaneously.
- [ ] **Manual Fire:** Verify that the `Space` bar (or bound key) triggers a single shot per press.
- [ ] **Auto-fire (Toggle):**
    - [ ] Press `F` -> Automatic firing begins (0.2s interval).
    - [ ] Press `F` again -> Firing stops immediately.
- [ ] **Joystick Support:** Connect a controller and verify that the left analog stick is detected for movement.

## 🌐 3. Protocol Integrity (Network Alignment)
- [ ] **Binary Alignment:** Ensure ship position is synchronized between client and server (no "ghost" offsets).
- [ ] **Score Update:** Destroy an enemy and confirm the `SCORE` UI increments.
    - *Note: If the score shows incoherent numbers, check the variable order in `Protocol.hpp`.*
- [ ] **Health Sync (Live):** Take damage and verify that UI hearts/health bar decrease accordingly.
- [ ] **Interpolation:** Verify that other players and enemies move smoothly without jittering or "teleporting."



## 🎨 4. Visual Feedback & Game States
- [ ] **Wave Transition:** Reach the score threshold (e.g., 100 points).
    - [ ] The wave label must update (e.g., `WAVE 2`).
    - [ ] Ambient background color must change via `applyWaveColorTheme`.
- [ ] **Death Feedback:** Verify that the player's explosion animation plays fully before transitioning to the `Game Over` screen.

## ⚙️ 5. Engine Robustness (ECS & Systems)
- [ ] **Memory Leaks:** Run the game for 5+ minutes with constant firing. Monitor RAM usage to ensure projectile entities are being cleaned up.
- [ ] **Entity Cleanup:** Verify that enemies/missiles exiting the screen bounds are properly destroyed in the ECS.
- [ ] **Frame-rate Independence:** Ensure the ship moves at the same speed on different monitors (60Hz vs 144Hz) using `DeltaTime`.
- [ ] **Z-Ordering:** Verify that missiles pass *under* the UI/HUD but *over* the background layers.



## 👥 6. Multiplayer & Synchronization
- [ ] **Simultaneous Connections:** Connect 2-4 clients. Verify they see each other with distinct player colors.
- [ ] **Race Conditions:** Two players shoot the same enemy. Verify only one receives the score and the other doesn't crash.
- [ ] **Disconnection/Rejoin:** Kill a client process. Verify the server frees the slot and allows a fresh connection.

## 📡 7. Stress Test & Network Resilience
- [ ] **Saturation:** Spawn 50+ enemies at once. Verify the client processes the packet burst without freezing.
- [ ] **Packet Loss Handling:** Simulate high latency. Verify entities move smoothly toward their last known position (Dead Reckoning).
- [ ] **Security/Deserialization:** Ensure the client ignores malformed or "garbage" packets without crashing.

## 🔊 8. Audio & Atmosphere
- [ ] **Spatialization:** Verify SFX (shots/explosions) are panned correctly based on the entity's screen position.
- [ ] **Mixing:** Ensure background music (BGM) volume is balanced against sound effects (SFX).
- [ ] **BGM Looping:** Verify the music restarts seamlessly without a noticeable gap or click.



## 🏁 9. End-Game Conditions
- [ ] **Win Condition:** Complete the final wave. Verify transition to the Victory screen.
- [ ] **Score Consistency:** Verify the final score on the Game Over screen matches the last score received in-game.
- [ ] **State Reset:** Clicking "BACK TO MENU" must reset all session variables (score, current wave, player stats).