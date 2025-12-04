from qgis.core import (
    QgsProject,
    QgsPalLayerSettings,
    QgsTextFormat,
    QgsVectorLayerSimpleLabeling
)
from qgis.PyQt.QtGui import QFont, QColor

project = QgsProject.instance()

# -------------------------------------------------------------------------
# Récupérer les couches
# -------------------------------------------------------------------------
cc        = project.mapLayersByName("Communautés de communes")[0]
coeur_pnc = project.mapLayersByName("Cœur parc national Cévennes")[0]

# ==============================
# 1) LABELS COMMUNAUTÉS DE COMMUNES
# ==============================
ccLabelSettings = QgsPalLayerSettings()
ccLabelSettings.enabled = True

# On utilise une expression pour mettre le nom en MAJUSCULE
# adapte "NOM" si ton champ a un autre nom
ccLabelSettings.fieldName = 'upper("NOM")'
ccLabelSettings.isExpression = True

ccText = QgsTextFormat()
font_cc = QFont('Georgia', 14)
font_cc.setBold(True)
ccText.setFont(font_cc)
ccText.setSize(14)

# texte beige clair
ccText.setColor(QColor(235, 225, 210))

# halo pour bien détacher le texte
buffer_cc = ccText.buffer()
buffer_cc.setEnabled(True)
buffer_cc.setSize(1.3)
buffer_cc.setColor(QColor(120, 60, 40))   # brun (même teinte que le contour)
ccText.setBuffer(buffer_cc)

ccLabelSettings.setFormat(ccText)

# Placement : par défaut, centré sur le polygone → ça va bien pour 2 grandes CC
ccLabeling = QgsVectorLayerSimpleLabeling(ccLabelSettings)
cc.setLabeling(ccLabeling)
cc.setLabelsEnabled(True)
cc.triggerRepaint()


# ==============================
# 2) LABEL "PARC NATIONAL DES CÉVENNES"
# ==============================
parcLabelSettings = QgsPalLayerSettings()
parcLabelSettings.enabled = True

# Texte fixe, pas dans un champ : on utilise une expression constante
parcLabelSettings.fieldName = "'Parc national des Cévennes'"
parcLabelSettings.isExpression = True

parcText = QgsTextFormat()
font_parc = QFont('Georgia', 18)
font_parc.setBold(True)
parcText.setFont(font_parc)
parcText.setSize(18)

# texte presque blanc
parcText.setColor(QColor(250, 245, 230))

# halo vert sombre léger
buffer_parc = parcText.buffer()
buffer_parc.setEnabled(True)
buffer_parc.setSize(1.6)
buffer_parc.setColor(QColor(60, 90, 50))
parcText.setBuffer(buffer_parc)

parcLabelSettings.setFormat(parcText)

parcLabeling = QgsVectorLayerSimpleLabeling(parcLabelSettings)
coeur_pnc.setLabeling(parcLabeling)
coeur_pnc.setLabelsEnabled(True)
coeur_pnc.triggerRepaint()

# Rafraîchir l’affichage
iface.mapCanvas().refresh()
