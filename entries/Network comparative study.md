# Comparative Study: Network Library

## 1\. Introduction

Since the Meow-Type is a multiplayer game, we have to deal with server-client communication in order to deliver a fast, low-latency game. we have taken these criteria into account:

  * **Low Latency:** Gameplay data (positions, inputs) must be transmitted as fast as possible. **UDP** is mandatory.
  * **Concurrency:** The server must handle multiple clients simultaneously without blocking the game loop.
  * **Reliability:** Critical events (connection, player death, game start) require reliability (TCP or Reliable UDP).
  * **Cross-Platform:** Must compile and run on Linux and Windows.

We evaluated four solutions for the network part of the meow-type:

1.  **OS Raw Sockets** (BSD/WinSock)
2.  **SFML Network**
3.  **ENet**
4.  **Asio (Standalone)**

-----

## 2\. Comparative Matrix

| Feature | **Raw Sockets** | **SFML Network** | **ENet** | **Asio** |
| :--- | :--- | :--- | :--- | :--- |
| **Abstraction Level** | Very Low (Kernel) | High | Medium | Low/Medium |
| **Protocol Support** | Any (TCP/UDP/Raw) | TCP & UDP | Reliable UDP | TCP, UDP, Serial, etc. |
| **Model** | Blocking / Non-blocking | Blocking (mostly) | Polling / Events | **Asynchronous (Proactor)** |
| **Performance** | High (if well coded) | Low/Medium | High | **Very High** |
| **Cross-Platform** | Difficult (Manual `#ifdef`) | Yes | Yes | Yes |
| **Modern C++** | No (C API) | Yes (Classic C++) | No (C API) | **Yes (Modern C++11/17)** |
| **Integration** | Native | Library link | Library link | Header-only (Standalone) |

-----

## 3\. Analysis of Contenders

### A. Raw Sockets (BSD / WinSock)

This involves using system calls like `socket()`, `bind()`, `recvfrom()`.

  * **Pros:** Zero overhead, absolute control.
  * **Cons:** Extremely verbose. requires managing platform differences manually (`closesocket` vs `close`, `WSAStartup` on Windows). Error handling is tedious.


  Too much boilerplate code for a modern C++ project. High risk of bugs and portability issues.

### B. SFML Network (`sf::UdpSocket`)

Since the client likely uses SFML for graphics, using it for networking seems logical.

  * **Pros:** Extremely easy. Integrated with the client.
  * **Cons:** Designed for simplicity, not scalability. The `sf::SocketSelector` relies on the `select()` system call, which is slow for many connections. It encourages blocking or synchronous designs which are bad for a real-time game server.
 
  Acceptable for a simple PROJECT, but lacks the asynchronous power required for an authoritative game server.

### C. ENet

A library dedicated to reliable UDP networking (used in the Cube engine).

  * **Pros:** Implements "Reliable UDP" (sequencing, acks) over UDP automatically. Very fast.
  * **Cons:** It is a **C library**, not C++ (It means that we would forced to encapsulate it). It forces a specific way of managing packets (channels, peers) that dictates your architecture.
  
  Good for pure gameplay, but less flexible than Asio for general architecture.

### D. Asio (Standalone)

A cross-platform C++ library for network and low-level I/O programming that provides a consistent asynchronous model.

  * **Pros:** The industry standard for C++ networking. Uses modern C++ patterns (lambdas, smart pointers). Decouples threading from I/O logic. Supports both TCP (for lobby/chat) and UDP (for gameplay) seamlessly in the same event loop.
  * **Cons:** harder learning curve than SFML.

-----

## 4\. Why Asio is the Best Choice for R-Type

We selected **Asio** as the core networking library for the R-Type Engine. Here is the justification:

### 1\. Asynchronous

Unlike SFML which waits for data (Blocking I/O) or checks if data is there (Polling), Asio uses an **Asynchronous** model.
This means that we can implement a non-blocking server, by continue updating the game loop while we're waiting for a packet.

### 2\. Modern C++ Integration

Asio is written in modern C++. It allows us to write safe and expressive code:

  * **Memory Safety:** It works natively with `std::shared_ptr` to manage the lifetime of connections (preventing Segfaults if a client disconnects during a read).
  * **Clean Code:** We can use `std::bind` or Lambdas for callbacks, avoiding the "function pointer hell" of C libraries like ENet.

### 4\. Protocol Agnostic

For R-Type, we **may** need a hybrid approach (to be confirmed):

  * **TCP** for the "Room/Lobby" phase (reliable, connection-oriented).
  * **UDP** for the "Game" phase (fast).
    Asio handles both protocols within the same `io_context` and the same logic structure. We don't need two different libraries

### 5\. Easy Integration (CPM)

Asio is "Header-Only" (in its standalone version). This simplifies our build system significantly. We don't need to link against heavy binaries.

```cmake
CPMAddPackage(
    NAME asio
    GITHUB_REPOSITORY chriskohlhoff/asio
    GIT_TAG asio-1-28-0
)
target_link_libraries(r-type_server PRIVATE asio)
```

## 5\. Conclusion

**Asio** offers the best balance between **performance**, **control**, and **modern C++ design**. It allows us to build a **Reactive Game Engine** where the network layer drives the game state updates without blocking the physics simulation.

While it requires a higher initial technical investment than SFML, it provides the robustness required for the "Advanced Networking" track of the project (handling latency, packet loss simulation, and multi-threading).