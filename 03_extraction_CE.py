import processing

monCheminDeBase = "D:/CAUSE/"

# 1. Récupérer la couche déjà chargée
layers_cours = QgsProject.instance().mapLayersByName("Cours d’eau")
if not layers_cours:
    print("⚠ Aucune couche trouvée avec le nom 'Cours d’eau'. Vérifie le nom exact dans le panneau des couches.")
else:
    cours_eau = layers_cours[0]

    # 2. Expression de filtrage sur TOPONYME
    expr_hydro = "\"TOPONYME\" IN (" \
                 "'l''Arre'," \
                 "'Ruisseau de Garéne'," \
                 "'la Vis'," \
                 "'la Dourbie'," \
                 "'le Trèvezel'," \
                 "'le Gard'," \
                 "'l''Hérault'" \
                 ")"

    # 3. Chemin de sortie
    hydro_principal_path = monCheminDeBase + "reseau_hydro_principal.shp"

    # 4. Extraction
    processing.run(
        "native:extractbyexpression",
        {
            "INPUT": cours_eau,
            "EXPRESSION": expr_hydro,
            "OUTPUT": hydro_principal_path
        }
    )

    # 5. Ajouter la nouvelle couche au projet
    hydro_principal = QgsVectorLayer(hydro_principal_path, "Réseau hydro principal", "ogr")
    QgsProject.instance().addMapLayer(hydro_principal)
