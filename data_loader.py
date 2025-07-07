import pandas as pd

def cargar_datos(ruta_excel="atenciones_qr.xlsx"):
    # Cargar datos desde la hoja 'datos_limpios', saltando la primera fila
    df = pd.read_excel(ruta_excel, sheet_name="datos_limpios", skiprows=1)

    # Renombrar columnas clave
    df = df.rename(columns={
        "Fecha": "fecha",
        "ID": "id_atencion",
        "estado": "tipo_atencion",
        "TIPO": "validador",
        "[740 720 741 742]": "tipo_validador",
        "AMID": "amid",

    })

    # Convertir fechas
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df = df.dropna(subset=["fecha"])

    # Crear columna Año-Mes tipo "2023-04"
    df["anio_mes"] = df["fecha"].dt.to_period("M").astype(str)

    print("Valores únicos en tipo_validador:")
    print(df["tipo_validador"].unique())

    return df
def cargar_resumen_validadores(ruta_excel="atenciones_qr.xlsx"):
    # Cargar desde la hoja 'Resumen', saltando las 4 primeras filas
    df_resumen = pd.read_excel(
        ruta_excel,
        sheet_name="Resumen",
        skiprows=3,
        usecols="A:E",
        nrows=9965  # Si sabes que hay 9965 filas
    )

    df_resumen = df_resumen.rename(columns={
        "AMID": "amid",
        "¿Ha llegado por falla QR?": "ha_fallado",
        "¿Cuantas Veces?": "veces",
        "¿Cuántos ingresos x QR?": "ingresos_qr",
        "¿Cuántas salidas x QR?": "salidas_qr"
    })
    print("Columnas disponibles en df_resumen:")
    print(df_resumen.columns.tolist())

    df_resumen["ha_fallado"] = df_resumen["ha_fallado"].fillna("No").str.strip()
    return df_resumen

