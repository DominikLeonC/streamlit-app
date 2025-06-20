# app_markowitz_mejorada.py

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import cvxpy as cp

# ===================== FUNCIONES =====================

def get_stock_data(symbols, start_date, end_date):
    data = pd.DataFrame()
    for symbol in symbols:
        try:
            df = yf.download(symbol, start=start_date, end=end_date, auto_adjust=True)
            if 'Adj Close' not in df.columns and 'Close' in df.columns:
                df['Adj Close'] = df['Close']
            if 'Adj Close' in df.columns:
                df = df[['Adj Close']].rename(columns={'Adj Close': symbol})
                data = pd.concat([data, df], axis=1)
            else:
                st.warning(f"No se pudo obtener datos válidos para {symbol}. Verifica el símbolo.")
        except Exception as e:
            st.error(f"Error al descargar datos para {symbol}: {e}")
    return data.dropna()

def markowitz_analysis(log_returns):
    n = log_returns.shape[1]
    mu = log_returns.mean() * 252
    sigma = log_returns.cov() * 252

    w = cp.Variable(n)
    ret = mu.T @ w
    risk = cp.quad_form(w, sigma)
    gamma = cp.Parameter(nonneg=True)  # tradeoff risk vs return
    gamma.value = 1
    prob = cp.Problem(cp.Maximize(ret - gamma * risk), [cp.sum(w) == 1, w >= 0])
    prob.solve()

    return {
        'weights': w.value,
        'expected_return': ret.value,
        'expected_volatility': np.sqrt(risk.value),
        'mu': mu,
        'sigma': sigma
    }

def plot_efficient_frontier(mu, sigma, n_points=50):
    n = len(mu)
    results = []
    for alpha in np.linspace(0, 1, n_points):
        w = cp.Variable(n)
        ret = mu.T @ w
        risk = cp.quad_form(w, sigma)
        prob = cp.Problem(cp.Maximize(alpha * ret - (1 - alpha) * risk), [cp.sum(w) == 1, w >= 0])
        prob.solve()
        results.append((np.sqrt(risk.value), ret.value))

    return zip(*results)

def monte_carlo_simulation(mu, sigma, weights, T=252, simulations=10000):
    daily_mu = mu / T
    daily_sigma = sigma / T
    returns = []
    for _ in range(simulations):
        sim_returns = np.random.multivariate_normal(daily_mu, daily_sigma, T)
        total_return = np.sum(sim_returns @ weights)
        returns.append(total_return)
    return returns

def export_portfolio(symbols, weights, amount):
    alloc = (np.array(weights) * amount).round(2)
    df = pd.DataFrame({"Símbolo": symbols, "Peso": weights, "Monto Invertido": alloc})
    return df

# ===================== APP PRINCIPAL =====================

def main():
    st.title("Análisis de Portafolio con Markowitz")
    st.sidebar.header("Configuración")

    start_date = st.sidebar.date_input("Fecha de inicio", pd.to_datetime("2021-01-01"))
    end_date = st.sidebar.date_input("Fecha de fin", pd.to_datetime("today"))
    investment_amount = st.sidebar.number_input("Monto a invertir (USD)", value=10000.0)
    symbols = [st.sidebar.text_input(f"Acción {i+1}", value="") for i in range(3)]
    symbols = [s for s in symbols if s.strip() != ""]

    modo_avanzado = st.sidebar.checkbox("Modo avanzado")

    if st.sidebar.button("Analizar"):
        if not symbols:
            st.warning("Ingresa al menos una acción válida.")
            return

        prices = get_stock_data(symbols, start_date, end_date)
        log_returns = np.log(prices / prices.shift(1)).dropna()

        result = markowitz_analysis(log_returns)
        weights = result['weights']

        st.subheader("Asignación de Portafolio Óptima")
        df_port = export_portfolio(symbols, weights, investment_amount)
        st.dataframe(df_port)
        st.download_button("Descargar CSV", df_port.to_csv(index=False).encode(), "portafolio.csv", "text/csv")

        # Gráfico de pastel
        fig1, ax1 = plt.subplots()
        ax1.pie(df_port["Monto Invertido"], labels=df_port["Símbolo"], autopct='%1.1f%%')
        ax1.set_title("Asignación de Inversión")
        st.pyplot(fig1)

        if modo_avanzado:
            st.subheader("Frontera Eficiente")
            risks, returns = plot_efficient_frontier(result['mu'], result['sigma'])
            fig2 = px.line(x=list(risks), y=list(returns), labels={'x': 'Riesgo', 'y': 'Retorno Esperado'}, title="Frontera Eficiente")
            st.plotly_chart(fig2)

            st.subheader("Simulación Monte Carlo")
            sims = monte_carlo_simulation(result['mu'], result['sigma'], weights)
            fig3 = px.histogram(sims, nbins=50, title="Distribución de Retornos Simulados")
            st.plotly_chart(fig3)

            st.subheader("Matriz de Correlación")
            fig4, ax4 = plt.subplots()
            sns.heatmap(log_returns.corr(), annot=True, cmap="coolwarm", ax=ax4)
            st.pyplot(fig4)

if __name__ == "__main__":
    main()

