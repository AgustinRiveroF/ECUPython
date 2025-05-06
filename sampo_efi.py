import tkinter as tk
from tkinter import ttk
import random
import time
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configuración Global
class Config:
    port = None
    baudrate = 115200
    connected = False
    demo_mode = True  # Modo demo activado por defecto

# Comunicación Serial (simulada para demo)
class SerialManager:
    def __init__(self):
        self.ser = None
        self.thread = None
        self.running = False

    def connect(self, port, baudrate):

        Config.connected = True
        self.running = True
        self.thread = threading.Thread(target=self.read_loop)
        self.thread.daemon = True
        self.thread.start()
        return True

    def disconnect(self):
        Config.connected = False
        self.running = False

    def read_loop(self):
        while self.running:
            time.sleep(1)  # Esperar 1 segundo para simular la lectura de datos
            if Config.demo_mode:
                rpm = random.randint(1000, 7000)
                temp = random.randint(60, 120)
                afr = random.uniform(10.0, 18.0)

                data = f"RPM:{rpm},TEMP:{temp},AFR:{afr:.2f}"

                self.update_ui(data)

    def update_ui(self, data):
        # Extraemos los datos simulados
        data_dict = dict(item.split(":") for item in data.split(","))
        app.update_live_data(data_dict)

    def send(self, data):
        pass  # Esta función no se usa en demo

