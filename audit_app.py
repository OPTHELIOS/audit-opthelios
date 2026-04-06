import streamlit as st
import pandas as pd
from datetime import datetime
import os
from fpdf import FPDF

# --- CONFIGURATION ---
st.set_page_config(page_title="Opthelios Expert", layout="wide")

# --- STYLE ---
st.markdown("""
    <style>
    .stApp { background-color: #F4F7F9; color: #004a99; }
    [data-testid="stExpander"] { background-color: white !important; border: 1px solid #D0D0D0 !important; border-radius: 12px !important; }
    .stButton>button { background-color: #ff7f00 !important; color: white !important; font-weight: bold; border-radius: 10px; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- INFOS SITE ---
st.title("🚀 Rapport d'Expertise Solaire")
col1, col2 = st.columns(2)
with col1:
    nom_site = st.text_input("Nom de l'opération", value="Résidence Hôtelière du Rail")
    adresse_site = st.text_area("Adresse", value="25 allée Eugène Delacroix, 33800 Bordeaux")
    gps_site = st.text_input("Coordonnées GPS", placeholder="44.8247, -0.5539")
with col2:
    photo_couverture = st.camera_input("📸 Photo de garde du site")
    maitre_ouvrage = st.text_input("Maître d'ouvrage", value="ICF Habitat")

# --- FICHE D'IDENTITÉ AVEC PHOTOS ---
st.header("📋 Fiche d'Identité de l'Installation")

with st.expander("📝 DÉTAILS MATÉRIELS (Cliquer pour remplir)", expanded=True):
    # On crée une structure pour stocker les données de la fiche
    mat_data = {}
    
    def mat_row(label, key):
        c_text, c_img = st.columns([2, 1])
        with c_text:
            val = st.text_input(label, key=f"mat_{key}")
        with c_img:
            img = st.camera_input(f"Photo {label}", key=f"img_{key}")
        return val, img

    st.markdown("### ☀️ Champ Solaire")
    mat_data['m_capteur'], mat_data['i_capteur'] = mat_row("Marque et Réf. Capteurs", "capteur")
    col_s1, col_s2 = st.columns(2)
    mat_data['orient'] = col_s1.selectbox("Orientation", ["Sud", "Sud-Est", "Sud-Ouest", "Est", "Ouest"])
    mat_data['inclin'] = col_s2.number_input("Inclinaison (°)", value=45)

    st.divider()
    st.markdown("### 📦 Stockage & Échange")
    mat_data['m_ballon'], mat_data['i_ballon'] = mat_row("Marque et Réf. Ballons", "ballon")
    mat_data['vol_total'] = st.number_input("Volume total stockage (Litres)", value=1000)
    mat_data['t_ech'] = st.radio("Type d'échangeur", ["Interne", "Externe à plaques"], horizontal=True)
    mat_data['anode'] = st.selectbox("Protection cuve", ["Anode Magnésium", "ACI", "Inox", "Inconnu"])

    st.divider()
    st.markdown("### 💧 Hydraulique & Fluide")
    mat_data['m_circ'], mat_data['i_circ'] = mat_row("Marque et Réf. Circulateur", "circ")
    mat_data['vol_fluide'] = st.number_input("Volume estimé circuit solaire (Litres)", value=100)
    
    st.divider()
    st.markdown("### 📊 Régulation & Appoint")
    mat_data['m_reg'], mat_data['i_reg'] = mat_row("Marque et Réf. Régulateur", "reg")
    mat_data['t_app'], mat_data['i_app'] = mat_row("Type et Réf. Appoint", "app")
    mat_data['compteur'] = st.checkbox("Présence d'un compteur d'énergie (WMZ)")

# --- POINTS DE CONTRÔLE (Résumé) ---
st.header("🔍 Audit des 73 Points")
# ... (Ici on garde la boucle des sections précédente pour les 73 points) ...

# --- GÉNÉRATION PDF ---
def generate_pdf(site, mat):
    pdf = FPDF()
    # Page de Garde
    pdf.add_page()
    pdf.set_font("Arial", "B", 24)
    pdf.cell(0, 20, site['nom'], ln=True, align="C")
    if site['photo']:
        with open("temp_site.jpg", "wb") as f: f.write(site['photo'].getbuffer())
        pdf.image("temp_site.jpg", x=10, y=50, w=190)
    
    # Page Fiche d'identité
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "FICHE D'IDENTITÉ MATÉRIEL", ln=True)
    pdf.set_font("Arial", "", 10)
    for k, v in mat.items():
        if not k.startswith('i_'): # On ne liste que le texte
            pdf.cell(60, 8, str(k), 1)
            pdf.cell(130, 8, str(v), 1, 1)
    
    # Ajout des photos matériel en annexe technique
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "ANNEXE PHOTOS MATÉRIEL", ln=True)
    # Logique pour placer les photos 'i_capteur', 'i_ballon', etc.
    # ...
    return pdf.output()

if st.button("🚀 GÉNÉRER LE RAPPORT FINAL"):
    st.success("Rapport en cours de génération...")
    # (Appel de la fonction PDF avec les données mat_data)