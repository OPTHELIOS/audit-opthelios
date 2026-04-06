import streamlit as st
import pandas as pd
from datetime import datetime
import os
from fpdf import FPDF

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Opthelios Expert Solaire", layout="wide", page_icon="☀️")

# --- 2. THEME & STYLE ---
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png")
st.sidebar.header("🎨 Personnalisation")
theme = st.sidebar.radio("Thème d'affichage", ["☀️ Clair", "🌙 Sombre"], horizontal=True)

# Définition des couleurs selon le thème
if theme == "🌙 Sombre":
    bg, card, txt, brd = "#121212", "#1E1E1E", "#FFFFFF", "#444444"
else:
    bg, card, txt, brd = "#F4F7F9", "#FFFFFF", "#004a99", "#D0D0D0"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {txt}; }}
    [data-testid="stExpander"] {{ background-color: {card} !important; border: 1px solid {brd} !important; border-radius: 12px !important; margin-bottom: 15px; }}
    .stButton>button {{ background-color: #ff7f00 !important; color: white !important; font-weight: bold; width: 100%; border-radius: 10px; height: 3.5em; }}
    .stProgress > div > div > div > div {{ background-color: #ff7f00 !important; }}
    .color-box {{ padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; font-size: 0.85em; color: white; margin: 2px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. INFOS SITE & COUVERTURE ---
st.title("🚀 Audit Technique Opthelios")

col_site1, col_site2 = st.columns(2)
with col_site1:
    st.subheader("📌 Identification de l'Audit")
    nom_site = st.text_input("Nom de l'opération (Site)", placeholder="Ex: Résidence Hôtelière du Rail")
    adresse_site = st.text_area("Adresse complète", placeholder="Ex: 25 allée Eugène Delacroix, 33800 Bordeaux")
    gps_site = st.text_input("📍 Coordonnées GPS (Latitude, Longitude)", placeholder="44.8247, -0.5539")
    maitre_ouvrage = st.text_input("Maître d'ouvrage / Client", placeholder="Ex: ICF Habitat")

with col_site2:
    st.subheader("📸 Visuel Rapport")
    photo_couverture = st.camera_input("Prendre la photo de façade (Page de garde)")
    annee_mes = st.text_input("Année de mise en service", placeholder="Ex: 2014")
    type_arch = st.selectbox("Architecture du système", ["CESC (Collectif)", "Auto-vidangeable", "Sous-pression", "Thermosiphon"])

# --- 4. FICHE D'IDENTITÉ TECHNIQUE ---
with st.expander("📝 FICHE D'IDENTITÉ DE L'INSTALLATION (Matériel)", expanded=True):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**☀️ Champ Solaire**")
        marque_capteur = st.text_input("Marque des capteurs", key="m_cap")
        ref_capteur = st.text_input("Type et Référence capteurs", key="r_cap")
        st.markdown("**📊 Régulation & Automatisme**")
        marque_regulo = st.text_input("Marque et type du régulateur", key="m_reg")
        st.markdown("**🔥 Système d'Appoint**")
        type_appoint = st.selectbox("Source d'énergie appoint", ["Électrique", "Gaz", "Fioul", "Bois", "PAC", "Réseau de chaleur", "Autres"])
        ref_appoint = st.text_input("Marque et référence de l'appoint (Chaudière/Thermoplongeur)")
    with c2:
        st.markdown("**📦 Stockage Solaire**")
        marque_ballon = st.text_input("Marque du/des ballons")
        type_ballon = st.radio("Nature du stockage", ["Sanitaire (ECS)", "Eau technique (Eau morte)"], horizontal=True)
        type_echangeur = st.radio("Mode d'échange", ["Interne (Serpentin)", "Externe (Plaques)"], horizontal=True)
        anode = st.selectbox("Protection contre la corrosion", ["Anode Magnésium", "Anode ACI (Courant imposé)", "Sans objet (Inox/Plastique)", "Inconnu / Non vérifiable"])

# --- 5. POINTS DE CONTRÔLE (73 POINTS) ---
sections = {
    "📄 Documentation & Elec": ["Schéma d'exécution", "Schéma Electrique", "Analyse Fonctionnelle", "Raccordements électriques", "Mise à la terre", "Signalétique de sécurité solaire", "Livret d'entretien présent"],
    "☀️ Capteurs & Toiture": ["Absence vannes isolement", "Traversée de toiture adaptée", "Supports conformes", "Raccordement capteurs", "Accès sécurisé", "Absence de masque proche", "Étanchéité des supports (Abas)", "État isolants câbles sondes (UV)"],
    "🧪 Fluide Caloporteur": ["Prélèvement fluide", "pH du fluide (Contrôle acidité)", "Type et Fabricant du Glycol", "Protection Antigel (Mesure Réfractomètre)", "Analyse visuelle (Coloration et Texture)"],
    "💧 Hydraulique Solaire": ["Sens circulation capteurs/échangeur", "Vannes remplissage/vidange", "Dégazeur sur ALLER", "Soupape conforme", "Bidon récupération fluide", "Circulateur sur RETOUR", "Clapet anti-retour RETOUR", "Vannes 3 voies (V3V)", "Disconnecteur sur appoint"],
    "🎈 Expansion": ["Vase d'expansion adapté", "Volume suffisant", "Dispositif isolement", "Raccordement sur RETOUR", "Pression conforme"],
    "📦 Stockage & Echangeur": ["Echangeur en contre-courant", "Vannes isolement échangeur", "Puissance échangeur conforme", "Ballons hors gel", "Accès brides/piquages", "Raccordement ballons", "Vannes de vidange basse", "Protection cathodique (Test)", "Calorifuge stockage", "Lyres anti-thermosiphon", "Soupape sécurité ballon"],
    "🚿 Distribution ECS": ["Mitigeur thermostatique", "T° aux points de puisage", "Bouclage conforme", "Clapets anti-retour", "Bouclage calorifugé"],
    "📊 Métrologie & Tests": ["Manomètre fonctionnel", "Débitmètre(s)", "Sonde ensoleillement", "Sonde capteur", "Sonde ballon", "Tests étanchéité réseau", "Rinçage réseau effectué", "Télécontrôleur/GTC", "Protection Surchauffe (Test 85°C)", "Écart de température (Delta T)"]
}

st.subheader("🔍 Audit Terrain")
all_results = []
total_pts = sum(len(pts) for pts in sections.values())

for sec, pts in sections.items():
    if sec == "🎈 Expansion" and type_arch == "Auto-vidangeable":
        total_pts -= len(pts)
        continue
        
    with st.expander(f"{sec}", expanded=False):
        for p in pts:
            st.markdown(f"#### 🔹 {p}")
            
            # --- AIDES VISUELLES PH & GLYCOL ---
            if "pH du fluide" in p:
                c1, c2, c3, c4 = st.columns(4)
                c1.markdown('<div class="color-box" style="background-color: #e74c3c;">Acidité < 7<br>Remplacer</div>', unsafe_allow_html=True)
                c2.markdown('<div class="color-box" style="background-color: #f1c40f;">Neutre 7-8<br>Surveiller</div>', unsafe_allow_html=True)
                c3.markdown('<div class="color-box" style="background-color: #2ecc71;">Idéal 8-10<br>OK</div>', unsafe_allow_html=True)
                c4.markdown('<div class="color-box" style="background-color: #3498db;">Basique > 10<br>OK</div>', unsafe_allow_html=True)
            
            if "Analyse visuelle" in p:
                c1, c2, c3 = st.columns(3)
                c1.markdown('<div class="color-box" style="background-color: #ff9ff3; color:black;">Rose/Bleu Limpide<br>Neuf</div>', unsafe_allow_html=True)
                c2.markdown('<div class="color-box" style="background-color: #f39c12;">Jaune/Orange<br>Usagé</div>', unsafe_allow_html=True)
                c3.markdown('<div class="color-box" style="background-color: #2c3e50;">Brun/Noir<br>Caramélisé</div>', unsafe_allow_html=True)

            col_form, col_cam = st.columns([1, 1])
            with col_form:
                res = st.radio("Verdict", ["Conforme", "Non Conforme", "Non Contrôlable", "Sans objet"], key=f"s_{p}", horizontal=True)
                obs = st.text_area("Observations", key=f"o_{p}", placeholder="Ex: Mesure au réfractomètre : -28°C", height=68)
            with col_cam:
                st.camera_input(f"Photo de preuve ({p})", key=f"c_{p}")
            
            all_results.append({"Section": sec, "Point": p, "Statut": res, "Obs": obs})
            st.divider()

# --- 6. BARRE DE PROGRESSION ---
completed = len([k for k in st.session_state if k.startswith("s_") and st.session_state[k] != "Sans objet"])
percent = min(100, int((completed / total_pts) * 100))
st.sidebar.markdown(f"### 📈 Progression : {percent}%")
st.sidebar.progress(percent)

# --- 7. MOTEUR PDF ---
class OptheliosPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Rapport Audit Solaire - Opthelios - Page {self.page_no()}", 0, 0, "C")

def generate_full_pdf(df, score, site_info, mat_info):
    pdf = OptheliosPDF()
    
    # PAGE 1 : COUVERTURE
    pdf.add_page()
    if os.path.exists("logo.png"): pdf.image("logo.png", 10, 10, 45)
    pdf.ln(55)
    pdf.set_font("Arial", "B", 28); pdf.set_text_color(0, 74, 153)
    pdf.cell(0, 15, site_info['nom'].upper(), ln=True)
    pdf.set_font("Arial", "", 18); pdf.set_text_color(100)
    pdf.cell(0, 10, site_info['adresse'], ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", "B", 16); pdf.set_text_color(0)
    pdf.cell(0, 10, "RAPPORT D'AUDIT TECHNIQUE SOLAIRE", ln=True)
    
    if site_info['photo']:
        with open("temp_cover.jpg", "wb") as f: f.write(site_info['photo'].getbuffer())
        pdf.image("temp_cover.jpg", x=10, y=125, w=190)
    
    pdf.set_y(235); pdf.set_font("Arial", "", 11)
    pdf.cell(0, 6, f"Maître d'ouvrage : {site_info['client']}", ln=True)
    pdf.cell(0, 6, f"Coordonnées GPS : {site_info['gps']}", ln=True)
    pdf.cell(0, 6, f"Année de mise en service : {site_info['annee']}", ln=True)
    pdf.cell(0, 6, f"Date de visite : {datetime.now().strftime('%d/%m/%Y')}", ln=True)

    # PAGE 2 : FICHE D'IDENTITÉ & SYNTHÈSE
    pdf.add_page()
    pdf.set_font("Arial", "B", 16); pdf.set_text_color(0, 74, 153)
    pdf.cell(0, 12, "1. FICHE D'IDENTITÉ DE L'INSTALLATION", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 9); pdf.set_fill_color(240, 240, 240); pdf.set_text_color(0)
    
    fiche = [
        ("Architecture", site_info['arch']),
        ("Capteurs", f"{mat_info['m_cap']} / {mat_info['r_cap']}"),
        ("Ballon Solaire", f"{mat_info['m_ballon']} - {mat_info['t_ballon']}"),
        ("Echangeur", mat_info['t_ech']),
        ("Protection Cuve", mat_info['anode']),
        ("Régulation", mat_info['m_reg']),
        ("Appoint", f"{mat_info['t_app']} ({mat_info['r_app']})")
    ]
    for label, val in fiche:
        pdf.cell(55, 8, label, 1, 0, 'L', True); pdf.cell(135, 8, str(val), 1, 1, 'L')
    
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"SCORE DE CONFORMITÉ GLOBAL : {score:.1f}%", ln=True)
    
    # PAGE 3+ : TABLEAU DES POINTS
    pdf.ln(5)
    pdf.set_fill_color(255, 127, 0); pdf.set_text_color(255); pdf.set_font("Arial", "B", 9)
    pdf.cell(95, 8, "Point de contrôle", 1, 0, 'L', True)
    pdf.cell(30, 8, "Statut", 1, 0, 'C', True)
    pdf.cell(65, 8, "Observations", 1, 1, 'L', True)
    
    pdf.set_text_color(0); pdf.set_font("Arial", "", 8)
    for _, row in df.iterrows():
        if row["Statut"] != "Sans objet":
            if row["Statut"] == "Non Conforme": pdf.set_text_color(200, 0, 0)
            else: pdf.set_text_color(0)
            pdf.cell(95, 7, str(row["Point"])[:60], 1)
            pdf.cell(30, 7, row["Statut"], 1, 0, 'C')
            pdf.cell(65, 7, str(row["Obs"])[:45], 1, 1)

    # PAGE FINALE : CONTACTS
    pdf.add_page(); pdf.set_y(100); pdf.set_font("Arial", "B", 14); pdf.set_text_color(0, 74, 153)
    pdf.cell(0, 10, "VOTRE EXPERT EN ÉNERGIE SOLAIRE", ln=True, align="C")
    pdf.ln(5); pdf.set_font("Arial", "", 12); pdf.set_text_color(0)
    pdf.cell(0, 7, "Moran GUILLERMIC", ln=True, align="C")
    pdf.cell(0, 7, "471 rue de Pratelmat, 56390 GRAND CHAMP", ln=True, align="C")
    pdf.cell(0, 7, "contact@opthelios.fr | 06.45.57.10.42", ln=True, align="C")
    pdf.cell(0, 7, "www.opthelios.com", ln=True, align="C")
    
    return pdf.output()

# --- 8. VALIDATION ET BOUTON ---
st.divider()
confirmation = st.checkbox("Je certifie l'exactitude technique des relevés effectués sur site.")

if st.button("🚀 GÉNÉRER LE RAPPORT D'EXPERTISE COMPLET"):
    if not confirmation:
        st.warning("Veuillez cocher la case de certification.")
    elif not nom_site:
        st.error("Veuillez renseigner au moins le nom de l'opération.")
    else:
        df_res = pd.DataFrame(all_results)
        df_eval = df_res[df_res["Statut"].isin(["Conforme", "Non Conforme"])]
        score = (len(df_eval[df_eval["Statut"] == "Conforme"]) / len(df_eval)) * 100 if len(df_eval) > 0 else 0
        
        site_info = {
            'nom': nom_site, 'adresse': adresse_site, 'gps': gps_site,
            'client': maitre_ouvrage, 'annee': annee_mes, 'photo': photo_couverture, 'arch': type_arch
        }
        mat_info = {
            'm_cap': marque_capteur, 'r_cap': ref_capteur, 'm_reg': marque_regulo,
            't_app': type_appoint, 'r_app': ref_appoint, 'm_ballon': marque_ballon,
            't_ballon': type_ballon, 't_ech': type_echangeur, 'anode': anode
        }
        
        pdf_bytes = generate_full_pdf(df_res, score, site_info, mat_info)
        st.balloons()
        st.download_button(
            label="📥 Télécharger le Rapport Expert (PDF)", 
            data=bytes(pdf_bytes), 
            file_name=f"Expertise_Opthelios_{nom_site.replace(' ', '_')}.pdf", 
            mime="application/pdf"
        )