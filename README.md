# 🚀 Sistema Negocio Pro - Documentación Oficial

## 1. Visión General del Proyecto
**Negocio Pro** es una aplicación web de gestión interna diseñada para centralizar la administración financiera de múltiples unidades de negocio (Quiniela, Local Av. Cba, Local Los Olmos). Permite registrar ingresos, gastos, gestionar deudas de proveedores con cuentas corrientes y visualizar reportes estadísticos en tiempo real.

## 2. Stack Tecnológico (Herramientas Utilizadas)
El sistema está construido bajo una arquitectura Cliente-Servidor clásica, utilizando las siguientes tecnologías:
* **Lenguaje Principal:** Python 3.
* **Framework Backend:** Flask (Microframework rápido y ligero para la lógica del servidor).
* **Base de Datos:** SQLite (Base de datos relacional local, manejada a través de Flask-SQLAlchemy).
* **Frontend (Diseño):** HTML5, Tailwind CSS (para los estilos visuales) y FontAwesome (para los íconos).
* **Gráficos:** Chart.js (Librería de JavaScript para renderizar los gráficos en el Dashboard).
* **Seguridad:** Werkzeug (para encriptar contraseñas) y Flask-Login (para sesiones de usuario).

## 3. Estructura de Archivos
El proyecto sigue una estructura modular para mantener el código ordenado:

📁 Proyecto_NegocioPro/
├── 📁 venv/                  # Entorno virtual (librerías aisladas de Python)
├── 📁 instance/              # Carpeta autogenerada donde vive la base de datos (datos.db)
├── 📁 app/                   # Carpeta principal de la aplicación
│   ├── 📁 templates/         # Archivos de diseño visual (HTML)
│   │   ├── base.html         # Plantilla maestra (Menú lateral y diseño base)
│   │   ├── index.html        # Pantalla del Dashboard / Panel de control
│   │   ├── proveedores.html  # Pantalla de gestión de proveedores
│   │   └── login.html        # Pantalla de inicio de sesión
│   ├── __init__.py           # Archivo que inicializa Flask y la Base de Datos
│   ├── models.py             # Estructura de las tablas de la base de datos
│   └── routes.py             # Lógica del sistema (las "rutas" o URLs)
├── run.py                    # Archivo principal para encender el servidor de desarrollo
├── requirements.txt          # Lista de librerías instaladas
└── iniciar_sistema.bat       # Script de automatización para arrancar el sistema con 2 clics

## 4. Base de Datos (Modelos Principales)
El sistema utiliza un Modelo Entidad-Relación mapeado en objetos (ORM). Las tablas principales son:
* **Tabla Usuario:** Almacena credenciales de acceso (id, username y password_hash encriptada).
* **Tabla Proveedor:** Gestiona las marcas (id, nombre, telefono, dia_visita y deuda).
* *(Otras tablas)*: Registros para Quiniela, Ingresos y Gastos locales.

## 5. Módulos y Funcionalidades
* **Dashboard (/):** Panel de control principal. Calcula dinámicamente el 15% de comisión, netos y ganancia total. Incluye un filtro de seguridad `or 0` para evitar errores si no hay datos.
* **Proveedores (/proveedores):** CRUD de proveedores. Permite agregar marcas, sumar deuda o registrar pagos rápidos.

## 6. Seguridad y Autenticación
* Rutas protegidas con `@login_required` de Flask-Login. Nadie entra sin iniciar sesión.
* Contraseñas guardadas con algoritmo de "hashing" (indescifrables en la base de datos).

---

## 7. Anatomía del Código (Cómo funciona por dentro)

Para facilitar el mantenimiento futuro, esta es la función exacta de cada archivo vital:

* **`run.py` (La llave de contacto):** Su única función es importar la aplicación y encender el servidor web en el puerto 5000.
* **`app/__init__.py` (La Fábrica):** Crea la app Flask, conecta la base de datos (`datos.db`), configura la clave secreta y prepara el sistema de login.
* **`app/models.py` (Los Planos de la BD):** En lugar de escribir SQL a mano, usamos "Clases" de Python (ej: `class Proveedor`). SQLAlchemy lee esto y crea las tablas reales.
* **`app/routes.py` (El Cerebro):** Recibe las peticiones del usuario, verifica la seguridad, le pide los datos a `models.py`, hace los cálculos matemáticos y le manda esos números a la pantalla HTML.
* **`app/templates/` (La Cara Visible):** Usamos Jinja2 para inyectar variables de Python en el HTML usando llaves `{{ variable }}`. `base.html` es el molde principal, y el resto hereda de él para no repetir código.