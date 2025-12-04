import os
import shutil
import processing

# Chemin de base
monCheminDeBase = 'D:/CAUSE/'

project = QgsProject.instance()

# 1. Récupérer la couche réseau hydro principal
layers_hydro = project.mapLayersByName("Réseau hydro principal")
if not layers_hydro:
    print("⚠ Aucune couche trouvée avec le nom 'Réseau hydro principal'. Vérifie le nom exact dans le panneau des couches.")
else:
    reseau_hydro = layers_hydro[0]

    # 2. Dossier pour la couche tampon
    _hydro_buffer = monCheminDeBase + '_zone_tampon_1km'
    if os.path.isdir(_hydro_buffer):
        shutil.rmtree(_hydro_buffer)
    os.mkdir(_hydro_buffer)

    # 3. Chemin du shapefile de sortie
    tampon_path = _hydro_buffer + r'\\zone_tampon_1km.shp'

    # 4. Buffer de 1 km (1000 m)
    processing.run(
        'native:buffer',
        {
            "INPUT": reseau_hydro,
            "DISTANCE": 1000,     
            "SEGMENTS": 10,
            "END_CAP_STYLE": 0,    
            "JOIN_STYLE": 0,
            "MITER_LIMIT": 2,
            "DISSOLVE": False,
            "DISSOLVE_ALL": False,
            "OUTPUT": tampon_path
        }
    )

    # 5. Ouvrir la couche tampon
    tampon_1km = QgsVectorLayer(tampon_path, "Zone tampon 1 km", "ogr")
    project.addMapLayer(tampon_1km)

    # 6. (Optionnel) : placer le buffer sous le réseau hydro dans la légende
    root = project.layerTreeRoot()
    myBelowLayer = root.findLayer(tampon_1km.id())
    myClone = myBelowLayer.clone()
    parent = myBelowLayer.parent()
    parent.insertChildNode(-1, myClone)
    parent.removeChildNode(myBelowLayer)

    print("Buffer 1 km créé dans", tampon_path)
