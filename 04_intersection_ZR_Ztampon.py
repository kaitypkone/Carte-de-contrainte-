# Récupération des couches 
layers_topo = project.mapLayersByName("Toponymie zones réglementées")
layers_tampon = project.mapLayersByName("Zone tampon 1 km")

if not layers_topo:
    print("Aucune couche trouvée avec le nom 'Toponymie zones réglementées'")
elif not layers_tampon:
    print("Aucune couche trouvée avec le nom 'Zone tampon 1 km'")
else:
    topo = layers_topo[0]
    tampon = layers_tampon[0]

    # Dossier de sortie 
    _zone_regl_ZT = monCheminDeBase + "_zone_reglementee_ZT"
    if os.path.isdir(_zone_regl_ZT):
        shutil.rmtree(_zone_regl_ZT)
    os.mkdir(_zone_regl_ZT)

    # Chemin du shapefile de sortie
    zone_regl_ZT_path = _zone_regl_ZT + r"\\zone_reglementee_ZT.shp"

    # Intersection
    processing.run(
        "qgis:intersection",
        {
            "INPUT": topo,
            "OVERLAY": tampon,
            # si tu veux garder tous les champs, tu peux laisser les listes vides
            "INPUT_FIELDS": [],
            "OVERLAY_FIELDS": [],
            "OVERLAY_FIELDS_PREFIX": "",
            "OUTPUT": zone_regl_ZT_path
        }
    )

    # --- Ouvrir la couche résultante ---
    zone_regl_ZT = QgsVectorLayer(zone_regl_ZT_path, "Zone réglementée ZT", "ogr")
    project.addMapLayer(zone_regl_ZT)

    print("Intersection Toponymie × Zone tampon 1 km créée :", zone_regl_ZT_path)
