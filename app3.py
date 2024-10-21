import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Distribuciones L", layout="wide")

# Función para generar el PDF con logo ajustado
def generar_pdf(df, total_sin_iva, iva, total_con_iva):
    pdf = FPDF()
    pdf.add_page()

    # Ruta del logo guardado en tu entorno de Streamlit
    logo_path = "/mnt/data/LOGOLEON.png"

    # Agregar logo más pequeño y en la parte superior sin interferir con el texto
    pdf.image(logo_path, x=85, y=10, w=40)  # Logo más pequeño y bien posicionado
    pdf.ln(40)  # Aumentar el espacio debajo del logo para que no se superponga con el texto

    # Datos de la empresa
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Distribuciones L: Productos Médicos", ln=True, align='C')

    # Datos de contacto
    pdf.set_font("Arial", '', 10)
    pdf.cell(200, 10, "Teléfono: +52 33 25 36 10 73", ln=True, align='C')
    pdf.cell(200, 10, "Correo: DistribucionesMedLeon@gmail.com", ln=True, align='C')

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

    # Términos y condiciones
    pdf.ln(20)
    pdf.set_font("Arial", '', 10)
    pdf.multi_cell(200, 10, "Términos y condiciones: Esta cotización es válida por 15 días. Los precios pueden variar sin previo aviso. "
                            "El cliente es responsable de revisar las especificaciones del producto antes de la compra.")

    # Generar archivo PDF
    return pdf.output(dest='S').encode('latin1')

# Página de inicio (Home)
def mostrar_home():
    # Mostrar el logo ya cargado directamente desde tu entorno
    st.image("/mnt/data/LOGOLEON.png", use_column_width=True)

    # Después del logo, el contenido de la página
    st.markdown("<h1 style='text-align: center; color: black;'>Bienvenidos a Distribuciones L: Productos Médicos</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: black;'>Nos especializamos en la venta de productos médicos de alta calidad.</h3>", unsafe_allow_html=True)

    # Información del producto Hexyn Antiséptico Médico
    st.markdown("<h4 style='color: black;'>Producto que ofrecemos:</h4>", unsafe_allow_html=True)
    st.write("- **Hexyn Antiséptico Médico**: Desde $241 MXN (para compras mayores a 30 unidades).")

    # Información de contacto
    st.markdown("<h4 style='text-align: center; color: black;'>Teléfono: +52 33 25 36 10 73</h4>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: black;'>Correo electrónico: DistribucionesMedLeon@gmail.com</h4>", unsafe_allow_html=True)

# Página de cotización con acceso restringido por contraseña
def mostrar_cotizacion():
    st.header("Cotización")
    
    # Continuamos con la funcionalidad de la cotización
    if 'cotizacion' not in st.session_state:
        st.session_state['cotizacion'] = pd.DataFrame(columns=["Producto", "Cantidad", "Precio Unitario", "Subtotal"])

    # Solo se muestra Hexyn Antiséptico Médico
    productos = {
        "Hexyn Antiséptico Médico": None  # Se asignará dinámicamente
    }

    # Función para obtener el precio del producto
    def obtener_precio(cantidad):
        if cantidad > 30:
            return 241  # Precio con descuento
        else:
            return 258.62  # Precio sin descuento

    # Formulario para agregar productos
    with st.form(key='formulario_producto'):
        col1, col2 = st.columns(2)
        with col1:
            producto_seleccionado = "Hexyn Antiséptico Médico"
            st.markdown(f"**Producto seleccionado**: {producto_seleccionado}")
        with col2:
            cantidad = st.number_input("Cantidad", min_value=1, value=1)
        agregar = st.form_submit_button("Agregar a la cotización")

    # Agregar producto a la cotización
    if agregar:
        precio_unitario = obtener_precio(cantidad)
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

        # Formateo de tabla y totales
        st.table(df.style.format({
            "Cantidad": "{:.0f}",
            "Precio Unitario": "${:,.2f}",
            "Subtotal": "${:,.2f}"
        }).set_properties(**{'text-align': 'center'}))

        col_total1, col_total2, col_total3 = st.columns(3)
        with col_total1:
            st.markdown(f"<b style='color: black;'>Total sin IVA:</b>\n${total_sin_iva:,.2f}", unsafe_allow_html=True)
        with col_total2:
            st.markdown(f"<b style='color: black;'>IVA (16%):</b>\n${iva:,.2f}", unsafe_allow_html=True)
        with col_total3:
            st.markdown(f"<b style='color: black;'>Total con IVA:</b>\n${total_con_iva:,.2f}", unsafe_allow_html=True)

        # Botón para descargar PDF
        if st.button("Descargar cotización en PDF"):
            pdf_content = generar_pdf(df, total_sin_iva, iva, total_con_iva)
            st.download_button(
                label="Descargar PDF",
                data=pdf_content,
                file_name="cotizacion_distribuciones_l.pdf",
                mime="application/pdf"
            )

    # Botón para reiniciar la cotización
    if st.button("Reiniciar cotización"):
        st.session_state['cotizacion'] = pd.DataFrame(columns=["Producto", "Cantidad", "Precio Unitario", "Subtotal"])
        st.success("La cotización ha sido reiniciada.")

# Manejo de navegación
def acceso_cotizacion():
    password = st.text_input("Introduce la contraseña", type="password")
    if password == "Leon2125":
        mostrar_cotizacion()
    elif password != "":
        st.error("Contraseña incorrecta")

# Barra de navegación en la parte superior izquierda
menu = st.sidebar.selectbox("Navegación", ["Home", "Cotización"])

if menu == "Home":
    mostrar_home()
elif menu == "Cotización":
    acceso_cotizacion()














