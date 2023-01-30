# betagouv-datasette

Données publiques de beta.gouv.fr sous un format exploitable grace à [datasette](https://datasette.io/)

Les données sont accessibles via une interface web avec une interface de filtres et de tri sur https://betagouv-datasette.fly.dev/

<img width="400" alt="startups-betagouv-datasette" src="https://user-images.githubusercontent.com/883348/215543594-4f90f03e-ac75-4b33-bf73-35e46ecb4d60.png">

Il y a aussi une API JSON documentée sur https://docs.datasette.io/en/stable/json_api.html

Par exemple pour filtrer les startups ayant défini une URL pour publier leur budget : https://betagouv-datasette.fly.dev/data/startups.json?_shape=objects&budget_url__notnull=1

TODO : 

- [ ] automatiser le rafraîchissement des données
- [ ] publier les events et les phases dans des tables à part avec des jointures 
