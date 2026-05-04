from flask import render_template, request, redirect, url_for, flash
from flask import current_app as app
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, Proveedor, RegistroQuiniela, Gasto, IngresoDespensa, Usuario
from sqlalchemy import func, extract
from datetime import datetime

# --- SISTEMA DE LOGIN Y SEGURIDAD ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Si el usuario ya entró, lo mandamos directo al panel
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Buscamos al usuario en la base de datos
        user = Usuario.query.filter_by(username=username).first()
        
        # Verificamos que exista y que la clave encriptada coincida
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos. Intentá de nuevo.', 'error')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- PANEL DE CONTROL ---
@app.route('/')
@login_required # <--- CANDADO DE SEGURIDAD
def index():
    hoy = datetime.now() # Sacamos la fecha de hoy
    mes_filtro = request.args.get('mes')
    if not mes_filtro:
        mes_filtro = f"{hoy.year}-{hoy.month:02d}"
    
    year, month = map(int, mes_filtro.split('-'))
    
    # 1. Datos Generales
    total_proveedores = Proveedor.query.count()
    recaudacion_quiniela = db.session.query(func.sum(RegistroQuiniela.recaudacion_bruta))\
        .filter(extract('year', RegistroQuiniela.fecha) == year)\
        .filter(extract('month', RegistroQuiniela.fecha) == month).scalar() or 0
    comision_quiniela = recaudacion_quiniela * 0.15

    # 2. Datos Despensa Av. Cba
    ingresos_cba = db.session.query(func.sum(IngresoDespensa.monto))\
        .filter(IngresoDespensa.sucursal == 'Av. Cba')\
        .filter(extract('year', IngresoDespensa.fecha) == year)\
        .filter(extract('month', IngresoDespensa.fecha) == month).scalar() or 0
        
    gastos_cba = db.session.query(func.sum(Gasto.monto))\
        .filter(Gasto.sucursal == 'Av. Cba')\
        .filter(extract('year', Gasto.fecha) == year)\
        .filter(extract('month', Gasto.fecha) == month).scalar() or 0
        
    neto_cba = ingresos_cba - gastos_cba

    # 3. Datos Despensa Los Olmos
    ingresos_olmos = db.session.query(func.sum(IngresoDespensa.monto))\
        .filter(IngresoDespensa.sucursal == 'Los Olmos')\
        .filter(extract('year', IngresoDespensa.fecha) == year)\
        .filter(extract('month', IngresoDespensa.fecha) == month).scalar() or 0
        
    gastos_olmos = db.session.query(func.sum(Gasto.monto))\
        .filter(Gasto.sucursal == 'Los Olmos')\
        .filter(extract('year', Gasto.fecha) == year)\
        .filter(extract('month', Gasto.fecha) == month).scalar() or 0
        
    neto_olmos = ingresos_olmos - gastos_olmos

    # 4. Total del Negocio Completo
    gastos_totales = gastos_cba + gastos_olmos
    ganancia_total_neta = comision_quiniela + neto_cba + neto_olmos

    # 5. NUEVO: Alertas de Proveedores
    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    dia_hoy = dias_semana[hoy.weekday()]
    
    proveedores_deuda = Proveedor.query.filter(Proveedor.deuda > 0).order_by(Proveedor.deuda.desc()).all()

    return render_template('index.html', 
                        mes_actual=mes_filtro,
                        total_p=total_proveedores, 
                        ganancia_quiniela=comision_quiniela,
                        neto_cba=neto_cba,
                        neto_olmos=neto_olmos,
                        gastos_totales=gastos_totales,
                        ganancia_total=ganancia_total_neta,
                        proveedores_deuda=proveedores_deuda, 
                        dia_hoy=dia_hoy)

