import streamlit as st
import pandas as pd
from fpdf import FPDF

# Título de la aplicación
st.title("Distribuciones L: Cotizador de Productos Médicos")

# Crear un diccionario de productos y sus precios
productos = {
    "Guantes de Nitrilo (Caja 100 unidades)": 350,
    "Mascarilla KN95 (Paquete de 10)": 150,
    "Gel Antibacterial 500ml": 80,
    "Bata Descartable (Paquete de 5)": 400,
    "Jeringas 5ml (Caja de 100 unidades)": 500,
    "Termómetro Infrarrojo": 1200,
    "Oxímetro de Pulso": 950,
    "Tensiómetro Digital": 1800,
    "Cubrebocas Triple Filtro (Caja de 50)": 100,
    "Alcohol en Gel 1L": 120,
    # Hexyn con condición especial de precios
    "Hexyn Antiséptico Médico": None  # Se asignará dinámicamente
}

# Función para obtener el precio del producto
def obtener_precio(producto, cantidad):
    if producto == "Hexyn Antiséptico Médico":
        if cantidad > 30:
            return 241  # Precio con descuento
        else:
            return 258.62  # Precio sin descuento
    else:
        return productos[producto]

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
    precio_unitario = obtener_precio(producto_seleccionado, cantidad)
    subtotal = precio_unitario * cantidad
    nuevo_producto = {
        "Producto": producto_seleccionado,
        "Cantidad": cantidad,
        "Precio Unitario": precio_unitario,
        "Subtotal": subtotal
    }
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

# Función para generar PDF
def generar_pdf(df, total_sin_iva, iva, total_con_iva):
    pdf = FPDF()
    pdf.add_page()
    
    # Título del documento
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Distribuciones L: Cotización de Productos Médicos", ln=True, align='C')
    
    pdf.ln(10)
    
    # Tabla de productos
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(50, 10, "Producto", border=1)
    pdf.cell(40, 10, "Cantidad", border=1)
    pdf.cell(50, 10, "Precio Unitario", border=1)
    pdf.cell(50, 10, "Subtotal", border=1)
    pdf.ln(10)
    
    pdf.set_font("Arial", '', 12)
    for index, row in df.iterrows():
        pdf.cell(50, 10, row['Producto'], border=1)
        pdf.cell(40, 10, str(int(row['Cantidad'])), border=1)
        pdf.cell(50, 10, f"${row['Precio Unitario']:.2f}", border=1)
        pdf.cell(50, 10, f"${row['Subtotal']:.2f}", border=1)
        pdf.ln(10)
    
    # Totales
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(50, 10, f"Total sin IVA: ${total_sin_iva:.2f}")
    pdf.ln(10)
    pdf.cell(50, 10, f"IVA (16%): ${iva:.2f}")
    pdf.ln(10)
    pdf.cell(50, 10, f"Total con IVA: ${total_con_iva:.2f}")
    
    # Generar archivo PDF
    return pdf.output(dest='S').encode('latin1')

# Botón para descargar la cotización en PDF
if st.button("Descargar cotización en PDF"):
    pdf_content = generar_pdf(df, total_sin_iva, iva, total_con_iva)
    st.download_button(
        label="Descargar PDF",
        data=pdf_content,
        file_name="cotizacion.pdf",
        mime="application/pdf"
    )

# Botón para reiniciar la cotización
if st.button("Reiniciar cotización"):
    st.session_state['cotizacion'] = pd.DataFrame(columns=["Producto", "Cantidad", "Precio Unitario", "Subtotal"])
    st.success("La cotización ha sido reiniciada.")







