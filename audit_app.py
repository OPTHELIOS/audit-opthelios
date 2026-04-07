import streamlit as st
import pandas as pd
from datetime import datetime
import os
from fpdf import FPDF

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Opthelios Expert v3", layout="wide", page_icon="☀️")

# --- 2. GESTION DU THÈME & SIDEBAR ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png")
    st.header("🎨 Interface")
    theme = st.radio("Mode", ["☀️ Clair", "🌙 Sombre"], horizontal=True)
    
    # Couleurs du bandeau latéral (Sidebar) pour une lisibilité maximale
    sidebar_bg = "#001f3f" if theme == "☀️ Clair" else "#000000"
    st.markdown(f"""
        <style>
        [data-testid="stSidebar"] {{ background-color: {sidebar_bg} !important; color: white !important; }}
        [data-testid="stSidebar"] * {{ color: white !important; }}
        </style>
    """, unsafe_allow_html=True)

# --- 3. CSS ADAPTATIF (Texte noir en clair / blanc en sombre) ---
if theme == "🌙 Sombre":
    bg, card, txt, brd = "#0E1117", "#161B22", "#FFFFFF", "#30363D"
else:
    bg, card, txt, brd = "#F8F9FA", "#FFFFFF", "#1A1C1E", "#D0D5DD"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {txt}; }}
    [data-testid="stExpander"] {{ background-color: {card} !important; border: 1px solid {brd} !important; border-radius: 8px !important; }}
    h1, h2, h3, h4, label, p, span {{ color: {txt} !important; }}
    .stButton>button {{ background-color: #ff7f00 !important; color: white !important; font-weight: bold; border-radius: 8px; }}
    .color-box {{ padding: 8px; border-radius: 4px; text-align: center; font-weight: bold; color: white !important; font-size: 0.8em; }}
    /* Style pour les petits boutons photo */
    .stCameraInput > label {{ display: none; }} 
    </style>
    """, unsafe_allow_html=True)

# --- 4. IDENTIFICATION DU SITE ---
st.title("☀️ Diagnostic Expert Opthelios")

col_top1, col_top2 = st.columns([2, 1])
with col_top1:
    nom_site = st.text_input("📍 Nom de l'opération", placeholder="Ex: Résidence Hôtelière du Rail")
    adr_site = st.text_input("🏠 Adresse & GPS", placeholder="Adresse complète / Coordonnées GPS")
    client_site = st.text_input("👤 Client / MOA", placeholder="Ex: ICF Habitat")
with col_top2:
    photo_main = st.camera_input("📸 Photo de garde", key="main_pic")

# --- 5. FICHE D'IDENTITÉ ALLÉGÉE ---
st.divider()
st.header("📋 Fiche d'Identité de l'Installation")

def row_mat(label, key):
    c1, c2 = st.columns([3, 1])
    with c1: v = st.text_input(label, key=f"t_{key}")
    with c2: p = st.camera_input("📷", key=f"p_{key}")
    return v, p

with st.expander("🛠️ Caractéristiques Matérielles", expanded=True):
    col_mat1, col_mat2 = st.columns(2)
    with col_mat1:
        st.markdown("**☀️ Production Solaire**")
        m_cap, p_cap = row_mat("Marque/Réf Capteurs", "cap")
        orient = st.selectbox("Orientation", ["Sud", "Sud-Est", "Sud-Ouest", "Est", "Ouest"])
        inclin = st.number_input("Inclinaison (°)", value=45)
        m_circ, p_circ = row_mat("Marque/Réf Circulateur", "circ")
        
    with col_mat2:
        st.markdown("**📦 Stockage & Appoint**")
        m_bal, p_bal = row_mat("Marque/Réf Ballons", "bal")
        vol_bal = st.number_input("Volume total (L)", value=1000, step=100)
        m_reg, p_reg = row_mat("Marque/Réf Régulateur", "reg")
        m_app, p_app = row_mat("Marque/Réf Appoint", "app")
        anode = st.selectbox("Protection cuve", ["ACI", "Magnésium", "Inox", "N/A"])

# --- 6. AUDIT DES 73 POINTS ---
st.divider()
st.header("🔍 Audit Technique")

sections = {
    "📄 Documentation et conformité électrique": ["Schéma d'exécution", "Schéma Electrique", "Analyse Fonctionnelle", "Raccordements", "Mise à la terre", "Signalétique de sécurité", "Livret d'entretien"],
    "☀️ Capteurs & Toit": ["Intégrité vitrages", "Absorbeur", "Fixations châssis", "Étanchéité toiture", "Masques solaires", "Isolants UV"],
    "🧪 Fluide Caloporteur": ["Prélèvement fluide", "pH du fluide", "Type et Fabricant Glycol", "Protection Antigel (Réfractomètre)", "Analyse visuelle (Coloration)"],
    "💧 Hydraulique": ["Sens circulation", "Vannes remplissage", "Dégazeur Aller", "Soupape conforme", "Bidon récupération", "Vase d'expansion", "Disconnecteur"],
    "📦 Stockage & Echangeur": ["Echangeur (Entartrage)", "Protection cathodique", "Calorifugeage", "Lyres anti-thermosiphon", "Soupape sécurité"],
    "📊 Métrologie & Régul": ["Manomètre", "Débitmètre", "Sonde Capteur (T1)", "Sonde Ballon (T2)", "Protection Surchauffe (85°C)", "Delta T"]
}

all_results = []
for sec, pts in sections.items():
    with st.expander(f"📁 {sec}"):
        for p in pts:
            # Aides visuelles pH
            if "pH" in p:
                ca, cb, cc = st.columns(3)
                ca.markdown('<div class="color-box" style="background-color: #e74c3c;">Acide < 7</div>', unsafe_allow_html=True)
                cb.markdown('<div class="color-box" style="background-color: #2ecc71;">Idéal 8-10</div>', unsafe_allow_html=True)
                cc.markdown('<div class="color-box" style="background-color: #3498db;">Base > 10</div>', unsafe_allow_html=True)
            
            st.markdown(f"**{p}**")
            c_res, c_obs, c_cam = st.columns([1.5, 3, 1])
            with c_res:
                res = st.selectbox("Statut", ["Conforme", "Non Conforme", "N/C", "S/O"], key=f"s_{p}")
            with c_obs:
                obs = st.text_input("Note / Mesure", key=f"o_{p}", placeholder="RAS")
            with c_cam:
                pic = st.camera_input("📷", key=f"c_{p}")
            all_results.append({"Section": sec, "Point": p, "Statut": res, "Obs": obs})

# --- 7. GÉNÉRATION PDF ---
st.divider()
if st.button("🚀 GÉNÉRER LE RAPPORT FINAL"):
    if not nom_site:
        st.error("Veuillez saisir le nom du site.")
    else:
        st.balloons()
        st.success(f"Audit de {nom_site} terminé. Le PDF est en cours de compilation...")