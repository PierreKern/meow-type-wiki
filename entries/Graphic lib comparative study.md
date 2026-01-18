Here is the translation of the R-Type technical study regarding the choice of the graphical library.

## Introduction

As part of the R-Type project (B-CPP-500), choosing a graphics library is crucial for developing a high-performance and maintainable **client** for a 2D multiplayer game. This study compares several solutions available in C++ and justifies the choice of **SFML** for the implementation of the graphical client.

**Important Note**: This study focuses on the library choice for the **client**.

---

## Evaluation Criteria

To objectively compare the graphics libraries, we use the following criteria:

1. **Ease of use**: Learning curve, API clarity.
2. **Performance**: 2D rendering, management of multiple entities.
3. **Portability**: Cross-platform support (Linux, Windows).
4. **Features**: Rendering, audio, network, input management.
5. **Documentation and community**: Quality of available resources.
6. **Integration**: Compatibility with CMake and package managers.
7. **License**: Legal constraints.
8. **Project Maturity**: Stability, maintenance.

---

## Compared Libraries

### 1. SFML (Simple and Fast Multimedia Library)

**Current Version**: 2.6.1 (3.0 in development)

### Pros

* **Clear and intuitive Object-Oriented API**: Modern design with well-organized classes.
* **Modularity**: System of modules (graphics, window, audio, network, system).
* **Excellent 2D Performance**: Specifically optimized for 2D games.
* **Quality Documentation**: Complete tutorials, numerous examples.
* **Native Network Support (Client-side)**: Integrated network module (UDP/TCP) for client-to-server communication.
* **Complete Management**: Graphics, audio, windowing, user inputs.
* **Large Community**: Active forum, numerous open-source projects.
* **Mature Cross-platform**: Stable support for Linux, Windows, macOS.
* **Easy Integration**: Compatible with Conan, vcpkg, CMake FetchContent.
* **Permissive License**: zlib/png license (very permissive).

### Cons

* No native 3D support (but sufficient for R-Type).
* Some abstractions may limit low-level control.
* Basic network module (but sufficient for the project).

### R-Type Use Case

* ✅ Perfect for a 2D shoot 'em up (graphical client).
* ✅ Network module adapted for UDP client → server communication.
* ✅ Fluid sprite and animation management.
* ✅ Audio support for sound effects and music.
* ✅ Pre-existing template/experience within the team.

**Global Score**: ⭐⭐⭐⭐⭐ (9.5/10)

---

### 2. SDL2 (Simple DirectMedia Layer 2)

**Current Version**: 2.28.5

### Pros

* **Very mature and stable**: Over 25 years of existence.
* **Excellent Performance**: Close to hardware.
* **Exceptional Portability**: Supports many platforms.
* **Fine Control**: Low-level access when necessary.
* **Rich Ecosystem**: SDL_image, SDL_mixer, SDL_ttf, SDL_net.
* **Industry Standard**: Used in many commercial games.
* **Exhaustive Documentation**: Huge amount of resources.
* **Permissive License**: zlib license.

### Cons

* **C API**: More verbose in C++, requires wrappers.
* **Less Object-Oriented**: Procedural design.
* **Learning Curve**: More complex for beginners.
* **Limited Abstractions**: Requires more "boilerplate" code.
* **No Core Network Module**: SDL_net is separate and basic.

### R-Type Use Case

* ✅ Sufficient performance for the project.
* ⚠️ Requires more code for the same functionality.
* ⚠️ C API less natural in C++.
* ❌ No pre-existing template/experience in the team.

**Global Score**: ⭐⭐⭐⭐ (7.5/10)

---

### 3. Raylib

**Current Version**: 5.0

### Pros

* **Extremely Simple**: Minimalist and clear API.
* **Modern**: Modern design with good practices.
* **Excellent Documentation**: Numerous tutorials and examples.
* **All-in-One**: Graphics, audio, inputs in a single package.
* **2D/3D Support**: Flexibility if evolution is needed.
* **Lightweight**: Low memory footprint.
* **Cross-platform**: Good multiplatform support.
* **Permissive License**: zlib/png license.

### Cons

* **Less Mature**: Newer, fewer reference projects.
* **Smaller Community**: Fewer community resources.
* **No Native Network Module**: Requires external library.
* **C-Oriented API**: Similar to SDL, less natural in C++.
* **Fewer High-Level Abstractions**: For certain advanced features.

### R-Type Use Case

* ✅ Adapted for 2D rendering.
* ❌ No integrated network support (critical for R-Type).
* ⚠️ Fewer references for multiplayer games.
* ❌ No pre-existing template/experience in the team.

