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
    "Hino J05E-US": {"cost_initial": 1320000 * 1.16, "km_per_liter": 7, "maintenance_annual": 8000, "capacidad_combustible": 200},
    "JAC X350": {"cost_initial": 600000 * 1.16, "km_per_liter": 6, "maintenance_annual": 8000, "capacidad_combustible": 100},
    "VolksWagen Delivery 6.160": {"cost_initial": 560000 * 1.16, "km_per_liter": 4, "maintenance_annual": 8000, "capacidad_combustible": 150},
    "ISUZU ELF600": {"cost_initial": 1050000 * 1.16, "km_per_liter": 7, "maintenance_annual": 8000, "capacidad_combustible": 140}
}

# Función para calcular costos anuales del camión diésel seleccionado
def calculate_diesel_costs(selected_model, diesel_fuel_cost, annual_kilometers, num_trucks, verification_cost, insurance_cost, tax_cost, inflation_rate, fuel_increase_rate):
    costs = []
    for year in range(1, 6):
        adjusted_fuel_cost = diesel_fuel_cost * ((1 + fuel_increase_rate) ** (year - 1))
        fuel_cost = (1 / diesel_trucks[selected_model]["km_per_liter"]) * adjusted_fuel_cost * annual_kilometers
        maintenance_cost = diesel_trucks[selected_model]["maintenance_annual"]
        fixed_costs = verification_cost + insurance_cost + tax_cost
        annual_cost = (fuel_cost + maintenance_cost + fixed_costs) * num_trucks
        costs.append(round(annual_cost * ((1 + inflation_rate) ** (year - 1)), 2))
    return costs

# Función para calcular costos anuales del camión eléctrico
def calculate_electric_costs(electric_data, cost_per_kwh, annual_kilometers, num_trucks, inflation_rate, electric_increase_rate):
    costs = []
    for year in range(1, 6):
        adjusted_cost_per_kwh = cost_per_kwh * ((1 + electric_increase_rate) ** (year - 1))
        electricity_cost = (annual_kilometers / electric_data["distance_per_charge_km"]) * (adjusted_cost_per_kwh * electric_data["battery_capacity_kwh"])
        maintenance_cost = electric_data["maintenance_annual"]
        fixed_costs = electric_data["insurance_annual"]
        battery_replacement_cost = electric_data["battery_replacement_cost"] if year % electric_data["battery_replacement_frequency_years"] == 0 else 0
        annual_cost = (electricity_cost + maintenance_cost + fixed_costs + battery_replacement_cost) * num_trucks
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
num_trucks_electric = st.number_input("Cantidad de camiones eléctricos:", value=10, min_value=1)
num_trucks_diesel = st.number_input("Cantidad de camiones diésel:", value=1, min_value=1)
st.write(f"Kilómetros recorridos anualmente por camión: {annual_kilometers} km")

st.divider()

# Costos fijos
st.markdown("<h4 style='text-align: center;'>Costos Fijos Camión Diesel</h4>", unsafe_allow_html=True)
verification_cost = st.number_input("Costo de verificación vehicular por camión ($):", value=687, min_value=0)
insurance_cost = st.number_input("Costo de seguro por camión ($):", value=53500, min_value=0)
tax_cost = st.number_input("Costo de tenencia por camión ($):", value=698, min_value=0)

st.divider()

# Precio del combustible diésel
st.markdown("<h4 style='text-align: center;'>Precio del Combustible Diésel</h4>", unsafe_allow_html=True)
diesel_fuel_cost = st.number_input("Costo del combustible diésel ($/litro):", value=25.30, min_value=0.01)
diesel_km_per_liter = st.number_input("Kilómetros por litro del camión diésel seleccionado:", value=float(diesel_trucks[selected_model]["km_per_liter"]), min_value=0.01)
diesel_consumption = 1 / diesel_km_per_liter

