import json
import os
import urllib.parse
import streamlit as st

st.set_page_config(
    page_title="Mon Assistant Crochet",
    page_icon="🧶",
    layout="centered",
)

FICHIER_FAVORIS = "favoris_crochet.json"

CATEGORIES = [
    "Toutes",
    "Maison",
    "Amigurumis / Jouets",
    "Pull",
    "Écharpe",
    "Bonnet",
]

SITES_PATRONS = [
    {
        "nom": "DROPS Design",
        "url": "https://www.garnstudio.com/search.php?action=browse&c=women&lang=fr",
        "categories": ["Maison", "Pull", "Écharpe", "Bonnet"],
        "recherche": "https://www.garnstudio.com/search.php?action=search&w={query}&lang=fr",
    },
    {
        "nom": "Hobbii (Gratuits)",
        "url": "https://hobbii.fr/modeles?filter=price%3A0",
        "categories": ["Maison", "Amigurumis / Jouets", "Pull", "Écharpe", "Bonnet"],
        "recherche": "https://hobbii.fr/modeles?search={query}&filter=price%3A0",
    },
    {
        "nom": "Ravelry (Gratuits)",
        "url": "https://www.ravelry.com/patterns/search#craft=crochet&availability=free&sort=best",
        "categories": ["Maison", "Amigurumis / Jouets", "Pull", "Écharpe", "Bonnet"],
        "recherche": "https://www.ravelry.com/patterns/search#craft=crochet&availability=free&query={query}",
    },
    {
        "nom": "Pinterest",
        "url": "https://www.pinterest.fr/search/pins/?q=patron%20crochet%20gratuit",
        "categories": ["Maison", "Amigurumis / Jouets", "Pull", "Écharpe", "Bonnet"],
        "recherche": "https://www.pinterest.fr/search/pins/?q={query}%20crochet%20patron%20gratuit",
    },
    {
        "nom": "Yarnspirations",
        "url": "https://www.yarnspirations.com/collections/patterns",
        "categories": ["Maison", "Pull", "Écharpe", "Bonnet"],
        "recherche": "https://www.yarnspirations.com/search?q={query}",
    },
    {
        "nom": "LoveCrafts (Gratuits)",
        "url": "https://www.lovecrafts.com/en-us/l/crochet/crochet-patterns/free-crochet-patterns",
        "categories": ["Maison", "Amigurumis / Jouets", "Pull", "Écharpe", "Bonnet"],
        "recherche": "https://www.lovecrafts.com/en-us/search?q={query}&filter-price.value=0",
    },
    {
        "nom": "Ribblr (Gratuits)",
        "url": "https://ribblr.com/patterns/crochet?price=free",
        "categories": ["Amigurumis / Jouets", "Pull", "Écharpe", "Bonnet"],
        "recherche": "https://ribblr.com/search?q={query}&price=free",
    },
    {
        "nom": "Lion Brand",
        "url": "https://www.lionbrand.com/collections/all-crochet-patterns",
        "categories": ["Maison", "Pull", "Écharpe", "Bonnet"],
        "recherche": "https://www.lionbrand.com/search?q={query}",
    },
    {
        "nom": "Supergurumi (Amigurumis)",
        "url": "https://www.supergurumi.com/amigurumi-patterns",
        "categories": ["Amigurumis / Jouets"],
        "recherche": "https://www.supergurumi.com/?s={query}",
    },
    {
        "nom": "All About Ami",
        "url": "https://www.allaboutami.com/patterns/",
        "categories": ["Maison", "Amigurumis / Jouets", "Bonnet"],
        "recherche": "https://www.allaboutami.com/?s={query}",
    },
]


def charger_favoris():
    if os.path.exists(FICHIER_FAVORIS):
        try:
            with open(FICHIER_FAVORIS, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def sauvegarder_favoris(favoris):
    with open(FICHIER_FAVORIS, "w", encoding="utf-8") as f:
        json.dump(favoris, f, ensure_ascii=False, indent=2)


if "favoris" not in st.session_state:
    st.session_state.favoris = charger_favoris()

st.title("🧶 Mon Assistant Crochet")
st.caption("Recherche rapide de patrons gratuits & sauvegarde par catégorie")

onglet_recherche, onglet_favoris = st.tabs(["🔍 Rechercher un patron", "⭐ Mes patrons sauvegardés"])

with onglet_recherche:
    col_cat, col_mot = st.columns([1, 2])
    with col_cat:
        categorie_choisie = st.selectbox("Catégorie", CATEGORIES)
    with col_mot:
        mot_cle = st.text_input("Mot-clé (ex: ours, granny, bonnet...)", "")

    mot_encode = urllib.parse.quote_plus(mot_cle.strip())

    st.subheader("Sites de patrons gratuits")

    sites_filtres = [
        site for site in SITES_PATRONS
        if categorie_choisie == "Toutes" or categorie_choisie in site["categories"]
    ]

    for site in sites_filtres:
        with st.container(border=True):
            c1, c2, c3 = st.columns([3, 1.3, 1.5])
            with c1:
                st.markdown(f"**{site['nom']}**")
                st.caption(" · ".join(site["categories"]))
            with c2:
                st.link_button("Catalogue", site["url"], use_container_width=True)
            with c3:
                if mot_encode:
                    url_recherche = site["recherche"].format(query=mot_encode)
                    st.link_button("Chercher", url_recherche, type="primary", use_container_width=True)
                else:
                    st.button("Chercher", key=f"disabled_{site['nom']}", disabled=True, use_container_width=True)

with onglet_favoris:
    st.subheader("Enregistrer un nouveau patron")
    with st.form("ajout_favori", clear_on_submit=True):
        titre_patron = st.text_input("Nom du modèle (ex: Bonnet côtelé DROPS)")
        url_patron = st.text_input("Lien URL du patron (https://...)")
        cat_patron = st.selectbox("Catégorie du patron", CATEGORIES[1:])
        soumis = st.form_submit_button("💾 Sauvegarder le patron")

        if soumis:
            if titre_patron.strip() and url_patron.strip():
                nouveau = {
                    "titre": titre_patron.strip(),
                    "url": url_patron.strip(),
                    "categorie": cat_patron,
                }
                st.session_state.favoris.append(nouveau)
                sauvegarder_favoris(st.session_state.favoris)
                st.success("Patron ajouté à votre liste !")
            else:
                st.warning("Veuillez remplir le nom et le lien URL du patron.")

    st.divider()
    st.subheader("Ma liste enregistrée")

    filtre_fav = st.selectbox("Filtrer mes favoris par catégorie", CATEGORIES, key="filtre_fav")
    favoris_affiches = [
        (idx, fav)
        for idx, fav in enumerate(st.session_state.favoris)
        if filtre_fav == "Toutes" or fav["categorie"] == filtre_fav
    ]

    if not favoris_affiches:
        st.info("Aucun patron enregistré dans cette catégorie pour le moment.")
    else:
        for idx, fav in favoris_affiches:
            with st.container(border=True):
                col_info, col_ouvrir, col_suppr = st.columns([4, 1.3, 0.8])
                with col_info:
                    st.markdown(f"**{fav['titre']}**")
                    st.caption(f"Catégorie : {fav['categorie']}")
                with col_ouvrir:
                    st.link_button("Ouvrir", fav["url"], use_container_width=True)
                with col_suppr:
                    if st.button("🗑️", key=f"del_{idx}", help="Supprimer"):
                        st.session_state.favoris.pop(idx)
                        sauvegarder_favoris(st.session_state.favoris)
                        st.rerun()
