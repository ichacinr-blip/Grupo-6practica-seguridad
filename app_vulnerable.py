import sqlite3
from flask import Flask, request

app = Flask(__name__)

# Estilos CSS compartidos para una interfaz moderna
CSS = '''
<style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f4f7f6;
        margin: 0;
        padding: 40px 20px;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 80vh;
    }
    .card {
        background: #ffffff;
        padding: 30px 40px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        width: 100%;
        max-width: 480px;
    }
    .card-wide {
        max-width: 700px;
    }
    h2 {
        color: #2c3e50;
        margin-top: 0;
        border-bottom: 2px solid #3498db;
        padding-bottom: 10px;
        font-size: 24px;
    }
    .form-group {
        margin-bottom: 20px;
    }
    label {
        display: block;
        margin-bottom: 6px;
        color: #34495e;
        font-weight: 600;
    }
    input[type="text"], input[type="password"] {
        width: 100%;
        padding: 10px 12px;
        border: 1px solid #ccc;
        border-radius: 6px;
        box-sizing: border-box;
        font-size: 14px;
        transition: border-color 0.3s;
    }
    input[type="text"]:focus, input[type="password"]:focus {
        border-color: #3498db;
        outline: none;
    }
    .btn {
        background-color: #3498db;
        color: white;
        padding: 12px;
        border: none;
        border-radius: 6px;
        width: 100%;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .btn:hover {
        background-color: #2980b9;
    }
    .alert {
        padding: 12px 15px;
        border-radius: 6px;
        margin-top: 20px;
        font-weight: 500;
        text-align: center;
    }
    .alert-success {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .alert-danger {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
    }
    th, td {
        padding: 12px 15px;
        border: 1px solid #dddddd;
        text-align: left;
    }
    th {
        background-color: #3498db;
        color: white;
    }
    tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    ul {
        list-style: none;
        padding: 0;
    }
    li {
        margin-bottom: 12px;
    }
    a.menu-link {
        display: block;
        padding: 12px 15px;
        background: #ecf0f1;
        color: #2c3e50;
        text-decoration: none;
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.3s;
    }
    a.menu-link:hover {
        background: #3498db;
        color: white;
    }
    .back-btn {
        display: inline-block;
        margin-top: 20px;
        color: #3498db;
        text-decoration: none;
        font-weight: 600;
    }
    .back-btn:hover {
        text-decoration: underline;
    }
</style>
'''

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            clave TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_factura TEXT,
            cliente TEXT,
            monto REAL,
            fecha TEXT
        )
    ''')
    
    cursor.execute("DELETE FROM usuarios")
    cursor.execute("INSERT INTO usuarios (usuario, clave) VALUES ('admin', 'admin123')")
    cursor.execute("INSERT INTO usuarios (usuario, clave) VALUES ('user1', 'clave123')")
    
    cursor.execute("DELETE FROM facturas")
    cursor.execute("INSERT INTO facturas (numero_factura, cliente, monto, fecha) VALUES ('FAC-001', 'Empresa A', 150.50, '2026-01-15')")
    cursor.execute("INSERT INTO facturas (numero_factura, cliente, monto, fecha) VALUES ('FAC-002', 'Empresa B', 1200.00, '2026-01-20')")
    cursor.execute("INSERT INTO facturas (numero_factura, cliente, monto, fecha) VALUES ('FAC-003', 'Cliente Juan', 85.00, '2026-02-01')")
    
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return f'''
        {CSS}
        <div class="card">
            <h2>Sistema de Pruebas de Seguridad</h2>
            <p><strong>Grupo #6</strong> - Trabajo Práctico Experimental 4</p>
            <ul>
                <li><a class="menu-link" href="/login-vulnerable">🔓 Login Vulnerable (SQL Injection)</a></li>
                <li><a class="menu-link" href="/login-seguro">🔒 Login Seguro (Parametrizado)</a></li>
                <li><a class="menu-link" href="/facturas">📄 Módulo de Facturas</a></li>
            </ul>
        </div>
    '''

@app.route('/login-vulnerable', methods=['GET', 'POST'])
def login_vulnerable():
    msg = ''
    if request.method == 'POST':
        user = request.form.get('usuario', '')
        clave = request.form.get('clave', '')
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        query = f"SELECT * FROM usuarios WHERE usuario = '{user}' AND clave = '{clave}'"
        try:
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                msg = f'<div class="alert alert-success">¡Acceso concedido! Bienvenido, {result[1]}.</div>'
            else:
                msg = '<div class="alert alert-danger">Credenciales incorrectas.</div>'
        except Exception as e:
            msg = f'<div class="alert alert-danger">Error SQL: {e}</div>'
        conn.close()
    
    return f'''
        {CSS}
        <div class="card">
            <h2>Login Vulnerable</h2>
            <form method="POST">
                <div class="form-group">
                    <label>Usuario:</label>
                    <input type="text" name="usuario" placeholder="Ingresa usuario">
                </div>
                <div class="form-group">
                    <label>Clave:</label>
                    <input type="password" name="clave" placeholder="Ingresa clave">
                </div>
                <button type="submit" class="btn">Ingresar</button>
            </form>
            {msg}
            <a href="/" class="back-btn">← Volver al inicio</a>
        </div>
    '''

@app.route('/login-seguro', methods=['GET', 'POST'])
def login_seguro():
    msg = ''
    if request.method == 'POST':
        user = request.form.get('usuario', '')
        clave = request.form.get('clave', '')
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        query = "SELECT * FROM usuarios WHERE usuario = ? AND clave = ?"
        cursor.execute(query, (user, clave))
        result = cursor.fetchone()
        if result:
            msg = f'<div class="alert alert-success">¡Acceso concedido de forma segura!</div>'
        else:
            msg = '<div class="alert alert-danger">Credenciales incorrectas.</div>'
        conn.close()
    
    return f'''
        {CSS}
        <div class="card">
            <h2>Login Seguro</h2>
            <form method="POST">
                <div class="form-group">
                    <label>Usuario:</label>
                    <input type="text" name="usuario" placeholder="Ingresa usuario">
                </div>
                <div class="form-group">
                    <label>Clave:</label>
                    <input type="password" name="clave" placeholder="Ingresa clave">
                </div>
                <button type="submit" class="btn">Ingresar</button>
            </form>
            {msg}
            <a href="/" class="back-btn">← Volver al inicio</a>
        </div>
    '''

@app.route('/facturas')
def ver_facturas():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM facturas")
    rows = cursor.fetchall()
    conn.close()
    
    filas = ""
    for r in rows:
        filas += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>${r[3]:.2f}</td><td>{r[4]}</td></tr>"
        
    return f'''
        {CSS}
        <div class="card card-wide">
            <h2>Lista de Facturas Registradas</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>N° Factura</th>
                        <th>Cliente</th>
                        <th>Monto</th>
                        <th>Fecha</th>
                    </tr>
                </thead>
                <tbody>
                    {filas}
                </tbody>
            </table>
            <a href="/" class="back-btn">← Volver al inicio</a>
        </div>
    '''

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)