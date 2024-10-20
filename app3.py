import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Distribuciones L: Cotizador de Productos Médicos")

# Crear un diccionario de productos y sus precios
productos = {
    "Guantes Médicos": 100,
    "Mascarillas": 50,
    "Gel Antibacterial": 30,
    "Batas Quirúrgicas": 150,
    "Jeringas": 10
}

st.header("Cotización")

# Inicializar una lista para almacenar los productos seleccionados
if 'cotizacion' not in st.session_state:
    st.session_state['cotizacion'] = pd.DataFrame(columns=["Producto", "Cantidad", "Precio Unitario", "Subtotal"])

# Formulario para agregar productos
with st.form(key='formulario_producto'):
    col1, col2 = st.columns(2)
    with col1:
        producto_seleccionado = st.selectbox("Selecciona un producto", list(productos.keys()))
    with col2:
        cantidad = st.number_input("Cantidad", min_value=1, value=1)
    agregar = st.form_submit_button("Agregar a la cotización")

# Agregar producto a la cotización
if agregar:
    precio_unitario = productos[producto_seleccionado]
    subtotal = precio_unitario * cantidad
    nuevo_producto = {
        "Producto": producto_seleccionado,
        "Cantidad": cantidad,
        "Precio Unitario": precio_unitario,
        "Subtotal": subtotal
    }
    # Usamos pd.concat en lugar de append, ya que append está obsoleto
    st.session_state['cotizacion'] = pd.concat(
        [st.session_state['cotizacion'], pd.DataFrame([nuevo_producto])],
        ignore_index=True
    )
    st.success(f"{producto_seleccionado} agregado a la cotización.")

# Mostrar cotización actual
st.subheader("Detalle de la cotización:")
if not st.session_state['cotizacion'].empty:
    df = st.session_state['cotizacion']
    total_sin_iva = df['Subtotal'].sum()
    iva = total_sin_iva * 0.16
    total_con_iva = total_sin_iva + iva

    st.table(df.style.format({
        "Cantidad": "{:.0f}",
        "Precio Unitario": "${:,.2f}",
        "Subtotal": "${:,.2f}"
    }))

    col_total1, col_total2, col_total3 = st.columns(3)
    with col_total1:
        st.write(f"**Total sin IVA:**\n${total_sin_iva:,.2f}")
    with col_total2:
        st.write(f"**IVA (16%):**\n${iva:,.2f}")
    with col_total3:
        st.write(f"**Total con IVA:**\n${total_con_iva:,.2f}")
else:
    st.write("No has agregado productos a la cotización.")

# Botón para reiniciar la cotización
if st.button("Reiniciar cotización"):
    st.session_state['cotizacion'] = pd.DataFrame(columns=["Producto", "Cantidad", "Precio Unitario", "Subtotal"])
    st.success("La cotización ha sido reiniciada.")








