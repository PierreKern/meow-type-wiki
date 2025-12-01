# Comparative Study: Package Manager Choice

## 1. Introduction

For the R-Type project, one of our main requirements is to have a **fully self-contained build**. The project needs to run on both Linux and Windows, and anyone should be able to build it without having to install specific libraries or tools globally on their machine.

We looked at the three main options available for C++ dependency management: **Conan**, **Vcpkg**, and **CPM.CMake**.

## 2. Comparison

Here is a quick breakdown of how they compare regarding our project needs:

| Feature | Conan | Vcpkg | CPM.CMake |
| :--- | :--- | :--- | :--- |
| **Prerequisites** | Python + Pip | Git + Bootstrapping script | CMake |
| **Setup Time** | High (Profiles, Remotes) | Medium (Cloning repo) | Low |
| **Build Speed** | Fast (Binary cache) | Slow (Builds from source) | Slow (Builds from source) |
| **Ease of Use** | Complex CLI | Toolchain files | Native CMake syntax |
| **Portability** | Low (Needs user setup) | Medium | High |

---

## 3. Why we rejected Conan and Vcpkg

### Conan
Conan is definitely the industry standard and great for big companies because it uses pre-compiled binaries (saving compile time). However, for our team, it adds too much friction:
* **Dependency on Python:** To use Conan, everyone needs Python and Pip installed.
* **Configuration:** We often ran into issues where the Conan profile on Linux didn't match the one on Windows (GCC vs MSVC versions), leading to ABI incompatibilities.

### Vcpkg
Vcpkg is excellent for Windows, but it feels too heavy for our project:
* **Size:** You have to clone the entire Vcpkg repository, which is huge.
* **Bootstrapping:** You can't just run `cmake`. You have to run a bootstrap script first to build the package manager itself.
* **CI/CD:** Setting up Vcpkg in a continuous integration pipeline takes a lot of time because it has to re-bootstrap every time.

---

## 4. Why we chose CPM.CMake

After testing all three, we decided to go with **CPM.CMake**. It is a lightweight wrapper around CMake's `FetchContent` module, and it fits our workflow perfectly.

### 1. Easy to build
The biggest advantage of CPM is that it requires **zero installation** once you've installed CMake. The package manager itself is just a small CMake script included in our repo.

### 2. Easy to use

Add a new external libray with CPM is **rather easy**.

For exemple, with **SFML** :

```bash

CPMAddPackage(
    NAME SFML
    GITHUB_REPOSITORY SFML/SFML
    GIT_TAG 2.5.1
    OPTIONS "SFML_BUILD_NETWORK=OFF"
)
```
It makes the fecthing fluid and easy for all the team members

### 3. Cross-Platform Compatibility

Since CPM compiles libraries from source using the project's own CMake configuration, it automatically adapts to the compiler we are using. Whether we are on Visual Studio (Windows) or GCC/Clang (Linux), CPM ensures the libraries are built with the exact same flags as our server and client.


# 5. Conclusion

While CPM.CMake means our clean builds take a little longer (since we compile dependencies from source), the trade-off is worth it. It provides the highest level of portability and ensures that our R-Type project is truly self-contained, meeting the subject's requirements without adding unnecessary tools to the developer's machine.
