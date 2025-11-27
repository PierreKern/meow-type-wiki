## Introduction

Dans le cadre du projet R-Type (B-CPP-500), le choix d'une bibliothèque graphique est crucial pour le développement du **client** d'un jeu 2D multijoueur performant et maintenable. Cette étude compare plusieurs solutions disponibles en C++ et justifie le choix de **SFML** pour l'implémentation du client graphique.

**Note importante** : Cette étude se concentre sur le choix de la bibliothèque pour le **client**.

---

## Critères d'Évaluation

Pour comparer objectivement les bibliothèques graphiques, nous utilisons les critères suivants :

1. **Facilité d'utilisation** : Courbe d'apprentissage, clarté de l'API
2. **Performance** : Rendu 2D, gestion de multiples entités
3. **Portabilité** : Support multiplateforme (Linux, Windows)
4. **Fonctionnalités** : Rendu, audio, réseau, gestion des entrées
5. **Documentation et communauté** : Qualité des ressources disponibles
6. **Intégration** : Compatibilité avec CMake et gestionnaires de paquets
7. **License** : Contraintes légales
8. **Maturité du projet** : Stabilité, maintenance

---

## Bibliothèques Comparées

### 1. SFML (Simple and Fast Multimedia Library)

**Version actuelle** : 2.6.1 (3.0 en développement)

### Avantages

- **API orientée objet claire et intuitive** : Design moderne avec des classes bien organisées
- **Modularité** : Système de modules (graphics, window, audio, network, system)
- **Performance excellente en 2D** : Optimisée spécifiquement pour les jeux 2D
- **Documentation de qualité** : Tutoriels complets, exemples nombreux
- **Support natif du réseau (côté client)** : Module network intégré (UDP/TCP) pour la communication client vers serveur
- **Gestion complète** : Graphismes, audio, fenêtrage, entrées utilisateur
- **Large communauté** : Forum actif, nombreux projets open source
- **Cross-platform mature** : Linux, Windows, macOS support stable
- **Intégration facile** : Compatible avec Conan, vcpkg, CMake FetchContent
- **License permissive** : zlib/png license (très permissive)

### Inconvénients

- Pas de support natif 3D (mais suffisant pour R-Type)
- Quelques abstractions peuvent limiter le contrôle bas niveau
- Module réseau basique (mais suffisant pour le projet)

### Cas d'usage R-Type

- ✅ Parfait pour un shoot'em up 2D (client graphique)
- ✅ Module network adapté pour la communication client → serveur UDP
- ✅ Gestion des sprites et animations fluide
- ✅ Support audio pour effets sonores et musiques
- ✅ Template/expérience préexistante dans l'équipe

**Score global** : ⭐⭐⭐⭐⭐ (9.5/10)

---

### 2. SDL2 (Simple DirectMedia Layer 2)

**Version actuelle** : 2.28.5

### Avantages

- **Très mature et stable** : Plus de 25 ans d'existence
- **Performance excellente** : Proche du matériel
- **Portabilité exceptionnelle** : Supporte de nombreuses plateformes
- **Contrôle fin** : Accès bas niveau quand nécessaire
- **Écosystème riche** : SDL_image, SDL_mixer, SDL_ttf, SDL_net
- **Industrie standard** : Utilisée dans de nombreux jeux commerciaux
- **Documentation exhaustive** : Énorme quantité de ressources
- **License permissive** : zlib license

### Inconvénients

- **API C** : Plus verbeux en C++, nécessite des wrappers
- **Moins orienté objet** : Design procédural
- **Courbe d'apprentissage** : Plus complexe pour débutants
- **Abstractions limitées** : Requiert plus de code "boilerplate"
- **Pas de module réseau dans le core** : SDL_net est séparé et basique

### Cas d'usage R-Type

- ✅ Performance suffisante pour le projet
- ⚠️ Nécessite plus de code pour la même fonctionnalité
- ⚠️ API C moins naturelle en C++
- ❌ Pas de template/expérience dans l'équipe

**Score global** : ⭐⭐⭐⭐ (7.5/10)

---

### 3. Raylib

**Version actuelle** : 5.0

### Avantages

- **Extrêmement simple** : API minimaliste et claire
- **Moderne** : Design moderne avec bonnes pratiques
- **Documentation excellente** : Tutoriels et exemples nombreux
- **Tout-en-un** : Graphismes, audio, inputs dans un seul package
- **Support 2D/3D** : Flexibilité si besoin d'évoluer
- **Léger** : Empreinte mémoire faible
- **Cross-platform** : Bon support multiplateforme
- **License permissive** : zlib/png license

### Inconvénients

- **Moins mature** : Plus récent, moins de projets de référence
- **Communauté plus petite** : Moins de ressources communautaires
- **Pas de module réseau natif** : Nécessite bibliothèque externe
- **API orientée C** : Similaire à SDL, moins naturelle en C++
- **Moins d'abstractions haut niveau** : Pour certaines fonctionnalités avancées

### Cas d'usage R-Type

