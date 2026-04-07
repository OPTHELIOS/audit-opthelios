import streamlit as st
import os

# --- 1. CONFIGURATION & STATE ---
st.set_page_config(page_title="Opthelios Expert v3", layout="wide", page_icon="☀️")

if 'extra_counters' not in st.session_state:
    st.session_state.extra_counters = []

# --- 2. GESTION DU THÈME ---
with st.sidebar:
    st.header("🎨 Interface")
    theme = st.radio("Mode", ["☀️ Clair", "🌙 Sombre"], horizontal=True)
    sidebar_bg = "#001f3f" if theme == "☀️ Clair" else "#000000"
    st.markdown(f"<style>[data-testid='stSidebar'] {{ background-color: {sidebar_bg} !important; }}</style>", unsafe_allow_html=True)

# --- 3. CSS & STYLES ---
st.markdown(f"""
    <style>
    .counter-block {{ border-left: 5px solid #ff7f00; padding: 15px; margin: 15px 0; border: 1px solid #ddd; border-radius: 8px; }}
    .stButton>button {{ background-color: #ff7f00 !important; color: white !important; font-weight: bold; border-radius: 8px; }}
    .ballon-card {{ background-color: rgba(255, 127, 0, 0.05); padding: 15px; border-radius: 10px; border: 1px dashed #ff7f00; margin-bottom: 10px; }}
    .section-header {{ color: #ff7f00; font-size: 1.2em; font-weight: bold; margin-top: 20px; border-bottom: 2px solid #ff7f00; padding-bottom: 5px; }}
    /* Suppression visuelle des labels de selectbox pour épurer */
    div[data-testid="stSelectbox"] label {{ display: none; }}
    div[data-testid="stTextInput"] label {{ display: none; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. EN-TÊTE ---
st.title("☀️ Diagnostic Expert Opthelios")
col_info1, col_info2 = st.columns([2, 1])
with col_info1:
    nom_site = st.text_input("📍 Nom de l'opération", placeholder="Nom du site...")
    adr_site = st.text_input("🏠 Adresse & GPS", placeholder="Coordonnées...")
    client_site = st.text_input("👤 Client / MOA", placeholder="Client...")
with col_info2:
    photo_main = st.camera_input("📸 Photo de garde", key="main_pic")

# --- 5. FICHE D'IDENTITÉ MATÉRIEL ---
st.divider()
st.header("📋 Fiche d'Identité Matériel")

with st.expander("🛠️ Caractéristiques & Stockage", expanded=True):
    # --- PARTIE PRODUCTION ---
    st.markdown('<p class="section-header">☀️ Production Solaire</p>', unsafe_allow_html=True)
    c_p1, c_p2 = st.columns(2)
    with c_p1:
        st.markdown("**Modèle**")
        st.text_input("Marque/Réf Capteurs", key="m_cap")
        st.markdown("**Quantité**")
        nb_capteurs = st.number_input("Nombre total de capteurs", min_value=1, value=1)
        st.markdown("**Orientation**")
        st.selectbox("Orientation", ["Sud", "Sud-Est", "Sud-Ouest", "Est", "Ouest"], key="orient")
    with c_p2:
        st.markdown("**Configuration**")
        nb_rangees = st.number_input("Nombre de rangées (champs)", min_value=1, value=1)
        st.markdown("**Inclinaison (°)**")
        st.number_input("Inclinaison", value=45, key="inclin")
        st.markdown("**Circulateur**")
        st.text_input("Marque/Réf Circulateur", key="m_circ")

    # --- PARTIE STOCKAGE ---
    st.markdown('<p class="section-header">📦 Stockage Solaire</p>', unsafe_allow_html=True)
    nb_ballons = st.number_input("Nombre de ballons solaires", min_value=1, value=1, step=1)
    
    if nb_ballons >= 2:
        st.selectbox("Raccordement hydraulique des ballons", ["En série", "En parallèle"], key="raccord_hydra")

    for i in range(int(nb_ballons)):
        st.markdown(f'<div class="ballon-card"><b>Ballon n°{i+1}</b>', unsafe_allow_html=True)
        cb1, cb2, cb3 = st.columns([2, 1, 1])
        with cb1: st.text_input(f"Marque/Réf", key=f"m_bal_{i}", placeholder="Marque...")
        with cb2: 
            st.text_input(f"Volume (L)", key=f"v_bal_{i}", placeholder="Volume...")
            st.selectbox(f"Type", ["Sanitaire", "Eau technique"], key=f"t_bal_{i}")
        with cb3: 
            st.number_input(f"Nb Échangeurs", 0, 3, 1, key=f"e_bal_{i}")
            st.selectbox(f"État", ["Correct", "Non conforme", "HS"], key=f"et_bal_{i}")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- PARTIE DISTRIBUTION ---
    st.markdown('<p class="section-header">🚿 Distribution Sanitaire</p>', unsafe_allow_html=True)
    cd1, cd2, cd3 = st.columns([1.5, 1, 1.5])
    with cd1:
        st.selectbox("Type", ["Bouclage sanitaire", "Traceur électrique", "Non présent"], key="dist_type")
        st.radio("Conformité", ["Conforme", "Non conforme"], horizontal=True, key="dist_conf")
    with cd2: st.camera_input("Photo", key="dist_photo")
    with cd3: st.text_area("Observations", key="dist_obs", placeholder="État calorifuge, pompe...")

# --- 6. AUDIT TECHNIQUE ---
st.divider()
st.header("🔍 Audit Technique")

# Construction dynamique des points selon la configuration
pts_toit = [
    "Intégrité des vitrages", "État de l'absorbeur", "Fixation châssis", "Étanchéité toiture", 
    "Sondes capteurs : Position & Fixation", "Traversée de toiture", "Isolants UV (état)"
]

# Ajout automatique de l'équilibrage si plusieurs rangées
if nb_rangees > 1:
    pts_toit.insert(4, "Équilibrage hydraulique des champs (TacoSetter / Vannes)")
    pts_toit.insert(5, "Uniformité des températures de retour par rangée")

sections = {
    "📄 Documentation & Élec": ["Schéma d'exécution", "Schéma Electrique", "Analyse Fonctionnelle", "Mise à la terre", "Signalétique"],
    "☀️ Capteurs & Toiture": pts_toit,
    "🧪 Fluide Caloporteur": ["pH du fluide", "Protection Antigel (°C)", "Analyse visuelle"],
    "💧 Circuit primaire": [
        "Sens de circulation", "Vannes remplissage", "Dégazeur Aller", "Soupape conforme", 
        "Vase : Pression gonflage", "Vase : Pression statique", "Vase : État membrane", "Disconnecteur"
    ],
    "📊 Régulation & Métrologie": [
        "Manomètre", "Débitmètre", "Sonde T1 (Cohérence)", "Sonde T2 (Cohérence)", 
        "Consigne Max (°C)", "Décharge thermique", "COMPTEURS"
    ]
}

def display_counter_block(label, type_c, key_id):
    st.markdown(f"**{label}**")
    with st.container():
        st.markdown('<div class="counter-block">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1.5, 1])
        with c1:
            st.radio("Présent ?", ["Oui", "Non"], key=f"pres_{key_id}", horizontal=True)
            st.radio("Conforme ?", ["Oui", "Non"], key=f"conf_{key_id}", horizontal=True)
        with c2:
            if type_c in ["ESU", "Calorimètre", "Électrique"]:
                st.text_input("Index (kWh/MWh)", key=f"idx_{key_id}")
            if type_c in ["ESU", "Calorimètre", "Volumétrique", "Vecs"]:
                st.text_input("Volume (m3)", key=f"vol_{key_id}")
            st.checkbox("Sondes en doigts de gant ?", key=f"dg_{key_id}")
        with c3: st.camera_input("📷", key=f"cam_{key_id}")
        st.markdown('</div>', unsafe_allow_html=True)

for sec, pts in sections.items():
    with st.expander(f"📁 {sec}"):
        for p in pts:
            if p == "COMPTEURS":
                display_counter_block("Compteur ESU", "ESU", "f_esu")
                display_counter_block("Compteur ECS (Vecs)", "Vecs", "f_vecs")
                st.markdown("#### ➕ Autre compteur")
                ca1, ca2 = st.columns(2)
                n_n = ca1.text_input("Nom", key="n_n", placeholder="Ex: Appoint...")
                n_t = ca2.selectbox("Type", ["Calorimètre", "Volumétrique", "Électrique"], key="n_t")
                if st.button("Ajouter"):
                    if n_n:
                        st.session_state.extra_counters.append({"name": n_n, "type": n_t})
                        st.rerun()
                for i, c in enumerate(st.session_state.extra_counters):
                    display_counter_block(c['name'], c['type'], f"extra_{i}")
            else:
                st.markdown(f"**{p}**")
                c1, c2, c3 = st.columns([1.5, 3, 1])
                with c1:
                    # Choix automatique du set de réponse selon le point
                    opts = ["Conforme", "Non Conforme", "N/C", "S/O"]
                    if "Sonde" in p or "Cohérence" in p: opts = ["Oui", "Non", "N/C"]
                    elif "membrane" in p: opts = ["OK", "HS", "À vérifier"]
                    st.selectbox(f"Statut {p}", opts, key=f"s_{p}")
                with c2: st.text_input(f"Obs {p}", key=f"o_{p}", placeholder="Observations / Mesures...")
                with c3: st.camera_input(f"Photo {p}", key=f"c_{p}")

# --- 7. GÉNÉRATION ---
st.divider()
if st.button("🚀 GÉNÉRER LE RAPPORT FINAL"):
    if not nom_site: st.error("Nom du site manquant.")
    else:
        st.balloons()
        st.success(f"Audit de {nom_site} validé.")