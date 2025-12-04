from qgis.core import (
    QgsProject,
    QgsFillSymbol,
    QgsLineSymbol,
    QgsMarkerSymbol,
    QgsSimpleFillSymbolLayer,
    QgsLinePatternFillSymbolLayer,
    QgsSingleSymbolRenderer
)
from qgis.PyQt.QtGui import QColor

project = QgsProject.instance()


# Récupérer les couches par leur NOM EXACT (comme dans ta légende)

hydro      = project.mapLayersByName("Réseau hydro principal")[0]
zone_ZT    = project.mapLayersByName("Zone réglementée ZT")[0]
zone_CC    = project.mapLayersByName("Zone réglementée CC")[0]
tampon     = project.mapLayersByName("Zone tampon 1 km")[0]
adhesion   = project.mapLayersByName("Aire adhésion PNC")[0]
coeur_pnc  = project.mapLayersByName("Cœur parc national Cévennes")[0]
cc         = project.mapLayersByName("Communautés de communes")[0]


# 1. Réseau hydro principal (bleu fin)

symbol_hydro = QgsLineSymbol.createSimple({
    'line_style': 'solid',
    'line_width': '0.45',
    'color': '#58B4FF'
})
hydro.renderer().setSymbol(symbol_hydro)
hydro.triggerRepaint()
iface.layerTreeView().refreshLayerSymbology(hydro.id())


# 2. Zone réglementée ZT = TRIANGLE ROUGE

symbol_ZT = QgsMarkerSymbol.createSimple({
    'name': 'triangle',
    'color': '255,0,0,255',     # rouge
    'outline_color': '0,0,0,255',
    'size': '4'
})
zone_ZT.renderer().setSymbol(symbol_ZT)
zone_ZT.triggerRepaint()
iface.layerTreeView().refreshLayerSymbology(zone_ZT.id())


# 3. Zone réglementée CC = CERCLE JAUNE

symbol_CC = QgsMarkerSymbol.createSimple({
    'name': 'circle',
    'color': '255,255,0,255',   # jaune
    'outline_color': '0,0,0,255',
    'size': '2'
})
zone_CC.renderer().setSymbol(symbol_CC)
zone_CC.triggerRepaint()
iface.layerTreeView().refreshLayerSymbology(zone_CC.id())


# 4. Zone tampon 1 km = contour rose en pointillés, sans remplissage

symbol_tampon = QgsFillSymbol.createSimple({
    'style': 'no',
    'outline_color': '255,105,180,255',  # rose
    'outline_width': '0.20',
    'line_style': 'dash'
})
tampon.renderer().setSymbol(symbol_tampon)
tampon.triggerRepaint()
iface.layerTreeView().refreshLayerSymbology(tampon.id())


# 5. Aire adhésion PNC 

symbol_adh = QgsFillSymbol()
symbol_adh.deleteSymbolLayer(0)

# couche simple transparente + contour vert
simple_layer = QgsSimpleFillSymbolLayer()
simple_layer.setFillColor(QColor(0, 0, 0, 0))            
simple_layer.setStrokeColor(QColor(120, 150, 60, 255))  
simple_layer.setStrokeWidth(0.6)

# couche de hachures
hatch_layer = QgsLinePatternFillSymbolLayer()
hatch_layer.setFillColor(QColor(120, 150, 60, 190))  # couleur des hachures
hatch_layer.setLineWidth(0.4)
hatch_layer.setDistance(3)
hatch_layer.setAngle(45)

symbol_adh.appendSymbolLayer(simple_layer)
symbol_adh.appendSymbolLayer(hatch_layer)

adhesion.setRenderer(QgsSingleSymbolRenderer(symbol_adh))
adhesion.triggerRepaint()
iface.layerTreeView().refreshLayerSymbology(adhesion.id())


# 6. Cœur parc national Cévennes = vert plein

symbol_coeur = QgsFillSymbol.createSimple({
    'style': 'solid',
    'color': '120,150,60,255',      # vert
    'outline_color': '80,100,50,255',
    'outline_width': '0.6'
})
coeur_pnc.renderer().setSymbol(symbol_coeur)
coeur_pnc.triggerRepaint()
iface.layerTreeView().refreshLayerSymbology(coeur_pnc.id())


# 7. Communautés de communes = beige + contour brun

symbol_cc = QgsFillSymbol.createSimple({
    'style': 'solid',
    'color': '238,221,167,255'      # beige clair
    'outline_color': '120,60,40,255',
    'outline_width': '1'
})
cc.renderer().setSymbol(symbol_cc)
cc.triggerRepaint()
iface.layerTreeView().refreshLayerSymbology(cc.id())


# Rafraîchir la carte

iface.mapCanvas().refresh()