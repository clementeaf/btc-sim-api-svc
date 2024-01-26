# Buda API

API para obtener información sobre spreads de mercados financieros.

## Configuración del Proyecto

### Requisitos Previos
Asegúrate de tener Docker instalado en tu máquina.

### Instrucciones de Ejecución

1. Clona el repositorio:

    ```bash
    git clone https://github.com/tu_usuario/buda-api.git
    cd buda-api
    ```

2. Construye la imagen Docker:

    ```bash
    docker build -t btc-sim-svc .
    ```

3. Ejecuta el contenedor:

    ```bash
    docker run -p 8000:8000 btc-sim-svc
    ```

La aplicación estará disponible en [http://localhost:8000](http://localhost:8000).

## Servicios

### `app/services/market_spread.py`

Contiene funciones para manejar la lógica de spread y actualizar bases de datos MongoDB.

### `app/utils/math_utils.py`

Proporciona funciones matemáticas útiles, como el cálculo de la dirección del spread.

## Estructura del Proyecto

- `app/main.py`: Código principal de la aplicación FastAPI.
- `app/models/spread_entry.py`: Definición del modelo `SpreadEntry`.
- `app/models/spreads_history.py`: Definición del modelo `SpreadHistory`.
- `app/services/market_spread.py`: Lógica para manejar spreads y persistencia.
- `app/utils/math_utils.py`: Funciones matemáticas útiles.
- `app/spreads_persistence.py`: Lógica para persistencia en MongoDB.
- `Dockerfile`: Configuración para construir la imagen Docker.

## Contribuciones

Si deseas contribuir al proyecto, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama para tus cambios (`git checkout -b feature/nueva_feature`).
3. Realiza tus cambios y haz commit (`git commit -am 'Agrega nueva_feature'`).
4. Sube tus cambios a tu fork (`git push origin feature/nueva_feature`).
5. Abre un Pull Request.

¡Gracias por contribuir!

## Rutas de la API

### `/markets`

- **Método:** `GET`
- **Descripción:** Retorna el spread más reciente en la primera llamada, seguido de una comparación entre la llamada más reciente y la anterior sin persistencia en la base de datos.
- **Parámetros Query:**
  - Ninguno
- **Respuesta:**
  - Tipo: JSON
  - Contenido: Historial de entradas de spread.

### `/get_price`

- **Método:** `GET`
- **Descripción:** Obtiene el precio más reciente para un mercado específico en un timestamp dado.
- **Parámetros Query:**
  - `timestamp` (Requerido): Timestamp para obtener el precio.
- **Respuesta:**
  - Tipo: JSON
  - Contenido: Objeto con el timestamp y el precio.
