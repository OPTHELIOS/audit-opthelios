import streamlit as st
import pandas as pd
from datetime import datetime
import os
from fpdf import FPDF

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Opthelios Expert", layout="wide", page_icon="☀️")

# --- 2. GESTION DU THÈME ET SIDEBAR ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png")
    st.header("🎨 Paramètres")
    theme = st.radio("Mode d'affichage", ["☀️ Clair", "🌙 Sombre"], horizontal=True)
    
    # Style spécifique pour la Sidebar (Bandeau de droite/gauche selon la langue)
    sidebar_bg = "#002b5c" if theme == "☀️ Clair" else "#000000"
    sidebar_txt = "#FFFFFF"

# --- 3. CSS ADAPTATIF ET LISIBILITÉ ---
if theme == "🌙 Sombre":
    bg, card, txt, brd = "#0E1117", "#161B22", "#FFFFFF", "#30363D"
else:
    bg, card, txt, brd = "#F8F9FA", "#FFFFFF", "#1A1C1E", "#D0D5DD"

st.markdown(f"""
    <style>
    /* Application globale */
    .stApp {{ background-color: {bg}; color: {txt}; }}
    
    /* Sidebar ultra-lisible */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        color: {sidebar_txt} !important;
    }}
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] label {{
        color: {sidebar_txt} !important;
    }}

    /* Cartes d'audit */
    [data-testid="stExpander"] {{
        background-color: {card} !important;
        border: 1px solid {brd} !important;
        border-radius: 10px !important;
    }}

    /* Texte forcé selon thème */
    h1, h2, h3, h4, p, span, label {{ color: {txt} !important; }}

    /* Bouton principal */
    .stButton>button {{
        background-color: #ff7f00 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px;
        height: 3.5em;
    }}

    /* Allègement des inputs de la fiche d'identité */
    .small-photo-btn {{ margin-top: -10px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. IDENTIFICATION DU SITE ---
st.title("☀️ Diagnostic Solaire Pro")

c1, c2 = st.columns([1.5, 1])
with c1:
    nom_site = st.text_input("📍 Nom de l'opération", placeholder="Ex: Résidence Hôtelière du Rail")
    adr_site = st.text_input("🏠 Adresse / GPS", placeholder="Adresse complète ou Coordonnées")
    moa_site = st.text_input("👤 Maître d'ouvrage", placeholder="Client")
with c2:
    photo_main = st.camera_input("Photo de couverture", key="main_pic")

st.divider()

# --- 5. FICHE D'IDENTITÉ ALLÉGÉE ---
st.header("📋 Fiche d'Identité Matériel")

def compact_row(label, key):
    """Crée une ligne compacte avec texte et petit bouton photo"""
    col_t, col_p = st.columns([3, 1])
    with col_t:
        val = st.text_input(label, key=f"t_{key}", help=f"Saisir la marque/réf pour {label}")
    with col_p:
        # L'appareil photo est intégré mais prend moins de place visuelle
        img = st.camera_input("📷", key=f"p_{key}")
    return val, img

with st.expander("🛠 Configuration de l'installation", expanded=True):
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.markdown("**☀️ Capteurs & Solaire**")
        m_cap, p_cap = compact_row("Marque/Réf Capteurs", "cap")
        orient = st.selectbox("Orientation", ["Sud", "SE", "SO", "Est", "Ouest"], key="orient")
        
    with row1_col2:
        st.markdown("**📦 Stockage & Échange**")
        m_bal, p_bal = compact_row("Marque/Réf Ballons", "bal")
        vol_bal = st.number_input("Volume total (L)", value=1000, step=100)

    st.divider()
    
    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        st.markdown("**💧 Hydraulique**")
        m_circ, p_circ = compact_row("Circulateur", "circ")
        m_reg, p_reg = compact_row("Régulateur", "reg")
        
    with row2_col2:
        st.markdown("**🔥 Appoint & Sécurité**")
        m_app, p_app = compact_row("Appoint (Marque/Type)", "app")
        anode = st.selectbox("Protection cuve", ["ACI", "Magnésium", "Inox", "N/A"])

# --- 6. AUDIT TERRAIN (73 POINTS) ---
st.divider()
st.header("🔍 Audit des 73 Points de Contrôle")

# Dictionnaire simplifié pour l'exemple, à garder complet dans ton code
sections = {
    "📄 Admin & Elec": ["Schéma d'exécution", "Schéma Electrique", "Mise à la terre", "Signalétique"],
    "☀️ Capteurs": ["Vannes d'isolement", "Supports", "Étanchéité", "Isolants UV"],
    "🧪 Fluide": ["pH du fluide", "Protection Antigel", "Analyse visuelle"],
    "💧 Hydraulique": ["Sens circulation", "Dégazeur", "Soupape", "Vase d'expansion"],
    "📦 Stockage": ["Puissance échangeur", "Calorifuge", "Protection cathodique"],
    "📊 Métrologie": ["Manomètre", "Débitmètre", "Sondes", "Delta T"]
}

all_results = []
for sec, pts in sections.items():
    with st.expander(f"📁 {sec}"):
        for p in pts:
            st.markdown(f"**{p}**")
            c_res, c_obs, c_cam = st.columns([1.5, 2, 1])
            with c_res:
                res = st.selectbox("Statut", ["Conforme", "Non Conforme", "N/C", "S/O"], key=f"s_{p}")
            with c_obs:
                obs = st.text_input("Note", key=f"o_{p}", placeholder="RAS")
            with c_cam:
                pic = st.camera_input("📸", key=f"c_{p}")
            all_results.append({"Point": p, "Statut": res, "Obs": obs})

# --- 7. BOUTON FINAL ---
st.divider()
if st.button("🚀 GÉNÉRER LE RAPPORT FINAL"):
    st.balloons()
    st.success("Rapport compilé avec succès !")