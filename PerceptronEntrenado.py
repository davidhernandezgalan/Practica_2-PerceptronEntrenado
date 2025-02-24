import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random

# Configuración de la ventana principal
class PerceptronGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Perceptrón Entrenado")

        # Inicializar variables: puntos, pesos y tasa de aprendizaje
        self.points = []  # Lista para almacenar puntos y su clase (1 o -1)
        self.weights = np.random.uniform(-3, 3, 3)  # Inicializar pesos aleatorios en el rango [-3, 3]
        self.learning_rate = 0.1  # Tasa de aprendizaje
        self.epoch = 0  # Contador de épocas
        
        # Crear el gráfico (Plano)
        self.figure, self.ax = plt.subplots()
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_xticks(np.arange(-10, 11, 1))
        self.ax.set_yticks(np.arange(-10, 11, 1))
        self.ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(0, color='black', linewidth=0.5)

        # Agregar gráfico a la interfaz
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
        self.canvas.mpl_connect('button_press_event', self.add_point)

        # Botones de control
        control_frame = tk.Frame(self)
        control_frame.pack()
        tk.Button(control_frame, text="GO", command=self.advance_epoch).pack(side=tk.LEFT)

        # Espacio para mostrar los valores de los pesos y bias
        self.weights_frame = tk.Frame(self)
        self.weights_frame.pack()
        
        self.w1_label = tk.Label(self.weights_frame, text=f"Peso w1: {self.weights[0]:.1f}")
        self.w1_label.grid(row=0, column=0)
        self.w2_label = tk.Label(self.weights_frame, text=f"Peso w2: {self.weights[1]:.1f}")
        self.w2_label.grid(row=1, column=0)
        self.bias_label = tk.Label(self.weights_frame, text=f"Bias w0: {self.weights[2]:.1f}")
        self.bias_label.grid(row=2, column=0)

        # Manejo de cierre
        self.protocol("WM_DELETE_WINDOW", self.on_closing)