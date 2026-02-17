# Projet INF6253-P1 — Web Sémantique  
Université du Québec en Outaouais (UQO)

##  Membres de l’équipe

-Lacpili AYARMA — Matricule : AYAL122793306
-Kossi Cyrille KPOTOGBE — Matricule : KPOK14369905
-Lamrous Mohamed Cherif — Matricule : LAMM11359801

---

# Description du projet

Ce projet est divisé en **trois parties**, correspondant à l’évolution du Web :

1.*Partie 1 — Web 1.0**  
   Génération automatique de pages HTML statiques à partir d’une base SQLite.

2.*Partie 2 — Web 3.0 enrichi**  
   Génération de pages HTML enrichies en RDFa, conversion en Turtle (TTL), production de JSON‑LD, et utilisation de Jena pour enrichir les données.

3.*Partie 3 — SPARQL* 
   Extraction RDF, création d’un graphe de connaissances, exécution de requêtes SPARQL et comparaison des performances.

Chaque partie contient son propre code, ses templates et ses résultats.

---

##Installation

###1. Créer un environnement virtuel (optionnel mais recommandé)

```bash
python3 -m venv venv
venv\Scripts\activate     

### 2. Installer les dépendances
```bash
pip install -r requirements.txt

### 3.Exécution du projet
Partie 1 — Web 1.0
Génération des pages HTML statiques :

```bash
python part1_web1/generate_html_pages.py
Les pages générées se trouvent dans :

Code
part1_web1/site_html/

Partie 2 — Web 3.0 enrichi
Génération des pages HTML enrichies en RDFa :
```bash
python part2_web3_enriched/generate_enriched_html_pages.py
Conversion RDFa → Turtle (TTL) :
```bash
python part2_web3_enriched/convert_rdfa_to_ttl.py
Génération JSON‑LD :
```bash
python part2_web3_enriched/utils_rdfa.py
Les résultats se trouvent dans :

site_html_enriched/
site_html_enriched_jena/
web_3.0_jsonld_output/

Partie 3 — SPARQL

python -m pip install requests

lancer Jena Fuseki

java -jar fuseki-server.jar

Exécution des requêtes SPARQL :
```bash
python part3_sparql/engine_sparql.py
Les requêtes sont dans :
part3_sparql/queries/
Les graphes RDF sont dans :

Code
part3_sparql/rdf/
Les résultats sont enregistrés dans :

Code
part3_sparql/resultats.txt

##  Organisation du projet

INF6253-P1/
│
├── part1_web1/
│   ├── app.py
│   ├── generate_html_pages.py
│   ├── templates/
│   ├── site_html/                 
│   └── resultats.txt
│
├── part2_web3_enriched/
│   ├── generate_enriched_html_pages.py
│   ├── utils_rdfa.py
│   ├── plot_comparaison.py
│   ├── templates/
│   ├── site_html_enriched/        
│   ├── site_html_enriched_jena/   
│   ├── web_3.0_jsonld_output/     
│   ├── comparaison_partie1_partie2.png
│   ├── temps_partie1_partie2.csv
│   └── results1.txt
│
├── part3_sparql/
│   ├── engine_sparql.py
│   ├── crawler_rdfa.py
│   ├── extract_partie1.py
│   ├── queries/                   
│   ├── rdf/                      
│   ├── templates/
│   ├── resultats.txt
│   └── comparaison_temps.png
│
├── README.md
└── requirements.txt

