# Protocole de Vérification R-Type

## 1. Configuration et UI (Settings)
- [ ] **Accès Menu :** Lancer le client et entrer dans "PARAMETRES" sans crash.
- [ ] **Affichage des Touches :** Vérifier que chaque action a deux colonnes (Primaire / Secondaire).
- [ ] **Procédure de Rebind :** - [ ] Cliquer sur un bouton -> Le texte doit indiquer une attente.
    - [ ] Appuyer sur une touche clavier -> Le bouton doit se mettre à jour avec le nom de la touche.
- [ ] **Volume :** Vérifier que les boutons `+` et `-` mettent à jour le texte du pourcentage et le volume global.

## 2. Système d'Inputs (Clavier & Manette)
- [ ] **Double Mapping :** Déplacer le vaisseau avec `ZQSD` (ou `WASD`) ET avec les `Flèches`.
- [ ] **Tir Manuel :** Vérifier que la barre `Espace` déclenche un tir.
- [ ] **Auto-fire (Toggle) :** - [ ] Appuyer sur `F` -> Le tir automatique s'active.
    - [ ] Appuyer à nouveau sur `F` -> Le tir s'arrête.
- [ ] **Joystick :** Vérifier que le stick analogique de la manette est détecté pour le mouvement.

## 3. Intégrité du Protocole (Alignement Réseau)
- [ ] **Mise à jour du Score :** Détruire un ennemi et confirmer que le texte `SCORE` s'incrémente.
    - *Note : Si le score affiche des chiffres incohérents, vérifier l'ordre des variables dans `Protocol.hpp`.*
- [ ] **Vies (Live) :** Se faire toucher et vérifier que les cœurs disparaissent.
- [ ] **Interpolation :** Vérifier que les autres joueurs et ennemis bougent de manière fluide (pas de téléportation).

## 4. Retours Visuels et Vagues
- [ ] **Changement de Vague :** Atteindre le palier de score.
    - [ ] Le label doit passer à `WAVE 2`.
    - [ ] La couleur de l'ambiance doit changer (`applyWaveColorTheme`).
- [ ] **Feedback Mort :** Vérifier que l'explosion du joueur se joue avant de passer au `Game Over`.

## 5. Robustesse du Moteur (ECS & Systèmes)
- [ ] **Fuites Mémoire (Memory Leaks) :** Laisser le jeu tourner 5 minutes en tirant en continu. Vérifier que la RAM ne monte pas en flèche (Nettoyage des entités Missiles).
- [ ] **Gestion des Entités :** Vérifier que les ennemis qui sortent de l'écran à gauche sont bien détruits (Cleanup automatique).
- [ ] **Frame-rate Independance :** Vérifier que le vaisseau ne va pas 2x plus vite si on a un écran 144Hz au lieu de 60Hz (DeltaTime check).
- [ ] **Z-Index :** Vérifier que les missiles passent bien *sous* le HUD mais *au-dessus* du décor de fond.

## 6. Multi-joueurs & Synchronisation
- [ ] **Connexion Simultanée :** Connecter 2 ou 3 clients. Vérifier qu'ils se voient tous et que les couleurs des noms sont bien distinctes.
- [ ] **Race Conditions :** Deux joueurs tirent sur le même ennemi. Vérifier que le serveur n'attribue le score qu'à un seul et ne fait pas crash le client qui reçoit une destruction d'entité déjà morte.
- [ ] **Re-connexion :** Fermer un client brutalement et le relancer. Vérifier que le serveur libère bien le slot et permet de revenir en jeu.

## 7. Stress Test Réseau (Latency & UDP)
- [ ] **Saturation :** Faire apparaître 50 ennemis en même temps via le serveur. Vérifier que le client ne freeze pas pendant le traitement des paquets.
- [ ] **Packet Loss :** Simuler un lag. Vérifier que les entités ne se téléportent pas n'importe comment (Qualité de l'interpolation).
- [ ] **Désérialisation :** Envoyer un paquet corrompu ou mal formé. Le client doit l'ignorer sans crash.

## 8. Audio & Ambiance
- [ ] **Spatialisation :** Vérifier que le son du tir sort bien du côté où se trouve le joueur (si implémenté).
- [ ] **Mixage :** Vérifier que la musique de fond ne couvre pas les effets sonores (SFX) d'explosion.
- [ ] **Looping :** Vérifier que la musique redémarre proprement à la fin de la boucle sans blanc sonore.

## 9. États de Fin de Partie
- [ ] **Win Condition :** Terminer la vague 10. Vérifier la transition vers l'écran de victoire.
- [ ] **Score Final :** Vérifier que le score affiché sur l'écran de Game Over correspond bien au dernier score reçu en jeu.
- [ ] **Retour au Menu :** Vérifier que cliquer sur "RETOUR" depuis le Game Over réinitialise bien les variables de jeu (score, vagues) pour une nouvelle partie.