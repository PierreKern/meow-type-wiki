# Contributing to Meow-Type

First off, thanks for taking the time to contribute! 🎉

We are building a multiplayer R-Type game engine using C++, SFML, and Asio. We follow an **Entity Component System (ECS)** architecture. This document will guide you through the process of setting up the project, understanding the codebase, and submitting your contributions.


## Getting Started

### Prerequisites

Ensure you have the following installed:

* **C++ Compiler** (GCC, Clang, or MSVC) supporting C++17 or later.
* **CMake** (3.16+).
* **Git**.
* **Dependencies**: SFML, Asio (usually handled via CMake/CPM).

### Building the Project

1. **Clone the repository:**
```bash
git clone https://github.com/your-org/r-type.git
cd r-type

```


2. **Build using CMake:**
```bash
# Clean build is recommended to avoid linker errors
rm -rf build 
cmake -B build -S .
cmake --build build

```


3. **Run the Game:**
* **Server:** `./rtype_server`
* **Client:** `.rtype_client`



---

## Project Architecture

The project is divided into three main parts:

### 1. The Engine (`src/Engine`)

The core ECS (Entity Component System) library.

* **Registry:** Manages entities and systems.
* **Components:** Data structures (e.g., `position`, `velocity`, `shield`). Defined in `src/Engine/Components/Components.hpp`.
* **Systems:** Logic that operates on components (e.g., `collision_system`, `movement_system`). Defined in `src/Engine/Systems/`.

### 2. The Server (`src/server`)

Handles game logic, authoritative state, and networking.

* `Game.cpp`: Main game loop and system registration.
* `GameNetwork.cpp`: Packet handling (UDP).
* `GameSystems.cpp`: Server-side specific logic (AI, Spawning).
* `GamePersistence.cpp`: Highscore file management.

### 3. The Client (`src/client`)

Handles rendering (SFML), inputs, and network interpolation.

* `GameScene.cpp`: Main rendering loop.
* Interprets `ENTITY_CREATE` / `ENTITY_UPDATE` packets to display sprites.

---

## Development Workflow

We use the **Feature Branch** workflow.

1. **Branch off `dev**`: Always start your work from the latest `dev` branch.
```bash
git checkout dev
git pull origin dev
git checkout -b feature/my-new-feature

```


2. **Commit often**: Write clear, descriptive commit messages.
* *Bad:* "fix bug"
* *Good:* "Fix: Prevent crash when missile hits shield"


3. **Keep it clean**: Do not commit build artifacts (`/build` folder, `.o` files).

---

## Coding Standards

* **Language:** C++17.
* **Naming Convention:**
* Variables and Functions: `snake_case` (e.g., `collision_system`, `spawn_enemy`).
* Classes and Structs: `CamelCase` or `snake_case` (be consistent with `Components.hpp`).
* Member variables: Prefix with `_` (e.g., `_registry`, `_server`).


* **Formatting:** Use 4 spaces for indentation.
* **Headers:** Use `#pragma once`.

---

## How to Add Features

### Adding a New Component (e.g., `Armor`)

1. Define the struct in `src/Engine/Components/Components.hpp`.
2. Register the component in the `Game` constructor (`src/server/Game.cpp`).
```cpp
_registry.register_component<armor>();

```



### Adding a New System

1. Declare the function in `src/Engine/Systems/Systems.hpp`.
2. Implement the logic in `src/Engine/Systems/Systems.cpp`.
3. Add the system to the pipeline in `src/server/Game.cpp` using `_registry.add_system<...>()`.

### Adding a Network Feature

1. Update `src/shared/Protocol.hpp` (Add struct and serialize/deserialize functions).
2. **Important:** You must rebuild **both** Client and Server after modifying the protocol to avoid deserialization errors.

---

## Network Protocol

The network logic is critical.

* **Header:** All packets start with a `PacketHeader` (Type + Size).
* **Serialization:** We use a binary serialization helper in `Protocol.hpp`.
* **Safety:** Always use `write_u32` for `int` and `write_u16` for `short`. **Never** mismatch types between read and write operations.

---

## Submitting a Pull Request

1. Push your branch to the repository.
2. Open a Pull Request against the `dev` branch.
3. **Checklist before submitting:**
* [ ] The code compiles without warnings.
* [ ] You have tested both Client and Server interaction.
* [ ] You have removed debug `std::cout` spam (unless useful for logging).
* [ ] If you modified `Systems.cpp` signature, you updated `Systems.hpp` and `Game.cpp`.



Happy Coding! 🚀