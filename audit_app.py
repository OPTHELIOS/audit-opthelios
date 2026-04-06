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

from fpdf import FPDF
import io

# --- FONCTION DE GÉNÉRATION PDF ---
class OptheliosPDF(FPDF):
    def header(self):
        if os.path.exists("logo.png"):
            self.image("logo.png", 10, 8, 33)
        self.set_font("Arial", "B", 15)
        self.set_text_color(0, 74, 153) # Bleu Opthelios
        self.cell(80)
        self.cell(30, 10, "RAPPORT DE DIAGNOSTIC SOLAIRE", 0, 0, "C")
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(128)
        self.cell(0, 10, f"Page {self.page_no()} | Opthelios - www.opthelios.com", 0, 0, "C")

def generate_pdf(nom_site, type_inst, df, score):
    pdf = OptheliosPDF()
    pdf.add_page()
    
    # Infos client
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(0)
    pdf.cell(0, 10, f"Site : {nom_site}", ln=True)
    pdf.cell(0, 10, f"Technicien : Moran GUILLERMIC", ln=True)
    pdf.cell(0, 10, f"Date : {datetime.now().strftime('%d/%m/%Y')}", ln=True)
    pdf.cell(0, 10, f"Installation : {type_inst}", ln=True)
    
    # Score Global
    pdf.ln(5)
    pdf.set_fill_color(255, 127, 0) # Orange Opthelios
    pdf.set_text_color(255)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 12, f"SCORE DE CONFORMITÉ : {score:.1f}%", ln=True, align="C", fill=True)
    pdf.ln(10)

    # Tableau des points
    pdf.set_text_color(0)
    pdf.set_font("Arial", "B", 10)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(90, 10, "Point de controle", 1, 0, "C", True)
    pdf.cell(30, 10, "Statut", 1, 0, "C", True)
    pdf.cell(70, 10, "Observations", 1, 1, "C", True)

    pdf.set_font("Arial", "", 9)
    for index, row in df.iterrows():
        if row["Statut"] != "N/A":
            # Gestion des couleurs pour le statut
            if row["Statut"] == "NC":
                pdf.set_text_color(200, 0, 0) # Rouge
            else:
                pdf.set_text_color(0, 128, 0) # Vert
            
            # Calcul de la hauteur pour le texte long
            start_y = pdf.get_y()
            pdf.multi_cell(90, 8, row["Point"], border=1)
            end_y = pdf.get_y()
            h = end_y - start_y
            
            pdf.set_y(start_y)
            pdf.set_x(100)
            pdf.cell(30, h, row["Statut"], border=1, align="C")
            pdf.cell(70, h, row["Observation"][:40], border=1, align="L")
            pdf.ln(h)
            pdf.set_text_color(0)

    return pdf.output(dest='S')

# --- SECTION BOUTON FINAL ---
st.markdown("### 🏁 Finalisation de l'Audit")
if st.button("📊 CALCULER LE BILAN ET GÉNÉRER LE RAPPORT PDF"):
    df = pd.DataFrame(all_results)
    df_app = df[df["Statut"] != "N/A"]
    
    if not df_app.empty:
        conformes = len(df_app[df_app["Statut"] == "OK"])
        score = (conformes / len(df_app)) * 100
        
        st.header(f"📈 Score de Conformité : {score:.1f}%")
        
        # Génération du fichier PDF en mémoire
        pdf_data = generate_pdf(nom_site, type_inst, df, score)
        
        st.download_button(
            label="📥 Télécharger le Rapport PDF Pro",
            data=bytes(pdf_data),
            file_name=f"Rapport_Opthelios_{nom_site}.pdf",
            mime="application/pdf"
        )
        
        # Petit récap visuel des NC pour Moran
        df_nc = df_app[df_app["Statut"] == "NC"]
        if not df_nc.empty:
            st.error("### 🚩 Anomalies détectées")
            st.table(df_nc[["Point", "Observation"]])
    else:
        st.warning("Veuillez renseigner des points avant de générer le PDF.")