import streamlit as st
import random
from datetime import datetime

st.set_page_config(page_title="Cuidar+", layout="wide")

# ---------------- ESTILO FINAL ESTÁVEL ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

/* BASE */
:root {
    color-scheme: light !important;
}

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Poppins', sans-serif;
    background-color: #F4F9F6 !important;
    color: #111 !important;
}

/* 🔥 NÃO USAR "*" GLOBAL (isso quebrava o selectbox) */

/* texto geral seguro */
p, span, label, h1, h2, h3, h4 {
    color: #111 !important;
}

/* STREAMLIT UI */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.block-container {
    padding: 1rem !important;
}

/* ---------------- CARD ---------------- */
.card {
    background: #ffffff !important;
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.06);
    margin-bottom: 15px;
    color: #111 !important;
}

.card * {
    color: #111 !important;
}

/* STATUS */
.status-ok {
    color: #2ECC71 !important;
    font-weight: bold;
}

.status-alerta {
    color: #E74C3C !important;
    font-weight: bold;
}

/* BOTÃO */
.stButton>button {
    background: linear-gradient(90deg, #2ECC71, #27AE60);
    color: white !important;
    border-radius: 20px;
    border: none;
    padding: 10px 20px;
}

/* ---------------- SELECTBOX (CORREÇÃO REAL) ---------------- */
div[data-baseweb="select"] {
    background-color: #fff !important;
    border-radius: 10px;
}

/* texto dentro do select */
div[data-baseweb="select"] * {
    color: #111 !important;
}

/* dropdown aberto (LISTA) */
ul[role="listbox"] {
    background: white !important;
    color: #111 !important;
}

li {
    color: #111 !important;
}

/* ---------------- RELÓGIO (CORRIGIDO VISUAL) ---------------- */
.watch {
    width: 220px;
    height: 260px;
    background: #111;
    border-radius: 30px;
    padding: 12px;
    margin: 0 auto;
}

.watch-screen {
    background: #000;
    border-radius: 20px;
    height: 100%;
    text-align: center;
    padding-top: 20px;
    color: #fff !important;
}

.watch-screen * {
    color: #fff !important;
}

.watch-time { font-size: 26px; }
.watch-status { font-size: 14px; margin:10px 0; }

.sos-btn {
    background:#E74C3C;
    color:#fff !important;
    border-radius:50%;
    width:80px;
    height:80px;
    line-height:80px;
    margin:10px auto;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<h2 style='text-align:center; color:#27AE60;'>Cuidar+</h2>
<p style='text-align:center; color:#666;'>Monitoramento inteligente para quem você ama ❤️</p>
""", unsafe_allow_html=True)

menu = st.selectbox("", ["Dashboard", "Monitorados", "Emergência", "Histórico"])

# ---------------- BANCO ----------------
if "pessoas" not in st.session_state:
    st.session_state.pessoas = [
        {"nome": "Mãe", "status": "Tudo bem", "local": "Casa",
         "batimentos": 72, "oxigenacao": 98, "passos": 3200, "calorias": 150, "sono": 7},

        {"nome": "Filho (TEA)", "status": "Em movimento", "local": "Escola",
         "batimentos": 90, "oxigenacao": 97, "passos": 5400, "calorias": 220, "sono": 8},

        {"nome": "Avô (Alzheimer)", "status": "Tudo bem", "local": "Praça",
         "batimentos": 68, "oxigenacao": 96, "passos": 2100, "calorias": 120, "sono": 6}
    ]

if "historico" not in st.session_state:
    st.session_state.historico = []

# ---------------- DASHBOARD ----------------
if menu == "Dashboard":

    st.subheader("📍 Monitoramento em tempo real")

    col1, col2 = st.columns([2,1])

    with col1:
        for p in st.session_state.pessoas:

            status_class = "status-ok" if p["status"] == "Tudo bem" else "status-alerta"

            st.markdown(f"""
            <div class='card'>
                <h3>{p['nome']}</h3>
                <p>Status: <span class='{status_class}'>{p['status']}</span></p>
                <p>📍 {p['local']}</p>
                <hr>
                ❤️ {p['batimentos']} bpm |
                🫁 {p['oxigenacao']}% |
                👣 {p['passos']} |
                🔥 {p['calorias']} kcal |
                😴 {p['sono']}h
            </div>
            """, unsafe_allow_html=True)

        if st.button("🔄 Atualizar dados"):
            for p in st.session_state.pessoas:
                p["status"] = random.choice(["Tudo bem", "Em movimento", "Alerta"])
                p["local"] = random.choice(["Casa", "Rua", "Praça", "Escola"])
                p["batimentos"] = random.randint(60, 110)
                p["oxigenacao"] = random.randint(94, 100)
                p["passos"] += random.randint(50, 200)
                p["calorias"] += random.randint(10, 30)
                p["sono"] = random.randint(5, 9)

    with col2:

        pessoa = st.selectbox("⌚ Dispositivo", [p["nome"] for p in st.session_state.pessoas])
        dados = next(p for p in st.session_state.pessoas if p["nome"] == pessoa)

        st.markdown(f"""
        <div class="watch">
            <div class="watch-screen">
                <div class="watch-time">🕒 {datetime.now().strftime("%H:%M")}</div>
                <div class="watch-status">❤️ {dados['batimentos']} bpm</div>
                <div class="watch-status">🫁 {dados['oxigenacao']}%</div>
                <div class="watch-status">👣 {dados['passos']}</div>
                <div class="sos-btn">SOS</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚨 Simular SOS"):
            st.session_state.historico.append({
                "pessoa": pessoa,
                "hora": datetime.now().strftime("%H:%M"),
                "tipo": "SOS relógio"
            })
            st.error("🚨 Alerta enviado!")

# ---------------- MONITORADOS ----------------
elif menu == "Monitorados":

    st.subheader("👤 Pessoas monitoradas")

    for p in st.session_state.pessoas:
        st.markdown(f"""
        <div class='card'>
            <h3>{p['nome']}</h3>
            <p>📍 {p['local']}</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------- EMERGÊNCIA ----------------
elif menu == "Emergência":

    st.subheader("🚨 Emergência")

    pessoa = st.selectbox("Quem precisa de ajuda?", [p["nome"] for p in st.session_state.pessoas])

    if st.button("ENVIAR ALERTA"):
        st.session_state.historico.append({
            "pessoa": pessoa,
            "hora": datetime.now().strftime("%H:%M"),
            "tipo": "SOS manual"
        })
        st.error("Alerta enviado!")

# ---------------- HISTÓRICO ----------------
elif menu == "Histórico":

    st.subheader("📊 Histórico")

    for h in st.session_state.historico[::-1]:
        st.markdown(f"""
        <div class='card'>
            <p><strong>{h['pessoa']}</strong></p>
            <p>{h['tipo']}</p>
            <p>{h['hora']}</p>
        </div>
        """, unsafe_allow_html=True)