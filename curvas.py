
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# CONFIGURACION DE LA APLICACION
# ==========================================

st.set_page_config(
    page_title="Graficador Matematico 3D",
    page_icon="📊",
    layout="wide"
)

st.title("📊 GRAFICADOR MATEMATICO 3D")
st.write(
    "Aplicacion interactiva para representar "
    "curvas y superficies matematicas."
)

st.sidebar.title("MENU PRINCIPAL")

modo = st.sidebar.selectbox(
    "Selecciona una modalidad:",
    ["Curvas 3D", "Superficies 3D"]
)

if modo == "Curvas 3D":
    figura = st.sidebar.selectbox(
        "Selecciona una curva:",
        ["Elipse", "Circunferencia", "Recta"]
    )
else:
    figura = st.sidebar.selectbox(
        "Selecciona una superficie:",
        ["Elipsoide", "Esfera", "Plano"]
    )

st.header("Configuracion de parametros")

# ==========================================
# INGRESO DE PARAMETROS
# ==========================================

if figura == "Elipse":

    col1, col2, col3 = st.columns(3)

    a = col1.number_input(
        "Semieje X (a)", min_value=0.1, value=5.0
    )
    b = col2.number_input(
        "Semieje Y (b)", min_value=0.1, value=3.0
    )
    z0 = col3.number_input(
        "Altura Z", value=0.0
    )

elif figura == "Circunferencia":

    col1, col2 = st.columns(2)

    r = col1.number_input(
        "Radio (r)", min_value=0.1, value=5.0
    )
    z0 = col2.number_input(
        "Altura Z", value=0.0
    )

elif figura == "Recta":

    st.write("Punto inicial de la recta:")

    col1, col2, col3 = st.columns(3)

    x0 = col1.number_input("X inicial", value=0.0)
    y0 = col2.number_input("Y inicial", value=0.0)
    z0 = col3.number_input("Z inicial", value=0.0)

    st.write("Vector de direccion:")

    col1, col2, col3 = st.columns(3)

    dx = col1.number_input("Direccion X", value=1.0)
    dy = col2.number_input("Direccion Y", value=1.0)
    dz = col3.number_input("Direccion Z", value=1.0)

    tmin = st.number_input("Valor minimo de t", value=-10.0)
    tmax = st.number_input("Valor maximo de t", value=10.0)

elif figura == "Elipsoide":

    col1, col2, col3 = st.columns(3)

    a = col1.number_input(
        "Radio X (a)", min_value=0.1, value=5.0
    )
    b = col2.number_input(
        "Radio Y (b)", min_value=0.1, value=3.0
    )
    c = col3.number_input(
        "Radio Z (c)", min_value=0.1, value=2.0
    )

elif figura == "Esfera":

    r = st.number_input(
        "Radio de la esfera", min_value=0.1, value=5.0
    )

elif figura == "Plano":

    st.write("Ecuacion del plano: z = ax + by + d")

    col1, col2, col3 = st.columns(3)

    a = col1.number_input("Coeficiente a", value=1.0)
    b = col2.number_input("Coeficiente b", value=1.0)
    d = col3.number_input("Constante d", value=0.0)

    rango = st.slider(
        "Rango de los ejes X e Y",
        min_value=5,
        max_value=30,
        value=10
    )

# ==========================================
# BOTON PARA GENERAR GRAFICA
# ==========================================

