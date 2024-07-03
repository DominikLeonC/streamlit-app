import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Configuración de la página
st.set_page_config(
    page_title="Comparación de Costos: Camión Diésel vs. Camión Eléctrico",
    layout="centered"
)

# Datos fijos del camión eléctrico (actualizados)
electric_data = {
    "model": "Sany FE601",
    "cost_initial": 1350000 * 1.16,  # Incluyendo IVA
    "battery_capacity_kwh": 84.48,
    "consumption_percentage_per_km": 2.33 / 100,
    "maintenance_annual": 4000,
    "battery_replacement_cost": 10000,
    "battery_replacement_frequency_years": 5,
    "insurance_annual": 53000,  # Seguro anual para camión eléctrico
    "distance_per_charge_km": 200
}

# Opciones de camiones diésel (Incluyendo IVA)
diesel_trucks = {
    "Hino J05E-US": {"cost_initial": 1320000 * 1.16, "km_per_liter": 6.5, "maintenance_annual": 8000, "capacidad_combustible": 200},
    "JAC X350": {"cost_initial": 600000 * 1.16, "km_per_liter": 6, "maintenance_annual": 8000, "capacidad_combustible": 100},
    "VolksWagen Delivery 6.160": {"cost_initial": 560000 * 1.16, "km_per_liter": 4, "maintenance_annual": 8000, "capacidad_combustible": 150},
    "ISUZU ELF600": {"cost_initial": 1050000 * 1.16, "km_per_liter": 6.4, "maintenance_annual": 8000, "capacidad_combustible": 140}
}

# Función para calcular costos anuales del camión diésel seleccionado
def calculate_diesel_costs(selected_model, diesel_fuel_cost, annual_kilometers, num_trucks, verification_cost, insurance_cost, tax_cost, inflation_rate, fuel_increase_rate):
    costs = []
    for year in range(1, 6):
        adjusted_fuel_cost = diesel_fuel_cost + (fuel_increase_rate * (year - 1))
        fuel_cost = (1 / diesel_trucks[selected_model]["km_per_liter"]) * adjusted_fuel_cost * annual_kilometers
        annual_cost = fuel_cost * num_trucks
        costs.append(round(annual_cost * ((1 + inflation_rate) ** (year - 1)), 2))
    return costs

# Función para calcular costos anuales del camión eléctrico
def calculate_electric_costs(electric_data, cost_per_kwh, annual_kilometers, num_trucks, inflation_rate, electric_increase_rate):
    costs = []
    for year in range(1, 6):
        adjusted_cost_per_kwh = cost_per_kwh + (electric_increase_rate * (year - 1))
        electricity_cost = (annual_kilometers / electric_data["distance_per_charge_km"]) * (adjusted_cost_per_kwh * electric_data["battery_capacity_kwh"])
        annual_cost = electricity_cost * num_trucks
        costs.append(round(annual_cost * ((1 + inflation_rate) ** (year - 1)), 2))
    return costs

# Título de la aplicación y nombre de la empresa
st.markdown("<h1 style='text-align: center; color: #FF4B4B; font-size: 60px;'>Comercializadora Sany</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: black; font-size: 36px;'>Comparación de Costos: Camión Diésel vs. Camión Eléctrico</h2>", unsafe_allow_html=True)

