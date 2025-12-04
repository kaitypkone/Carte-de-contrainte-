#importation des fichiers
# Chemin de base
monCheminDeBase = 'D:/CAUSE/'

project = QgsProject.instance()

# Fond OSM
urlWithParams = "type=xyz&url=http://tile.openstreetmap.org/{z}/{x}/{y}.png"
osm = QgsRasterLayer(urlWithParams, "OpenStreetMap", "wms")

# Tes couches vecteur
aire_adhesion = QgsVectorLayer(monCheminDeBase + 'aire-adhesion-parc-national-des-cevennes.shp',
                               'Aire adhésion PNC', 'ogr')

epci = QgsVectorLayer(monCheminDeBase + 'EPCI.shp',
                      'EPCI', 'ogr')

toponymie_zones = QgsVectorLayer(monCheminDeBase + 'TOPONYMIE_ZONES_REGLEMENTEES.shp',
                                 'Toponymie zones réglementées', 'ogr')

cours_eau = QgsVectorLayer(monCheminDeBase + 'COURS_D_EAU.shp',
                           'Cours d’eau', 'ogr')

coeur_parc = QgsVectorLayer(monCheminDeBase + 'coeur_parc_national_cevennes.shp',
                            'Cœur parc national Cévennes', 'ogr')

# Ajout des couches au projet
project.addMapLayer(aire_adhesion)
project.addMapLayer(epci)
project.addMapLayer(toponymie_zones)
project.addMapLayer(cours_eau)
project.addMapLayer(coeur_parc)

project.addMapLayer(osm)
osm.setOpacity(0.75)

iface.mapCanvas().refresh()
