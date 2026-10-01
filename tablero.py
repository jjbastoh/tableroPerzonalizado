import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io


# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Tablero de Dibujo",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CSS PERSONALIZADO
# ============================================================

st.markdown(
    """
    <style>

        /* Fondo general */
        .stApp {
            background: linear-gradient(
                135deg,
                #0f172a,
                #1e293b,
                #312e81
            );
            color: white;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(
                180deg,
                #111827,
                #1e1b4b
            );
            border-right: 1px solid rgba(255,255,255,0.1);
        }

        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #ffffff;
        }

        /* Título */
        .titulo {
            text-align: center;
            font-size: 3rem;
            font-weight: 800;
            margin-top: 10px;
            margin-bottom: 5px;
            background: linear-gradient(
                90deg,
                #38bdf8,
                #818cf8,
                #c084fc
            );
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Subtítulo */
        .subtitulo {
            text-align: center;
            color: #cbd5e1;
            font-size: 1.1rem;
            margin-bottom: 30px;
        }

        /* Tarjeta del tablero */
        .canvas-card {
            background: rgba(255,255,255,0.08);
            padding: 25px;
            border-radius: 25px;
            border: 1px solid rgba(255,255,255,0.15);
            box-shadow: 0 20px 50px rgba(0,0,0,0.35);
            backdrop-filter: blur(12px);
            margin: auto;
        }

        /* Caja informativa */
        .info-box {
            background: rgba(59,130,246,0.12);
            border-left: 4px solid #38bdf8;
            padding: 15px;
            border-radius: 10px;
            color: #e2e8f0;
            margin-bottom: 20px;
        }

        /* Separadores */
        hr {
            border-color: rgba(255,255,255,0.15);
        }

        /* Labels */
        label {
            color: #e2e8f0 !important;
            font-weight: 500 !important;
        }

        /* Selectbox */
        div[data-baseweb="select"] > div {
            background-color: rgba(255,255,255,0.08);
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.15);
        }

        /* Color picker */
        div[data-testid="stColorPicker"] {
            margin-bottom: 10px;
        }

        /* Botones */
        .stButton > button,
        .stDownloadButton > button {
            width: 100%;
            border-radius: 10px;
            font-weight: 600;
        }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ENCABEZADO
# ============================================================

st.markdown(
    '<div class="titulo">🎨 Mi Tablero de Dibujo</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">'
    'Crea, dibuja y experimenta con diferentes herramientas'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# ESTADO DE LA APLICACIÓN
# ============================================================

if "clear_canvas" not in st.session_state:
    st.session_state.clear_canvas = False


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🎨 Panel de Diseño")
    st.markdown("---")

    # --------------------------------------------------------
    # DIMENSIONES
    # --------------------------------------------------------

    st.markdown("### 📐 Dimensiones")

    canvas_width = st.slider(
        "Ancho del tablero",
        min_value=300,
        max_value=700,
        value=500,
        step=50
    )

    canvas_height = st.slider(
        "Alto del tablero",
        min_value=200,
        max_value=600,
        value=300,
        step=50
    )

    st.markdown("---")

    # --------------------------------------------------------
    # HERRAMIENTA
    # --------------------------------------------------------

    st.markdown("### 🖌️ Herramienta")

    drawing_mode = st.selectbox(
        "Modo de dibujo",
        (
            "freedraw",
            "line",
            "rect",
            "circle",
            "transform",
            "polygon",
            "point"
        ),
        format_func=lambda x: {
            "freedraw": "✏️ Dibujo libre",
            "line": "📏 Línea",
            "rect": "⬜ Rectángulo",
            "circle": "⭕ Círculo",
            "transform": "🔄 Transformar",
            "polygon": "🔷 Polígono",
            "point": "📍 Punto"
        }[x]
    )

    st.markdown("---")

    # --------------------------------------------------------
    # ESTILO
    # --------------------------------------------------------

    st.markdown("### 🎨 Estilo")

    stroke_width = st.slider(
        "Grosor del trazo",
        min_value=1,
        max_value=30,
        value=5,
        step=1
    )

    stroke_color = st.color_picker(
        "Color del trazo",
        "#38BDF8"
    )

    bg_color = st.color_picker(
        "Color de fondo",
        "#0F172A"
    )

    st.markdown("---")

    # --------------------------------------------------------
    # BOTÓN LIMPIAR
    # --------------------------------------------------------

    if st.button("🗑️ Limpiar tablero", use_container_width=True):
        st.session_state.clear_canvas = True
        st.rerun()

    st.markdown("---")

    st.info(
        "💡 Consejo: usa diferentes colores y herramientas "
        "para crear diseños más interesantes."
    )


# ============================================================
# ÁREA PRINCIPAL
# ============================================================

st.markdown(
    """
    <div class="info-box">
        🖌️ <b>Área de dibujo</b><br>
        Selecciona una herramienta desde el panel izquierdo
        y comienza a crear.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CANVAS
# ============================================================

st.markdown(
    '<div class="canvas-card">',
    unsafe_allow_html=True
)


# Usamos una clave que cambia solamente cuando se solicita
# limpiar el tablero.

canvas_key = f"drawing_canvas_{st.session_state.clear_canvas}"


canvas_result = st_canvas(
    fill_color="rgba(56, 189, 248, 0.25)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=canvas_height,
    width=canvas_width,
    drawing_mode=drawing_mode,
    key=canvas_key,
)


st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# Después de recrear el canvas, volvemos el estado a False.
if st.session_state.clear_canvas:
    st.session_state.clear_canvas = False


# ============================================================
# OBTENER LA IMAGEN DE FORMA SEGURA
# ============================================================

image_data = None

try:
    image_data = canvas_result.image_data

except RuntimeError:
    # Esto ocurre cuando el canvas todavía no tiene
    # una imagen disponible.
    image_data = None

except Exception:
    # Evita que un problema interno de la librería
    # derribe toda la aplicación.
    image_data = None


# ============================================================
# VISTA PREVIA Y DESCARGA
# ============================================================

if image_data is not None:

    st.markdown("---")

    st.markdown("### ✨ Tu creación")

    st.caption(
        "Puedes modificar el tamaño, colores y herramienta "
        "desde el panel lateral."
    )

    # --------------------------------------------------------
    # CONVERTIR A PNG
    # --------------------------------------------------------

    try:

        # image_data normalmente llega como array RGBA.
        image = Image.fromarray(image_data.astype("uint8"))

        # Mostrar imagen
        st.image(
            image,
            caption="Vista previa de tu dibujo",
            width=canvas_width
        )

        # ----------------------------------------------------
        # PREPARAR DESCARGA
        # ----------------------------------------------------

        png_buffer = io.BytesIO()

        image.save(
            png_buffer,
            format="PNG"
        )

        png_buffer.seek(0)

        # ----------------------------------------------------
        # BOTÓN DESCARGAR
        # ----------------------------------------------------

        st.download_button(
            label="⬇️ Descargar dibujo como PNG",
            data=png_buffer,
            file_name="mi_dibujo.png",
            mime="image/png",
            use_container_width=True
        )

    except Exception as e:

        st.warning(
            "No se pudo generar la vista previa de la imagen."
        )


# ============================================================
# INFORMACIÓN ADICIONAL
# ============================================================

with st.expander("ℹ️ Información"):

    st.write(
        "Este tablero permite realizar dibujos utilizando "
        "diferentes herramientas."
    )

    st.write(
        "Puedes seleccionar dibujo libre, líneas, rectángulos, "
        "círculos, polígonos, puntos y transformación."
    )

    st.write(
        "También puedes cambiar el color, el grosor del trazo "
        "y el color de fondo."
    )

requirements.txt