# Sección sobre la empresa
st.markdown("""
<div style='text-align: center;'>
<h4>Sobre Nosotros</h4>
<p>Comercializadora Sany se dedica a la venta de camiones eléctricos, ofreciendo las mejores opciones del mercado para que tu negocio sea más sostenible y eficiente. Nos comprometemos a brindar productos de alta calidad y un servicio excepcional a nuestros clientes.</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# Selección de modelo de camión diésel
st.markdown("<h4 style='text-align: center;'>Seleccione el modelo de camión diésel</h4>", unsafe_allow_html=True)
selected_model = st.selectbox("", list(diesel_trucks.keys()))

st.divider()

# Datos de operación
st.markdown("<h4 style='text-align: center;'>Datos de Operación</h4>", unsafe_allow_html=True)
daily_kilometers = st.number_input("Kilómetros recorridos diariamente por camión:", value=50, min_value=1)
annual_kilometers = st.number_input("Kilómetros recorridos anualmente por camión:", value=daily_kilometers * 312, min_value=1)
num_trucks_electric = st.number_input("Cantidad de camiones eléctricos:", value=1, min_value=1)
num_trucks_diesel = st.number_input("Cantidad de camiones diésel:", value=1, min_value=1)
st.write(f"Kilómetros recorridos anualmente por camión: {annual_kilometers} km")

st.divider()

# Costos fijos
st.markdown("<h4 style='text-align: center;'>Costos Fijos Camión Diesel</h4>", unsafe_allow_html=True)
apply_verification = st.checkbox("¿Aplica verificación vehicular?", value=True)
apply_tax = st.checkbox("¿Aplica refrendo?", value=True)
verification_cost = st.number_input("Costo de verificación vehicular por camión ($):", value=687 if apply_verification else 0, min_value=0)
tax_cost = st.number_input("Costo de refrendo por camión ($):", value=734 if apply_tax else 0, min_value=0)
insurance_cost = st.number_input("Costo de seguro por camión ($):", value=53500, min_value=0)

st.divider()

# Precio del combustible diésel
st.markdown("<h4 style='text-align: center;'>Precio del Combustible Diésel</h4>", unsafe_allow_html=True)
diesel_fuel_cost = st.number_input("Costo del combustible diésel ($/litro):", value=25.54, min_value=0.01)
diesel_km_per_liter = st.number_input("Kilómetros por litro del camión diésel seleccionado:", value=float(diesel_trucks[selected_model]["km_per_liter"]), min_value=0.01)
diesel_consumption = 1 / diesel_km_per_liter

# Gráfica del comportamiento del precio del diésel
st.markdown("<h4 style='text-align: center;'>Comportamiento del Precio del Diésel en México (2018-2024)</h4>", unsafe_allow_html=True)
# Datos de precios del diésel de 2018 a 2023
data = {
    "Fecha": [
        "2018-01", "2018-02", "2018-03", "2018-04", "2018-05", "2018-06", "2018-07", "2018-08", "2018-09", "2018-10", "2018-11", "2018-12",
        "2019-01", "2019-02", "2019-03", "2019-04", "2019-05", "2019-06", "2019-07", "2019-08", "2019-09", "2019-10", "2019-11", "2019-12",
        "2020-01", "2020-02", "2020-03", "2020-04", "2020-05", "2020-06", "2020-07", "2020-08", "2020-09", "2020-10", "2020-11", "2020-12",
        "2021-01", "2021-02", "2021-03", "2021-04", "2021-05", "2021-06", "2021-07", "2021-08", "2021-09", "2021-10", "2021-11", "2021-12",
        "2022-01", "2022-02", "2022-03", "2022-04", "2022-05", "2022-06", "2022-07", "2022-08", "2022-09", "2022-10", "2022-11", "2022-12",
        "2023-01", "2023-02", "2023-03", "2023-04", "2023-05", "2023-06", "2023-07", "2023-08", "2023-09", "2023-10", "2023-11", "2023-12"
    ],
    "Precio_Diesel": [
        17.16, 17.42, 17.57, 17.69, 17.80, 18.02, 18.25, 18.42, 18.55, 18.75, 19.14, 19.35,
        19.52, 19.61, 19.65, 19.74, 19.87, 20.05, 20.25, 20.37, 20.48, 20.67, 20.88, 21.05,
        21.10, 21.18, 20.95, 19.72, 19.34, 19.55, 19.78, 19.98, 20.12, 20.29, 20.45, 20.62,
        20.78, 20.93, 21.04, 21.18, 21.34, 21.55, 21.72, 21.89, 22.05, 22.20, 22.35, 22.50,
        22.60, 22.75, 22.90, 23.05, 23.20, 23.35, 23.50, 23.65, 23.80, 23.95, 24.10, 24.25,
        24.30, 24.45, 24.60, 24.75, 24.90, 25.05, 25.20, 25.35, 25.50, 25.65, 25.80, 25.95
    ]
}

# Crear el DataFrame
df = pd.DataFrame(data)

# Convertir la columna de fechas a tipo datetime
df["Fecha"] = pd.to_datetime(df["Fecha"])

# Configurar la gráfica de líneas
plt.figure(figsize=(12, 6))
plt.plot(df["Fecha"], df["Precio_Diesel"], marker='o', linestyle='-', color='b')
plt.title('Comportamiento del Precio del Diésel en México (2018-2023)')
plt.xlabel('Fecha')
plt.ylabel('Precio (MXN por litro)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Mostrar la gráfica en Streamlit
st.pyplot(plt)

st.divider()

# Precio del kWh
st.markdown("<h4 style='text-align: center;'>Precio de la Electricidad</h4>", unsafe_allow_html=True)
cost_per_kwh = st.number_input("Costo de la electricidad ($/kWh):", value=3.00, min_value=0.01)

# Información técnica del camión Sany FE601
st.markdown("<h4 style='text-align: center;'>Ficha Técnica del Camión Sany FE601</h4>", unsafe_allow_html=True)
st.markdown("""
<div style='display: flex; justify-content: center;'>
<table style='border-collapse: collapse; width: 60%; text-align: left;'>
    <tr><th style='border: 1px solid black; padding: 8px;'>Modelo</th><td style='border: 1px solid black; padding: 8px;'>Sany FE601</td></tr>
    <tr><th style='border: 1px solid black; padding: 8px;'>Capacidad de Batería</th><td style='border: 1px solid black; padding: 8px;'>84.48 kWh</td></tr>
    <tr><th style='border: 1px solid black; padding: 8px;'>Consumo por Kilómetro</th><td style='border: 1px solid black; padding: 8px;'>0.45 kWh</td></tr>
    <tr><th style='border: 1px solid black; padding: 8px;'>Distancia por Carga Completa</th><td style='border: 1px solid black; padding: 8px;'>200 km</td></tr>
    <tr><th style='border: 1px solid black; padding: 8px;'>Costo Inicial</th><td style='border: 1px solid black; padding: 8px;'>$1,566,000 (incluye IVA)</td></tr>
    <tr><th style='border: 1px solid black; padding: 8px;'>Mantenimiento Anual</th><td style='border: 1px solid black; padding: 8px;'>$4,000</td></tr>
    <tr><th style='border: 1px solid black; padding: 8px;'>Seguro Anual</th><td style='border: 1px solid black; padding: 8px;'>$53,000</td></tr>
</table>
</div>
""", unsafe_allow_html=True)

st.divider()

# Inflación y aumento de precios
st.markdown("<h4 style='text-align: center;'>Inflación y Aumento de Precios</h4>", unsafe_allow_html=True)
inflation_rate = st.number_input("Tasa de inflación anual (%):", value=4.20, min_value=0.0, step=0.1) / 100
fuel_increase_rate = st.number_input("Incremento anual del precio del combustible diésel ($):", value=1.10, min_value=0.0, step=0.1)
electric_increase_rate = st.number_input("Incremento anual del precio de la electricidad ($):", value=0.40, min_value=0.0, step=0.1)

# Calcular costos anuales
diesel_annual_costs = calculate_diesel_costs(selected_model, diesel_fuel_cost, annual_kilometers, num_trucks_diesel, verification_cost, insurance_cost, tax_cost, inflation_rate, fuel_increase_rate)
electric_annual_costs = calculate_electric_costs(electric_data, cost_per_kwh, annual_kilometers, num_trucks_electric, inflation_rate, electric_increase_rate)

# Crear DataFrame para mostrar los resultados
df = pd.DataFrame({
    "Año": list(range(1, 6)),
    "Costo Anual - Diésel": diesel_annual_costs,
    "Costo Anual - Eléctrico": electric_annual_costs,
    "Costo Acumulado - Diésel": pd.Series(diesel_annual_costs).cumsum(),
    "Costo Acumulado - Eléctrico": pd.Series(electric_annual_costs).cumsum()
})

st.divider()

# Mostrar resultados
st.markdown("<h4 style='text-align: center;'>Resultados Comparativos</h4>", unsafe_allow_html=True)
st.table(df.style.format({"Costo Anual - Diésel": "{:,.2f}", "Costo Anual - Eléctrico": "{:,.2f}", "Costo Acumulado - Diésel": "{:,.2f}", "Costo Acumulado - Eléctrico": "{:,.2f}"}))

st.markdown(f"""
<div style='text-align: center;'>
    <p><b>Cantidad de camiones seleccionados:</b> {num_trucks_diesel} diésel y {num_trucks_electric} eléctricos</p>
    <p>Los costos van aumentando año tras año debido a la inflación y al aumento de los precios.</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# Tabla comparativa final
comparison_data = {
    "Concepto": [
        "Seguro anual",
        "Refrendo",
        "Mantenimiento (Anual o cada 40K km)",
        "Verificación anual",
        "Combustible anual promedio"
    ],
    "Año 1 (Diésel)": [
        insurance_cost * num_trucks_diesel,
        tax_cost * num_trucks_diesel,
        diesel_trucks[selected_model]["maintenance_annual"] * num_trucks_diesel,
        verification_cost * num_trucks_diesel,
        diesel_annual_costs[0]
    ],
    "Año 1 (Eléctrico)": [
        electric_data["insurance_annual"] * num_trucks_electric,
        0,
        electric_data["maintenance_annual"] * num_trucks_electric,
        0,
        electric_annual_costs[0]
    ],
    "Acumulado a 5 años (Diésel)": [
        insurance_cost * num_trucks_diesel * 5,
        tax_cost * num_trucks_diesel * 5,
        diesel_trucks[selected_model]["maintenance_annual"] * num_trucks_diesel * 5,
        verification_cost * num_trucks_diesel * 5,
        sum(diesel_annual_costs)
    ],
    "Acumulado a 5 años (Eléctrico)": [
        electric_data["insurance_annual"] * num_trucks_electric * 5,
        0,
        electric_data["maintenance_annual"] * num_trucks_electric * 5,
        0,
        sum(electric_annual_costs)
    ]
}

comparison_df = pd.DataFrame(comparison_data)
comparison_df = comparison_df.applymap(lambda x: f"{x:,.2f}" if isinstance(x, (int, float)) else x)
st.markdown("<h4 style='text-align: center;'>Tabla Comparativa Final</h4>", unsafe_allow_html=True)
st.table(comparison_df)

# Cálculo del ahorro total
total_savings = (
    (insurance_cost * num_trucks_diesel * 5 + tax_cost * num_trucks_diesel * 5 + diesel_trucks[selected_model]["maintenance_annual"] * num_trucks_diesel * 5 + verification_cost * num_trucks_diesel * 5 + sum(diesel_annual_costs))
    - (electric_data["insurance_annual"] * num_trucks_electric * 5 + electric_data["maintenance_annual"] * num_trucks_electric * 5 + sum(electric_annual_costs))
)

st.divider()

# Mostrar resumen de ahorro
st.markdown("<h4 style='text-align: center;'>Resumen de ahorro de Combustible</h4>", unsafe_allow_html=True)
summary_data = {
    "Concepto": ["Costo Total - Diésel", "Costo Total - Eléctrico", "Ahorro"],
    "Valor ($)": [sum(diesel_annual_costs), sum(electric_annual_costs), total_savings]
}
summary_df = pd.DataFrame(summary_data)

st.table(summary_df)

if total_savings > 0:
    st.success(f"El camión eléctrico ahorra ${total_savings:,.2f} en comparación con el camión diésel seleccionado en 5 años.")
else:
    st.warning(f"El camión diésel seleccionado es más económico por ${-total_savings:,.2f} en comparación con el camión eléctrico en 5 años.")

st.divider()

# Pie de página
st.markdown("""
<div style='text-align: center;'>
<p>&copy; 2024 Comercializadora Sany. Todos los derechos reservados.</p>
</div>
""", unsafe_allow_html=True)












