import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import cvxpy as cp

# Función para obtener los datos de Yahoo Finance
def get_stock_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

# Función para calcular el rendimiento anual
def calculate_annual_return(data):
    return ((data.iloc[-1]['Adj Close'] / data.iloc[0]['Adj Close']) ** (1 / len(data))) - 1

# Función para realizar el análisis de Markowitz
def markowitz_analysis(data):
    log_returns = np.log(data / data.shift(1)).dropna()
    n = len(log_returns.columns)
    weights = cp.Variable(n)
    expected_return = cp.sum(cp.multiply(weights, log_returns.mean())) * 252
    variance = cp.quad_form(weights, log_returns.cov().values)
    risk_free_rate = 0.0  # Tasa libre de riesgo
    objective = cp.Maximize(expected_return - risk_free_rate * variance)
    constraints = [cp.sum(weights) == 1, weights >= 0]
    problem = cp.Problem(objective, constraints)
    problem.solve()
    return {
        'weights': weights.value,
        'expected_return': expected_return.value,
        'expected_volatility': cp.sqrt(variance).value,
        'cov': log_returns.cov().values
    }

# Función para calcular la inversión óptima basada en los pesos obtenidos de Markowitz
def calculate_optimal_investment(markowitz_results, investment_amount, risk_level):
    # Asignar el porcentaje de inversión basado en el riesgo
    risk_tolerance = {
        'Alto': 0.15,
        'Moderado': 0.07,
        'Bajo': 0.03
    }
    risk_tolerance = risk_tolerance.get(risk_level, 0.03)

    # Calcular la inversión óptima basada en el nivel de riesgo
    total_volatility = sum(result['expected_volatility'] for result in markowitz_results.values())
    optimal_investment = {}
    for symbol, result in markowitz_results.items():
        weight = result['expected_volatility'] / total_volatility
        investment_share = (1 - risk_tolerance) * weight * investment_amount
        optimal_investment[symbol] = investment_share

    return optimal_investment

# Función para trazar la frontera eficiente de Markowitz
def plot_efficient_frontier(markowitz_results, risk_level):
    risks = []
    portfolios = []

    for symbol, result in markowitz_results.items():
        risks.append(result['expected_volatility'])
        portfolios.append(result['expected_return'])

    # Calcular el punto óptimo en la frontera eficiente según el nivel de riesgo
    max_sharpe_index = np.argmax(portfolios)
    max_sharpe_risk = risks[max_sharpe_index]
    max_sharpe_return = portfolios[max_sharpe_index]

    return risks, portfolios, max_sharpe_risk, max_sharpe_return

