import streamlit as st
import matplotlib.pyplot as plt

# =====================================================
# TÍTULO
# =====================================================

st.title("📊 Simulador CDT + FIC")
st.write("Simulación de crecimiento del capital con reinversión anual")

# =====================================================
# INPUTS
# =====================================================

capital_inicial = st.number_input(
    "Capital inicial",
    value=1_000_000,
    step=1_000_000
)

ahorro_mensual = st.number_input(
    "Ahorro mensual",
    value=1_500_000,
    step=100_000
)

tasa_cdt = st.number_input(
    "Tasa CDT EA (%)",
    value=13.0
) / 100

tasa_fic = st.number_input(
    "Tasa FIC EA (%)",
    value=8.0
) / 100

anios = st.slider(
    "Años de inversión",
    1,
    30,
    5
)

# =====================================================
# CONVERSIÓN FIC MENSUAL
# =====================================================

tasa_fic_mensual = (1 + tasa_fic) ** (1/12) - 1

# =====================================================
# FUNCIONES
# =====================================================

def calcular_cdt(capital, tasa):
    intereses = capital * tasa
    return intereses, capital + intereses


def calcular_fic(ahorro_mensual, tasa_mensual):
    saldo = 0
    for _ in range(12):
        saldo *= (1 + tasa_mensual)
        saldo += ahorro_mensual
    return saldo

# =====================================================
# SIMULACIÓN
# =====================================================

capital_actual = capital_inicial
historial = []

for anio in range(1, anios + 1):

    intereses_cdt, valor_cdt = calcular_cdt(capital_actual, tasa_cdt)
    valor_fic = calcular_fic(ahorro_mensual, tasa_fic_mensual)

    capital_final = valor_cdt + valor_fic

    historial.append({
        "Año": anio,
        "Capital Inicial": capital_actual,
        "Intereses CDT": intereses_cdt,
        "Valor CDT": valor_cdt,
        "Valor FIC": valor_fic,
        "Capital Final": capital_final
    })

    capital_actual = capital_final

# =====================================================
# RESUMEN FINAL
# =====================================================

st.subheader("💰 Capital final")

st.success(f"${historial[-1]['Capital Final']:,.0f}")

# =====================================================
# EVOLUCIÓN DETALLADA
# =====================================================

st.subheader("📈 Evolución del capital")

for d in historial:

    st.markdown(f"""
### AÑO {d['Año']}

Capital inicial: ${d['Capital Inicial']:,.0f}  
Intereses CDT:   ${d['Intereses CDT']:,.0f}  
Valor CDT final: ${d['Valor CDT']:,.0f}  
Valor FIC:       ${d['Valor FIC']:,.0f}  
Capital final:   ${d['Capital Final']:,.0f}  

---

""")

# =====================================================
# GRÁFICO
# =====================================================

anios = [d["Año"] for d in historial]
capitales = [d["Capital Final"] for d in historial]

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(anios, capitales, marker="o", linewidth=3, color="green")

# valores en el gráfico
for x, y in zip(anios, capitales):
    ax.text(x, y, f"${y:,.0f}", ha="center", va="bottom", fontsize=9)

ax.set_title("Crecimiento del capital")
ax.set_xlabel("Años")
ax.set_ylabel("Capital")
ax.grid(True)

st.pyplot(fig)
