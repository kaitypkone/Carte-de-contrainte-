
# 3. API 
import os
import requests
import json
import wikipedia
from qgis.PyQt.QtGui import QImage, QPainter, QColor

# Chemin 
monCheminDeBase = 'D:/CAUSE/'

# # 3.1 Logos

def telecharger_logo(url, save_path):
    """Télécharge un logo + ajoute un fond vert comme le prof."""
    try:
        r = requests.get(url)
        if r.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(r.content)
        else:
            return ''

        # ajout fond vert
        img = QImage(save_path)
        largeur = img.width() + 40
        hauteur = img.height() + 40

        fond = QImage(largeur, hauteur, QImage.Format_ARGB32)
        fond.fill(QColor(21, 187, 161))  # vert instit

        p = QPainter(fond)
        p.drawImage((largeur-img.width())//2, (hauteur-img.height())//2, img)
        p.end()

        save_green = save_path.replace(".png", "_fond_vert.png")
        fond.save(save_green)
        return save_green

    except Exception as ex:
        print("Erreur logo :", ex)
        return ''


# Logo 1 
logo1 = telecharger_logo(
    "https://cmi.u-cergy.fr/wp-content/uploads/2020/11/CY-Cergy-Paris-Universite_coul.png",
    monCheminDeBase + "logo1.png"
)




# 3.2 IMAGE WIKIDATA 


qid_parc = "Q1368807"  # Parc national des Cévennes
url_wikidata = f"https://www.wikidata.org/wiki/Special:EntityData/{qid_parc}.json"

headers = {'User-Agent': 'kaity@example.com'}

try:
    j = requests.get(url_wikidata, headers=headers).json()
    entity = j["entities"][qid_parc]

    image_name = (
        entity["claims"]
        .get("P18", [{}])[0]
        .get("mainsnak", {})
        .get("datavalue", {})
        .get("value", None)
    )

    if image_name:
        parc_image_url = "https://commons.wikimedia.org/wiki/Special:FilePath/" + image_name.replace(" ", "_")
    else:
        parc_image_url = ""

except Exception as ex:
    print("Erreur Wikidata :", ex)
    parc_image_url = ""



# 3.3 TEXTE WIKIPEDIA


wikipedia.set_lang("fr")
try:
    parc_wiki_content = wikipedia.summary("Parc national des Cévennes", sentences=4)
except Exception as ex:
    print("Erreur Wikipédia :", ex)
    parc_wiki_content = "Résumé Wikipédia indisponible."
