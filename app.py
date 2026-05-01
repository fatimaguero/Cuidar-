import streamlit as st
import random

st.set_page_config(page_title="Cuidar+", layout="wide")

# ---------------- ESTILO ----------------
st.markdown("""
<style>
html { color-scheme: light; }

@media (prefers-color-scheme: dark) {
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #F4F9F6 !important;
        color: #111 !important;
    }
}

html, body, [data-testid="stAppViewContainer"] {
    font-family: sans-serif;
    background-color: #F4F9F6 !important;
    color: #111 !important;
}

p, span, label, h1, h2, h3, h4 {
    color: #111 !important;
}

#MainMenu, footer, header {visibility: hidden;}

.card {
    background: #fff;
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
</style>
""", unsafe_allow_html=True)

# ---------------- ESTADO ----------------
if "logado" not in st.session_state:
    st.session_state.logado = False

if "pedido" not in st.session_state:
    st.session_state.pedido = None

# ---------------- LANDING ----------------
if not st.session_state.logado:

    st.markdown("""
    <div style='text-align:center; padding:40px'>
        <h1 style='color:#27AE60;'>Cuidar+</h1>
        <p style='font-size:18px; color:#555;'>
        Cuidar de quem você ama é presença, segurança e amor ❤️
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.image("https://images.unsplash.com/photo-1511895426328-dc8714191300", use_container_width=True)

    st.markdown("### 💚 Por que usar o Cuidar+")

    st.markdown("""
    <div style='font-size:16px; color:#444;'>

    <b>👨‍👩‍👧‍👦 Cuidado contínuo com quem você ama</b><br>
    Acompanhe em tempo real a saúde e a rotina de familiares.

    <br><br>

    <b>❤️ Monitoramento inteligente</b><br>
    Batimentos, oxigenação, passos e sono.

    <br><br>

    <b>🚨 Segurança em qualquer momento</b><br>
    Alertas de emergência instantâneos.

    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 💳 Plano")
    st.success("R$ 19,90 / mês")

    tipo = st.radio("", ["Entrar", "Criar conta"], horizontal=True)

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if tipo == "Criar conta":
        nome = st.text_input("Nome")

    if st.button(tipo):

        if tipo == "Criar conta":
            if nome and email and senha:
                st.success("Conta criada!")
                st.session_state.logado = True
                st.rerun()
            else:
                st.warning("Preencha tudo")
        else:
            if email and senha:
                st.success("Login realizado!")
                st.session_state.logado = True
                st.rerun()
            else:
                st.warning("Preencha email e senha")

    st.stop()

# ---------------- HEADER ----------------
st.markdown("<h2 style='text-align:center; color:#27AE60;'>Cuidar+</h2>", unsafe_allow_html=True)

menu = st.selectbox("", ["Minha Família", "Monitorados", "Emergência", "Loja"])

# ---------------- BANCO ----------------
if "pessoas" not in st.session_state:
    st.session_state.pessoas = [
        {"nome": "Mãe", "local": "Casa", "batimentos": 72, "oxigenacao": 98, "passos": 3200, "sono": 7},
        {"nome": "Filho (TEA)", "local": "Escola", "batimentos": 90, "oxigenacao": 97, "passos": 5400, "sono": 8},
        {"nome": "Avô (Alzheimer)", "local": "Praça", "batimentos": 68, "oxigenacao": 96, "passos": 2100, "sono": 6}
    ]

# ---------------- ALERTA ----------------
def verificar(p):
    if p["batimentos"] > 100 or p["oxigenacao"] < 95:
        return "Alerta"
    return "Tudo bem"

# ---------------- MINHA FAMÍLIA ----------------
if menu == "Minha Família":

    st.subheader("📍 Monitoramento")

    for p in st.session_state.pessoas:
        status = verificar(p)
        classe = "status-ok" if status == "Tudo bem" else "status-alerta"

        st.markdown(f"""
        <div class='card'>
        <h3>{p['nome']}</h3>
        <p class='{classe}'>{status}</p>
        <p>📍 {p['local']}</p>
        <hr>
        ❤️ {p['batimentos']} bpm |
        🫁 {p['oxigenacao']}% |
        👣 {p['passos']} |
        😴 {p['sono']}h
        </div>
        """, unsafe_allow_html=True)

    if st.button("Atualizar dados"):
        for p in st.session_state.pessoas:
            p["batimentos"] = random.randint(60,110)
            p["oxigenacao"] = random.randint(94,100)
            p["passos"] += random.randint(50,200)
            p["sono"] = random.randint(5,9)

# ---------------- MONITORADOS ----------------
elif menu == "Monitorados":

    st.markdown("### 👨‍👩‍👧‍👦 Sua família")

    for p in st.session_state.pessoas:
        st.markdown(f"""
        <div class='card'>
        <h3>{p['nome']}</h3>
        <p>📍 {p['local']}</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------- EMERGÊNCIA ----------------
elif menu == "Emergência":

    pessoa = st.selectbox("Pessoa", [p["nome"] for p in st.session_state.pessoas])

    if st.button("🚨 SOS"):
        st.error(f"Alerta enviado para {pessoa}!")

# ---------------- LOJA ----------------
elif menu == "Loja":

    st.subheader("⌚ Relógio Cuidar+")
    st.image("relogio.jpg", width=250)

    st.success("R$ 279,90")

    nome = st.text_input("Nome")
    endereco = st.text_input("Endereço")

    if st.button("Comprar"):
        if nome and endereco:
            st.success("Pedido realizado!")
        else:
            st.warning("Preencha os dados")

    # ---------------- AVALIAÇÕES ----------------
    st.markdown("---")
    st.subheader("⭐ Avaliações de clientes")

    avaliacoes = [
        {"nome": "Maria S.", "nota": 5, "comentario": "Me sinto muito mais tranquila acompanhando meu pai."},
        {"nome": "Carlos R.", "nota": 4, "comentario": "Muito útil, só poderia ter bateria maior."},
        {"nome": "Ana L.", "nota": 5, "comentario": "Interface simples, perfeito para idosos."}
    ]

    for a in avaliacoes:
        st.markdown(f"**{a['nome']}** - {'⭐'*a['nota']}")
        st.write(a["comentario"])
        st.markdown("---")

    