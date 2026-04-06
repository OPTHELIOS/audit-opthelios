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

# --- VARIABLES DE COULEUR ---
if theme == "🌙 Sombre":
    bg_col, card_col, txt_col, brd_col = "#121212", "#1E1E1E", "#FFFFFF", "#444444"
else:
    bg_col, card_col, txt_col, brd_col = "#F4F7F9", "#FFFFFF", "#004a99", "#D0D0D0"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_col}; color: {txt_col}; }}
    h1, h2, h3, p, span, label {{ color: {txt_col} !important; }}
    [data-testid="stExpander"] {{
        background-color: {card_col} !important;
        border: 1px solid {brd_col} !important;
        border-radius: 8px !important;
        margin-bottom: 15px;
    }}
    .stButton>button {{
        background-color: #ff7f00 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 5px !important;
        width: 100%;
        height: 3em;
    }}
    /* Style spécifique pour les photos */
    [data-testid="stCameraInput"] {{
        border: 1px solid {brd_col} !important;
        border-radius: 8px;
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
    pdf.set_text_color(0)
    pdf.cell(0, 8, f"Site : {nom}", ln=True)
    pdf.cell(0, 8, f"Type : {type_i}", ln=True)
    pdf.cell(0, 8, f"Score Final : {score:.1f}%", ln=True)
    pdf.ln(5)
    
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", "B", 9)
    pdf.cell(85, 8, "Point de controle", 1, 0, 'L', True)
    pdf.cell(35, 8, "Statut", 1, 0, 'C', True)
    pdf.cell(70, 8, "Observations", 1, 1, 'L', True)
    
    pdf.set_font("Arial", "", 8)
    for _, row in df.iterrows():
        if row["Statut"] != "Sans objet":
            h = 7
            if row["Statut"] == "Non Conforme":
                pdf.set_text_color(200, 0, 0)
            else:
                pdf.set_text_color(0)
            pdf.cell(85, h, str(row["Point"])[:50], 1)
            pdf.cell(35, h, row["Statut"], 1, 0, 'C')
            pdf.cell(70, h, str(row["Obs"])[:45], 1, 1)
    return pdf.output()

# --- 5. CORPS DE L'AUDIT ---
st.title("☀️ Diagnostic Solaire Opthelios")

all_results = []
for sec, pts in audit_sections.items():
    if sec == "🎈 Expansion" and type_inst == "Autovidangeable":
        continue
    with st.expander(f"{sec}"):
        for p in pts:
            st.markdown(f"### 🔹 {p}")
            c1, c2 = st.columns([1, 1])
            
            with c1:
                res = st.radio(
                    "Conformité", 
                    ["Conforme", "Non Conforme", "Non Contrôlable", "Sans objet"], 
                    key=f"s_{p}", 
                    horizontal=True
                )
                obs = st.text_area("Observations / Recommandations", key=f"o_{p}", placeholder="RAS", height=80)
            
            with c2:
                # Capture photo par ligne
                img_file = st.camera_input(f"Photo : {p}", key=f"cam_{p}")
                if img_file:
                    st.success("Photo enregistrée")
            
            all_results.append({"Point": p, "Statut": res, "Obs": obs})
            st.divider()

# --- 6. BILAN ---
if st.button("📊 GÉNÉRER LE RAPPORT FINAL"):
    df_res = pd.DataFrame(all_results)
    df_valide = df_res[df_res["Statut"] != "Sans objet"]
    
    if not df_valide.empty:
        # Score calculé sur Conforme vs (Conforme + Non Conforme)
        total_eval = len(df_valide[df_valide["Statut"].isin(["Conforme", "Non Conforme"])])
        if total_eval > 0:
            score_f = (len(df_valide[df_valide["Statut"] == "Conforme"]) / total_eval) * 100
        else:
            score_f = 0
            
        st.header(f"📈 Score de Conformité : {score_f:.1f}%")
        
        try:
            pdf_out = generate_pdf(nom_site, type_inst, df_valide, score_f)
            st.download_button(
                label="📥 Télécharger le Rapport PDF", 
                data=bytes(pdf_out), 
                file_name=f"Audit_{nom_site}.pdf", 
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Erreur PDF : {e}")
            
        df_nc = df_valide[df_valide["Statut"] == "Non Conforme"]
        if not df_nc.empty:
            st.error("### 🚩 Points Non Conformes")
            st.table(df_nc[["Point", "Obs"]])
    else:
        st.warning("Veuillez remplir au moins un point.")