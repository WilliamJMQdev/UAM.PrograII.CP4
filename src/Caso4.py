import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, messagebox

#Se importa la libreria para mostrar mensajes de error
import os

##FUNCIONES PRINCIPALES
def LoadCSV(file_path):
    try:
        data = pd.read_csv(file_path, sep=";")

        # Convertir las columnas 'Cantidad' y 'PrecioUnitario' a tipo numérico
        data ['cantidad'] = pd.to_numeric(data ['Cantidad'], errors='coerce')
        data ['preciounitario'] = pd.to_numeric(data ['PrecioUnitario'], errors='coerce')

         # Convertir la columna 'Fecha' a tipo datetime
        data ['FECHA'] = pd.to_datetime(data ['Fecha'], errors='coerce')

        return data
    
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")
        return None
    
def AnalizeData(df):
    try:
        #Venta total por producto
        df ["SubTotal"] = df ["Cantidad"] * df ["PrecioUnitario"]

        #Totales
        Venta = df["SubTotal"].sum()
        Ventapromedio = df["SubTotal"].mean()

        Masvendido = df.groupby("Producto")["Cantidad"].sum().idxmax()
        Menosvendido = df.groupby("Producto")["Cantidad"].sum().idxmin()

        Diamasventas = df.groupby("Fecha")["SubTotal"].sum().idxmax()
        Diamenosventas = df.groupby("Fecha")["SubTotal"].sum().idxmin()

        resultados = (
            f"RESULTADOS DEL ANALISIS DE VENTAS\n\n"
            f"Venta Total: ${Venta:,.2f}\n"
            f"Venta Promedio: ${Ventapromedio:,.2f}\n"
            f"Producto Más Vendido: {Masvendido}\n"
            f"Producto Menos Vendido: {Menosvendido}\n"
            f"Día con Más Ventas: {Diamasventas}\n"
            f"Día con Menos Ventas: {Diamenosventas}\n"
            )
        return resultados
    
    #e significa que se captura cualquier excepción que pueda ocurrir durante la ejecución del bloque try
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo analizar los datos: {e}")

##FUNCIONES PARA GUI
def CargarArchivo():
    global file_path

    ruta = filedialog.askopenfilename(
        title="Seleccionar su archivo .CSV",
        filetypes=[("Archivos CSV", "*.csv")]
    )

    if not ruta:
        return
    
    if not ruta.endswith('.csv'):
        messagebox.showwarning("Error", "Por favor seleccione un archivo .CSV válido.")
        file_path = None

    file_path = ruta   

    etiqueta_archivo.config(text=f"Archivo cargado: {os.path.basename(file_path)}")

def WorkData():
    if not file_path:
        messagebox.showwarning("Error", "No se ha cargado ningún archivo.")
        return
    
    df = LoadCSV(file_path)
    if df is None:
        return
    
    resultados = AnalizeData(df)
    if resultados:
        txt_resultados.delete(1.0, tk.END)
        txt_resultados.insert(tk.END, resultados)

        etiqueta_archivo.config(text=f"Archivo cargado: {os.path.basename(file_path)}")

##GUI

ventana = tk.Tk()
ventana.title("Análisis de Ventas desde CSV")
ventana.geometry("600x400")

file_path = None

btn_cargar = tk.Button(ventana, text="Cargar Archivo CSV", command=CargarArchivo)
btn_cargar.pack(pady=10)

etiqueta_archivo = tk.Label(ventana, text="Ningún archivo cargado")
etiqueta_archivo.pack(pady=5)

btn_analizar = tk.Button(ventana, text="Analizar Datos", command=WorkData)
btn_analizar.pack(pady=10)

txt_resultados = tk.Text(ventana, height=15, width=70)
txt_resultados.pack(pady=10)

ventana.mainloop()