# --- DESPENSAS: INGRESOS ---
@app.route('/ingresos', methods=['GET', 'POST'])
@login_required # <--- CANDADO DE SEGURIDAD
def ingresos():
    if request.method == 'POST':
        sucursal = request.form.get('sucursal')
        monto = float(request.form.get('monto'))
        nuevo_ingreso = IngresoDespensa(sucursal=sucursal, monto=monto)
        db.session.add(nuevo_ingreso)
        db.session.commit()
        return redirect(url_for('ingresos'))

    lista_ingresos = IngresoDespensa.query.order_by(IngresoDespensa.fecha.desc()).all()
    return render_template('ingresos.html', ingresos=lista_ingresos)

@app.route('/eliminar_ingreso/<int:id>')
@login_required
def eliminar_ingreso(id):
    ingreso = IngresoDespensa.query.get(id)
    if ingreso:
        db.session.delete(ingreso)
        db.session.commit()
    return redirect(url_for('ingresos'))

# --- GASTOS ---
@app.route('/gastos', methods=['GET', 'POST'])
@login_required # <--- CANDADO DE SEGURIDAD
def gastos():
    if request.method == 'POST':
        sucursal = request.form.get('sucursal')
        descripcion = request.form.get('descripcion')
        monto = float(request.form.get('monto'))
        nuevo_gasto = Gasto(sucursal=sucursal, descripcion=descripcion, monto=monto)
        db.session.add(nuevo_gasto)
        db.session.commit()
        return redirect(url_for('gastos'))

    lista_gastos = Gasto.query.order_by(Gasto.fecha.desc()).all()
    return render_template('gastos.html', gastos=lista_gastos)

@app.route('/eliminar_gasto/<int:id>')
@login_required
def eliminar_gasto(id):
    gasto = Gasto.query.get(id)
    if gasto:
        db.session.delete(gasto)
        db.session.commit()
    return redirect(url_for('gastos'))

# --- PROVEEDORES ---
@app.route('/proveedores', methods=['GET', 'POST'])
@login_required # <--- CANDADO DE SEGURIDAD
def proveedores():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        dia = request.form.get('dia_visita')
        # CAPTURAMOS LA DEUDA INICIAL
        deuda = float(request.form.get('deuda') or 0)
        nuevo_p = Proveedor(nombre=nombre, telefono=telefono, dia_visita=dia, deuda=deuda)
        db.session.add(nuevo_p)
        db.session.commit()
        return redirect(url_for('proveedores'))
    
    lista_proveedores = Proveedor.query.all()
    return render_template('proveedores.html', proveedores=lista_proveedores)

@app.route('/eliminar_proveedor/<int:id>')
@login_required
def eliminar_proveedor(id):
    p = Proveedor.query.get(id)
    if p:
        db.session.delete(p)
        db.session.commit()
    return redirect(url_for('proveedores'))

@app.route('/actualizar_deuda/<int:id>', methods=['POST'])
@login_required
def actualizar_deuda(id):
    p = Proveedor.query.get(id)
    if p:
        monto = float(request.form.get('monto', 0))
        accion = request.form.get('accion')
        
        if accion == 'sumar':
            p.deuda += monto
        elif accion == 'restar':
            p.deuda -= monto
            if p.deuda < 0:
                p.deuda = 0
                
        db.session.commit()
    return redirect(url_for('proveedores'))

# --- QUINIELA ---
@app.route('/quiniela', methods=['GET', 'POST'])
@login_required # <--- CANDADO DE SEGURIDAD
def quiniela():
    if request.method == 'POST':
        recaudacion = float(request.form.get('recaudacion'))
        premios = float(request.form.get('premios'))
        neto = recaudacion - premios
        
        nuevo_registro = RegistroQuiniela(
            recaudacion_bruta=recaudacion,
            premios_pagados=premios,
            neto_caja=neto
        )
        db.session.add(nuevo_registro)
        db.session.commit()
        return redirect(url_for('quiniela'))

    registros = RegistroQuiniela.query.order_by(RegistroQuiniela.fecha.desc()).all()
    return render_template('quiniela.html', registros=registros)

@app.route('/eliminar_quiniela/<int:id>')
@login_required
def eliminar_quiniela(id):
    registro = RegistroQuiniela.query.get(id)
    if registro:
        db.session.delete(registro)
        db.session.commit()
    return redirect(url_for('quiniela'))