**Global Score**: ⭐⭐⭐ (6.5/10)

---

### 4. Allegro 5

**Current Version**: 5.2.9

### Pros

* **Historic**: Proven library since the 90s.
* **Complete**: Audio, graphics, inputs, primitives.
* **Solid Performance**: Optimized for 2D.
* **Cross-platform**: Support for numerous platforms.
* **Modular Addons**: Extension system.

### Cons

* **Declining Community**: Less active than before.
* **Aging Documentation**: Some resources are obsolete.
* **Dated API**: Design less modern than SFML/Raylib.
* **Fewer Recent Projects**: Fewer contemporary examples.
* **No Network Module**: Not integrated.

### R-Type Use Case

* ⚠️ Functional but less modern.
* ❌ No native network support.
* ❌ Less active community.
* ❌ No pre-existing template/experience in the team.

**Global Score**: ⭐⭐ (5.5/10)

---

## Synthetic Comparison Table

| Criteria | SFML | SDL2 | Raylib | Allegro 5 |
| --- | --- | --- | --- | --- |
| **Ease of Use (C++)** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **2D Performance** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Portability** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Network Support** | ⭐⭐⭐⭐ | ⭐⭐ | ❌ | ❌ |
| **Documentation** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **CMake/Package Integration** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Community** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Integrated Audio** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Team Experience** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐ |

---

## Justification of Choice: SFML

### Main Reasons

### 1. **Pre-existing Experience**

The team already has a functional SFML template. This existing codebase represents a considerable advantage:

* Reduction in learning time.
* Startup code already written and tested.
* Patterns and best practices already established.
* Significant time savings on development.

### 2. **Modern Object-Oriented API**

Unlike SDL2 or Raylib (C APIs), SFML offers a native C++ API with:

```cpp
// SFML Example - Natural in C++
sf::RenderWindow window(sf::VideoMode(800, 600), "R-Type");
sf::Sprite playerSprite;
playerSprite.setTexture(texture);
playerSprite.setPosition(100.f, 100.f);
window.draw(playerSprite);

// vs SDL2 - More verbose
SDL_Window* window = SDL_CreateWindow("R-Type",
    SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
    800, 600, SDL_WINDOW_SHOWN);
SDL_Renderer* renderer = SDL_CreateRenderer(window, -1,
    SDL_RENDERER_ACCELERATED);
// ... more boilerplate code ...

```

### 3. **Integrated Network Support (Client-Side)**

The `sf::Network` module provides:

* Ready-to-use `sf::UdpSocket` and `sf::TcpSocket` classes for the client.
* Packet management with `sf::Packet` (automatic serialization).
* Consistent API with the rest of SFML.
* Perfectly suited for R-Type client → server communication.

**Note**: The server generally uses Asio or system sockets directly (not SFML), as it does not need graphical rendering. The SFML client communicates with this server.

```cpp
// UDP Example CLIENT side with SFML
sf::UdpSocket socket;
socket.bind(sf::Socket::AnyPort);
sf::Packet packet;
packet << player.x << player.y << player.action;
socket.send(packet, serverIP, serverPort);

```

### 4. **Modularity Aligned with the Project (Client-Side)**

SFML's modular architecture perfectly matches the client's requirements:

* **sf::Graphics** → Rendering Engine (client)
* **sf::Network** → Client networking (communication with the server)
* **sf::Audio** → Audio Engine (client)
* **sf::Window** → Input Management (client)

This separation facilitates the creation of a structured client with decoupled subsystems.

**Global R-Type Architecture**:

* **Server**: Asio/System sockets + Game logic (no SFML).
* **Client**: SFML (graphics + audio + input) + Network communication to server.

### 5. **Ecosystem and Community**

* Complete and up-to-date official documentation.
* Active forums (SFML Forum).
* Numerous tutorials and open-source projects.
* Excellent integration with modern tools (CMake, Conan, vcpkg).

### 6. **Compatibility with Project Requirements**

✅ **CMake**: Excellent support, FindSFML.cmake available.

✅ **Package Managers**: Available on Conan, vcpkg, and CPM.

✅ **Cross-platform**: Robust Linux and Windows support.

✅ **Performance**: Optimized for 2D games like R-Type.

✅ **License**: zlib/png (permissive, no constraints).

---

## Technical Considerations Specific to R-Type

### Sprite and Animation Management

SFML offers an efficient and intuitive sprite system:

