# ***_TP Noté Python : Prévisions Météorologiques_***

## ***Description***

Ce projet consiste à requêter OpenWeatherMap pour lire le contenu JSON des prévisions météorologiques sur les 5 prochains jours (intervalle de 3h). L'analyse se concentre sur la somme des précipitations et le décompte des changements majeurs de temps.

## **Objectifs**

* Récupérer les prévisions météorologiques pour une ville et un pays donnés
* Calculer le cumul des précipitations (pluie et neige) en millimètres (mm) pour chaque jour
* Compter le nombre de transitions majeures observées dans la journée (changement de catégorie météo et variation de température de plus de 3°C)

## **Fonctionnement**

1. Lancer le programme et choisir la ville et le pays pour les prévisions
2. Récupérer les prévisions météorologiques pour les 5 prochains jours avec un intervalle de 3h
3. Traiter les données pour calculer les cumuls de précipitations et compter les transitions majeures
4. Générer un fichier JSON avec les résultats

  ## **Structure du Fichier JSON**

  Le fichier JSON généré aura la structure suivante :
  ```json
  {
    "forecast_location_name": "Orlando",
    "country_code": "US",
    "total_rain_period_mm": 54.2,
    "total_snow_period_mm": 0.0,
    "max_humidity_period": 95,
    "forecast_details": [
      {
        "date_local": "2023-09-28",
        "rain_cumul_mm": 12.5,
        "snow_cumul_mm": 0.0,
        "major_transitions_count": 2
      },
      {
        "date_local": "2023-09-29",
        "rain_cumul_mm": 4.1,
        "snow_cumul_mm": 0.0,
        "major_transitions_count": 0
      },
      ...
    ]
  }

  ```
## **Affichage terminal**

A la fin de son exécution, le programme affichera un tableau avec les valeurs qui nous intéressent dans ce style :
```table
+-------------------------------------------------------------+
|                  Prévisions météorologiques                 |
+------------+------------+------------+----------------------+
|    Date    | Pluie (mm) | Neige (mm) | Transitions majeures |
+------------+------------+------------+----------------------+
| 2025-11-21 |    0.14    |    0.22    |          0           |
| 2025-11-22 |     0      |    0.26    |          2           |
| 2025-11-23 |   12.14    |     0      |          1           |
| 2025-11-24 |    5.18    |     0      |          0           |
| 2025-11-25 |    3.35    |     0      |          0           |
| 2025-11-26 |    0.10    |     0      |          0           |
+------------+------------+------------+----------------------+

```
## **Initialisation de l'environnement de développement**
Voici le procéder pour initialiser l'environnement de la solution:
*1. Dans un premier temps, télécharger le fichier .zip ou bien clone le répertoire via la commande suivante :*
```bash
git clone https://github.com/DarkMax31/WeatherAPI_Python.git
```
 Une fois le .zip extrait ou le git cloner, il faudra utiliser un IDE pour executer le code (ex: VS Code)

*2. Se rendre ensuite à la racine du projet puis creer un environnement virtuel python :*
  * Vérifier d'abord si vous avez python et pip d'installées :
    ```bash
    python --version
    pip --version
    ```
*3. Installer ensuite l'environnment virtuel python :*
```bash
python -m venv nom_de_votre_environnement
```
*4. Lancez l'environnment virtuel :*
  * Sous Windows:
  ```bash
  nom_de_votre_environnement\Scripts\activate
  ```
  * Sous Linux/Mac
  ```bash
  source nom_de_votre_environnement/bin/activate
  ```
Pour désactiver l'environnment :
  ```bash
  deactivate
  ```
*5. Pour finir, installez les dépendances contenues dans le fichier "requirements.txt" comme ci-dessous :*
  ```bash
  pip install -r requirements.txt
  ```
## **Modifications dans les fichiers du projet et lancement**
Avant de lancer le programme, il vous faudra changer quelques variables, notamment aux endroits suivants:
* /classes/APIKey.py -> Modifier la valeur de la clé API par là votre, optenable via le lien suivant: https://home.openweathermap.org/api_keys
* /classes/WeatherForecast.py -> Modifier la valeur de verify (ligne 18) par le chemin de votre certificat (ex: "C://path/to/certificat.ca")

Vous pouvez désormais exécuter le fichier main.py