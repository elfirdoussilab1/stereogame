# Feather

## Introduction

Feather est un moteur de jeu 3D basé sur pygame utilisant GLSL.
Il est léger et permet de faire des choses simples comme afficher des formes 3D en mouvement sur un écran.

Il est conçu pour afficher pour entrelacer 8 vues sur l'écran 1920 * 1080 d'Alioscopy.

## Utilisation

### Scene

Une fois PyGame initialisé, il nout faut une scene :

```py
from feather import Scene

scene = Scene()
```

### Utiliser les shapes

On peut ensuite ajouter des shapes à notre scène :

```py
from feather.shapes import Cube

cube = Cube("cube", False, scene)
```

### Utiliser les materials

On peut ajouter un material à une shape :

```py
from feather.materials import ColorMaterial

colorMat = ColorMaterial(1.0, 0.0, 0.0)
cube.setMaterial(colorMat)
```