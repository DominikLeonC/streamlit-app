import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Distribuciones L: Cotizador de Productos Médicos")

# Crear una lista de productos
productos = ["Guantes Médicos", "Mascarillas", "Gel Antibacterial", "Batas Quirúrgicas", "Jeringas"]
precios = [100, 50, 30, 150, 10]  # Precios sin IVA

# Input para seleccionar productos y cantidades
st.header("Cotización")
producto_seleccionado = st.selectbox("Selecciona un producto", productos)
cantidad = st.number_input("Cantidad", min_value=1, value=1)

# Obtener el precio sin IVA
precio_unitario = precios[productos.index(producto_seleccionado)]
subtotal = precio_unitario * cantidad

# Cálculo del IVA y total
iva = subtotal * 0.16
total = subtotal + iva

# Mostrar detalles de la cotización
st.write(f"**Producto seleccionado**: {producto_seleccionado}")
st.write(f"**Cantidad**: {cantidad}")
st.write(f"**Precio sin IVA**: ${subtotal:.2f}")
st.write(f"**IVA (16%)**: ${iva:.2f}")
st.write(f"**Precio final**: ${total:.2f}")

# Botón para confirmar la cotización
if st.button("Confirmar cotización"):
    st.success("Cotización confirmada")

# Guardar la cotización en un dataframe
df = pd.DataFrame({
    "Producto": [producto_seleccionado],
    "Cantidad": [cantidad],
    "Precio sin IVA": [subtotal],
    "IVA": [iva],
    "Total": [total]
})

# Mostrar tabla de cotización
st.subheader("Detalle de la cotización:")
st.dataframe(df)








