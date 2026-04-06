import streamlit as st
import pandas as pd
from datetime import datetime
import os
from fpdf import FPDF

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Opthelios Expert Solaire", layout="wide", page_icon="☀️")

# --- 2. THEME & DESIGN ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png")
    st.header("🎨 Personnalisation")
    theme = st.radio("Thème", ["☀️ Clair", "🌙 Sombre"], horizontal=True)
    st.divider()
    nom_site = st.text_input("📍 Nom du Site", placeholder="Ex: Résidence Horizon")
    type_inst = st.selectbox("⚙️ Architecture", ["CESC", "Auto-vidangeable", "Sous-pression", "Thermosiphon"])

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
    /* Style pour les aides visuelles */
    .color-box {{ padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; font-size: 0.8em; color: white; margin: 2px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DONNÉES ---
sections = {
    "📄 Admin & Elec": ["Schéma d'exécution", "Schéma Electrique", "Analyse Fonctionnelle", "Raccordements", "Mise à la terre", "Signalétique de sécurité solaire", "Livret d'entretien présent"],
    "☀️ Capteurs & Toit": ["Absence vannes isolement", "Traversée de toiture", "Supports conformes", "Raccordement capteurs", "Accès sécurisé", "Absence de masque", "Étanchéité des supports (Abas)", "État isolants câbles sondes (UV)"],
    "💧 Hydraulique": ["Sens circulation", "Vannes remplissage", "Dégazeur Aller", "Soupape conforme", "Bidon récupération", "Circulateur Retour", "Clapet Retour", "V3V fonctionnelles", "Disconnecteur sur appoint"],
    "🧪 Fluide Caloporteur": [
        "Prélèvement fluide", 
        "pH du fluide (Contrôle acidité)", 
        "Type et Fabricant du Glycol", 
        "Protection Antigel (Mesure Réfractomètre)",
        "Analyse visuelle (Coloration et Texture)"
    ],
    "🎈 Expansion": ["Vase adapté", "Volume suffisant", "Isolement", "Raccordement Retour", "Pression conforme"],
    "📦 Stockage & Echangeur": ["Contre-courant", "Vannes échangeur", "Puissance échangeur", "Local hors gel", "Accès brides", "Raccordement ballons", "Vidange basse", "Protection cathodique", "Calorifuge", "Lyres anti-thermosiphon", "Soupape sécurité"],
    "🚿 Distribution ECS": ["Mitigeur présent", "Température points puisage", "Bouclage conforme", "Clapets anti-retour", "Bouclage calorifugé"],
    "📊 Métrologie & Régul": ["Manomètre", "Débitmètre", "Sonde ensoleillement", "Sonde capteur", "Sonde ballon", "Tests étanchéité", "Rinçage réseau", "Télécontrôleur", "Protection Surchauffe (Test 85°C)", "Écart de température (Delta T)"]
}

# --- 4. CALCUL DE PROGRESSION ---
st.title("☀️ Diagnostic Expert Opthelios")
progress_bar = st.empty()
progress_text = st.empty()

# --- 5. FORMULAIRE D'AUDIT ---
all_results = []
total_pts = sum(len(pts) for pts in sections.values())

for sec, pts in sections.items():
    if sec == "🎈 Expansion" and type_inst == "Auto-vidangeable":
        total_pts -= len(pts)
        continue
        
    with st.expander(f"{sec}", expanded=False):
        for p in pts:
            st.markdown(f"#### 🔹 {p}")
            
            # --- AJOUT DES AIDES VISUELLES SPÉCIFIQUES ---
            if "pH du fluide" in p:
                st.info("💡 Référentiel pH Solaire :")
                c1, c2, c3, c4 = st.columns(4)
                c1.markdown('<div class="color-box" style="background-color: #e74c3c;">Acidité < 7<br>DANGER</div>', unsafe_allow_html=True)
                c2.markdown('<div class="color-box" style="background-color: #f1c40f;">Neutre 7-8<br>SURVEILLER</div>', unsafe_allow_html=True)
                c3.markdown('<div class="color-box" style="background-color: #2ecc71;">Idéal 8-10<br>CONFORME</div>', unsafe_allow_html=True)
                c4.markdown('<div class="color-box" style="background-color: #3498db;">Base > 10<br>OK</div>', unsafe_allow_html=True)
            
            if "Analyse visuelle" in p:
                st.info("💡 État du Glycol :")
                c1, c2, c3 = st.columns(3)
                c1.markdown('<div class="color-box" style="background-color: #ff9ff3; color: black;">Rose/Bleu Limpide<br>NEUF</div>', unsafe_allow_html=True)
                c2.markdown('<div class="color-box" style="background-color: #f39c12;">Orange/Jaune<br>USAGÉ</div>', unsafe_allow_html=True)
                c3.markdown('<div class="color-box" style="background-color: #2c3e50;">Brun/Noir/Opaque<br>CARAMÉLISÉ</div>', unsafe_allow_html=True)

            col_form, col_cam = st.columns([1, 1])
            
            with col_form:
                res = st.radio("Statut", ["Conforme", "Non Conforme", "Non Contrôlable", "Sans objet"], key=f"s_{p}", horizontal=True)
                obs = st.text_area("Note technique", key=f"o_{p}", placeholder="Résultats des mesures...", height=68)
            
            with col_cam:
                img = st.camera_input(f"Photo {p}", key=f"c_{p}")
            
            all_results.append({"Point": p, "Statut": res, "Obs": obs})
            st.divider()

# Gestion progression
completed = len([k for k in st.session_state if k.startswith("s_") and st.session_state[k] != "Sans objet"])
percent = min(100, int((completed / total_pts) * 100))
progress_bar.progress(percent)
progress_text.markdown(f"**Progression : {percent}%** ({completed}/{total_pts})")

# --- 6. VALIDATION ---
st.markdown("### 🖋️ Validation du Diagnostic")
nom_tech = st.text_input("Nom du technicien", value="Moran GUILLERMIC")
confirmation = st.checkbox("Je certifie la conformité des tests caloporteurs effectués.")

# --- 7. GÉNÉRATION PDF ---
class ProPDF(FPDF):
    def header(self):
        if os.path.exists("logo.png"): self.image("logo.png", 10, 8, 30)
        self.set_font("Arial", "B", 12)
        self.set_text_color(0, 74, 153)
        self.cell(0, 10, "RAPPORT D'EXPERTISE TECHNIQUE", ln=True, align="R")
        self.ln(10)

def make_pdf(df, score, site, tech):
    pdf = ProPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0)
    pdf.cell(0, 10, f"SITE : {site}", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 7, f"Technicien : {tech} | Date : {datetime.now().strftime('%d/%m/%Y')}", ln=True)
    pdf.cell(0, 7, f"Score global de conformité : {score:.1f}%", ln=True)
    pdf.ln(5)
    
    pdf.set_fill_color(255, 127, 0)
    pdf.set_text_color(255)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(90, 8, "Point de contrôle", 1, 0, 'L', True)
    pdf.cell(35, 8, "Statut", 1, 0, 'C', True)
    pdf.cell(65, 8, "Observations", 1, 1, 'L', True)
    
    pdf.set_text_color(0)
    pdf.set_font("Arial", "", 8)
    for _, row in df.iterrows():
        if row["Statut"] != "Sans objet":
            pdf.cell(90, 7, str(row["Point"])[:55], 1)
            pdf.cell(35, 7, row["Statut"], 1, 0, 'C')
            pdf.cell(65, 7, str(row["Obs"])[:45], 1, 1)
    return pdf.output()

if st.button("🚀 GÉNÉRER LE RAPPORT FINAL"):
    if not confirmation:
        st.warning("Veuillez valider les tests avant l'export.")
    else:
        df_final = pd.DataFrame(all_results)
        df_eval = df_final[df_final["Statut"].isin(["Conforme", "Non Conforme"])]
        score = (len(df_eval[df_eval["Statut"] == "Conforme"]) / len(df_eval)) * 100 if len(df_eval) > 0 else 0
        st.balloons()
        pdf_bytes = make_pdf(df_final, score, nom_site, nom_tech)
        st.download_button("📥 Télécharger le PDF Expert", data=bytes(pdf_bytes), file_name=f"Expertise_Opthelios_{nom_site}.pdf")