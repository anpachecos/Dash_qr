import dash
from data_loader import cargar_datos, cargar_resumen_validadores
from layout import crear_layout
from callbacks import registrar_callbacks

# Cargar datos desde Excel
df = cargar_datos("atenciones_qr.xlsx")
df_resumen = cargar_resumen_validadores("atenciones_qr.xlsx")

# Crear app Dash
app = dash.Dash(__name__)
app.title = "Dashboard QR"

# Definir layout
app.layout = crear_layout(df, df_resumen)

# Registrar lógica de interactividad
registrar_callbacks(app, df, df_resumen)

# Ejecutar servidor
if __name__ == "__main__":
    app.run(debug=True)
