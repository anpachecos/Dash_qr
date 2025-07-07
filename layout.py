from dash import html, dcc

def crear_layout(df, df_resumen):
    return html.Div([
        html.H1("Atenciones por Falla QR – Laboratorio",style={"textAlign": "center", "margin-bottom": "30px"}),
        html.H6("Versión 1.0", style={"textAlign": "center", "color": "gray", "margin-bottom": "30px"}),

        html.Div([
            html.Label("Rango de Fechas:"),
            dcc.DatePickerRange(
                id='filtro-fecha',
                start_date=df["fecha"].min(),
                end_date=df["fecha"].max(),
                display_format='YYYY-MM-DD'
            ),
        ], style={"margin-bottom": "20px"}),

        dcc.Graph(id='grafico-barras'),

        html.Hr(),

        html.Div([
            html.Div([
                html.H3("Total de Atenciones por Tipo de Validador"),

                html.Div(
                    id='contenedor-tarjetas',
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "repeat(2, 1fr)",  # Forzamos 2 columnas
                        "gap": "10px",
                        "justifyItems": "center",
                        "alignItems": "center"
                    }
                )

            ], style={
                "flex": "1",
                "padding": "10px",
                "minWidth": "300px",
                "maxWidth": "50%",
                "boxSizing": "border-box",
                "display": "flex",
                "flexDirection": "column",
                "justifyContent": "center"
            }),

            html.Div([
                html.H3("Proporción de Validadores con Fallas QR"),
                dcc.Graph(id="grafico-pastel", style={"height": "400px"})
            ], style={
                "flex": "1",
                "padding": "10px",
                "minWidth": "300px",
                "maxWidth": "50%",
                "overflow": "hidden",
                "boxSizing": "border-box"
            })
        ], style={
            "display": "flex",
            "flexDirection": "row",
            "justifyContent": "space-between",
            "flexWrap": "wrap"
        }),

        
        html.Hr(),

        html.Div([
            # Columna izquierda: Top 10
            html.Div([
                html.H3("Top 10 Validadores con Más Fallas QR"),
                dcc.Loading(
                    id="loading-tabla-top",
                    children=[
                        html.Div(id="tabla-top-validadores")
                    ],
                    type="default"
                ),
            ], style={
                "flex": "1",
                "padding": "10px",
                "minWidth": "300px",
                "maxWidth": "50%",
                "boxSizing": "border-box"
            }),

            # Columna derecha: Consulta individual
            html.Div([
                html.H3("Consulta Individual por Validador (AMID)"),
                dcc.Dropdown(
                    id="dropdown-amid",
                    options=[{"label": str(a), "value": a} for a in df_resumen["amid"].dropna().unique()],
                    placeholder="Selecciona un validador"
                ),
                html.Div(id="resultado-amid", style={"marginTop": "20px"})
            ], style={
                "flex": "1",
                "padding": "10px",
                "minWidth": "300px",
                "maxWidth": "50%",
                "boxSizing": "border-box"
            })
        ], style={
            "display": "flex",
            "flexDirection": "row",
            "justifyContent": "space-between",
            "flexWrap": "wrap"
        }),
        html.Footer(
            html.P("Desarrollado por Antonia Pacheco", style={"textAlign": "center", "marginTop": "15px", "color": "gray"}),
            style={"marginTop": "50px", "padding": "20px", "backgroundColor": "#f8f9fa", "borderTop": "1px solid #e9ecef"}
        )
    ])
