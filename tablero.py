TypeError: This app has encountered an error. The original error message is redacted to prevent data leaks. Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app).
Traceback:
File "/mount/src/tableroperzonalizado/tablero.py", line 239, in <module>
    canvas_result = st_canvas(
                    ^^^^^^^^^^
""", unsafe_allow_html=True)


# ============================================================
# TÍTULO
# ============================================================

st.markdown(
    '<div class="main-title">💭 Pizarra de Pensamiento</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Dibuja libremente tus ideas y posteriormente conviértelas '
    'en una nube de pensamiento inteligente.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Configuración")

    # --------------------------------------------------------
    # Nombre
    # --------------------------------------------------------

    st.subheader("📝 Tu proyecto")

    project_name = st.text_input(
        "Nombre del tablero",
        value="Mi nube de pensamiento"
    )

    st.divider()

    # --------------------------------------------------------
    # DIMENSIONES
    # --------------------------------------------------------

    st.subheader("📐 Dimensiones")

    canvas_width = st.slider(
        "Ancho",
        min_value=300,
        max_value=1000,
        value=600,
        step=50
    )

    canvas_height = st.slider(
        "Alto",
        min_value=200,
        max_value=700,
        value=400,
        step=50
    )

    st.caption(
        f"📏 Tamaño actual: {canvas_width} × {canvas_height}px"
    )

    st.divider()

    # --------------------------------------------------------
    # HERRAMIENTA
    # --------------------------------------------------------

    st.subheader("🖌️ Herramienta")

    drawing_mode = st.selectbox(
        "Selecciona una herramienta",
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
            "freedraw": "✏️ Lápiz",
            "line": "📏 Línea",
            "rect": "⬜ Rectángulo",
            "circle": "⭕ Círculo",
            "transform": "🔄 Mover / Transformar",
            "polygon": "🔷 Polígono",
            "point": "📍 Punto"
        }.get(x, x)
    )

    # --------------------------------------------------------
    # GROSOR
    # --------------------------------------------------------

    stroke_width = st.slider(
        "Grosor del trazo",
        min_value=1,
        max_value=40,
        value=5
    )

    # --------------------------------------------------------
    # COLOR TRAZO
    # --------------------------------------------------------

    stroke_color = st.color_picker(
        "🎨 Color del trazo",
        "#000000"
    )

    # --------------------------------------------------------
    # COLOR FONDO
    # --------------------------------------------------------

    bg_color = st.color_picker(
        "🖼️ Color del fondo",
        "#FFFFFF"
    )

    st.divider()

    # --------------------------------------------------------
    # ACCIONES
    # --------------------------------------------------------

    st.subheader("⚡ Acciones")

    show_grid = st.checkbox(
        "Mostrar cuadrícula",
        value=False
    )


# ============================================================
# CABECERA DEL TABLERO
# ============================================================

col1, col2 = st.columns([4, 1])

with col1:

    st.subheader(
        f"🧠 {project_name}"
    )

with col2:

    st.caption(
        "Área de trabajo"
    )


# ============================================================
# FONDO
# ============================================================

# Creamos una cuadrícula opcional mediante CSS visual.
if show_grid:

    st.markdown(
        """
        <style>
        .canvas-container {
            background-image:
                linear-gradient(#e2e8f0 1px, transparent 1px),
                linear-gradient(90deg, #e2e8f0 1px, transparent 1px);
            background-size: 25px 25px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# CANVAS
# ============================================================

canvas_result = st_canvas(

    fill_color="rgba(255, 165, 0, 0.2)",

    stroke_width=stroke_width,

    stroke_color=stroke_color,

    background_color=bg_color,

    height=canvas_height,

    width=canvas_width,

    drawing_mode=drawing_mode,

    display_toolbar=True,

    key="thinking_board"

)


# ============================================================
# INFORMACIÓN
# ============================================================

if canvas_result.image_data is not None:

    st.markdown(
        f"""
        <div class="info-box">

        <b>💭 Espacio de pensamiento activo</b><br>

        Puedes dibujar palabras, círculos, flechas,
        conexiones y cualquier elemento que represente
        tus ideas.

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# BOTONES
# ============================================================

st.divider()

col1, col2, col3 = st.columns(3)


# ------------------------------------------------------------
# DESCARGAR
# ------------------------------------------------------------

with col1:

    if canvas_result.image_data is not None:

        image = Image.fromarray(
            canvas_result.image_data.astype("uint8")
        )

        buffer = io.BytesIO()

        image.save(
            buffer,
            format="PNG"
        )

        st.download_button(
            label="⬇️ Descargar dibujo",
            data=buffer.getvalue(),
            file_name=f"{project_name}.png",
            mime="image/png",
            use_container_width=True
        )


# ------------------------------------------------------------
# ESTADO
# ------------------------------------------------------------

with col2:

    st.metric(
        "Tamaño",
        f"{canvas_width} × {canvas_height}"
    )


# ------------------------------------------------------------
# PRÓXIMO PASO
# ------------------------------------------------------------

with col3:

    convertir = st.button(
        "🧠 Convertir en nube",
        type="primary",
        use_container_width=True
    )


# ============================================================
# CONVERTIR
# ============================================================

if convertir:

    if canvas_result.image_data is None:

        st.warning(
            "Primero dibuja algo en el tablero."
        )

    else:

        st.success(
            "✅ Dibujo preparado para convertirlo "
            "en una nube de pensamiento."
        )

        st.info(
            "El siguiente paso es conectar este botón "
            "con la inteligencia artificial para detectar "
            "las ideas, palabras y relaciones del dibujo."
        )
