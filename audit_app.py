import streamlit as st
import pandas as pd
from datetime import datetime
import os
from fpdf import FPDF

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Opthelios Expert Solaire", layout="wide", page_icon="☀️")

# --- 2. THEME & STYLE ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png")
    st.header("🎨 Personnalisation")
    theme = st.radio("Thème", ["☀️ Clair", "🌙 Sombre"], horizontal=True)
    st.divider()
    st.markdown("### 📞 Contact Opthelios")
    st.write("**Moran GUILLERMIC**")
    st.write("contact@opthelios.fr | 06 45 57 10 42")

# --- 3. QUESTIONS PRÉLIMINAIRES (PAGE DE GARDE) ---
st.title("🚀 Nouvel Audit Solaire Thermique")

col_g1, col_g2 = st.columns(2)
with col_g1:
    st.subheader("📌 Informations Site")
    nom_site = st.text_input("Nom de l'opération", placeholder="Ex: Résidence Hôtelière du Rail")
    adresse_site = st.text_area("Adresse complète", placeholder="25 allée Eugène Delacroix, 33800 Bordeaux")
    gps_site = st.text_input("Coordonnées GPS", placeholder="44.8247, -0.5539")
    maitre_ouvrage = st.text_input("Maître d'ouvrage / Client", placeholder="Ex: ICF Habitat")

with col_g2:
    st.subheader("📸 Visuel de couverture")
    photo_couverture = st.camera_input("Prendre la photo de façade du site")
    annee_mes = st.text_input("Année de mise en service", placeholder="Ex: 2014")
    type_inst = st.selectbox("Architecture du système", ["CESC", "Auto-vidangeable", "Sous-pression", "Thermosiphon"])

st.divider()

# --- 4. BASE DE DONNÉES DES 73 POINTS ---
sections = {
    "📄 Documentation & Elec": ["Schéma d'exécution", "Schéma Electrique", "Analyse Fonctionnelle", "Raccordements", "Mise à la terre", "Signalétique de sécurité solaire", "Livret d'entretien présent"],
    "☀️ Capteurs & Toit": ["Absence vannes isolement", "Traversée de toiture", "Supports conformes", "Raccordement capteurs", "Accès sécurisé", "Absence de masque", "Étanchéité des supports (Abas)", "État isolants câbles sondes (UV)"],
    "🧪 Fluide Caloporteur": ["Prélèvement fluide", "pH du fluide (Contrôle acidité)", "Type et Fabricant du Glycol", "Protection Antigel (Réfractomètre)", "Analyse visuelle (Coloration/Texture)"],
    "💧 Hydraulique": ["Sens circulation", "Vannes remplissage", "Dégazeur Aller", "Soupape conforme", "Bidon récupération", "Circulateur Retour", "Clapet Retour", "V3V fonctionnelles", "Disconnecteur sur appoint"],
    "🎈 Expansion": ["Vase adapté", "Volume suffisant", "Isolement", "Raccordement Retour", "Pression conforme"],
    "📦 Stockage & Echangeur": ["Contre-courant", "Vannes échangeur", "Puissance échangeur", "Local hors gel", "Accès brides", "Raccordement ballons", "Vidange basse", "Protection cathodique", "Calorifuge", "Lyres anti-thermosiphon", "Soupape sécurité"],
    "🚿 Distribution ECS": ["Mitigeur présent", "Température points puisage", "Bouclage conforme", "Clapets anti-retour", "Bouclage calorifugé"],
    "📊 Métrologie & Régul": ["Manomètre", "Débitmètre", "Sonde ensoleillement", "Sonde capteur", "Sonde ballon", "Tests étanchéité", "Rinçage réseau", "Télécontrôleur", "Protection Surchauffe (Test 85°C)", "Écart de température (Delta T)"]
}

# --- 5. FORMULAIRE D'AUDIT ---
all_results = []
for sec, pts in sections.items():
    if sec == "🎈 Expansion" and type_inst == "Auto-vidangeable": continue
    with st.expander(f"{sec}", expanded=False):
        for p in pts:
            st.markdown(f"#### 🔹 {p}")
            col_form, col_cam = st.columns([1, 1])
            with col_form:
                res = st.radio("Statut", ["Conforme", "Non Conforme", "Non Contrôlable", "Sans objet"], key=f"s_{p}", horizontal=True)
                obs = st.text_area("Note technique", key=f"o_{p}", placeholder="Observations...", height=68)
            with col_cam:
                img = st.camera_input(f"Photo {p}", key=f"c_{p}")
            all_results.append({"Section": sec, "Point": p, "Statut": res, "Obs": obs})

