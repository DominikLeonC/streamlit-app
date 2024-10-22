import streamlit as st
import pandas as pd
from fpdf import FPDF
from PIL import Image

# Configuración de la página
st.set_page_config(page_title="Distribuciones L", layout="wide")

# Función para generar el PDF con el nombre del cliente, ajuste de cuadro y términos al final
def generar_pdf(df, total_sin_iva, iva, total_con_iva, cliente):
    pdf = FPDF()
    pdf.add_page()

    # Ruta del logo guardado en tu entorno de Streamlit
    logo_path = "LOGOLEON.png"

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

    # Nombre del cliente
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, f"Cliente: {cliente}", ln=True, align='C')

    pdf.ln(10)

    # Tabla de productos
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(90, 10, "Producto", border=1)
    pdf.cell(40, 10, "Cantidad", border=1)
    pdf.cell(30, 10, "Precio Unitario", border=1)
    pdf.cell(30, 10, "Subtotal", border=1)
    pdf.ln(10)

    pdf.set_font("Arial", '', 12)
    for index, row in df.iterrows():
        pdf.multi_cell(90, 10, row['Producto'], border=1)  # Ajuste del ancho de celda para evitar que el texto se salga
        pdf.cell(40, -10, str(int(row['Cantidad'])), border=1)
        pdf.cell(30, -10, f"${row['Precio Unitario']:.2f}", border=1)
        pdf.cell(30, -10, f"${row['Subtotal']:.2f}", border=1)
        pdf.ln(10)

    # Totales
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(50, 10, f"Total sin IVA: ${total_sin_iva:.2f}")
    pdf.ln(10)
    pdf.cell(50, 10, f"IVA (16%): ${iva:.2f}")
    pdf.ln(10)
    pdf.cell(50, 10, f"Total con IVA: ${total_con_iva:.2f}")

    # Términos y condiciones al final
    pdf.ln(20)
    pdf.set_font("Arial", '', 10)
    pdf.multi_cell(200, 10, "Términos y condiciones: Esta cotización es válida por 15 días. Los precios pueden variar sin previo aviso. "
                            "El cliente es responsable de revisar las especificaciones del producto antes de la compra.")

    # Generar archivo PDF
    return pdf.output(dest='S').encode('latin1')

# Página de inicio (Home)
def mostrar_home():
    # Centrar contenido con HTML para asegurar un formato correcto
    st.markdown("""
        <div style="text-align: center;">
            <h1 style='color: black;'>Bienvenidos a Distribuciones L: Productos Médicos</h1>
        </div>
        """, unsafe_allow_html=True)

    # Mostrar el logo centrado debajo del título
    try:
        logo = Image.open("LOGOLEON.png")  # Asegúrate de que el archivo del logo esté en el directorio adecuado
        st.image(logo, use_column_width=False, width=150)
    except FileNotFoundError:
        st.error("El archivo del logo no se encontró. Asegúrate de que esté en el directorio correcto.")

    # Después del logo, el contenido de la página
    st.markdown("<h3 style='text-align: center; color: black;'>Nos especializamos en la venta de productos médicos de alta calidad.</h3>", unsafe_allow_html=True)

    # Información de los productos y sus fichas técnicas como imágenes centradas
    st.markdown("<h4 style='text-align: center; color: black;'>Productos que ofrecemos:</h4>", unsafe_allow_html=True)

    # Producto Hexyn con ficha técnica como imagen centrada
    st.markdown("""
        <div style="text-align: center;">
            <p><b>Hexyn Antiséptico Médico</b>: Desde $241 MXN (para compras mayores a 30 unidades).</p>
            <p>Ficha técnica del producto:</p>
        </div>
        """, unsafe_allow_html=True)

    try:
        ficha_hexyn = Image.open("FichaTHexyn.png")  # Asegúrate de que el archivo de la ficha técnica esté en el directorio adecuado
        st.image(ficha_hexyn, use_column_width=False, width=500)  # Ajuste de tamaño
    except FileNotFoundError:
        st.error("El archivo de la ficha técnica de Hexyn no se encontró. Asegúrate de que esté en el directorio correcto.")

    # Producto Jabón Clorexi con ficha técnica como imagen centrada
    st.markdown("""
        <div style="text-align: center;">
            <p><b>Jabón Clorexi de 1L (Automático)</b>: $405.17 MXN (sin IVA).</p>
            <p>Ficha técnica del producto:</p>
        </div>
        """, unsafe_allow_html=True)

    try:
        ficha_jabon = Image.open("FichaTJab.png")  # Asegúrate de que el archivo de la ficha técnica esté en el directorio adecuado
        st.image(ficha_jabon, use_column_width=False, width=500)  # Ajuste de tamaño
    except FileNotFoundError:
        st.error("El archivo de la ficha técnica de Jabón Clorexi no se encontró. Asegúrate de que esté en el directorio correcto.")

    st.markdown("""
        <div style="text-align: center;">
            <p><b>Jabón Clorexi de 1L (Manual)</b>: $362.06 MXN (sin IVA).</p>
        </div>
        """, unsafe_allow_html=True)

    # Información de contacto centrada
    st.markdown("""
        <div style="text-align: center;">
            <h4>Teléfono: +52 33 25 36 10 73</h4>
            <h4>Correo electrónico: DistribucionesMedLeon@gmail.com</h4>
        </div>
        """, unsafe_allow_html=True)

# Página de cotización con acceso restringido por contraseña
def mostrar_cotizacion():
    st.header("Cotización")
    
    # Campo para ingresar el nombre del cliente
    cliente = st.text_input("Nombre del cliente")

    # Continuamos con la funcionalidad de la cotización
    if 'cotizacion' not in st.session_state:
        st.session_state['cotizacion'] = pd.DataFrame(columns=["Producto", "Cantidad", "Precio Unitario", "Subtotal"])

    # Función para obtener el precio del producto
    def obtener_precio(producto, cantidad):
        if producto == "Hexyn Antiséptico Médico":
            return 241 if cantidad > 30 else 258.62
        elif producto == "Jabón Clorexi de 1L (Automático)":
            return 405.17  # Precio sin IVA
        elif producto == "Jabón Clorexi de 1L (Manual)":
            return 362.06  # Precio sin IVA

    # Formulario para agregar productos
    with st.form(key='formulario_producto'):
        col1, col2 = st.columns(2)
        with col1:
            producto_seleccionado = st.selectbox("Selecciona el producto", ["Hexyn Antiséptico Médico", "Jabón Clorexi de 1L (Automático)", "Jabón Clorexi de 1L (Manual)"])
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
            pdf_content = generar_pdf(df, total_sin_iva, iva, total_con_iva, cliente)
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