- ✅ Adapté pour le rendu 2D
- ❌ Pas de support réseau intégré (critique pour R-Type)
- ⚠️ Moins de références pour jeux multijoueurs
- ❌ Pas de template/expérience dans l'équipe

**Score global** : ⭐⭐⭐ (6.5/10)

---

### 4. Allegro 5

**Version actuelle** : 5.2.9

### Avantages

- **Historique** : Bibliothèque éprouvée depuis les années 90
- **Complète** : Audio, graphismes, inputs, primitives
- **Performance solide** : Optimisée pour le 2D
- **Cross-platform** : Support de nombreuses plateformes
- **Addons modulaires** : Système d'extensions

### Inconvénients

- **Communauté en déclin** : Moins active qu'auparavant
- **Documentation vieillissante** : Certaines ressources obsolètes
- **API datée** : Design moins moderne que SFML/Raylib
- **Moins de projets récents** : Moins d'exemples contemporains
- **Pas de module réseau** : Non intégré

### Cas d'usage R-Type

- ⚠️ Fonctionnel mais moins moderne
- ❌ Pas de support réseau natif
- ❌ Communauté moins active
- ❌ Pas de template/expérience dans l'équipe

**Score global** : ⭐⭐ (5.5/10)

---

## Tableau Comparatif Synthétique

| Critère | SFML | SDL2 | Raylib | Allegro 5 |
| --- | --- | --- | --- | --- |
| **Facilité d'utilisation (C++)** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Performance 2D** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Portabilité** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Support réseau** | ⭐⭐⭐⭐ | ⭐⭐ | ❌ | ❌ |
| **Documentation** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Intégration CMake/Package Managers** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Communauté** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Audio intégré** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Expérience équipe** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐ |

---

## Justification du Choix : SFML

### Raisons Principales

### 1. **Expérience Préexistante**

L'équipe dispose déjà d'une template SFML fonctionnelle. Cette base de code existante représente un avantage considérable :

- Réduction du temps d'apprentissage
- Code de démarrage déjà écrit et testé
- Patterns et bonnes pratiques déjà établis
- Gain de temps significatif sur le développement

### 2. **API Orientée Objet Moderne**

Contrairement à SDL2 ou Raylib (API C), SFML propose une API C++ native avec :

```cpp
// Exemple SFML - Naturel en C++
sf::RenderWindow window(sf::VideoMode(800, 600), "R-Type");
sf::Sprite playerSprite;
playerSprite.setTexture(texture);
playerSprite.setPosition(100.f, 100.f);
window.draw(playerSprite);

// vs SDL2 - Plus verbeux
SDL_Window* window = SDL_CreateWindow("R-Type",
    SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
    800, 600, SDL_WINDOW_SHOWN);
SDL_Renderer* renderer = SDL_CreateRenderer(window, -1,
    SDL_RENDERER_ACCELERATED);
// ... plus de code boilerplate ...

```

### 3. **Support Réseau Intégré (Côté Client)**

Le module `sf::Network` fournit :

- Classes `sf::UdpSocket` et `sf::TcpSocket` prêtes à l'emploi pour le client
- Gestion des paquets avec `sf::Packet` (sérialisation automatique)
- API cohérente avec le reste de SFML
- Parfaitement adapté pour la communication client → serveur de R-Type

**Note** : Le serveur utilise généralement Asio ou des sockets système directement (pas SFML), car il n'a pas besoin de rendu graphique. SFML côté client communique avec ce serveur.

```cpp
// Exemple UDP côté CLIENT avec SFML
sf::UdpSocket socket;
socket.bind(sf::Socket::AnyPort);
sf::Packet packet;
packet << player.x << player.y << player.action;
socket.send(packet, serverIP, serverPort);

```

### 4. **Modularité Alignée avec le Projet (Côté Client)**

L'architecture modulaire de SFML correspond parfaitement aux exigences du client :

- **sf::Graphics** → Rendering Engine (client)
- **sf::Network** → Client networking (communication avec le serveur)
- **sf::Audio** → Audio Engine (client)
- **sf::Window** → Input Management (client)

Cette séparation facilite la création d'un client bien structuré avec des subsystèmes découplés.

**Architecture globale R-Type** :

- **Serveur** : Asio/sockets système + logique de jeu (pas de SFML)
- **Client** : SFML (graphics + audio + input) + communication réseau vers serveur

### 5. **Écosystème et Communauté**

- Documentation officielle complète et à jour
- Forums actifs (SFML Forum)
- Nombreux tutoriels et projets open source
- Excellente intégration avec les outils modernes (CMake, Conan, vcpkg)

### 6. **Compatibilité avec les Exigences du Projet**

✅ **CMake** : Excellent support, FindSFML.cmake disponible

✅ **Package Managers** : Disponible sur Conan, vcpkg, et CPM

✅ **Cross-platform** : Linux et Windows support robuste

✅ **Performance** : Optimisée pour les jeux 2D comme R-Type

✅ **License** : zlib/png (permissive, pas de contraintes)

---

