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

    # Marcar puntos en el plano
    def add_point(self, event):
        if event.inaxes:
            x, y = round(event.xdata), round(event.ydata)
            
            # Clic izquierdo para clase -1 (rojo), clic derecho para clase 1 (azul)
            if event.button == 1:
                self.points.append((x, y, -1))
                self.ax.plot(x, y, 'ro', markersize=12) #Color rojo
            elif event.button == 3:
                self.points.append((x, y, 1))
                self.ax.plot(x, y, 'bo', markersize=12) #Color azul
            
            self.canvas.draw()

    # Algoritmo del perceptrón
    def advance_epoch(self):
        if not self.points:
            messagebox.showwarning("Error", "Ingresa Puntos al plano para continuar.")
            return

        error_occurred = False
        #Recorre los puntos y aplica el algoritmo de correccion de error
        for x, y, label in self.points:
            input_vector = np.array([x, y, 1]) #Añade BIAS
            prediction = np.dot(self.weights, input_vector) #Calcula la salida del perceptron
            predicted_label = 1 if prediction >= 0 else -1
            
            #Actualiza pesos si esta incorrecta
            if predicted_label != label:
                error_occurred = True
                self.weights += self.learning_rate * (label - predicted_label) * input_vector

        # Redibujar el gráfico con los nuevos pesos
        self.ax.clear()
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_xticks(np.arange(-10, 11, 1))
        self.ax.set_yticks(np.arange(-10, 11, 1))
        self.ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(0, color='black', linewidth=0.5)
        
        for x, y, label in self.points:
            color = 'bo' if label == 1 else 'ro'
            self.ax.plot(x, y, color, markersize=12)   

            # Dibujar hiperplano
        x_vals = np.array(self.ax.get_xlim())
        if self.weights[1] != 0:
            y_vals = - (self.weights[0] / self.weights[1]) * x_vals - (self.weights[2] / self.weights[1])
            self.ax.plot(x_vals, y_vals, 'g--')

        self.canvas.draw()

        # Actualizar etiquetas
        self.w1_label.config(text=f"Peso w1: {self.weights[0]:.1f}")
        self.w2_label.config(text=f"Peso w2: {self.weights[1]:.1f}")
        self.bias_label.config(text=f"Bias w0: {self.weights[2]:.1f}")
        
        #Errores
        if not error_occurred:
            messagebox.showinfo("Correcto", f"Se clasificaron exitosamente los puntos en la época {self.epoch + 1}")
        else:
            self.epoch += 1

     #Cerra figura y ventana
    def on_closing(self):
        plt.close(self.figure)
        self.destroy()

#Ejecutar aplicación
if __name__ == "__main__":
    app = PerceptronGUI()
    app.mainloop()       