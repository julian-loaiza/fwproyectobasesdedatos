from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Añade esta línea. Puedes usar cualquier texto.
app.secret_key = 'development_key'

# Configuración de la base de datos
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'proyectos_informaticos'),
        user=os.getenv('DB_USER', 'usuario'),
        password=os.getenv('DB_PASSWORD', '1234'),
        port=os.getenv('DB_PORT', '5432')
    )
    return conn

# --- Rutas Principales de la Aplicación ---
@app.route('/')
def index():
    """Página de inicio."""
    return render_template('index.html')

# --- Operaciones CRUD para la tabla 'docente' ---

@app.route('/docentes')
def docentes():
    """Muestra la lista de todos los docentes."""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM docente ORDER BY nombre;')
    lista_docentes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('docentes.html', docentes=lista_docentes)

@app.route('/docente/add', methods=['POST'])
def add_docente():
    """Añade un nuevo docente a la base de datos."""
    if request.method == 'POST':
        documento = request.form['documento']
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        titulo = request.form['titulo']
        anos_experiencia = request.form['anos_experiencia']
        
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                'INSERT INTO docente (documento, nombre, direccion, titulo, anosexperiencia)'
                'VALUES (%s, %s, %s, %s, %s)',
                (documento, nombre, direccion, titulo, anos_experiencia)
            )
            conn.commit()
            flash('Docente añadido con éxito.', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error al añadir docente: {str(e)}', 'danger')
        finally:
            cur.close()
            conn.close()
        
        return redirect(url_for('docentes'))

@app.route('/docente/update/<string:documento>', methods=['POST'])
def update_docente(documento):
    """Actualiza los datos de un docente existente."""
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        titulo = request.form['titulo']
        anos_experiencia = request.form['anos_experiencia']
        
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                'UPDATE docente SET nombre = %s, direccion = %s, titulo = %s, anosexperiencia = %s '
                'WHERE documento = %s',
                (nombre, direccion, titulo, anos_experiencia, documento)
            )
            conn.commit()
            flash('Docente actualizado con éxito.', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error al actualizar docente: {str(e)}', 'danger')
        finally:
            cur.close()
            conn.close()
        
        return redirect(url_for('docentes'))

@app.route('/docente/delete/<string:documento>')
def delete_docente(documento):
    """Elimina un docente de la base de datos."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM docente WHERE documento = %s', (documento,))
        conn.commit()
        flash('Docente eliminado con éxito.', 'success')
    except Exception as e:
        conn.rollback()
        # Captura el error de clave foránea para un mensaje más claro
        if 'violates foreign key constraint' in str(e):
            flash('Error: No se puede eliminar el docente porque es jefe de uno o más proyectos.', 'danger')
        else:
            flash(f'Error al eliminar docente: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('docentes'))

# --- Operaciones CRUD para la tabla 'proyecto' ---

@app.route('/proyectos')
def proyectos():
    """Muestra la lista de proyectos y los docentes para el formulario."""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # --- CAMBIO EN LA CONSULTA ---
    # Ahora unimos usando la nueva clave primaria numérica: d.codigo
    cur.execute("""
        SELECT p.*, d.nombre as nombre_jefe 
        FROM proyecto p 
        LEFT JOIN docente d ON p.docentejefe = d.codigo 
        ORDER BY p.codigo;
    """)
    lista_proyectos = cur.fetchall()
    
    # --- CAMBIO EN LA CONSULTA DE DOCENTES ---
    # Necesitamos obtener el 'codigo' para usarlo en el formulario.
    cur.execute('SELECT codigo, nombre FROM docente ORDER BY nombre;')
    lista_docentes = cur.fetchall()
    
    cur.close()
    conn.close()
    return render_template('proyectos.html', proyectos=lista_proyectos, docentes=lista_docentes)
    
    # Consulta para obtener todos los docentes para el menú desplegable
    cur.execute('SELECT documento, nombre FROM docente ORDER BY nombre;')
    lista_docentes = cur.fetchall()
    
    cur.close()
    conn.close()
    return render_template('proyectos.html', proyectos=lista_proyectos, docentes=lista_docentes)
    
    # Consulta para obtener todos los docentes para el menú desplegable
    cur.execute('SELECT documento, nombre FROM docente ORDER BY nombre;')
    lista_docentes = cur.fetchall()
    
    cur.close()
    conn.close()
    return render_template('proyectos.html', proyectos=lista_proyectos, docentes=lista_docentes)

@app.route('/proyecto/add', methods=['POST'])
def add_proyecto():
    """Añade un nuevo proyecto a la base de datos."""
    if request.method == 'POST':
        nombre = request.form['nombre']
        aliado = request.form['aliado']
        descripcion = request.form['descripcion']
        presupuesto = request.form['presupuesto']
        horas_estimadas = request.form['horas_estimadas']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        docente_jefe = request.form['docente_jefe']
        
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                'INSERT INTO proyecto (nombre, aliado, descripcion, presupuesto, horasestimadas, fechainicio, fechafin, docentejefe)'
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                (nombre, aliado, descripcion, presupuesto, horas_estimadas, fecha_inicio, fecha_fin, docente_jefe)
            )
            conn.commit()
            flash('Proyecto añadido con éxito.', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error al añadir proyecto: {str(e)}', 'danger')
        finally:
            cur.close()
            conn.close()
        
        return redirect(url_for('proyectos'))

@app.route('/proyecto/update/<int:codigo>', methods=['POST'])
def update_proyecto(codigo):
    """Actualiza los datos de un proyecto existente."""
    if request.method == 'POST':
        nombre = request.form['nombre']
        aliado = request.form['aliado']
        descripcion = request.form['descripcion']
        presupuesto = request.form['presupuesto']
        horas_estimadas = request.form['horas_estimadas']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        docente_jefe = request.form['docente_jefe']
        
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                'UPDATE proyecto SET nombre = %s, aliado = %s, descripcion = %s, presupuesto = %s, '
                'horasestimadas = %s, fechainicio = %s, fechafin = %s, docentejefe = %s '
                'WHERE codigo = %s',
                (nombre, aliado, descripcion, presupuesto, horas_estimadas, fecha_inicio, fecha_fin, docente_jefe, codigo)
            )
            conn.commit()
            flash('Proyecto actualizado con éxito.', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error al actualizar proyecto: {str(e)}', 'danger')
        finally:
            cur.close()
            conn.close()
        
        return redirect(url_for('proyectos'))

@app.route('/proyecto/delete/<int:codigo>')
def delete_proyecto(codigo):
    """Elimina un proyecto de la base de datos."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM proyecto WHERE codigo = %s', (codigo,))
        conn.commit()
        flash('Proyecto eliminado con éxito.', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error al eliminar proyecto: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('proyectos'))

# --- Arranque de la Aplicación ---
if __name__ == '__main__':
    app.run(debug=True)