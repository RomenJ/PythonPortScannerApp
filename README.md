La aplicación "Port Scanner App" es una herramienta gráfica desarrollada en Python utilizando Tkinter. Su propósito principal es escanear los puertos abiertos de un host especificado a través de una URL.<b> La finalidad es puramente didáctica</b>. El programa incluye una interfaz gráfica de usuario (GUI) con varias características que facilitan la interacción y presentación de los resultados.

Estructura de la Interfaz
Al abrir la aplicación, los usuarios son recibidos por una cabecera que incluye un título llamativo "PORT SCANNER" y una imagen centrada debajo del título. Esta imagen es un icono de lupa ("lupa.jpg"), que se ha redimensionado a 50x50 píxeles para encajar perfectamente en el diseño. La cabecera se coloca dentro de un marco (header_frame), que mantiene el título y la imagen organizados y visualmente atractivos.

Componentes Principales
Entrada de URL: La interfaz incluye un campo de entrada (Entry) donde los usuarios pueden introducir la URL del host que desean escanear. Un Label acompaña este campo para guiar a los usuarios.

Botón de Escaneo: Un botón etiquetado como "Escanear" inicia el proceso de escaneo de puertos cuando se pulsa.

Barra de Progreso: Una barra de progreso (Progressbar) se muestra mientras el escaneo está en curso. Esta barra ayuda a los usuarios a visualizar que el proceso está activo y proporciona feedback sobre el progreso.

Área de Resultados: Los resultados del escaneo se muestran en un widget de texto (Text). Este área permite a los usuarios ver los puertos abiertos y otros mensajes generados durante el escaneo. Incluye un scrollbar para facilitar la navegación a través de los resultados cuando hay mucha información.

Botón de Parar Escaneo: Un botón adicional permite detener el escaneo en curso. Este botón está inicialmente desactivado y solo se habilita cuando el escaneo está activo.

Funcionalidad del Escáner de Puertos
El escaneo de puertos se realiza mediante el uso de múltiples hilos, lo que permite un escaneo más rápido y eficiente. El número de hilos utilizados se define por la variable num_threads, que está configurada en 50.

Obtención de la Dirección IP: El método get_host_address se encarga de convertir la URL proporcionada en una dirección IP. Utiliza la librería socket para resolver el nombre del host.

Escaneo de Puertos: La función port_scan intenta establecer una conexión con cada puerto del host. Si se puede establecer una conexión, el puerto se considera abierto y se añade a la lista de puertos abiertos (openports). Además, el servicio asociado al puerto se intenta identificar usando getservbyport.

Manejo de Hilos: La función threader maneja la distribución del trabajo entre los hilos. Cada hilo obtiene un puerto de una cola (port_queue) y llama a port_scan para escanearlo. La cola asegura que cada puerto se escanee una sola vez.

Inicio y Detención del Escaneo
El proceso de escaneo se inicia al pulsar el botón "Escanear". Esta acción:

Habilita la barra de progreso.
Desactiva el botón de escaneo para evitar múltiples inicios simultáneos.
Habilita el botón de parada.
Resuelve la dirección IP del host.
Llena una cola con los números de puertos a escanear (del puerto 79 al 9091 por defecto).
Inicia los hilos que ejecutan el escaneo.
El botón "Parar Escaneo" permite al usuario detener el escaneo en cualquier momento. Esto se logra estableciendo un evento de parada (stop_event), que los hilos chequean periódicamente para decidir si deben finalizar. <b>El desarrollador del código no se hace responsable de acciones maliciosas o beneficiosas realizadas por terceros</b>

Usabilidad y Flexibilidad
La aplicación es fácil de usar gracias a su interfaz intuitiva y sus componentes bien organizados. La adición de una cabecera con título e imagen mejora la experiencia del usuario al hacer la aplicación más profesional y atractiva. Además, el uso de múltiples hilos y una barra de progreso proporciona un escaneo eficiente y feedback continuo al usuario.

En resumen, la "Port Scanner App" es una herramienta útil y bien diseñada para la tarea de escanear puertos, combinando funcionalidad y una interfaz gráfica amigable.
