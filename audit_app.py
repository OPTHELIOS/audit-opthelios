import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Opthelios Audit Solaire", 
    layout="wide", 
    page_icon="☀️"
)

# --- 2. GESTION DU THÈME ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png")
    
    st.header("🎨 Apparence")
    theme = st.radio("Mode d'affichage", ["☀️ Clair", "🌙 Sombre"], horizontal=True)
    
    st.divider()
    st.header("📌 Identification")
    nom_site = st.text_input("📍 Nom du Site", placeholder="Ex: Résidence Horizon")
    type_inst = st.selectbox("⚙️ Architecture", ["Pressurisé", "Auto-vidangeable"])
    
    st.divider()
    st.markdown("### 📞 Contact Opthelios")
    st.write("**Moran GUILLERMIC**")
    st.write("✉️ contact@opthelios.fr")
    st.write("📞 06 45 57 10 42")
    st.write("🌐 [www.opthelios.com](https://www.opthelios.com)")

# Couleurs dynamiques
if theme == "🌙 Sombre":
    bg_color, card_color, text_color, border_color = "#121212", "#1E1E1E", "#FFFFFF", "#333333"
else:
    bg_color, card_color, text_color, border_color = "#F8F9FA", "#FFFFFF", "#004a99", "#E0E0E0"

# Application du CSS (Correction de l'erreur précédente)
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    h1, h2, h3, p, span, label {{ color: {text_color} !important; }}
    [data-testid="stExpander"] {{
        background-color: {card_color} !important;
        border: 1px solid {border_color} !important;
        border-radius: 12px !important;
        margin-bottom: 15px;
    }}
    .stButton>button {{
        background-color: #ff7f00 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        width: 100%;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DONNÉES DES 63 POINTS ---
audit_sections = {
    "📄 Dossier & Élec": {
        "img": "https://images.unsplash.com/photo-1581092334651-ddf26d9a1930?q=80&w=600",
        "pts": ["Schéma d'exécution", "Schéma Électrique", "Analyse Fonctionnelle", "Raccordements électriques", "Conformité générale", "Mise à la terre"]
    },
    "☀️ Capteurs & Toiture": {
        "img": "https://images.unsplash.com/photo-1509391366360-fe09a921cb35?q=80&w=600",
        "pts": ["Absence vannes isolement circuit", "Traversée de toiture", "Supports conformes", "Raccordement capteurs", "Accès sécurisé", "Absence de masques", "Équilibrage par champ", "Équilibreurs lisibles", "Matériaux conformes"]
    },
    "💧 Réseau Hydraulique": {
        "img": "https://images.unsplash.com/photo-1621905251189-08b45d6a269e?q=80&w=600",
        "pts": ["Sens de circulation", "Vannes remplissage", "Dégazeur (Aller)", "Soupape sécurité", "Bidon récupération", "Circulateur sur retour", "Clapet anti-retour", "V3V fonctionnelles"]
    },
    "🎈 Expansion (Cond.)": {
        "img": "https://images.unsplash.com/photo-1585333127302-729217a01d51?q=80&w=600",
        "pts": ["Vase adapté", "Volume suffisant", "Dispositif isolement", "Raccordement retour", "Pression de gonflage"]
    },
    "🔄 Stockage & Échange": {
        "img": "https://images.unsplash.com/photo-1595187121250-711e74f80838?q=80&w=600",
        "pts": ["Contre-courant échangeur", "Vannes échangeur", "Puissance échangeur", "Local hors gel", "Passage porte", "Accès brides", "Raccordement ballons", "Absence clapet inter-ballons", "Vannes vidange", "Sonde haute", "Protection cathodique", "Calorifuge", "Lyres anti-thermosiphon", "Soupape ballon"]
    },
    "📊 Métrologie & Tests": {
        "img": "https://images.unsplash.com/photo-1576086213369-97a306d36557?q=80&w=600",
        "pts": ["Manomètre", "Débitmètre", "Sonde ensoleillement", "Seuil éclairement", "Sonde température capteur", "Sonde température Bas de ballon", "Prélèvement caloporteur", "Thermomètres échangeur", "Compteur eau froide", "Étanchéité conforme", "Pression épreuve", "Pression réglée", "Rinçage réseau", "Télécontrôleur", "Liaison distance"]
    }
}

# --- 4. CORPS DE L'AUDIT ---
st.title("☀️ Audit Diagnostic Solaire - Opthelios")

all_results = []
for sec_name, data in audit_sections.items():
    if sec_name == "🎈 Expansion (Cond.)" and type_inst == "Auto-vidangeable":
        continue

    with st.expander(f"🔍 {sec_name}", expanded=False):
        c_img, c_form = st.columns([1, 2.5])
        with c_img:
            st.image(data["img"], use_container_width=True)
        with c_form:
            for pt in data["pts"]:
                col1, col2, col3 = st.columns([2, 1, 1.5])
                with col1: st.write(f"**{pt}**")
                with col2: res = st.selectbox("Statut", ["OK", "NC", "N/A"], key=f"st_{pt}", label_visibility="collapsed")
                with col3: obs = st.text_input("Note", key=f"obs_{pt}", placeholder="Obs...", label_visibility="collapsed")
                all_results.append({"Cat": sec_name, "Point": pt, "Statut": res, "Obs": obs})
                st.divider()

# --- 5. BILAN ---
if st.button("📊 CALCULER LE SCORE FINAL"):
    df = pd.DataFrame(all_results)
    df_app = df[df["Statut"] != "N/A"]
    if not df_app.empty:
        conformes = len(df_app[df_app["Statut"] == "OK"])
        score = (conformes / len(df_app)) * 100
        st.header(f"📈 Score Global : {score:.1f}%")
        st.download_button("📥 Télécharger CSV", df.to_csv(index=False).encode('utf-8'), f"Audit_{nom_site}.csv", "text/csv")
    else:
        st.error("Aucune donnée saisie.")