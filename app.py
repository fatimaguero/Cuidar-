import streamlit as st
import random
from datetime import datetime
import time
import pandas as pd

st.set_page_config(page_title="Cuidar+", layout="wide")

# ---------------- ESTILO ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

html, body {
    font-family: 'Poppins', sans-serif;
    background-color: #F4F9F6;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.card {
    background: white;
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.06);
    margin-bottom: 15px;
}

.status-ok { color:#2ECC71; font-weight:bold; }
.status-alerta { color:#E74C3C; font-weight:bold; }

.stButton>button {
    background: linear-gradient(90deg, #2ECC71, #27AE60);
    color: white;
    border-radius: 20px;
    border: none;
    padding: 10px 20px;
}

/* relógio */
.watch {
    width: 220px;
    height: 260px;
    background: #111;
    border-radius: 30px;
    padding: 12px;
    margin: 0 auto;
}

.watch-screen {
    background: black;
    border-radius: 20px;
    height: 100%;
    color: white;
    text-align: center;
    padding-top: 20px;
}

.watch-time { font-size: 26px; }
.watch-status { font-size: 14px; margin:10px 0; }

.sos-btn {
    background:#E74C3C;
    color:white;
    border-radius:50%;
    width:80px;
    height:80px;
    line-height:80px;
    margin:10px auto;
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

if "batimentos_historico" not in st.session_state:
    st.session_state.batimentos_historico = []

# ---------------- DASHBOARD ----------------
if menu == "Dashboard":

    st.subheader("📍 Monitoramento em tempo real")

    col1, col2 = st.columns([2,1])

    # -------- LISTA --------
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

    # -------- RELÓGIO --------
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
            agora = datetime.now().strftime("%H:%M")
            st.session_state.historico.append({
                "pessoa": pessoa,
                "hora": agora,
                "tipo": "SOS relógio"
            })
            st.error(f"🚨 Alerta de {pessoa}!")

    # -------- GRÁFICO DO AVÔ --------
    st.markdown("### ❤️ Monitoramento cardíaco (Avô)")

    avo = next(p for p in st.session_state.pessoas if "Avô" in p["nome"])

    novo_valor = random.randint(60, 100)
    st.session_state.batimentos_historico.append(novo_valor)

    if len(st.session_state.batimentos_historico) > 20:
        st.session_state.batimentos_historico.pop(0)

    df = pd.DataFrame(st.session_state.batimentos_historico, columns=["bpm"])

    st.line_chart(df)

    # alerta automático
    if novo_valor > 100:
        st.error("⚠️ Batimentos elevados detectados!")
    elif novo_valor < 60:
        st.warning("⚠️ Batimentos baixos!")

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

    nome = st.text_input("Adicionar novo")

    if st.button("Adicionar"):
        if nome:
            st.session_state.pessoas.append({
                "nome": nome,
                "status": "Tudo bem",
                "local": "Desconhecido",
                "batimentos": 70,
                "oxigenacao": 98,
                "passos": 0,
                "calorias": 0,
                "sono": 7
            })
            st.success("Adicionado!")

# ---------------- EMERGÊNCIA ----------------
elif menu == "Emergência":

    st.subheader("🚨 Central de emergência")

    pessoa = st.selectbox("Quem precisa de ajuda?", [p["nome"] for p in st.session_state.pessoas])

    if st.button("🚨 ENVIAR ALERTA"):
        agora = datetime.now().strftime("%H:%M")

        st.session_state.historico.append({
            "pessoa": pessoa,
            "hora": agora,
            "tipo": "SOS manual"
        })

        st.error(f"🚨 Alerta enviado para {pessoa}!")

# ---------------- HISTÓRICO ----------------
elif menu == "Histórico":

    st.subheader("📊 Histórico")

    if st.session_state.historico:
        for h in st.session_state.historico[::-1]:
            st.markdown(f"""
            <div class='card'>
                <p><strong>{h['pessoa']}</strong></p>
                <p>{h['tipo']}</p>
                <p>{h['hora']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Nenhum evento ainda")