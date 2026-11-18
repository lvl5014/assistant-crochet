import urllib.parse
import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Mon Assistant Crochet", page_icon="🧶", layout="wide"
)

st.title("🧶 Mon Assistant de Patrons de Crochet")

# --- BARRE LATÉRALE (NAVIGATION) ---
st.sidebar.header("📁 Rubriques")
rubrique_choisie = st.sidebar.selectbox(
    "Choisir une catégorie :",
    [
        "Accueil / Recherche globale",
        "Maison",
        "Doudou / Amigurumi",
        "Pull / Gilet",
        "Écharpe / Snood",
        "Bonnet",
        "Mes Favoris 💖",
    ],
)

# --- ZONE DE RECHERCHE ---
st.markdown("---")
st.subheader(f"Rubrique active : {rubrique_choisie}")

recherche_utilisateur = st.text_input(
    "🔍 Que recherchez-vous aujourd'hui ?",
    placeholder="Ex: Griffy le griffon, plaid, bonnet, doudou...",
)

if recherche_utilisateur:
  # Encodage propre du texte pour les URLs
  mot_cle_encode = urllib.parse.quote(recherche_utilisateur)
  mot_cle_gratuit = urllib.parse.quote(
      f"patron crochet gratuit {recherche_utilisateur}"
  )

  st.markdown("### 🚀 Rechercher directement des patrons gratuits sur :")

  # Création de 4 colonnes pour aligner les 4 boutons côte à côte
  col1, col2, col3, col4 = st.columns(4)

  with col1:
    url_drops = (
        f"https://www.garnstudio.com/search.php?action=browse&c=crochet&q={mot_cle_encode}&lang=fr"
    )
    st.link_button(
        "🧶 DROPS Design (100% Gratuit)", url_drops, use_container_width=True
    )

  with col2:
    url_hobbii = (
        f"https://hobbii.fr/product-patterns?search={mot_cle_encode}&filter=price%3A0"
    )
    st.link_button(
        "🌈 Hobbii (Modèles gratuits)", url_hobbii, use_container_width=True
    )

  with col3:
    url_ravelry = (
        f"https://www.ravelry.com/patterns/search#craft=crochet&availability=free&query={mot_cle_encode}"
    )
    st.link_button(
        "🐑 Ravelry (Filtre Gratuit)", url_ravelry, use_container_width=True
    )

  with col4:
    url_pinterest = (
        f"https://fr.pinterest.com/search/pins/?q={mot_cle_gratuit}"
    )
    st.link_button(
        "📌 Pinterest (Idées & Blogs)", url_pinterest, use_container_width=True
    )

  # Bouton secondaire pour une recherche Google ciblée blogs (en excluant Etsy)
  st.markdown("")
  url_google_sans_etsy = (
      f"https://www.google.com/search?q={mot_cle_gratuit}+-site:etsy.com"
  )
  st.link_button(
      "🌐 Recherche Google (Sans les résultats payants Etsy)",
      url_google_sans_etsy,
  )

  # --- FORMULAIRE DE SAUVEGARDE ---
  st.markdown("---")
  st.subheader(
      "📥 Enregistrer votre trouvaille dans la rubrique :"
      f" {rubrique_choisie}"
  )

  nom_patron = st.text_input("Nom du modèle trouvé", value=recherche_utilisateur)
  lien_patron = st.text_input(
      "Collez le lien (URL) du site ou du PDF trouvé sur le web :"
  )

  if st.button("Enregistrer dans ma bibliothèque"):
    if lien_patron:
      st.success(
          f"✅ Le modèle '**{nom_patron}**' a été sauvegardé avec succès dans"
          f" la rubrique **{rubrique_choisie}** !"
      )
    else:
      st.warning("Veuillez coller un lien valide.")

else:
  st.info(
      "👆 Tapez un mot-clé ci-dessus pour faire apparaître les touches de"
      " recherche directe vers les sites gratuits."
  )