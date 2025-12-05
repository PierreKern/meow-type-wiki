# Binary UDP Protocol

When designing a binary network protocol for our R-Type game, it is necessary to choose an endianness convention—that is, the order in which the bytes of a multi-byte integer are encoded.

The two possible approaches are **Big Endian** and **Little Endian**.

This study compares both options and justifies the endianness chosen for our protocol.

---

## 1. Definition of the Two Models

### Little Endian

Bytes are stored from the **least significant to the most significant**.

Example: `0x12345678` is stored in memory as:

`78 56 34 12`

Architectures that use it natively:

- Intel x86 / x86_64  
- ARM (Android, iOS, embedded Linux)

### Big Endian

Bytes are stored from the **most significant to the least significant**.

Example: `0x12345678` becomes:

`12 34 56 78`

---

## 2. Comparison Criteria

### 2.1 Network Interoperability

Big Endian is the format used by:

- TCP  
- UDP  
- IP  
- DNS  
- TLS  
- WebSockets  

Little Endian is **not used by any standardized network protocol**.

For a binary UDP protocol, **Big Endian is naturally the standard format**.

---

### 2.2 Cross-Platform Compatibility

All platforms can handle Big Endian using standard functions (`htonl`, `ntohl`).

Network tools (Wireshark, tcpdump) also assume Big Endian by default.

Little Endian is native on modern CPUs but **not suitable for a network protocol shared across different operating systems**.

Big Endian ensures strong portability and long-term stability in a multi-platform environment.

---

### 2.3 Performance

Little Endian is slightly faster **locally**, since it matches CPU architectures.

Big Endian requires conversion (`htons` / `ntohs`), but the cost is **very small**.

In a game like R-Type:

- Few bytes are transmitted  
- Moderate frequency  
- No real performance impact  

In a lightweight UDP binary protocol, **the performance difference is negligible**.

---

### 2.4 Development Simplicity

**Big Endian**:

- Aligned with all existing network code examples  
- Packet inspection is easier in network tools  
- Fewer interpretation errors  

**Little Endian**:

- Only intuitive at CPU level  
- Can complicate network debugging (tools will display reversed endianness)

---

### 2.5 Reliability & Error Prevention

Little Endian makes it easy to introduce errors when:

- A remote client uses a different platform  
- An external bot is developed  
- Another language connects (Go, Rust, JS, Python, etc.)

Big Endian avoids these issues because **all network libraries already assume network byte order**.

For a minimalistic UDP binary protocol:

**Big Endian is the most robust and maintainable choice.**

---

## 3. Final Decision: Big Endian (Network Byte Order)

**Justification:**

We chose to use Big Endian for all multi-byte fields in our protocol.  
This ensures compatibility with network standards, maximum interoperability between platforms, and better readability in network analysis tools. The conversion cost is negligible and largely outweighed by the robustness and clarity of the format.
