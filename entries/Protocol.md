
# R-Type UDP Protocol

This document describes the binary protocol used by the Meow-Type/R-Type server and client. It is written so that any developer can implement a compatible UDP client from scratch without needing to dig through the codebase.

## Transport

- **Transport:** UDP (IPv4).
- **Default ports:** The server expects a port passed on the command line (e.g., `./rtype_server 4242`).
- **Framing:** Each datagram contains exactly one protocol message. Messages are self-delimited by a 3-byte header.
- **Endianness:** All multi-byte integers are **big-endian** (network byte order). Sizes are unsigned unless noted.
- **Reliability:** UDP is fire-and-forget. The protocol keeps payloads small so the game can tolerate occasional packet loss. A client should be ready to resend transient inputs if needed.

## Message header

Every packet starts with a 3-byte header:

| Offset | Size | Name | Description |
| ------ | ---- | ----- | ----------- |
| 0 | 1 | type | `MessageType` enum value (see below) |
| 1 | 2 | size | Total packet size **including** the 3-byte header |
The server/client helper `make_header` writes this header and reserves space for the payload, while `parse_header` validates it when deserializing. A packet is only processed when `size` exactly matches the datagram length.【F:src/server/include/Protocol.hpp†L10-L46】【F:src/server/include/Protocol.hpp†L115-L137】

### Message type enum

| Enum value | Hex | Direction | Purpose |
| ---------- | --- | --------- | ------- |
| `CLIENT_HELLO` | `0x01` | Client → Server | Opens a session and advertises the player name. |
| `SERVER_WELCOME` | `0x02` | Server → Client | Confirms the connection and assigns a player ID. |
| `CLIENT_DISCONNECT` | `0x03` | Client → Server | Graceful disconnect notification. |
| `INPUT` | `0x10` | Client → Server | Single-frame input (movement + actions). |
| `ENTITY_CREATE` | `0x20` | Server → Client | Spawns an entity with initial position and type. |
| `ENTITY_UPDATE` | `0x21` | Server → Client | Updates an entity’s position/type. |
| `ENTITY_DESTROY` | `0x22` | Server → Client | Removes an entity from the world. |
| `PLAYER_LEFT` | `0x24` | Server → Client | Notifies that a player disconnected. |
| `ENTITY_HIT` | `0x25` | Server → Client | Damage notification. |
| `ENTITY_COLLISION` | `0x26` | Server → Client | Collision details (type + impact). |
| `ENTITY_MOVE` | `0x27` | Server → Client | Velocity update plus position. |
| `ENTITY_DEATH` | `0x28` | Server → Client | Entity death with killer ID. |
| `ENTITY_SHOOT` | `0x29` | Server → Client | Projectile creation from a shooter. |

## Connection lifecycle

1. **Client starts UDP socket** bound to any local port.
2. **Send `CLIENT_HELLO`:**

- Fields: `clientNonce` (`uint32`), `name[16]` (ASCII, null-padded if shorter).【F:src/server/include/Protocol.hpp†L48-L60】【F:src/server/include/Protocol.hpp†L169-L182】
- The nonce is user-chosen; it can be random for debugging/log correlation.

3. **Receive `SERVER_WELCOME`:** server replies with `playerId` (`uint16`).【F:src/server/include/Protocol.hpp†L52-L58】【F:src/server/include/Protocol.hpp†L140-L147】
4. **Snapshot delivery:** immediately after `SERVER_WELCOME`, the server sends an entity snapshot (`ENTITY_CREATE` packets) so the client renders current state before live updates.【F:src/server/Game.cpp†L217-L231】
5. **Live updates:** client sends `INPUT` packets every frame; server broadcasts entity state (`ENTITY_MOVE`, `ENTITY_UPDATE`, `ENTITY_SHOOT`, `ENTITY_DESTROY`, etc.).【F:src/server/Game.cpp†L204-L230】【F:src/server/Game.cpp†L330-L372】
6. **Disconnect:** client may send `CLIENT_DISCONNECT`; server also broadcasts `PLAYER_LEFT` when a player exits (message type reserved, not yet serialized in codebase but part of the enum).【F:src/server/include/Protocol.hpp†L11-L33】【F:src/server/include/Protocol.hpp†L62-L66】

## Packet payloads

Below are the binary layouts (immediately after the 3-byte header). All multi-byte fields are big-endian.

### Client → Server

- **CLIENT_HELLO (0x01)**
- `uint32 clientNonce`
- `char name[16]`
- **INPUT (0x10)**
- `uint16 playerId`
- `uint8 directionFlags` — 0=UP, 1=DOWN, 2=LEFT, 3=RIGHT【F:src/server/include/Protocol.hpp†L68-L76】
- `uint8 actionFlags` — bitfield, bit0 = FIRE
- **CLIENT_DISCONNECT (0x03)**
- `uint16 playerId`

