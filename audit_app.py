import streamlit as st
import pandas as pd
from datetime import datetime
import os
from fpdf import FPDF

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Opthelios Pro Audit", layout="wide", page_icon="☀️")

# --- 2. THEME & DESIGN ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png")
    st.header("🎨 Personnalisation")
    theme = st.radio("Thème", ["☀️ Clair", "🌙 Sombre"], horizontal=True)
    st.divider()
    nom_site = st.text_input("📍 Nom du Site", placeholder="Ex: Résidence Horizon")
    type_inst = st.selectbox("⚙️ Architecture", ["CESC", "Auto-vidangeable", "Sous-pression", "Thermosiphon"])
    st.info("💡 Conseil : Prenez les photos en mode paysage pour un meilleur rendu PDF.")

# Couleurs
if theme == "🌙 Sombre":
    bg, card, txt, brd = "#121212", "#1E1E1E", "#FFFFFF", "#444444"
else:
    bg, card, txt, brd = "#F4F7F9", "#FFFFFF", "#004a99", "#D0D0D0"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {txt}; }}
    [data-testid="stExpander"] {{ background-color: {card} !important; border: 1px solid {brd} !important; border-radius: 12px !important; }}
    .stButton>button {{ background-color: #ff7f00 !important; color: white !important; font-weight: bold; height: 3.5em; border-radius: 10px; }}
    .stProgress > div > div > div > div {{ background-color: #ff7f00 !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DONNÉES ÉTENDUE (73 POINTS) ---
sections = {
    "📄 Admin & Elec": ["Schéma d'exécution", "Schéma Electrique", "Analyse Fonctionnelle", "Raccordements", "Mise à la terre", "Signalétique de sécurité solaire 🆕", "Livret d'entretien présent 🆕"],
    "☀️ Capteurs & Toit": ["Absence vannes isolement", "Traversée de toiture", "Supports conformes", "Raccordement capteurs", "Accès sécurisé", "Absence de masque", "Étanchéité des supports (Abas) 🆕", "État isolants câbles sondes (UV) 🆕"],
    "💧 Hydraulique": ["Sens circulation", "Vannes remplissage", "Dégazeur Aller", "Soupape conforme", "Bidon récupération", "Circulateur Retour", "Clapet Retour", "V3V fonctionnelles", "Disconnecteur sur appoint 🆕"],
    "🧪 Fluide Caloporteur": ["Prélèvement fluide", "pH du fluide (Corrosion) 🆕", "Date péremption fluide 🆕", "Protection Gel (Test +4°C) 🆕"],
    "🎈 Expansion": ["Vase adapté", "Volume suffisant", "Isolement", "Raccordement Retour", "Pression conforme"],
    "📦 Stockage & Echangeur": ["Contre-courant", "Vannes échangeur", "Puissance échangeur", "Local hors gel", "Accès brides", "Raccordement ballons", "Vidange basse", "Protection cathodique", "Calorifuge", "Lyres anti-thermosiphon", "Soupape sécurité"],
    "🚿 Distribution ECS": ["Mitigeur présent", "Température points puisage", "Bouclage conforme", "Clapets anti-retour", "Bouclage calorifugé"],
    "📊 Métrologie & Régul": ["Manomètre", "Débitmètre", "Sonde ensoleillement", "Sonde capteur", "Sonde ballon", "Tests étanchéité", "Rinçage réseau", "Télécontrôleur", "Protection Surchauffe (Test 85°C) 🆕", "Écart de température (Delta T) 🆕"]
}

# --- 4. CALCUL DE PROGRESSION ---
st.title("☀️ Diagnostic Solaire Haute Précision")
progress_bar = st.empty()
progress_text = st.empty()

# --- 5. FORMULAIRE D'AUDIT ---
all_results = []
filled_count = 0
total_pts = sum(len(pts) for pts in sections.values())

for sec, pts in sections.items():
    if sec == "🎈 Expansion" and type_inst == "Auto-vidangeable":
        total_pts -= len(pts)
        continue
        
    with st.expander(f"{sec}", expanded=False):
        for p in pts:
            st.markdown(f"#### 🔹 {p}")
            col_form, col_cam = st.columns([1, 1])
            
            with col_form:
                res = st.radio("Statut", ["Conforme", "Non Conforme", "Non Contrôlable", "Sans objet"], key=f"s_{p}", horizontal=True)
                obs = st.text_area("Note technique", key=f"o_{p}", placeholder="RAS", height=68)
                if res != "Sans objet" and (obs != "" or res != "Conforme"):
                    filled_count += 0 # Logique de progression simple
            
            with col_cam:
                img = st.camera_input(f"Photo {p}", key=f"c_{p}")
            
            all_results.append({"Point": p, "Statut": res, "Obs": obs})
            st.divider()

# Mise à jour progression (basée sur les clés existantes dans session_state)
completed = len([k for k in st.session_state if k.startswith("s_") and st.session_state[k] != "Sans objet"])
percent = min(100, int((completed / total_pts) * 100))
progress_bar.progress(percent)
progress_text.markdown(f"**Progression de l'audit : {percent}%** ({completed} / {total_pts} points)")

# --- 6. SIGNATURE ---
st.markdown("### 🖋️ Validation & Signature")
# Note : Pour une vraie signature tactile, on utilise souvent streamlit-drawable-canvas
# Ici on simule une validation par nom pour rester sur les librairies standards
nom_tech = st.text_input("Nom du technicien", value="Moran GUILLERMIC")
confirmation = st.checkbox("Je certifie l'exactitude des relevés terrain.")

# --- 7. GÉNÉRATION RAPPORT ---
class ProPDF(FPDF):
    def header(self):
        if os.path.exists("logo.png"): self.image("logo.png", 10, 8, 30)
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, f"RAPPORT EXPERT - {datetime.now().strftime('%d/%m/%Y')}", ln=True, align="R")
        self.ln(10)

def make_pdf(df, score, site, tech):
    pdf = ProPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"AUDIT TECHNIQUE : {site}", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 7, f"Technicien : {tech}", ln=True)
    pdf.cell(0, 7, f"Score de conformité : {score:.1f}%", ln=True)
    pdf.ln(5)
    
    # Tableau
    pdf.set_fill_color(255, 127, 0)
    pdf.set_text_color(255)
    pdf.cell(90, 8, "Point de contrôle", 1, 0, 'L', True)
    pdf.cell(35, 8, "Statut", 1, 0, 'C', True)
    pdf.cell(65, 8, "Observations", 1, 1, 'L', True)
    
    pdf.set_text_color(0)
    pdf.set_font("Arial", "", 8)
    for _, row in df.iterrows():
        if row["Statut"] != "Sans objet":
            pdf.cell(90, 7, str(row["Point"])[:50], 1)
            pdf.cell(35, 7, row["Statut"], 1, 0, 'C')
            pdf.cell(65, 7, str(row["Obs"])[:40], 1, 1)
    return pdf.output()

if st.button("🚀 FINALISER ET GÉNÉRER LE RAPPORT PRO"):
    if not confirmation:
        st.warning("Veuillez cocher la case de certification avant d'exporter.")
    else:
        df_final = pd.DataFrame(all_results)
        df_eval = df_final[df_final["Statut"].isin(["Conforme", "Non Conforme"])]
        score = (len(df_eval[df_eval["Statut"] == "Conforme"]) / len(df_eval)) * 100 if len(df_eval) > 0 else 0
        
        st.balloons()
        pdf_bytes = make_pdf(df_final, score, nom_site, nom_tech)
        st.download_button("📥 Télécharger le Rapport Expert (PDF)", data=bytes(pdf_bytes), file_name=f"Audit_Expert_{nom_site}.pdf")