# Interfaz Gráfica
class SampoEFIApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sampo E.F.I Manager v1.0")
        self.geometry("900x600")
        self.configure(bg='#1e1e1e')

        self.serial_mgr = SerialManager()
        self.create_widgets()

        self.rpm_data = []
        self.temp_data = []
        self.afr_data = []

    def create_widgets(self):
        header = tk.Label(self, text="Sampo E.F.I Manager v1.0", fg="white", bg="#1e1e1e", font=("Arial", 20))
        header.pack(pady=10)

        frame_conn = tk.Frame(self, bg="#1e1e1e")
        frame_conn.pack(pady=5)

        self.port_cb = ttk.Combobox(frame_conn, values=self.get_serial_ports())
        self.port_cb.pack(side=tk.LEFT, padx=5)
        self.btn_conn = tk.Button(frame_conn, text="Conectar", command=self.toggle_connection)
        self.btn_conn.pack(side=tk.LEFT, padx=5)

        self.conn_status = tk.Label(frame_conn, text="Desconectado", fg="red", bg="#1e1e1e")
        self.conn_status.pack(side=tk.LEFT, padx=10)

        self.btn_demo = tk.Button(self, text="Desactivar Modo Demo", command=self.toggle_demo_mode)
        self.btn_demo.pack(pady=10)

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(expand=1, fill="both")

        self.tab_live = self.create_tab_live()
        self.tab_config = self.create_tab_config()
        self.tab_race = self.create_tab_race()
        self.tab_program = self.create_tab_program()

        self.tabs.add(self.tab_live, text="Live Data")
        self.tabs.add(self.tab_config, text="Configuración")
        self.tabs.add(self.tab_race, text="Carrera")
        self.tabs.add(self.tab_program, text="Programable")

    def get_serial_ports(self):
        return ["COM1", "COM2", "COM3"]

    def toggle_connection(self):
        if not Config.connected:
            port = self.port_cb.get()
            if self.serial_mgr.connect(port, Config.baudrate):
                self.conn_status.config(text="Conectado", fg="green")
                self.btn_conn.config(text="Desconectar")
            else:
                self.conn_status.config(text="Error", fg="red")
        else:
            self.serial_mgr.disconnect()
            self.conn_status.config(text="Desconectado", fg="red")

    def toggle_demo_mode(self):
        Config.demo_mode = not Config.demo_mode
        if Config.demo_mode:
            self.btn_demo.config(text="Desactivar Modo Demo")
        else:
            self.btn_demo.config(text="Activar Modo Demo")

    def create_tab_live(self):
        tab_live = tk.Frame(self.tabs, bg="#1e1e1e")
        tab_live.configure(bg="#1e1e1e")
        
        self.rpm_label = tk.Label(tab_live, text="RPM: 0", fg="white", bg="#1e1e1e", font=("Arial", 16))
        self.rpm_label.pack(pady=10)

        self.temp_label = tk.Label(tab_live, text="TEMP: 0°C", fg="white", bg="#1e1e1e", font=("Arial", 16))
        self.temp_label.pack(pady=10)

        self.afr_label = tk.Label(tab_live, text="AFR: 0.0", fg="white", bg="#1e1e1e", font=("Arial", 16))
        self.afr_label.pack(pady=10)

        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.ax.set_title('Datos en Tiempo Real')
        self.ax.set_xlabel('Tiempo (s)')
        self.ax.set_ylabel('Valores')
        self.line_rpm, = self.ax.plot([], [], label="RPM", color='blue')
        self.line_temp, = self.ax.plot([], [], label="TEMP", color='red')
        self.line_afr, = self.ax.plot([], [], label="AFR", color='green')

        self.canvas = FigureCanvasTkAgg(self.fig, master=tab_live)
        self.canvas.get_tk_widget().pack(pady=20)

        self.ax.legend()

        return tab_live

    def update_live_data(self, data_dict):
        self.rpm_label.config(text=f"RPM: {data_dict['RPM']}")
        self.temp_label.config(text=f"TEMP: {data_dict['TEMP']}°C")
        self.afr_label.config(text=f"AFR: {data_dict['AFR']}")

        if Config.demo_mode:
            self.update_data('RPM', int(data_dict['RPM']))
            self.update_data('TEMP', int(data_dict['TEMP']))
            self.update_data('AFR', float(data_dict['AFR']))

    def update_data(self, param, value):
        if param == 'RPM':
            self.rpm_data.append(value)
        elif param == 'TEMP':
            self.temp_data.append(value)
        elif param == 'AFR':
            self.afr_data.append(value)

        if len(self.rpm_data) > 50:
            self.rpm_data.pop(0)
            self.temp_data.pop(0)
            self.afr_data.pop(0)

        self.line_rpm.set_xdata(range(len(self.rpm_data)))
        self.line_rpm.set_ydata(self.rpm_data)

        self.line_temp.set_xdata(range(len(self.temp_data)))
        self.line_temp.set_ydata(self.temp_data)

        self.line_afr.set_xdata(range(len(self.afr_data)))
        self.line_afr.set_ydata(self.afr_data)

        self.ax.relim()
        self.ax.autoscale_view()

        self.canvas.draw()

    def create_tab_config(self):
        tab_config = tk.Frame(self.tabs, bg="#1e1e1e")

        tk.Label(tab_config, text="Puerto Serial:", fg="white", bg="#1e1e1e").pack(pady=5)
        self.port_input = ttk.Combobox(tab_config, values=self.get_serial_ports())
        self.port_input.pack(pady=5)

        tk.Label(tab_config, text="Baudrate:", fg="white", bg="#1e1e1e").pack(pady=5)
        self.baudrate_input = ttk.Entry(tab_config)
        self.baudrate_input.insert(0, str(Config.baudrate))
        self.baudrate_input.pack(pady=5)

        save_button = tk.Button(tab_config, text="Guardar Configuración", command=self.save_config)
        save_button.pack(pady=10)

        return tab_config

    def save_config(self):
        Config.port = self.port_input.get()
        Config.baudrate = int(self.baudrate_input.get())
        print(f"Configuración guardada: Puerto={Config.port}, Baudrate={Config.baudrate}")

    def create_tab_race(self):
        tab_race = tk.Frame(self.tabs, bg="#1e1e1e")
        self.race_button = tk.Button(tab_race, text="Iniciar Carrera", command=self.toggle_race)
        self.race_button.pack(pady=20)
        return tab_race

    def toggle_race(self):
        if self.race_button.cget("text") == "Iniciar Carrera":
            self.race_button.config(text="Detener Carrera")
        else:
            self.race_button.config(text="Iniciar Carrera")

    def create_tab_program(self):
        tab_program = tk.Frame(self.tabs, bg="#1e1e1e")
        
        tk.Label(tab_program, text="Parámetro de Inyección:", fg="white", bg="#1e1e1e").pack(pady=5)
        self.injection_param = ttk.Entry(tab_program)
        self.injection_param.pack(pady=5)

        program_button = tk.Button(tab_program, text="Guardar Configuración", command=self.save_program)
        program_button.pack(pady=10)

        return tab_program

    def save_program(self):
        print(f"Parámetro de inyección guardado: {self.injection_param.get()}")

if __name__ == "__main__":
    app = SampoEFIApp()
    app.mainloop()