# Función para calcular y mostrar la matriz de covarianza
def show_covariance_matrix(data):
    st.subheader('Matriz de Covarianza')
    covariance_matrix = data.pct_change().cov()
    st.write(covariance_matrix)

    # Interpretación de la matriz de covarianza
    st.write('La matriz de covarianza muestra cómo varían los rendimientos de las acciones en conjunto. Los valores más altos indican una mayor correlación entre los rendimientos de las acciones, mientras que los valores más bajos indican una menor correlación.')

    # Heatmap de la matriz de covarianza
    plt.figure(figsize=(10, 8))
    sns.heatmap(covariance_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Matriz de Covarianza')
    plt.xlabel('Acciones')
    plt.ylabel('Acciones')
    st.pyplot(plt)

# Función para mostrar la distribución de rendimientos de cada activo
def show_return_distribution(data):
    st.subheader('Distribución de Rendimientos')
    for symbol in data.columns:
        st.write(f"**{symbol}**")
        plt.figure(figsize=(8, 6))
        sns.histplot(data[symbol].pct_change().dropna(), kde=True)
        plt.title(f'Distribución de Rendimientos de {symbol}')
        plt.xlabel('Rendimiento Diario')
        plt.ylabel('Frecuencia')
        st.pyplot(plt)

    # Interpretación de la distribución de rendimientos
    st.write('La distribución de rendimientos muestra la frecuencia con la que los rendimientos de las acciones ocurren. Un pico más alto en el histograma indica que los rendimientos están más concentrados alrededor de ese valor.')

# Función para mostrar el heatmap de correlación
def show_correlation_heatmap(data):
    st.subheader('Heatmap de Correlación')
    correlation_matrix = data.pct_change().corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Heatmap de Correlación')
    plt.xlabel('Acciones')
    plt.ylabel('Acciones')
    st.pyplot(plt)

    # Interpretación del heatmap de correlación
    st.write('El heatmap de correlación muestra la relación entre los rendimientos de las acciones. Los valores más cercanos a 1 indican una correlación positiva perfecta, mientras que los valores cercanos a -1 indican una correlación negativa perfecta. Un valor cercano a 0 indica una correlación débil o nula.')

# Función para obtener la cartera eficiente
def get_efficient_portfolio(portfolios, risk_level):
    if risk_level == 'Alto':
        max_sharpe_index = np.argmax(portfolios)
    elif risk_level == 'Moderado':
        max_sharpe_index = np.argmax(portfolios)
    else:
        max_sharpe_index = np.argmax(portfolios)

    return max_sharpe_index

# Función principal
def main():
    # Título y descripción
    st.title('Análisis de Acciones con Markowitz')
    st.write('Esta aplicación te permite analizar el rendimiento de hasta tres acciones utilizando el método de optimización de Markowitz.')

    # Sidebar para ingresar los parámetros
    st.sidebar.header('Configuración')
    start_date = st.sidebar.date_input('Fecha de inicio', value=pd.to_datetime('2021-01-01'))
    end_date = st.sidebar.date_input('Fecha de fin', value=pd.to_datetime('today'))

    # Selección de acciones
    st.sidebar.header('Selección de Acciones')
    symbols = [st.sidebar.text_input(f'Acción {i+1}', value='', key=i) for i in range(3)]
    symbols = [symbol for symbol in symbols if symbol]  # Eliminar entradas vacías

    # Cantidad de dinero a invertir
    investment_amount = st.sidebar.number_input('Cantidad a Invertir', min_value=0.0, value=10000.0, step=1000.0)

    # Nivel de riesgo
    risk_level = st.sidebar.selectbox('Nivel de Riesgo', ['Alto', 'Moderado', 'Bajo'])

    # Botón para cargar los datos
    if st.sidebar.button('Cargar Datos'):
        if not symbols:
            st.warning('Por favor ingresa al menos una acción.')
            return

        st.subheader('Datos de Acciones Seleccionadas')
        combined_data = pd.DataFrame()
        markowitz_results = {}
        for symbol in symbols:
            data = get_stock_data(symbol, start_date, end_date)
            st.write(f"**{symbol}**")
            st.write(data)

            # Calcular el rendimiento anual
            annual_return = calculate_annual_return(data)
            st.write(f"Rendimiento Anual de {symbol}: {annual_return:.2%}")

            # Agregar datos a DataFrame combinado
            combined_data[symbol] = data['Adj Close']

            # Gráfico de precios de cierre ajustados
            plt.figure(figsize=(10, 5))
            plt.plot(data.index, data['Adj Close'], label='Precio de Cierre Ajustado')
            plt.title(f'Precio de Cierre Ajustado de {symbol}')
            plt.xlabel('Fecha')
            plt.ylabel('Precio de Cierre Ajustado')
            plt.legend()
            st.pyplot(plt)

            # Realizar análisis de Markowitz
            markowitz_results[symbol] = markowitz_analysis(data)

        # Mostrar la matriz de covarianza
        show_covariance_matrix(combined_data)

        # Mostrar la distribución de rendimientos
        show_return_distribution(combined_data)

        # Mostrar el heatmap de correlación
        show_correlation_heatmap(combined_data)

        # Calcular la inversión óptima
        optimal_investment = calculate_optimal_investment(markowitz_results, investment_amount, risk_level)

        # Análisis de Markowitz
        st.subheader('Análisis de Markowitz')
        st.write('Utilizando el método de Markowitz, encontramos la siguiente información para cada acción:')
        for symbol, result in markowitz_results.items():
            st.write(f"**{symbol}**")
            st.write(f"Rendimiento Esperado: {result['expected_return']:.2%}")
            st.write(f"Volatilidad Esperada: {result['expected_volatility']:.2%}")
            st.write(f"Relación de Sharpe: {(result['expected_return'] - 0) / result['expected_volatility']:.2f}")

        # Graficar la frontera eficiente
        risks, portfolios, max_sharpe_risk, max_sharpe_return = plot_efficient_frontier(markowitz_results, risk_level)
        efficient_portfolio_index = get_efficient_portfolio(portfolios, risk_level)
        fig2, ax2 = plt.subplots()
        ax2.plot(risks, portfolios, marker='o', linestyle='-', label='Frontera Eficiente')
        ax2.scatter(max_sharpe_risk, max_sharpe_return, color='red', label='Punto Óptimo')
        ax2.annotate(f'Optimo', (max_sharpe_risk, max_sharpe_return), textcoords="offset points", xytext=(-15,10), ha='center', fontsize=8)
        ax2.set_xlabel('Volatilidad Esperada')
        ax2.set_ylabel('Rendimiento Esperado')
        ax2.set_title('Frontera Eficiente de Markowitz')
        ax2.legend()
        st.pyplot(fig2)

        # Interpretación de las últimas dos gráficas
        st.subheader('Interpretación de las Gráficas')
        st.write('La segunda gráfica representa la frontera eficiente de Markowitz, que muestra el trade-off entre el rendimiento esperado y la volatilidad esperada del portafolio. El punto óptimo en esta gráfica indica la combinación de riesgo y rendimiento que maximiza la utilidad para el cliente, teniendo en cuenta su nivel de riesgo tolerado.')

        st.write('La primera gráfica muestra la asignación de inversión óptima para el cliente, considerando su nivel de riesgo y la información obtenida del análisis de Markowitz. Según esta asignación, el cliente debe invertir su dinero de la siguiente manera:')
        for symbol, investment_share in optimal_investment.items():
            st.write(f" - {investment_share:.2f} USD en la acción {symbol}")

        # Gráfico de pastel para la asignación de inversión óptima
        labels = optimal_investment.keys()
        sizes = optimal_investment.values()
        fig3, ax3 = plt.subplots()
        ax3.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax3.axis('equal')
        plt.title('Asignación de Inversión Óptima')
        st.pyplot(fig3)

# Ejecutar la aplicación
if __name__ == "__main__":
    main()