if st.button("GENERAR GRAFICA 3D", type="primary"):

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    ecuacion = ""

    # ======================================
    # 1. ELIPSE
    # ======================================

    if figura == "Elipse":

        t = np.linspace(0, 2*np.pi, 500)

        x = a * np.cos(t)
        y = b * np.sin(t)
        z = np.full_like(t, z0)

        ax.plot(x, y, z, linewidth=2, label="Elipse")

        ecuacion = (
            rf"\frac{{x^2}}{{{a}^2}} + "
            rf"\frac{{y^2}}{{{b}^2}} = 1,\quad z={z0}"
        )

    # ======================================
    # 2. CIRCUNFERENCIA
    # ======================================

    elif figura == "Circunferencia":

        t = np.linspace(0, 2*np.pi, 500)

        x = r * np.cos(t)
        y = r * np.sin(t)
        z = np.full_like(t, z0)

        ax.plot(
            x, y, z,
            linewidth=2,
            label="Circunferencia"
        )

        ecuacion = rf"x^2+y^2={r}^2,\quad z={z0}"

    # ======================================
    # 3. RECTA
    # ======================================

    elif figura == "Recta":

        if tmin >= tmax:
            st.error(
                "El valor minimo de t debe ser menor "
                "que el valor maximo."
            )
            st.stop()

        if dx == 0 and dy == 0 and dz == 0:
            st.error(
                "El vector de direccion no puede ser cero."
            )
            st.stop()

        t = np.linspace(tmin, tmax, 500)

        x = x0 + dx*t
        y = y0 + dy*t
        z = z0 + dz*t

        ax.plot(x, y, z, linewidth=2, label="Recta")

        ecuacion = (
            rf"(x,y,z)=({x0},{y0},{z0})"
            rf"+t({dx},{dy},{dz})"
        )

    # ======================================
    # 4. ELIPSOIDE
    # ======================================

    elif figura == "Elipsoide":

        u = np.linspace(0, 2*np.pi, 100)
        v = np.linspace(0, np.pi, 100)

        U, V = np.meshgrid(u, v)

        x = a*np.cos(U)*np.sin(V)
        y = b*np.sin(U)*np.sin(V)
        z = c*np.cos(V)

        ax.plot_surface(
            x, y, z,
            cmap="viridis",
            alpha=0.85,
            edgecolor="none"
        )

        ecuacion = (
            rf"\frac{{x^2}}{{{a}^2}}+"
            rf"\frac{{y^2}}{{{b}^2}}+"
            rf"\frac{{z^2}}{{{c}^2}}=1"
        )

    # ======================================
    # 5. ESFERA
    # ======================================

    elif figura == "Esfera":

        u = np.linspace(0, 2*np.pi, 100)
        v = np.linspace(0, np.pi, 100)

        U, V = np.meshgrid(u, v)

        x = r*np.cos(U)*np.sin(V)
        y = r*np.sin(U)*np.sin(V)
        z = r*np.cos(V)

        ax.plot_surface(
            x, y, z,
            cmap="plasma",
            alpha=0.85,
            edgecolor="none"
        )

        ecuacion = rf"x^2+y^2+z^2={r}^2"

    # ======================================
    # 6. PLANO
    # ======================================

    elif figura == "Plano":

        x = np.linspace(-rango, rango, 50)
        y = np.linspace(-rango, rango, 50)

        X, Y = np.meshgrid(x, y)

        Z = a*X + b*Y + d

        ax.plot_surface(
            X, Y, Z,
            cmap="coolwarm",
            alpha=0.85,
            edgecolor="none"
        )

        ecuacion = rf"z={a}x+{b}y+{d}"

    # ======================================
    # CONFIGURACION DE LA GRAFICA
    # ======================================

    ax.set_xlabel("Eje X")
    ax.set_ylabel("Eje Y")
    ax.set_zlabel("Eje Z")

    ax.set_title(f"{figura} en 3D")

    ax.grid(True)
    ax.set_box_aspect((1, 1, 1))

    if figura in ["Elipse", "Circunferencia", "Recta"]:
        ax.legend()

    st.pyplot(fig, use_container_width=True)

    plt.close(fig)

    # ======================================
    # MOSTRAR ECUACION
    # ======================================

    st.subheader("Ecuacion matematica")
    st.latex(ecuacion)

    st.success("Grafica generada correctamente.")

elif opcion == "Plano":
    st.subheader("Dashboard: Gráfica de un plano en 3D")

    st.write("Ecuación general: Ax + By + Cz + D = 0")

    col1, col2 = st.columns(2)

    with col1:
        A = st.number_input("Coeficiente A", value=2.0)
        B = st.number_input("Coeficiente B", value=3.0)

    with col2:
        C = st.number_input("Coeficiente C", value=1.0)
        D = st.number_input("Coeficiente D", value=-6.0)

    if st.button("Graficar plano"):
        if A == 0 and B == 0 and C == 0:
            st.error("Debes ingresar al menos un coeficiente distinto de cero.")
        else:
            valores = np.linspace(-10, 10, 50)
            X, Y = np.meshgrid(valores, valores)

            fig = plt.figure(figsize=(9, 7))
            ax = fig.add_subplot(111, projection="3d")

            if C != 0:
                Z = (-A * X - B * Y - D) / C
                ax.plot_surface(X, Y, Z, alpha=0.7, cmap="viridis")

            elif B != 0:
                Y_plano = (-A * valores - D) / B
                Y, Z = np.meshgrid(Y_plano, valores)
                X = np.tile(valores, (len(valores), 1))
                ax.plot_surface(X, Y, Z, alpha=0.7, cmap="viridis")

            else:
                X_plano = -D / A
                Y, Z = np.meshgrid(valores, valores)
                X = np.full_like(Y, X_plano)
                ax.plot_surface(X, Y, Z, alpha=0.7, cmap="viridis")

            ax.set_xlabel("Eje X")
            ax.set_ylabel("Eje Y")
            ax.set_zlabel("Eje Z")
            ax.set_title("Representación del plano en 3D")

            st.pyplot(fig)

            st.success(
                f"Ecuación del plano: {A}x + {B}y + {C}z + ({D}) = 0"
            )