# --- 6. MOTEUR PDF (PRO VERSION) ---
class OptheliosPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Rapport d'Audit Solaire - Opthelios - Page {self.page_no()}", 0, 0, "C")

def generate_pro_report(df, score, info_site):
    pdf = OptheliosPDF()
    
    # PAGE 1 : COUVERTURE (Style RHR Bordeaux)
    pdf.add_page()
    if os.path.exists("logo.png"):
        pdf.image("logo.png", 10, 10, 40)
    
    pdf.ln(50)
    pdf.set_font("Arial", "B", 26)
    pdf.set_text_color(0, 74, 153)
    pdf.cell(0, 15, info_site['nom'].upper(), ln=True, align="L")
    
    pdf.set_font("Arial", "", 18)
    pdf.set_text_color(100)
    pdf.cell(0, 10, info_site['adresse'].split(',')[1].strip() if ',' in info_site['adresse'] else "", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0)
    pdf.cell(0, 10, "RAPPORT D'AUDIT TECHNIQUE", ln=True)
    pdf.cell(0, 10, "Solaire Thermique", ln=True)
    
    # Photo de couverture si dispo
    if info_site['photo']:
        # Enregistrement temporaire de la photo pour le PDF
        with open("temp_cover.jpg", "wb") as f:
            f.write(info_site['photo'].getbuffer())
        pdf.image("temp_cover.jpg", x=10, y=130, w=190)
    
    pdf.set_y(230)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 7, f"Client : {info_site['client']}", ln=True)
    pdf.cell(0, 7, f"GPS : {info_site['gps']}", ln=True)
    pdf.cell(0, 7, f"Mise en service : {info_site['annee']}", ln=True)
    pdf.cell(0, 7, f"Date de l'audit : {datetime.now().strftime('%d/%m/%Y')}", ln=True)

    # PAGE 2 : SYNTHÈSE ET TABLEAU
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 15, "Synthèse des contrôles", ln=True)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Score de conformité global : {score:.1f}%", ln=True)
    pdf.ln(5)
    
    pdf.set_fill_color(255, 127, 0) # Orange Opthelios
    pdf.set_text_color(255)
    pdf.cell(90, 8, "Point de contrôle", 1, 0, 'L', True)
    pdf.cell(35, 8, "Statut", 1, 0, 'C', True)
    pdf.cell(65, 8, "Observations", 1, 1, 'L', True)
    
    pdf.set_text_color(0)
    pdf.set_font("Arial", "", 8)
    for _, row in df.iterrows():
        if row["Statut"] != "Sans objet":
            # Alerte rouge si non conforme
            if row["Statut"] == "Non Conforme": pdf.set_text_color(200, 0, 0)
            else: pdf.set_text_color(0)
            
            pdf.cell(90, 7, str(row["Point"])[:55], 1)
            pdf.cell(35, 7, row["Statut"], 1, 0, 'C')
            pdf.cell(65, 7, str(row["Obs"])[:45], 1, 1)

    # DERNIÈRE PAGE : CONTACTS
    pdf.add_page()
    pdf.set_y(100)
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 74, 153)
    pdf.cell(0, 10, "VOTRE CONTACT OPT'HELIOS", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0)
    pdf.cell(0, 7, "Moran GUILLERMIC", ln=True, align="C")
    pdf.cell(0, 7, "471 rue de Pratelmat, 56390 GRAND CHAMP", ln=True, align="C")
    pdf.cell(0, 7, "contact@opthelios.fr | 06.45.57.10.42", ln=True, align="C")
    pdf.cell(0, 7, "www.opthelios.com", ln=True, align="C")
    
    return pdf.output()

# --- 7. BOUTON FINAL ---
if st.button("🚀 GÉNÉRER LE RAPPORT FINAL"):
    df_res = pd.DataFrame(all_results)
    df_eval = df_res[df_res["Statut"].isin(["Conforme", "Non Conforme"])]
    score = (len(df_eval[df_eval["Statut"] == "Conforme"]) / len(df_eval)) * 100 if len(df_eval) > 0 else 0
    
    info_site = {
        'nom': nom_site, 'adresse': adresse_site, 'gps': gps_site,
        'client': maitre_ouvrage, 'annee': annee_mes, 'photo': photo_couverture
    }
    
    pdf_bytes = generate_pro_report(df_res, score, info_site)
    st.download_button("📥 Télécharger le Rapport Expert", data=bytes(pdf_bytes), file_name=f"Audit_Opthelios_{nom_site}.pdf")