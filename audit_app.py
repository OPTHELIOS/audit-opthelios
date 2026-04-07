import streamlit as st
import pandas as pd
import os

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Opthelios Expert v3", layout="wide", page_icon="☀️")

# --- 2. GESTION DU THÈME & SIDEBAR ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png")
    st.header("🎨 Interface")
    theme = st.radio("Mode", ["☀️ Clair", "🌙 Sombre"], horizontal=True)
    
    sidebar_bg = "#001f3f" if theme == "☀️ Clair" else "#000000"
    st.markdown(f"""
        <style>
        [data-testid="stSidebar"] {{ background-color: {sidebar_bg} !important; color: white !important; }}
        [data-testid="stSidebar"] * {{ color: white !important; }}
        </style>
    """, unsafe_allow_html=True)

# --- 3. CSS ADAPTATIF ---
if theme == "🌙 Sombre":
    bg, card, txt, brd = "#0E1117", "#161B22", "#FFFFFF", "#30363D"
else:
    bg, card, txt, brd = "#F8F9FA", "#FFFFFF", "#1A1C1E", "#D0D5DD"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {txt}; }}
    [data-testid="stExpander"] {{ background-color: {card} !important; border: 1px solid {brd} !important; border-radius: 8px !important; }}
    h1, h2, h3, h4, label, p, span {{ color: {txt} !important; }}
    .stButton>button {{ background-color: #ff7f00 !important; color: white !important; font-weight: bold; border-radius: 8px; height: 3.5em; }}
    .counter-block {{ border-left: 4px solid #ff7f00; padding: 15px; margin: 10px 0; background-color: {bg}; border-radius: 5px; border: 1px solid {brd}; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. IDENTIFICATION DU SITE ---
st.title("☀️ Diagnostic Expert Opthelios")

col_top1, col_top2 = st.columns([2, 1])
with col_top1:
    nom_site = st.text_input("📍 Nom de l'opération", placeholder="Ex: Résidence du Rail")
    adr_site = st.text_input("🏠 Adresse & GPS", placeholder="Adresse / Coordonnées")
    client_site = st.text_input("👤 Client / MOA")
with col_top2:
    photo_main = st.camera_input("📸 Photo de garde", key="main_pic")

# --- 5. FICHE D'IDENTITÉ MATÉRIEL ---
st.divider()
st.header("📋 Fiche d'Identité Matériel")

def row_mat(label, key):
    c1, c2 = st.columns([3, 1])
    with c1: v = st.text_input(label, key=f"t_{key}")
    with c2: p = st.camera_input("📷", key=f"p_{key}")
    return v, p

with st.expander("🛠️ Caractéristiques Matérielles", expanded=True):
    c_m1, c_m2 = st.columns(2)
    with c_m1:
        st.markdown("**☀️ Production Solaire**")
        m_cap, p_cap = row_mat("Marque/Réf Capteurs", "cap")
        orient = st.selectbox("Orientation", ["Sud", "Sud-Est", "Sud-Ouest", "Est", "Ouest"])
        inclin = st.number_input("Inclinaison (°)", value=45)
        m_circ, p_circ = row_mat("Marque/Réf Circulateur", "circ")
    with c_m2:
        st.markdown("**📦 Stockage & Appoint**")
        m_bal, p_bal = row_mat("Marque/Réf Ballons", "bal")
        vol_bal = st.number_input("Volume total (L)", value=1000, step=100)
        m_reg, p_reg = row_mat("Marque/Réf Régulateur", "reg")
        m_app, p_app = row_mat("Marque/Réf Appoint", "app")

# --- 6. AUDIT TECHNIQUE ---
st.divider()
st.header("🔍 Audit Technique")

sections = {
    "📄 Documentation et conformité électrique": ["Schéma d'exécution", "Schéma Electrique", "Mise à la terre", "Signalétique"],
    "☀️ Capteurs & Toit": ["Intégrité vitrages", "Absorbeur", "Fixation châssis", "Étanchéité toiture", "Sondes capteurs"],
    "🧪 Fluide Caloporteur": ["pH du fluide", "Protection Antigel", "Analyse visuelle"],
    "💧 Circuit primaire solaire": ["Sens circulation", "Vannes remplissage", "Dégazeur", "Vase d'Expansion (bar)"],
    "📦 Stockage & Echangeur": ["Echangeur", "Protection cathodique", "Calorifugeage", "Soupape"],
    "📊 Régulation solaire et métrologie": [
        "Manomètre", "Débitmètre", "Sonde Capteur (T1)", "Sonde Ballon (T2)", 
        "Consigne température max", "Paramètres de décharge", 
        "Compteur énergie solaire utile (ESU)", "Compteur ECS (Vecs)"
    ]
}

all_results = []

for sec, pts in sections.items():
    with st.expander(f"📁 {sec}"):
        for p in pts:
            # --- CAS SPÉCIFIQUE COMPTEURS (ESU / ECS) ---
            if "Compteur" in p:
                st.markdown(f"**### 📊 {p}**")
                st.markdown('<div class="counter-block">', unsafe_allow_html=True)
                c1, c2, c3 = st.columns([1, 1, 1])
                with c1:
                    pres = st.radio(f"Présent ? ({p})", ["Oui", "Non"], key=f"pres_{p}", horizontal=True)
                    conf = st.radio(f"Conforme ? ({p})", ["Oui", "Non"], key=f"conf_{p}", horizontal=True)
                with c2:
                    if "ESU" in p:
                        idx = st.text_input("Index (kWh ou MWh)", key=f"idx_{p}")
                    vol = st.text_input("Volume (m3)", key=f"vol_{p}")
                with c3:
                    pic = st.camera_input(f"Photo {p}", key=f"cam_{p}")
                st.markdown('</div>', unsafe_allow_html=True)
                all_results.append({"Point": p, "Présent": pres, "Conforme": conf})
            
            # --- CAS GÉNÉRAL DES POINTS DE CONTRÔLE ---
            else:
                st.markdown(f"**{p}**")
                c_res, c_obs, c_cam = st.columns([1.5, 3, 1])
                
                # Logique des labels
                opt = ["Conforme", "Non Conforme", "N/C", "S/O"]
                lbl = "Verdict"
                if "Sonde" in p:
                    lbl, opt = "Cohérent", ["Oui", "Non", "N/C"]
                elif "décharge" in p:
                    lbl, opt = "Statut", ["Activé", "Désactivé", "S/O"]

                with c_res:
                    res = st.selectbox(lbl, opt, key=f"s_{p}")
                with c_obs:
                    obs = st.text_input("Note / Mesure", key=f"o_{p}")
                with c_cam:
                    cam = st.camera_input("📷", key=f"c_{p}")
                all_results.append({"Section": sec, "Point": p, "Statut": res, "Obs": obs})

# --- 7. GÉNÉRATION ---
st.divider()
if st.button("🚀 GÉNÉRER LE RAPPORT FINAL"):
    if not nom_site:
        st.error("Veuillez saisir le nom du site.")
    else:
        st.balloons()
        st.success(f"Audit de {nom_site} validé.")