```cpp
class AnimatedSprite {
    sf::Sprite sprite;
    std::vector<sf::IntRect> frames;
    sf::Clock clock;
    size_t currentFrame = 0;

    void update() {
        if (clock.getElapsedTime().asSeconds() > 0.1f) {
            currentFrame = (currentFrame + 1) % frames.size();
            sprite.setTextureRect(frames[currentFrame]);
            clock.restart();
        }
    }
};

```

### Network Architecture

**R-Type Architecture**:

* **Server**: Asio or system sockets (BSD/Winsock), multithreaded, authoritative.
* **Client**: SFML `sf::Network` module to communicate with the server.

The SFML network module integrates well on the client side:

* `sf::Packet` can serialize data to be sent to the server.
* Non-blocking sockets allow integration into the client game loop.
* Natural communication with the authoritative server (primarily UDP).

```cpp
// CLIENT Side (SFML)
sf::UdpSocket clientSocket;
clientSocket.setBlocking(false);

// Sending inputs to server
sf::Packet inputPacket;
inputPacket << playerID << inputState;
clientSocket.send(inputPacket, serverIP, serverPort);

// Receiving server updates
sf::Packet updatePacket;
sf::IpAddress sender;
unsigned short port;
if (clientSocket.receive(updatePacket, sender, port) == sf::Socket::Done) {
    // Process world updates
}

```

### Scrolling and Camera

SFML facilitates starfield scrolling management:

```cpp
sf::View camera;
camera.setCenter(player.position);
camera.move(scrollSpeed * deltaTime, 0.f);
window.setView(camera);

```

---

## Discarded Alternatives and Why

### Why not SDL2?

Although SDL2 is excellent, it has drawbacks for our context:

* C API requiring wrappers in C++.
* No prior experience within the team.
* Network module (SDL_net) less mature than sf::Network.
* More "boilerplate" code for the same features.

### Why not Raylib?

* Absence of native network module (critical for R-Type).
* Smaller community, fewer resources for multiplayer.
* No existing codebase within the team.

### Why not a complete engine (Unity, Godot, UE)?

The subject explicitly forbids complete game engines:

> "libraries with a too broad scope, or existing game engines (UE, Unity, Godot, etc.) are strictly forbidden"

The pedagogical objective is to build our own engine architecture.

---

## Risks and Mitigations

### Identified Risks

1. **Basic SFML Network Module**
* **Mitigation**: Sufficient for R-Type, possibility to use Asio as a supplement if necessary.


2. **No 3D Support**
* **Mitigation**: Not necessary for a horizontal 2D shoot 'em up.


3. **Evolution towards SFML 3.0**
* **Mitigation**: SFML 2.6 is stable, migration to 3.0 possible later if needed.



### Vigilance Points

* Encapsulate SFML dependencies well to facilitate testing.
* Create abstractions if necessary (e.g., IRenderer interface).
* Document architectural choices related to SFML.

---

## Conclusion

**The choice of SFML for the R-Type client is optimal** for the following reasons:

1. ✅ **Technical Experience**: Existing template, reduced learning curve.
2. ✅ **Modern C++ API**: Natural for a C++ project, object-oriented.
3. ✅ **Complete Client-Side Features**: Graphics, Audio, Network, Input in a single package.
4. ✅ **Client Network Support**: Network module adapted to communicate with the server.
5. ✅ **Performance**: Optimized for fast 2D games like shmups.
6. ✅ **Project Compatibility**: CMake, package managers, cross-platform.
7. ✅ **Ecosystem**: Documentation, community, abundant examples.
8. ✅ **Modularity**: Clear architecture for the graphical client.

**Global R-Type Architecture**:

* **Client**: SFML (rendering + audio + input + server communication).
* **Server**: Asio/System sockets + Authoritative game logic (no SFML).

SFML allows us to focus on implementing the client (graphical interface, rendering, user interactions) and communicating with the server, while offering the flexibility needed to create a clean and maintainable client architecture.

---

## References

* [Official SFML Documentation](https://www.sfml-dev.org/documentation/2.6.1/)
* [SFML Forum](https://en.sfml-dev.org/forums/)
* [SFML Game Development Book](https://www.packtpub.com/product/sfml-game-development/9781849696845)
* [SDL2 Documentation](https://wiki.libsdl.org/)
* [Raylib Documentation](https://www.raylib.com/)
* [Game Networking Resources](https://github.com/MFatihMAR/Game-Networking-Resources)
* [Fast-Paced Multiplayer](https://www.gabrielgambetta.com/client-server-game-architecture.html)

---

*Document produced as part of project B-CPP-500 R-Type - EPITECH Nancy*

*Author: Maylle*

*Date: November 25, 2025*