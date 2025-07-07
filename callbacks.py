from dash import Input, Output
import plotly.express as px
from dash import dcc, html
from dash import dash_table


def registrar_callbacks(app, df, df_resumen):
    @app.callback(
        Output('grafico-barras', 'figure'),
        Input('filtro-fecha', 'start_date'),
        Input('filtro-fecha', 'end_date')
    )
    def actualizar_grafico(start_date, end_date):
        # Filtrar el DataFrame según rango de fechas
        datos_filtrados = df[(df["fecha"] >= start_date) & (df["fecha"] <= end_date)]

        # Agrupar por año-mes y contar
        resumen = (
            datos_filtrados.groupby("anio_mes")
            .size()
            .reset_index(name="cantidad")
            .sort_values("anio_mes")
        )
        print(resumen)
        print(resumen.dtypes)

        # Crear gráfico de barras
        fig = px.bar(resumen,
                     x="anio_mes",
                     y="cantidad",
                     labels={"anio_mes": "Año-Mes", "cantidad": "Cantidad de Atenciones"},
                     text="cantidad")

        fig.update_layout(
            title="Cantidad de Atenciones por Mes",
            xaxis_tickangle=-45,
            plot_bgcolor="#f9f9f9"
        )

        return fig
     # NUEVO CALLBACK → gráfico por tipo de validador
    @app.callback(
        Output('contenedor-tarjetas', 'children'),
        Input('filtro-fecha', 'start_date'),
        Input('filtro-fecha', 'end_date')
    )
    def actualizar_tarjetas(start_date, end_date):
        datos_filtrados = df[(df["fecha"] >= start_date) & (df["fecha"] <= end_date)]
        tipos = [720, 740, 741, 742]
        tarjetas = []

        for tipo in tipos:
            total = (datos_filtrados["tipo_validador"] == tipo).sum()
            tarjetas.append(
                html.Div([
                    html.H4(f"Validador {tipo}"),
                    html.P(f"{total} atenciones", style={"fontSize": "24px", "fontWeight": "bold"})
                ], style={
                    "backgroundColor": "#f2f2f2",
                    "padding": "20px",
                    "margin": "10px",
                    "borderRadius": "10px",
                    "width": "140px",
                    "textAlign": "center",
                    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"
                })
            )

        return tarjetas  # Devuelve solo la lista

    
    @app.callback(
        Output("grafico-pastel", "figure"),
        Input("filtro-fecha", "start_date"),
        Input("filtro-fecha", "end_date")  # requerido aunque no se usa directamente aquí
    )
    def actualizar_grafico_pastel(start_date, end_date):
        total = len(df_resumen)
        con_falla = (df_resumen["ha_fallado"].str.lower() == "sí").sum()
        sin_falla = total - con_falla

        resumen = {
            "Con al menos 1 falla": con_falla,
            "Sin fallas registradas": sin_falla
        }

        fig = px.pie(
            names=list(resumen.keys()),
            values=list(resumen.values()),
            title="Validadores con y sin fallas QR",
            hole=0.4
        )
        return fig
    
    @app.callback(
        Output("tabla-top-validadores", "children"),
        Input("filtro-fecha", "start_date"),
        Input("filtro-fecha", "end_date")
    )
    def mostrar_top_validadores(_, __):
        top_df = (
            df_resumen[df_resumen["veces"] > 0]
            .sort_values("veces", ascending=False)
            .head(10)
            .copy()
        )

        # Renombrar columnas para que se vean como en tu ejemplo
        top_df = top_df.rename(columns={
            "amid": "Validador (AMID)",
            "ha_fallado": "¿Ha fallado?",
            "veces": "Cantidad de fallas",
            "ingresos_qr": "Ingresos QR",
            "salidas_qr": "Salidas QR"
        })

        return dash_table.DataTable(
            columns=[{"name": col, "id": col} for col in top_df.columns],
            data=top_df.to_dict("records"),
            style_cell={"textAlign": "center"},
            style_header={"fontWeight": "bold", "backgroundColor": "#f0f0f0"},
            style_table={"overflowX": "auto", "width": "100%"},
        )
    

    @app.callback(
        Output("resultado-amid", "children"),
        Input("dropdown-amid", "value")
    )
    def mostrar_info_validador(amid):
        if not amid:
            return ""

        fila = df_resumen[df_resumen["amid"] == amid]

        if fila.empty:
            return html.P("Validador no encontrado.")

        fila = fila.rename(columns={
            "ha_fallado": "¿Ha fallado?",
            "veces": "Cantidad de fallas",
            "ingresos_qr": "Ingresos QR",
            "salidas_qr": "Salidas QR"
        })

        fila = fila[["¿Ha fallado?", "Cantidad de fallas", "Ingresos QR", "Salidas QR"]]

        return dash_table.DataTable(
            columns=[{"name": col, "id": col} for col in fila.columns],
            data=fila.to_dict("records"),
            style_cell={"textAlign": "center", "padding": "10px"},
            style_header={"fontWeight": "bold", "backgroundColor": "#f0f0f0"},
            style_table={"width": "80%", "margin": "auto"}
        )


        
        