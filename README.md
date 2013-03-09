
Concept
---
Génération dynamique d'un poster sur l'histoire de la philosophie dans le monde.

Les informations présentes:

- philosophes
- personnages historiques célèbres
- faits historiques importants
- grands livres philosophiques
- courant philosophiques/de pensée
- écoles philosophiques
- diverses statistiques: densité philosophique/siècle, ...

Les principales difficultés du projet (en vrac):

- constituer une base d'informations suffisamment importante (quantitativement)
- sélectionner les informations de manière objective (occident-orient vs asie), critères de sélection, ..
- représenter l'information de manière "design" (collaboration harmonieuse entre intelligence, esthétique et ergonomie) : c'est le point crucial et le plus compliqué!
- le temps

Techniques:
---
- Base de Donnée MySQL pour le stockage des données relatives aux différentes informations philosophiques (Philosophes, Livres, Courants, Evènements historiques, Personnages, …)
- NodeBox (http://nodebox.net/) pour la librairie 2D (sous MacOsX) permettant la génération de l'image (TIFF)
- Python (http://python.org) pour le langage de programmation
- Personal Brain (http://www.thebrain.com/) - Mind Mapping - pour la modélisation de l'ontologie philosophique
- Wikipedia pour récupérer les descriptions des courants philosophiques
- NodeBox 3 (http://nodebox.net/node/)

Philo v1 (2006)
---
Basé sur NodeBox 1 (http://nodebox.net/).

![screenshot](https://raw.github.com/ig2gi/philo_graph/master/build/philo12_min.png)

[view large image (6600x2700)] (https://raw.github.com/ig2gi/philo_graph/master/build/philo12.png)

Détails:

l'élargissement progressif de la rivière est proportionnelle à la densité philosophique
la courbe du bas représente la densité philosophique rapportée à un instant donné
les lignes de vie des philosophes sont proportionnelles à leur durée de vie, cette ligne de vie suit la forme de la rivière

Philo v2 (2012)
---
Basé sur NodeBox 2 version beta (http://beta.nodebox.net/).

![screenshot](https://raw.github.com/ig2gi/philo_graph/master/build/philov2_nbx2_min.png)


[view large image (1730x1200)] (https://raw.github.com/ig2gi/philo_graph/master/build/philov2_nbx2.png)

- Refonte totale du design. 
- Abandon de la notion de "rivière" au profit d'une représentation "sunburst".
- Test de nodebox2

Philo v3 (2012)
---
Basé sur NodeBox 3 version alpha (http://beta.nodebox.net/)

- Ajout des influences entre philosophes.
- Abandon de la base locale au profit de l'utilisation de *DBPedia*.

