import processing

monCheminDeBase = "D:/CAUSE/"

# 1. Récupérer la couche déjà chargée dans le projet
epci = QgsProject.instance().mapLayersByName("EPCI")[0]

# 2. Expression de sélection
expr_epci = "\"NOM\" IN ('CC Causses Aigoual Cévennes', 'CC du Pays Viganais')"

# 3. Chemin du fichier de sortie
communes_cc_path = monCheminDeBase + "communaute_de_communes.shp"

# 4. Extraction par expression
processing.run(
    "native:extractbyexpression",
    {
        "INPUT": epci,
        "EXPRESSION": expr_epci,
        "OUTPUT": communes_cc_path
    }
)

# 5. Ouvrir automatiquement la nouvelle couche
communes_cc = QgsVectorLayer(communes_cc_path, "Communautés de communes", "ogr")
QgsProject.instance().addMapLayer(communes_cc)
