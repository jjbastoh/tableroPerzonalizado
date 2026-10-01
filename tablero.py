import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io


# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Mi Tablero de Dibujo",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# COLORES
# ============================================================

COLOR_FONDO = "#EAF6F8"
COLOR_CELESTE = "#9DD9E8"
COLOR_CELESTE_OSCURO = "#5FAFC2"
COLOR_BEIGE = "#F3E7D3"
COLOR_CREMA = "#FFFDF8"
COLOR_TEXTO = "#40545A"
COLOR_BORDE = "#C9DDE0"
COLOR_TRAZO = "#5FAFC2"


# ============================================================
# CSS
# ============================================================

st.markdown(
    f"""
    <style>

        /* ================================================
           FONDO GENERAL
           ================================================ */

        .stApp {{
            background:
                linear-gradient(
                    135deg,
                    {COLOR_FONDO} 0%,
                    {COLOR_BEIGE} 50%,
                    #F8F5EE 100%
                );

            color: {COLOR_TEXTO};
        }}


        /* ================================================
           SIDEBAR
           ================================================ */

        section[data-testid="stSidebar"] {{
            background:
                linear-gradient(
                    180deg,
                    #DDF2F5 0%,
                    #EAF6F8 45%,
                    #F3E7D3 100%
                );

            border-right:
                1px solid {COLOR_BORDE};
        }}


        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {{
            color: {COLOR_TEXTO};
        }}


        /* ================================================
           TÍTULO
           ================================================ */

        .titulo {{
            text-align: center;

            font-size: 3rem;

            font-weight: 800;

            margin-top: 10px;

            margin-bottom: 5px;

            color: {COLOR_CELESTE_OSCURO};
        }}


        /* ================================================
           SUBTÍTULO
           ================================================ */

        .subtitulo {{
            text-align: center;

            color: #68777A;

            font-size: 1.1rem;

            margin-bottom: 30px;
        }}


        /* ================================================
           TARJETA DEL TABLERO
           ================================================ */

        .canvas-card {{
            background:
                rgba(255, 253, 248, 0.88);

            padding: 25px;

            border-radius: 24px;

            border:
                1px solid {COLOR_BORDE};

            box-shadow:
                0 15px 40px rgba(80, 110, 115, 0.16);

            margin: auto;
        }}


        /* ================================================
           CAJA DE INFORMACIÓN
           ================================================ */

        .info-box {{
            background:
                rgba(157, 217, 232, 0.28);

            border-left:
                5px solid {COLOR_CELESTE_OSCURO};

            padding: 16px;

            border-radius: 12px;

            color: {COLOR_TEXTO};

            margin-bottom: 20px;
        }}


        /* ================================================
           TEXTO GENERAL
           ================================================ */

        p,
        span,
        div {{
            color: inherit;
        }}


        /* ================================================
           LABELS
           ================================================ */

        label {{
            color: {COLOR_TEXTO} !important;

            font-weight: 600 !important;
        }}


        /* ================================================
           SELECTBOX
           ================================================ */

        div[data-baseweb="select"] > div {{
            background-color:
                rgba(255, 253, 248, 0.85);

            border-radius: 10px;

            border:
                1px solid {COLOR_BORDE};
        }}


        /* ================================================
           SLIDERS
           ================================================ */

        div[data-baseweb="slider"] {{
            margin-bottom: 12px;
        }}


        /* ================================================
           BOTONES
           ================================================ */

        .stButton > button,
        .stDownloadButton > button {{

            width: 100%;

            border-radius: 12px;

            font-weight: 700;

            background-color:
                {COLOR_CELESTE_OSCURO};

            color: white;

            border:
                1px solid {COLOR_CELESTE_OSCURO};

            transition: 0.2s;
        }}


        .stButton > button:hover,
        .stDownloadButton > button:hover {{

            background-color:
                #4C9EAF;

            color: white;

            border-color:
                #4C9EAF;
        }}


        /* ================================================
           EXPANDER
           ================================================ */

        div[data-testid="stExpander"] {{

            background:
                rgba(255, 253, 248, 0.75);

            border:
                1px solid {COLOR_BORDE};

            border-radius: 12px;
        }}


        /* ================================================
           ALERTA INFO
           ================================================ */

        div[data-testid="stAlert"] {{

            background:
                rgba(243, 231, 211, 0.85);

            border-radius: 12px;
        }}

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
# ESTADO DEL CANVAS
# ============================================================

if "canvas_version" not in st.session_state:
    st.session_state.canvas_version = 0


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🎨 Panel de Diseño")

    st.markdown("---")


    # ========================================================
    # DIMENSIONES
    # ========================================================

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


    # ========================================================
    # HERRAMIENTA
    # ========================================================

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


    # ========================================================
    # ESTILO
    # ========================================================

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
        COLOR_TRAZO
    )


    bg_color = st.color_picker(
        "Color de fondo",
        COLOR_CREMA
    )


    st.markdown("---")


    # ========================================================
    # BOTÓN LIMPIAR
    # ========================================================

    if st.button(
        "🗑️ Limpiar tablero",
        use_container_width=True
    ):

        st.session_state.canvas_version += 1

        st.rerun()


    st.markdown("---")


    # ========================================================
    # CONSEJO
    # ========================================================

    st.info(
        "💡 Consejo: combina diferentes colores y herramientas "
        "para crear diseños originales."
    )


# ============================================================
# INFORMACIÓN DEL TABLERO
# ============================================================

st.markdown(
    """
    <div class="info-box">

        🖌️ <strong>Área de dibujo</strong><br>

        Selecciona una herramienta desde el panel izquierdo
        y comienza a crear.

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CONTENEDOR DEL CANVAS
# ============================================================

st.markdown(
    '<div class="canvas-card">',
    unsafe_allow_html=True
)


# ============================================================
# CANVAS
# ============================================================

canvas_result = st_canvas(

    fill_color="rgba(157, 217, 232, 0.25)",

    stroke_width=stroke_width,

    stroke_color=stroke_color,

    background_color=bg_color,

    height=canvas_height,

    width=canvas_width,

    drawing_mode=drawing_mode,

    key=f"drawing_canvas_{st.session_state.canvas_version}"

)


st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# OBTENER IMAGEN DE FORMA SEGURA
# ============================================================

image_data = None

try:

    image_data = canvas_result.image_data

except RuntimeError:

    image_data = None

except Exception:

    image_data = None


# ============================================================
# VISTA PREVIA
# ============================================================

if image_data is not None:

    st.markdown("---")

    st.markdown("### ✨ Tu creación")

    st.caption(
        "Aquí puedes ver una vista previa de tu dibujo."
    )


    try:

        image = Image.fromarray(
            image_data.astype("uint8")
        )


        # ====================================================
        # MOSTRAR DIBUJO
        # ====================================================

        st.image(
            image,
            caption="Vista previa de tu dibujo",
            width=canvas_width
        )


        # ====================================================
        # CREAR PNG
        # ====================================================

        png_buffer = io.BytesIO()

        image.save(
            png_buffer,
            format="PNG"
        )

        png_buffer.seek(0)


        # ====================================================
        # BOTÓN DESCARGA
        # ====================================================

        st.download_button(

            label="⬇️ Descargar dibujo como PNG",

            data=png_buffer.getvalue(),

            file_name="mi_dibujo.png",

            mime="image/png",

            use_container_width=True

        )


    except Exception:

        st.warning(
            "No se pudo generar la vista previa del dibujo."
        )


# ============================================================
# INFORMACIÓN
# ============================================================

with st.expander("ℹ️ Información"):

    st.write(
        "Este tablero permite realizar dibujos utilizando "
        "diferentes herramientas."
    )

    st.write(
        "Puedes utilizar dibujo libre, líneas, rectángulos, "
        "círculos, polígonos, puntos y transformación."
    )

    st.write(
        "También puedes cambiar el color, el grosor del trazo "
        "y el color de fondo."
    )

