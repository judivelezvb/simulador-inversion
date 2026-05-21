import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# =====================================================
# CONFIGURACIÓN INICIAL
# =====================================================

CAPITAL_INICIAL = 140_000_000
AHORRO_MENSUAL = 1_500_000

TASA_CDT_EA = 0.13
TASA_FIC_EA = 0.08

ANIOS = 5
MESES_POR_ANIO = 12

# =====================================================
# CONVERSIÓN DE TASAS
# =====================================================

tasa_fic_mensual = (1 + TASA_FIC_EA) ** (1 / 12) - 1

# =====================================================
# FUNCIONES
# =====================================================

def calcular_cdt(capital, tasa_ea):
    """
    Calcula el valor final del CDT después de 1 año
    """

    intereses = capital * tasa_ea
    valor_final = capital + intereses

    return intereses, valor_final


def calcular_fic(
    ahorro_mensual,
    tasa_mensual,
    meses=12
):
    """
    Simula el ahorro mensual en el FIC
    """

    saldo = 0

    for _ in range(meses):

        # generar intereses
        saldo *= (1 + tasa_mensual)

        # agregar ahorro mensual
        saldo += ahorro_mensual

    return saldo


def simular_inversion(
    capital_inicial,
    ahorro_mensual,
    tasa_cdt,
    tasa_fic_m,
    anios
):
    """
    Ejecuta la simulación completa
    """

    capital_actual = capital_inicial

    historial = []

    for anio in range(1, anios + 1):

        # =========================
        # CDT
        # =========================

        intereses_cdt, valor_cdt = calcular_cdt(
            capital_actual,
            tasa_cdt
        )

        # =========================
        # FIC
        # =========================

        valor_fic = calcular_fic(
            ahorro_mensual,
            tasa_fic_m
        )

        # =========================
        # TOTAL
        # =========================

        capital_final = valor_cdt + valor_fic

        historial.append({

            "Año": anio,

            "Capital Inicial":
            capital_actual,

            "Intereses CDT":
            intereses_cdt,

            "Valor CDT":
            valor_cdt,

            "Valor FIC":
            valor_fic,

            "Capital Final":
            capital_final
        })

        # reinversión total
        capital_actual = capital_final

    return historial


def mostrar_resultados(historial):

    print("\n" + "=" * 60)
    print("      EVOLUCIÓN DEL CAPITAL")
    print("=" * 60)

    for dato in historial:

        print(f"\nAÑO {dato['Año']}")

        print(
            f"Capital inicial: "
            f"${dato['Capital Inicial']:,.0f}"
        )

        print(
            f"Intereses CDT:   "
            f"${dato['Intereses CDT']:,.0f}"
        )

        print(
            f"Valor CDT final: "
            f"${dato['Valor CDT']:,.0f}"
        )

        print(
            f"Valor FIC:       "
            f"${dato['Valor FIC']:,.0f}"
        )

        print(
            f"Capital final:   "
            f"${dato['Capital Final']:,.0f}"
        )

        print("-" * 60)

    capital_final = historial[-1]["Capital Final"]

    print("\n" + "=" * 60)
    print(f"CAPITAL FINAL DESPUÉS DE {ANIOS} AÑOS")
    print("=" * 60)

    print(f"\n${capital_final:,.0f}")


def graficar_resultados(historial):

    anios = [d["Año"] for d in historial]

    capitales = [
        d["Capital Final"]
        for d in historial
    ]

    plt.figure(figsize=(12, 6))

    # Línea principal
    plt.plot(
        anios,
        capitales,
        marker="o",
        linewidth=3,
        color="darkgreen"
    )

    # Área sombreada
    plt.fill_between(
        anios,
        capitales,
        alpha=0.15,
        color="green"
    )

    # Etiquetas
    for x, y in zip(anios, capitales):

        plt.annotate(
            f"${y:,.0f}",

            (x, y),

            textcoords="offset points",

            xytext=(0, 12),

            ha="center",

            fontsize=10,

            bbox=dict(
                facecolor="white",
                alpha=0.85,
                edgecolor="gray",
                boxstyle="round,pad=0.4"
            )
        )

    plt.title(
        "Crecimiento del Capital (CDT + FIC)",
        fontsize=16
    )

    plt.xlabel(
        "Años",
        fontsize=13
    )

    plt.ylabel(
        "Capital acumulado ($)",
        fontsize=13
    )

    plt.grid(alpha=0.3)

    plt.tight_layout()

    plt.show()

# =====================================================
# EJECUCIÓN
# =====================================================

historial = simular_inversion(

    capital_inicial=CAPITAL_INICIAL,

    ahorro_mensual=AHORRO_MENSUAL,

    tasa_cdt=TASA_CDT_EA,

    tasa_fic_m=tasa_fic_mensual,

    anios=ANIOS
)

mostrar_resultados(historial)

graficar_resultados(historial)