# R-TYPE Network Protocol (Binary UDP Specification)
 
This document defines the binary UDP protocol used between the R-Type
authoritative server and the graphical clients.
 
The protocol is:
- **Binary** (compact and fast)
- **UDP-based** (real-time gameplay)
- **Minimalistic** (only essential messages)
- **Cross-platform**
 
All multi-byte integers use **network byte order (Big Endian)**.
 
---
 
# 0. Endianness Specification
 
All integers of size 2 bytes or more (`uint16_t`, `uint32_t`) are encoded in  
**Big Endian**, also called **Network Byte Order**.
 
This ensures:
- predictable packet layout across platforms,
- compatibility with standard tools like Wireshark and tcpdump,
- alignment with existing network protocols (UDP, TCP, IP).
 
Example:
- A `uint16_t` value `0x1234` is sent as `12 34`
- A `uint32_t` value `0x11223344` is sent as `11 22 33 44`
 
Single-byte fields (`uint8_t`) do not depend on endianness.
 
---
 
# 1. Packet Structure
 
Every packet starts with the same header:
 
## 1.1 PacketHeader (3 bytes)
 
| Field | Type | Size | Description |
|-------|------|------|-------------|
| type  | u8   | 1 | Message type (`MessageType`) |
| size  | u16  | 2 | Total size of the packet (header + payload) |
 
If `size` does not match the actual datagram length,  
the packet **must be discarded**.
 
---
 
# 2. Message Types
 
```text
0x01  CLIENT_HELLO
0x02  SERVER_WELCOME
0x03  CLIENT_DISCONNECT
 
0x10  INPUT
 
0x20  ENTITY_CREATE
0x21  ENTITY_UPDATE
0x22  ENTITY_DESTROY
0x24  PLAYER_LEFT
0x25  ENTITY_HIT
0x26  ENTITY_COLLISION