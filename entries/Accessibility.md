# 🔎 Comparative Study: Accessibility in an R-Type Style Video Game

## 1. Introduction
As part of the development of our networked game inspired by **R-Type**, we studied the main accessibility recommendations derived from current video game standards (WCAG 2.1, Game Accessibility Guidelines, AAA practices).

The objective is twofold:
1. Identify the difficulties encountered by players with different types of disabilities.
2. Compare existing solutions to select those that can be integrated into our production without excessively increasing its complexity.

This study covers three main categories of accessibility:
- **Physical and Motor**
- **Audio and Visual**
- **Mental and Cognitive**

---

## 2. Physical and Motor Accessibility

### 2.1 Identified Issues
People with motor disabilities may experience:
- Difficulty reaching specific keys.
- Inability to hold a key down (holding vs. toggling).
- Need to use a controller (gamepad) rather than a keyboard.
- Difficulty performing multiple simultaneous actions.

A shoot ’em up like *R-Type* requires reflexes, precision, and repetitive actions, which can represent a significant barrier.

### 2.2 Existing Solutions (Comparison)

| Solution | Pros | Cons | Feasibility for our project |
|---|---:|---|---|
| **Full Key Rebinding** | Indispensable and highly useful | Requires an options menu | **Highly Feasible** |
| **Controller Support** | Increased accessibility | Significant development time | Feasible, but not priority |
| **Keyboard Alternatives (WASD, Arrows)** | Very simple | Low customization | **Easily Implemented** |
| **Toggleable Auto-fire** | Reduces motor strain | Slightly modifies gameplay | **Feasible** |
| **"Slow-motion" Mode** | Useful for severe disabilities | Breaks gameplay balance | Not suitable |

### 2.3 Selected Choices
We retain:
- Full keyboard remapping
- Alternative default keys (WASD / Arrows)
- Auto-fire option

These elements offer high accessibility value for a low development cost.

---

## 3. Audio and Visual Accessibility

### 3.1 Identified Issues
Target audience:
- Color blindness
- Visual impairment
- Total or partial deafness
- Sensitivity to contrast or brightness

Difficulties in a shoot ’em up:
- Shots and enemies blending together.
- Warning sounds impossible to hear.
- Lighting effects potentially bothersome.
- Enemy spawn speed difficult to track visually.

### 3.2 Existing Solutions (Comparison)

| Solution | Pros | Cons | Feasibility |
|---|---:|---|---|
| **Separate Music / SFX Volume** | Modern standard | None | **Very Easy** |
| **Full Mute** | Indispensable | None | **Very Easy** |
| **Visual Indicators for Spawning Enemies** | Helps hearing-impaired & colorblind | Risk of visual clutter | **Feasible** |
| **High Contrast HUD** | Improves readability | Additional graphic work | Feasible |
| **Colorblind Mode** | Inclusive | Unnecessary if Color is simple | Not priority |
| **Subtitles for Audio Signals** | Helps deafness | No narrative audio | Not essential |

### 3.3 Selected Choices
- Separate Music / Effects volume control
- Visual warnings upon enemy appearance (halo/icon)
- Master Mute

These choices target the needs of deaf, hard-of-hearing, or visually impaired players without burdening development.

---

## 4. Mental and Cognitive Accessibility

### 4.1 Identified Issues
Possible limitations:
- Photosensitive epilepsy
- Difficulty processing multiple pieces of information at once
- ADHD / Cognitive fatigue
- Sensitivity to flashing lights or rapid visual effects

An R-Type-like game is particularly visually busy, which can quickly become problematic.

### 4.2 Existing Solutions (Comparison)

| Solution | Pros | Cons | Feasibility |
|---|---:|---|---|
| **Epilepsy Warning at Start** | Mandatory and standard | None | **Very Easy** |
| **"Low-Flash" Mode (Reduced effects)** | Highly useful | Requires alternative assets | Feasible |
| **Slow Tutorial Mode** | Facilitates understanding | Additional content | Medium |
| **Reduction of On-screen Elements** | Useful | Modifies gameplay | Not suitable |

### 4.3 Selected Choices
- Epilepsy warning at launch
- "Reduce Flashing Effects" Mode (dampened explosions, no strobe effects)

These measures address critical needs while remaining achievable within the project scope.

---

## 5. Conclusion
The comparative study highlights that certain aspects of accessibility can be easily integrated into a shoot ’em up, while others alter the gameplay too drastically.

The goal is not to exhaustively cover every disability, but to respect basic standards while offering simple yet effective options.

### Features Selected for Our Project
- Keyboard Rebinding
- Alternative Keys
- Auto-fire
- Separate Music / SFX Settings
- Master Mute
- Visual Warning for Enemy Spawns
- Epilepsy Warning
- "Low-Flash" Mode

These choices place our project within a responsible and realistic approach to accessibility, consistent with current best practices without overloading the workload.