## Considérations Techniques Spécifiques à R-Type

### Gestion des Sprites et Animations

SFML offre un système de sprites efficace et intuitif :

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

### Architecture Réseau

**Architecture R-Type** :

- **Serveur** : Asio ou sockets système (BSD/Winsock), multithreadé, authoritative
- **Client** : Module `sf::Network` de SFML pour communiquer avec le serveur

Le module network de SFML s'intègre bien côté client :

- Les `sf::Packet` peuvent sérialiser les données à envoyer au serveur
- Les sockets non-bloquants permettent l'intégration dans la game loop du client
- Communication naturelle avec le serveur authoritative (UDP principalement)

```cpp
// Côté CLIENT (SFML)
sf::UdpSocket clientSocket;
clientSocket.setBlocking(false);

// Envoi des inputs au serveur
sf::Packet inputPacket;
inputPacket << playerID << inputState;
clientSocket.send(inputPacket, serverIP, serverPort);

// Réception des updates du serveur
sf::Packet updatePacket;
sf::IpAddress sender;
unsigned short port;
if (clientSocket.receive(updatePacket, sender, port) == sf::Socket::Done) {
    // Traiter les updates du monde
}

```

### Scrolling et Caméra

SFML facilite la gestion du starfield scrolling :

```cpp
sf::View camera;
camera.setCenter(player.position);
camera.move(scrollSpeed * deltaTime, 0.f);
window.setView(camera);

```

---

## Alternatives Écartées et Pourquoi

### Pourquoi pas SDL2 ?

Bien que SDL2 soit excellent, il présente des inconvénients pour notre contexte :

- API C nécessitant des wrappers en C++
- Pas d'expérience préalable dans l'équipe
- Module réseau (SDL_net) moins mature que sf::Network
- Plus de code "boilerplate" pour les mêmes fonctionnalités

### Pourquoi pas Raylib ?

- Absence de module réseau natif (critique pour R-Type)
- Communauté plus petite, moins de ressources pour le multijoueur
- Pas de base de code existante dans l'équipe

### Pourquoi pas un moteur complet (Unity, Godot, UE) ?

Le sujet interdit explicitement les moteurs de jeu complets :

> "libraries with a too broad scope, or existing game engines (UE, Unity, Godot, etc.) are strictly forbidden"
> 

L'objectif pédagogique est de construire notre propre architecture de moteur.

---

## Risques et Mitigations

### Risques Identifiés

1. **Module réseau SFML basique**
    - **Mitigation** : Suffisant pour R-Type, possibilité d'utiliser Asio en complément si nécessaire
2. **Pas de support 3D**
    - **Mitigation** : Non nécessaire pour un shoot'em up 2D horizontal
3. **Évolution vers SFML 3.0**
    - **Mitigation** : SFML 2.6 est stable, migration vers 3.0 possible ultérieurement si besoin

### Points de Vigilance

- Bien encapsuler les dépendances SFML pour faciliter les tests
- Créer des abstractions si nécessaire (ex: interface IRenderer)
- Documenter les choix d'architecture liés à SFML

---

## Conclusion

**Le choix de SFML pour le client R-Type est optimal** pour les raisons suivantes :

1. ✅ **Expérience technique** : Template existante, courbe d'apprentissage réduite
2. ✅ **API moderne C++** : Naturelle pour un projet en C++, orientée objet
3. ✅ **Fonctionnalités complètes côté client** : Graphics, Audio, Network, Input en un seul package
4. ✅ **Support réseau client** : Module network adapté pour communiquer avec le serveur
5. ✅ **Performance** : Optimisée pour les jeux 2D rapides comme les shmups
6. ✅ **Compatibilité projet** : CMake, package managers, cross-platform
7. ✅ **Écosystème** : Documentation, communauté, exemples abondants
8. ✅ **Modularité** : Architecture claire pour le client graphique

**Architecture globale R-Type** :

- **Client** : SFML (rendu + audio + input + communication serveur)
- **Serveur** : Asio/sockets système + logique de jeu authoritative (pas de SFML)

SFML permet de se concentrer sur l'implémentation du client (interface graphique, rendu, interactions utilisateur) et sur la communication avec le serveur, tout en offrant la flexibilité nécessaire pour créer une architecture client propre et maintenable.

---

## Références

- [Documentation officielle SFML](https://www.sfml-dev.org/documentation/2.6.1-fr/)
- [SFML Forum](https://en.sfml-dev.org/forums/)
- [SFML Game Development Book](https://www.packtpub.com/product/sfml-game-development/9781849696845)
- [SDL2 Documentation](https://wiki.libsdl.org/)
- [Raylib Documentation](https://www.raylib.com/)
- [Game Networking Resources](https://github.com/MFatihMAR/Game-Networking-Resources)
- [Fast-Paced Multiplayer](https://www.gabrielgambetta.com/client-server-game-architecture.html)

---

*Document réalisé dans le cadre du projet B-CPP-500 R-Type - EPITECH Nancy*

*Auteur : Maylle*

*Date : 25 novembre 2025*