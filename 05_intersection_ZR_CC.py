# --- Récupération des couches ---
layers_topo = project.mapLayersByName("Toponymie zones réglementées")
layers_cc = project.mapLayersByName("Communautés de communes")  # adapte si le nom est différent

if not layers_topo:
    print("Aucune couche trouvée avec le nom 'Toponymie zones réglementées'")
elif not layers_cc:
    print("Aucune couche trouvée avec le nom 'Communautés de communes'")
else:
    topo = layers_topo[0]
    cc = layers_cc[0]

    # --- Dossier de sortie ---
    _zone_regl_CC = monCheminDeBase + "_zone_reglementee_CC"
    if os.path.isdir(_zone_regl_CC):
        shutil.rmtree(_zone_regl_CC)
    os.mkdir(_zone_regl_CC)

    # Chemin du shapefile de sortie
    zone_regl_CC_path = _zone_regl_CC + r"\\zone_reglementee_CC.shp"

    # --- Intersection ---
    processing.run(
        "qgis:intersection",
        {
            "INPUT": topo,
            "OVERLAY": cc,
            "INPUT_FIELDS": [],
            "OVERLAY_FIELDS": [],
            "OVERLAY_FIELDS_PREFIX": "",
            "OUTPUT": zone_regl_CC_path
        }
    )

    # --- Ouvrir la couche résultante ---
    zone_regl_CC = QgsVectorLayer(zone_regl_CC_path, "Zone réglementée CC", "ogr")
    project.addMapLayer(zone_regl_CC)

    print("Intersection Toponymie × Communautés de communes créée :", zone_regl_CC_path)
