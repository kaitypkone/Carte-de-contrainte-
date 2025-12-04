from qgis.core import (
    QgsProject,
    QgsPrintLayout,
    QgsLayoutItemMap,
    QgsLayoutItemLegend,
    QgsLayoutItemScaleBar,
    QgsLayoutItemLabel,
    QgsLayoutItemPicture,
    QgsLayoutPoint,
    QgsLayoutSize,
    QgsUnitTypes,
    QgsLayoutExporter
)
from qgis.PyQt.QtGui import QFont, QColor
from qgis.PyQt.QtCore import Qt
import os
# Paramètres

project = QgsProject.instance()
manager = project.layoutManager()

monCheminDeBase = 'D:/CAUSE/'
cartes_dir = os.path.join(monCheminDeBase, "_cartes")
os.makedirs(cartes_dir, exist_ok=True)

layout_name = "Parc_Cevennes"


# 1. Suppression de l'ancien layout ( javais deja lancer la mise en page )

for l in manager.printLayouts():
    if l.name() == layout_name:
        manager.removeLayout(l)


# 2. Créer le layout

layout = QgsPrintLayout(project)
layout.initializeDefaults()
layout.setName(layout_name)
manager.addLayout(layout)


# 3. Carte principale = même contenu que le canevas QGIS

map_item = QgsLayoutItemMap(layout)
map_item.setRect(20, 20, 200, 140)

# faire la meme extent que ce que tu vois actuellement dans QGIS j'avais deja zoomé que mon ecran 
map_item.setExtent(iface.mapCanvas().extent())

# 3.2 prendre les couches qui sont affichés 
map_item.setLayers(iface.mapCanvas().layers())

map_item.setFrameEnabled(True)

layout.addLayoutItem(map_item)
map_item.attemptMove(QgsLayoutPoint(10, 28, QgsUnitTypes.LayoutMillimeters))
map_item.attemptResize(QgsLayoutSize(210, 165, QgsUnitTypes.LayoutMillimeters))


# 4. Titre 
title = QgsLayoutItemLabel(layout)
title.setText("Carte des contraintes réglementaires")
title.setFont(QFont("Georgia", 20, QFont.Bold))
title.setFontColor(QColor(40, 40, 40))
layout.addLayoutItem(title)
title.attemptMove(QgsLayoutPoint(10, 5, QgsUnitTypes.LayoutMillimeters))

subtitle = QgsLayoutItemLabel(layout)
subtitle.setText("dans la Communauté de communes Cévennes Aigoual")
subtitle.setFont(QFont("Georgia", 12))
subtitle.setFontColor(QColor(70, 70, 70))
layout.addLayoutItem(subtitle)
subtitle.attemptMove(QgsLayoutPoint(10, 15, QgsUnitTypes.LayoutMillimeters))


# 5. Légende
legend = QgsLayoutItemLegend(layout)
legend.setTitle("Légende")
legend.setLinkedMap(map_item)
legend.setAutoUpdateModel(True)
layout.addLayoutItem(legend)
legend.attemptMove(QgsLayoutPoint(225, 28, QgsUnitTypes.LayoutMillimeters))
legend.adjustBoxSize()

# 6. Texte Wikipédia 
if 'parc_wiki_content' in globals() and parc_wiki_content:
    wiki_title = QgsLayoutItemLabel(layout)
    wiki_title.setText("Parc national des Cévennes (Wikipédia)")
    wiki_title.setFont(QFont("Georgia", 11, QFont.Bold))
    wiki_title.setFontColor(QColor(40, 40, 40))
    layout.addLayoutItem(wiki_title)
    wiki_title.attemptMove(QgsLayoutPoint(225, 70, QgsUnitTypes.LayoutMillimeters))

    wiki_label = QgsLayoutItemLabel(layout)
    wiki_label.setText(parc_wiki_content)
    wiki_label.setFont(QFont("Verdana", 8))
    wiki_label.setFontColor(QColor(40, 40, 40))
    wiki_label.setBackgroundEnabled(True)
    wiki_label.setBackgroundColor(QColor(255, 255, 255, 230))
    wiki_label.setMargin(1.0)
    layout.addLayoutItem(wiki_label)
    wiki_label.attemptMove(QgsLayoutPoint(225, 78, QgsUnitTypes.LayoutMillimeters))
    wiki_label.attemptResize(QgsLayoutSize(65, 45, QgsUnitTypes.LayoutMillimeters))

# 7. Image Wikidata du parc 
if 'parc_image_url' in globals() and parc_image_url:
    parc_img = QgsLayoutItemPicture(layout)
    parc_img.setPicturePath(parc_image_url)
    layout.addLayoutItem(parc_img)
    parc_img.attemptResize(QgsLayoutSize(65, 50, QgsUnitTypes.LayoutMillimeters))
    parc_img.attemptMove(QgsLayoutPoint(225, 128, QgsUnitTypes.LayoutMillimeters))

# 8. Logos 
x_logo = 225
if 'logo1' in globals() and logo1:
    logo_item1 = QgsLayoutItemPicture(layout)
    logo_item1.setPicturePath(logo1)
    layout.addLayoutItem(logo_item1)
    logo_item1.attemptResize(QgsLayoutSize(30, 20, QgsUnitTypes.LayoutMillimeters))
    logo_item1.attemptMove(QgsLayoutPoint(x_logo, 5, QgsUnitTypes.LayoutMillimeters))
    x_logo += 32


# 9. Barre d'échelle

scalebar = QgsLayoutItemScaleBar(layout)
scalebar.setStyle('Single Box')
scalebar.setLinkedMap(map_item)
scalebar.setUnits(QgsUnitTypes.DistanceKilometers)
scalebar.setNumberOfSegments(3)
scalebar.setNumberOfSegmentsLeft(0)
scalebar.setUnitsPerSegment(5)
scalebar.setUnitLabel('km')
scalebar.setFont(QFont('Verdana', 8))
scalebar.update()

layout.addLayoutItem(scalebar)
scalebar.attemptMove(QgsLayoutPoint(10, 195, QgsUnitTypes.LayoutMillimeters))

# 10. Export PDF

exporter = QgsLayoutExporter(layout)
pdf_path = os.path.join(cartes_dir, "Parc_Cevennes.pdf")
exporter.exportToPdf(pdf_path, QgsLayoutExporter.PdfExportSettings())

print("Carte exportée :", pdf_path)
