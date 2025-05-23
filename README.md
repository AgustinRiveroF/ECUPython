🧠 Sampo E.F.I Manager v1.0
Sampo E.F.I Manager es una interfaz gráfica moderna para gestionar y visualizar datos en tiempo real de una ECU (Unidad de Control Electrónico) para vehículos con inyección electrónica.

🧪 Incluye un modo demo interactivo con datos simulados, ideal para probar sin hardware conectado.

🚀 Características
Visualización en tiempo real de:

- RPM
- Temperatura del motor
- Relación aire/combustible (AFR)
- Gráficos dinámicos con actualizaciones en vivo

Pestañas interactivas:

- Live Data: monitoreo en tiempo real
- Configuración: seleccionar puerto y baudrate
- Carrera: simular inicio y fin de carrera
- Programable: modificar parámetros avanzados
- Conexión (simulada o real) vía puerto serial
- Activar/Desactivar modo demo con un botón

📦 Requisitos
Asegurate de tener instalado Python 3.8 o superior.

Dependencias:
pip install matplotlib pyserial

🛠️ Instalación y ejecución
Cloná el repositorio o descargá el .zip

Instalá las dependencias si no las tenés:

pip install matplotlib pyserial

Ejecutá la app:

python sampo_efi.py

🎮 Modo Demo
Podés activar o desactivar el Modo Demo desde la interfaz gráfica (botón "Activar/Desactivar Modo Demo"). En este modo no se requiere ningún dispositivo físico: los datos se generan aleatoriamente para simular una ECU real.

💻 Modo Real
Si tenés una ECU conectada por puerto serial:

Conectá el dispositivo

Seleccioná el puerto correcto en el combo box

Presioná "Conectar"

Desactivá el modo demo

⚠️ Asegurate de que la configuración del puerto y baudrate coincidan con los valores de tu ECU.#   E C U P y t h o n 
 
 