### Server → Client

- **SERVER_WELCOME (0x02)**
- `uint16 playerId` (server-assigned)【F:src/server/include/Protocol.hpp†L52-L58】
- **ENTITY_CREATE (0x20)**
- `uint16 entityId`
- `uint8 entityType` — see `EntityType` enum (1=PLAYER, 2=MONSTER, 3=PLAYER_MISSILE, 4=ENEMY_MISSILE, 5=OBSTACLE, 6=POWERUP)【F:src/server/include/Protocol.hpp†L35-L46】
- `uint16 x`
- `uint16 y`
- **ENTITY_UPDATE (0x21)**
- Same layout as `ENTITY_CREATE` (updates position/type).【F:src/server/include/Protocol.hpp†L78-L93】
- **ENTITY_MOVE (0x27)**
- `uint16 entityId`
- `uint8 entityType`
- `int16 vx`
- `int16 vy`
- `uint16 x`
- `uint16 y`
- **ENTITY_DEATH (0x28)**
- `uint16 entityId`
- `uint8 entityType`
- `uint16 killerId`
- **ENTITY_SHOOT (0x29)**
- `uint16 shooterId`
- `uint16 projectileId`
- `uint8 projectileType`
- `uint16 x`
- `uint16 y`
- `int16 vx`
- `int16 vy`
- **ENTITY_DESTROY (0x22)**
- `uint16 entityId`
- **ENTITY_HIT (0x25)**
- `uint16 attackerId`
- `uint16 targetId`
- `uint8 damage`
- `uint8 remainingHp`
- **ENTITY_COLLISION (0x26)**
- `uint16 entityA`
- `uint16 entityB`
- `uint8 collisionType` — 0=OBSTACLE, 1=BLOCK, 2=HURT, 3=POWERUP
- `uint8 impactForce`
- **PLAYER_LEFT (0x24)**
- `uint16 playerId`

## Serialization helpers

The protocol code provides reusable helpers you can mirror in any language:

- `write_u16 / write_u32` push big-endian integers into a byte buffer.
- `make_header(type, payload_size)` builds the header.
- `serialize(message)` functions return the full packet buffer for each struct.
- `parse_header` checks size consistency.
- `deserialize(raw, message)` functions validate the type and populate structs.
You can port these helpers directly when implementing a custom client.【F:src/server/include/Protocol.hpp†L95-L167】【F:src/server/include/Protocol.hpp†L182-L282】

## Example client flow (pseudo-code)

```text
socket = udp(bind=0.0.0.0:any) 
# 1) Say hello 
hello.clientNonce = random_u32() 
hello.name = "PlayerOne\0" 
send(to=server, serialize(hello)) 
# 2) Wait for SERVER_WELCOME 
packet = recv() 
if packet.type == SERVER_WELCOME: 
 myId = packet.playerId 
# 3) Game loop: send inputs, render state 
auto input = { playerId: myId, directionFlags: DOWN, actionFlags: FIRE } 
loop every frame: 
 send(to=server, serialize(input)) 
 while recv_available(): 
 msg = deserialize(next_packet) 
 update_local_world(msg) 
```

## Server behavior notes

- The server is built with Asio’s async UDP socket. Incoming datagrams are queued, then processed in the main loop (`process_network_messages`).【F:src/server/include/UDP.hpp†L10-L55】【F:src/server/Game.cpp†L173-L207】
- On `CLIENT_HELLO`, the server creates a player entity, assigns an incremental `playerId`, replies with `SERVER_WELCOME`, then pushes a full entity snapshot to the new client.【F:src/server/Game.cpp†L209-L231】
- Each tick (~60 Hz), the server broadcasts entity creations, movements, and destructions to all known endpoints using the helper `broadcast` method.【F:src/server/Game.cpp†L317-L372】
- Position, velocity, collision, and shooting logic is purely server-authoritative; clients should treat server packets as truth and only send desired inputs.

## Tips for new client implementations

- Keep your UDP socket open and non-blocking; process all queued datagrams each frame.
- Trust server state: reconcile local predictions when authoritative updates arrive.
- Use big-endian conversions; mismatched endianness will scramble IDs and positions.
- Handle unexpected/duplicate packets gracefully—UDP can reorder or drop datagrams.
- Keep names ≤16 chars (pad with zeros). Longer names must be truncated before sending.
With these details, you can implement a UDP client in any language that speaks the Meow-Type protocol without referencing the existing C++ code.