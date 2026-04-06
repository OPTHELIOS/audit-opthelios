import streamlit as st
import pandas as pd
from datetime import datetime
import os
from fpdf import FPDF

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Opthelios Audit Solaire", 
    layout="wide", 
    page_icon="☀️"
)

# --- 2. GESTION DU THÈME ET STYLE ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png")
    
    st.header("🎨 Apparence")
    theme = st.radio("Mode d'affichage", ["☀️ Clair", "🌙 Sombre"], horizontal=True)
    
    st.divider()
    st.header("📌 Identification Site")
    nom_site = st.text_input("📍 Nom du Site", placeholder="Ex: Résidence Horizon")
    
    st.subheader("⚙️ Configuration")
    type_inst = st.selectbox("Type d'installation", [
        "Chauffe-eau solaire collectif (CESC)", 
        "Autovidangeable", 
        "Sous-pression", 
        "Thermosiphon"
    ])
    
    st.divider()
    st.markdown("### 📞 Contact Opthelios")
    st.write("**Moran GUILLERMIC**")
    st.write("✉️ contact@opthelios.fr")
    st.write("📞 06 45 57 10 42")
    st.write("🌐 [www.opthelios.com](https://www.opthelios.com)")

# Couleurs dynamiques
if theme == "🌙 Sombre":
    bg_col, card_col, txt_col, brd_col = "#121212", "#1E1E1E", "#FFFFFF", "#444444"
else:
    bg_col, card_col, txt_col, brd_col = "#F4F7F9", "#FFFFFF", "#004a99", "#D0D0D0"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_col}; color: {text_col}; }}
    h1, h2, h3, p, span, label {{ color: {text_col} !important; }}
    [data-testid="stExpander"] {{
        background-color: {card_col} !important;
        border: 1px solid {brd_col} !important;
        border-radius: 8px !important;
        margin-bottom: 10px;
    }}
    .stButton>button {{
        background-color: #ff7f00 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 5px !important;
        width: 100%;
        height: 3em;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DONNÉES DES POINTS ---
audit_sections = {
    "📄 Documentation & Elec": ["Schéma d'exécution", "Schéma Electrique", "Analyse Fonctionnelle", "Raccordements", "Installation générale", "Mise à la terre"],
    "☀️ Capteurs & Toiture": ["Absence de vannes d'isolement", "Traversée de toiture adaptée", "Supports conformes", "Raccordement capteurs", "Accès sécurisé", "Absence de masque"],
    "⚖️ Equilibrage & Canalisations": ["Equilibrage champ", "Equilibreurs exploitables", "Matériaux conformes"],
    "💧 Hydraulique Solaire": ["Sens de circulation", "Vannes remplissage", "Dégazeur Aller", "Soupape conforme", "Bidon récupération", "Circulateur Retour", "Clapet Retour", "V3V fonctionnelles"],
    "🎈 Expansion": ["Vase adapté", "Volume suffisant", "Dispositif isolement", "Raccordement Retour", "Pression conforme"],
    "📦 Stockage & Echangeur": ["Contre-courant", "Vannes échangeur", "Puissance échangeur", "Local hors gel", "Accès brides", "Raccordement ballons", "Vidange basse", "Protection cathodique", "Calorifuge", "Soupape sécurité"],
    "🚿 Distribution ECS": ["Mitigeur présent", "Température points puisage", "Bouclage conforme", "Clapets anti-retour", "Bouclage calorifugé"],
    "📊 Métrologie & Tests": ["Manomètre", "Débitmètre", "Sonde ensoleillement", "Sonde capteur", "Sonde ballon", "Prélèvement caloporteur", "Tests étanchéité", "Rinçage réseau", "Télécontrôleur"]
}

# --- 4. LOGIQUE PDF ---
class OptheliosPDF(FPDF):
    def header(self):
        if os.path.exists("logo.png"):
            self.image("logo.png", 10, 8, 30)
        self.set_font("Arial", "B", 14)
        self.set_text_color(0, 74, 153)
        self.cell(0, 10, "RAPPORT DE DIAGNOSTIC SOLAIRE", ln=True, align="R")
        self.ln(10)

def generate_pdf(nom, type_i, df, score):
    pdf = OptheliosPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, f"Site : {nom}", ln=True)
    pdf.cell(0, 8, f"Type : {type_i}", ln=True)
    pdf.cell(0, 8, f"Score Final : {score:.1f}%", ln=True)
    pdf.ln(5)
    
    # Entête tableau
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(100, 8, "Point de controle", 1, 0, 'L', True)
    pdf.cell(25, 8, "Statut", 1, 0, 'C', True)
    pdf.cell(65, 8, "Observations", 1, 1, 'L', True)
    
    pdf.set_font("Arial", "", 9)
    for _, row in df.iterrows():
        # ICI : Vérification stricte des noms de colonnes "Point", "Statut", "Obs"
        h = 7
        pdf.set_text_color(200, 0, 0) if row["Statut"] == "NC" else pdf.set_text_color(0)
        pdf.cell(100, h, str(row["Point"])[:55], 1)
        pdf.cell(25, h, row["Statut"], 1, 0, 'C')
        pdf.cell(65, h, str(row["Obs"])[:35], 1, 1)
    return pdf.output()

# --- 5. CORPS DE L'AUDIT ---
st.title("☀️ Diagnostic Solaire Opthelios")

all_results = []
for sec, pts in audit_sections.items():
    if sec == "🎈 Expansion" and type_inst == "Autovidangeable":
        continue
    with st.expander(f"{sec}"):
        for p in pts:
            c1, c2, c3 = st.columns([3, 1, 2])
            with c1: st.markdown(f"🔹 {p}")
            # IMPORTANT : Les clés dans le dictionnaire final seront "Point", "Statut", "Obs"
            res = c2.selectbox("Statut", ["OK", "NC", "N/A"], key=f"s_{p}", label_visibility="collapsed")
            obs = c3.text_input("Notes", key=f"o_{p}", placeholder="Observation...", label_visibility="collapsed")
            all_results.append({"Point": p, "Statut": res, "Obs": obs})

# --- 6. BILAN ---
if st.button("📊 GÉNÉRER LE RAPPORT FINAL"):
    df_res = pd.DataFrame(all_results)
    df_valide = df_res[df_res["Statut"] != "N/A"]
    
    if not df_valide.empty:
        score_f = (len(df_valide[df_valide["Statut"] == "OK"]) / len(df_valide)) * 100
        st.header(f"📈 Score : {score_f:.1f}%")
        
        # Génération PDF sécurisée
        try:
            pdf_out = generate_pdf(nom_site, type_inst, df_valide, score_f)
            st.download_button("📥 Télécharger le Rapport PDF", data=bytes(pdf_out), file_name=f"Audit_{nom_site}.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"Erreur lors de la création du PDF : {e}")
            
        df_nc = df_valide[df_valide["Statut"] == "NC"]
        if not df_nc.empty:
            st.error("### 🚩 Points non conformes")
            st.table(df_nc[["Point", "Obs"]])
    else:
        st.warning("Veuillez remplir au moins un point.")