# Gráfica del comportamiento del precio del diésel
st.markdown("<h4 style='text-align: center;'>Comportamiento del Precio del Diésel en México (2023)</h4>", unsafe_allow_html=True)
data = {
    "Fecha": ["2023-01", "2023-02", "2023-03", "2023-04", "2023-05", "2023-06", "2023-07", "2023-08", "2023-09", "2023-10", "2023-11"],
    "Precio_Diesel": [24.00, 24.20, 24.30, 24.40, 24.50, 24.60, 24.70, 24.80, 24.90, 25.00, 25.10]
}
df = pd.DataFrame(data)
fig, ax = plt.subplots()
ax.plot(df["Fecha"], df["Precio_Diesel"], marker='o', linestyle='-', color='b')
ax.set_title('Comportamiento del Precio del Diésel en México (2023)')
ax.set_xlabel('Fecha')
ax.set_ylabel('Precio (MXN/Litro)')
ax.grid(True)
ax.set_xticklabels(df["Fecha"], rotation=45)
st.pyplot(fig)

st.divider()

# Precio del kWh
st.markdown("<h4 style='text-align: center;'>Precio de la Electricidad</h4>", unsafe_allow_html=True)
cost_per_kwh = st.number_input("Costo de la electricidad ($/kWh):", value=3.00, min_value=0.01)
electric_distance_per_charge = st.number_input("Kilómetros por carga completa del camión eléctrico:", value=float(electric_data["distance_per_charge_km"]), min_value=0.01)

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
inflation_rate = st.number_input("Tasa de inflación anual (%):", value=4.0, min_value=0.0, step=0.1) / 100
fuel_increase_rate = st.number_input("Incremento anual del precio del combustible diésel (%):", value=1.50, min_value=0.0, step=0.1) / 100
electric_increase_rate = st.number_input("Incremento anual del precio de la electricidad (%):", value=0.40, min_value=0.0, step=0.1) / 100

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
st.table(df)

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
        "Valor del Auto",
        "Seguro anual",
        "Tenencia",
        "Mantenimiento (Anual o cada 40K km)",
        "Verificación anual",
        "Combustible anual promedio"
    ],
    "Año 1 (Diésel)": [
        diesel_trucks[selected_model]["cost_initial"] * num_trucks_diesel,
        insurance_cost * num_trucks_diesel,
        tax_cost * num_trucks_diesel,
        diesel_trucks[selected_model]["maintenance_annual"] * num_trucks_diesel,
        verification_cost * num_trucks_diesel,
        diesel_annual_costs[0]
    ],
    "Año 1 (Eléctrico)": [
        electric_data["cost_initial"] * num_trucks_electric,
        electric_data["insurance_annual"] * num_trucks_electric,
        0,
        electric_data["maintenance_annual"] * num_trucks_electric,
        0,
        electric_annual_costs[0]
    ],
    "Acumulado a 5 años (Diésel)": [
        diesel_trucks[selected_model]["cost_initial"] * num_trucks_diesel,
        insurance_cost * num_trucks_diesel * 5,
        tax_cost * num_trucks_diesel * 5,
        diesel_trucks[selected_model]["maintenance_annual"] * num_trucks_diesel * 5,
        verification_cost * num_trucks_diesel * 5,
        sum(diesel_annual_costs)
    ],
    "Acumulado a 5 años (Eléctrico)": [
        electric_data["cost_initial"] * num_trucks_electric,
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

st.divider()

# Cálculo del ahorro
total_diesel_cost = df["Costo Acumulado - Diésel"].iloc[-1]
total_electric_cost = df["Costo Acumulado - Eléctrico"].iloc[-1]
savings = total_diesel_cost - total_electric_cost

# Cálculo del ahorro anual
annual_savings = [d - e for d, e in zip(diesel_annual_costs, electric_annual_costs)]

# Crear DataFrame para mostrar el ahorro anual
savings_df = pd.DataFrame({
    "Año": list(range(1, 6)),
    "Ahorro Anual ($)": annual_savings
})

st.divider()

# Formateador de moneda
def currency(x, pos):
    'The two args are the value and tick position'
    return "${:,.0f}".format(x)

formatter = FuncFormatter(currency)

# Gráfico de costos acumulados
st.markdown("<h4 style='text-align: center;'>Gráfico de Costos Acumulados</h4>", unsafe_allow_html=True)
fig, ax = plt.subplots()
ax.plot(df["Año"], df["Costo Acumulado - Diésel"], label="Diésel", color='blue', marker='o')
ax.plot(df["Año"], df["Costo Acumulado - Eléctrico"], label="Eléctrico", color='green', marker='o')
ax.set_ylabel("Costo Acumulado ($)")
ax.set_xlabel("Año")
ax.set_title("Comparación de Costos Acumulados")
ax.legend()
ax.yaxis.set_major_formatter(formatter)

st.pyplot(fig)

st.divider()

# Resumen de Costos Totales
st.markdown("<h4 style='text-align: center;'>Resumen de Costos Totales</h4>", unsafe_allow_html=True)
summary_data = {
    "Concepto": ["Costo Total - Diésel", "Costo Total - Eléctrico", "Ahorro"],
    "Valor ($)": [total_diesel_cost, total_electric_cost, savings]
}
summary_df = pd.DataFrame(summary_data)

st.table(summary_df)

if savings > 0:
    st.success(f"El camión eléctrico ahorra ${savings:,.2f} en comparación con el camión diésel seleccionado en 5 años.")
else:
    st.warning(f"El camión diésel seleccionado es más económico por ${-savings:,.2f} en comparación con el camión eléctrico en 5 años.")

st.divider()

# Mostrar ahorro anual
st.markdown("<h4 style='text-align: center;'>Ahorro Anual</h4>", unsafe_allow_html=True)
st.table(savings_df)

st.divider()

# Cálculo de la reducción de emisiones de CO2
co2_emission_per_liter_diesel = 2.68  # kg de CO2 por litro de diésel
total_diesel_fuel_consumed = diesel_consumption * annual_kilometers * num_trucks_diesel * 5  # Consumo total de diésel en 5 años
total_co2_emissions_diesel = total_diesel_fuel_consumed * co2_emission_per_liter_diesel
total_co2_emissions_electric = 0  # Asumimos cero emisiones de CO2 para camiones eléctricos
percentage_reduction = ((total_co2_emissions_diesel - total_co2_emissions_electric) / total_co2_emissions_diesel) * 100

# Interpretación escrita con explicación detallada
st.markdown(f"""
<div style='text-align: center;'>
<h4>Interpretación de Resultados</h4>
<p>La gráfica de costos acumulados muestra la diferencia en los costos totales entre el camión diésel y el camión eléctrico a lo largo de 5 años.</p>
<p><b>Costo Total - Diésel</b>: ${total_diesel_cost:,.2f}</p>
<p><b>Costo Total - Eléctrico</b>: ${total_electric_cost:,.2f}</p>
<p><b>Ahorro</b>: ${savings:,.2f}</p>
</div>
""", unsafe_allow_html=True)

# Explicación del cálculo
st.markdown("""
<div style='text-align: center;'>
<h4>Explicación del Cálculo</h4>
<p>Para calcular los costos anuales y acumulados, se realizaron los siguientes pasos:</p>
<ol style='text-align: left;'>
    <li><b>Costo Anual de Diésel:</b> Se calculó multiplicando el consumo de combustible (litros/km) por el costo del combustible (pesos/litro) y el kilometraje anual. Luego se sumaron los costos fijos anuales y los costos de mantenimiento, ajustados por la tasa de inflación y el aumento del precio del combustible.</li>
    <li><b>Costo Anual de Eléctrico:</b> Se calculó multiplicando el consumo de energía (% por km) por la capacidad de la batería (kWh) y el costo de la electricidad (pesos/kWh) y el kilometraje anual. Luego se sumaron los costos fijos anuales y los costos de mantenimiento, ajustados por la tasa de inflación y el aumento del precio de la electricidad.</li>
    <li><b>Costo Acumulado:</b> Se calcularon sumando los costos anuales acumulados a lo largo de los 5 años.</li>
    <li><b>Ahorro Anual:</b> Se calculó restando el costo anual del camión eléctrico al costo anual del camión diésel para cada año.</li>
    <li><b>Ahorro Total:</b> Se calculó restando el costo acumulado del camión eléctrico al costo acumulado del camión diésel.</li>
</ol>
<p>Estos cálculos permiten obtener una visión clara y detallada de los costos y ahorros asociados con cada tipo de camión a lo largo del tiempo.</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# Pie de página
st.markdown("""
<div style='text-align: center;'>
<p>&copy; 2024 Comercializadora Sany. Todos los derechos reservados.</p>
</div>
""", unsafe_allow_html=True)













