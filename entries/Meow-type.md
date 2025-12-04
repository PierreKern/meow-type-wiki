# Meow-Type

## Table of Contents
1. [Introduction](#1-introduction)
2. [Setup](#2-setup)
3. [Technical considerations](#3-stack)
4. [Authors](#4-authors)
5. [License](#5-license)


## 1. Introduction

Meow-Type is an reboot of the **R-Type** game, with less spaceships and more cats, using our own Engine.

The game is a **shoot'em up**. The goal is to destroy you're ennemies plane's by shooting them with your own missiles.

On the contrary of the orginal R-Type, Meow-Type is a **multiplayer** game, that means you can play solo or collaborate with your friends.


## 2. Setup

The project runs on **Linux** and **Windows**.

### Requirements

    - CMake

You can find CMake documentation and installation [here](https://cmake.org/download/).

### How-to build

```bash

git git@github.com:EpitechPGE3-2025/G-CPP-500-NCY-5-2-rtype-2.git

cmake -B build

cmake --build build
```

## 3. How to play

First, you will have to lauch both **server** & **client** : 

```bash

./build/src/server/rtype_server 4242

./build/src/client/rtype_client

```

You're now ready to play !

Use **Arrow key** to move your player, and press **Space** to shoot & kill your ennemies.

## 3. Stack

### 1. Stack

Meow-Type is built with **C++** for engine and game logic, **SFML** for render and **Asio** for networking.

We use **CMake CPM** to handle third-party librairies.

Our engine is made thanks to and **ECS**.

### 2. Basic tree

You can find below the **tree** of the project.

```bash
├── CMakeLists.txt
├── README.md
└── src
    ├── client
    │   ├── CMakeLists.txt
    │   └── main.cpp
    ├── Engine
    │   ├── CMakeLists.txt
    │   ├── Components
    │   │   └── Components.hpp
    │   ├── Engine.cpp
    │   ├── Entity
    │   │   ├── Entity.hpp
    │   │   ├── Registry.hpp
    │   │   └── SparseArray.hpp
    │   └── Systems
    │       └── Systems.hpp
    └── server
        ├── CMakeLists.txt
        ├── Game.cpp
        ├── include
        │   ├── Game.hpp
        │   ├── Protocol.hpp
        │   └── UDP.hpp
        └── main.cpp

```

### 3. Documentation & contribution

Our documentation is decentralised on our **wiki**, you can find it [here](https://www.meow-type-wiki.onrender.com).

You can find technical documentations, tutorials and lore.

You can also find a guideline on How-to contribute.


## 4. Authors

This project exist thanks to 5 five amazing developers, who played a crucial role in the development :

**Maelle Mohr**, graphical developer & head of organisation

**Léa-Marie Rebert**, graphical developer & head of sprite/animation

**Elias Wach**, server developer & head of CI/CD

**Hugo Rupp**, server developer & head of network

**Pierre Kern**, server developer & head of compatibility

## 5. License

Meow-Type is a **free**, **open-source** software. Please do not copy it for commercial purposes, contribute instead :)