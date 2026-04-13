# Información del Proyecto Flask_Spike

Este archivo detalla el funcionamiento interno, las funciones principales y las operaciones disponibles en el proyecto.

## 1. ¿Cómo funciona el proyecto?

El proyecto es una API RESTful construida con Flask y SQLite que sirve para gestionar una lista de tareas (To-Do list). Utiliza una arquitectura dividida en **4 capas principales** para separar las responsabilidades (Clean Architecture simplificada):

- **Entrada (`app.py`):** Es el punto de inicio de la aplicación y sirve para levantar el servidor web en el puerto 5000.
- **Capa HTTP o de Enrutamiento (`src/webserver.py`):** Recibe las peticiones HTTP del cliente (frontend, Postman, etc.). Su responsabilidad es validar la entrada, transformar los datos a JSON y manejar los códigos de estado de respuesta (200, 201, 404, etc.).
- **Capa de Servicio o Casos de Uso (`src/task.py`):** Sirve como intermediario encapsulando la lógica de negocio. Recibe las llamadas del servidor web y delega las operaciones al repositorio de la base de datos.
- **Capa de Repositorio o Persistencia (`src/task_repository_sqlite.py`):** Se encarga de interactuar directamente con la base de datos `tasks.db` utilizando comandos SQL (SQLite 3). Al ejecutarse, inicializa la base de datos y crea la tabla si no existe.

---

## 2. Explicación de cada función

A continuación, se detalla qué hace cada función agrupada por su archivo.

### Funciones en `src/webserver.py`
Son los "endpoints" o rutas de comunicación por donde entran las peticiones.
- **`hello_root()`**: Responde a la ruta base `/` entregando un mensaje simple en HTML para comprobar que la API funciona.
- **`get_tasks()`**: Responde a la solicitud `GET /tasks` obteniendo todas las tareas y devolviéndolas en formato JSON.
- **`get_task(task_id)`**: Responde a `GET /tasks/<id>` validando si existe una tarea con el ID dado y devolviéndola en JSON; si no existe, devuelve un error 404.
- **`new_task()`**: Maneja una petición `POST /tasks`. Extrae el JSON enviado por el cliente, verifica que contenga un "titulo" y procede a pedir su creación. Devuelve un estado 201 si tiene éxito.
- **`update_task_route(task_id)`**: Es llamada con `PUT /tasks/<id>`. Verifica que vengan los datos obligatorios (titulo) e intenta modificar la tarea. Si la tarea no existía regresa un 404.
- **`delete_task(task_id)`**: Se ejecuta con `DELETE /tasks/<id>`. Intenta eliminar la tarea y devuelve un estado 204 sin contenido en caso de éxito.

### Funciones en `src/task.py`
Son los controladores de negocio. No tienen lógica pesada en este proyecto pero mantienen las capas limpias. 
- **`get_task_by(task_id)`**: Toma un ID e invoca al método de lectura (`read`) del repositorio.
- **`get_all_tasks()`**: Invoca al método de lectura de todas las tareas (`read_all`) en el repositorio.
- **`post_task(new_task)`**: Toma los datos de un diccionario e invoca a `create()` para insertarlo en la base de datos.
- **`update_task(task_id, update_task_data)`**: Toma un ID y la información enviada, pasándola a `update()` para modificar una tabla.
- **`del_task(task_id)`**: Recibe el ID de una tarea a borrar y se lo da a `delete()` del repositorio.

### Funciones en `src/task_repository_sqlite.py`
Se encargan de ejecutar consultas `SQL`.
- **`_init_db()`**: Función de uso interno. Conecta al archivo `tasks.db` y crea la estructura inicial de la tabla `tasks` (columnas: id, titulo, descripcion, completada, fecha_creacion) si es que esta no existía previamente.
- **`_task_from_row(row)`**: Un auxiliar. Toma como parámetro la fila "cruda" devuelta por SQLite (que es una tupla ej: `(1, 'titulo', ...)`) y la convierte a un Diccionario de Python estructurado para enviarlo más adelante como JSON.
- **`read(task_id)`**: Usa `SELECT ... WHERE id = ?` en SQLite para leer una única fila y retornarla en su formato preprocesado.
- **`read_all()`**: Hace un query de tipo `SELECT ... ORDER BY id` para traer todas las filas, procesarlas secuencialmente en un array y retornarlas.
- **`create(new_task)`**: Ejecuta un `INSERT INTO` en la base de datos acomodando los valores "titulo", "descripcion" y estado. Devuelve el número automático (id de inserción) mediante `lastrowid`.
- **`update(task_id, update_task_data)`**: Modifica datos a través de una query `UPDATE`. Devuelve formato booleano (`True` o `False`) comprobando que las filas afectadas fuesen mayores que cero.
- **`delete(task_id)`**: Elimina de la base de datos los elementos especificados en la query `DELETE`. Igualmente retorna un booleano confirmando la eliminación.

---

## 3. ¿Cuántas Peticiones CRUD se pueden hacer?

La sigla *CRUD* hace referencia a las 4 funciones básicas implementadas en sistemas de base de datos o almacenamiento: Create, Read, Update y Delete. 

El código de este proyecto expone exactamente **5 peticiones o endpoints CRUD**:

1. **C**reate (Crear): **1 petición.** 
   - `POST /tasks` -> Crea una nueva tarea.
2. **R**ead (Leer): **2 peticiones.**
   - `GET /tasks` -> Lee todas las tareas existentes.
   - `GET /tasks/<id>` -> Lee los detalles de una única tarea basándose en su ID.
3. **U**pdate (Actualizar): **1 petición.**
   - `PUT /tasks/<id>` -> Modifica y sobreescribe los campos de una tarea existente.
4. **D**elete (Eliminar): **1 petición.**
   - `DELETE /tasks/<id>` -> Elimina una tarea basándose en su ID.

En total suman **5 operaciones HTTP en formato CRUD** expuestas a los clientes.
