from . import db
from datetime import date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# --- NUEVO: Modelo de Usuario para el Login Seguro ---
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# --- PROVEEDORES ---
class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    dia_visita = db.Column(db.String(20))
    deuda = db.Column(db.Float, default=0.0)

# --- QUINIELA ---
class RegistroQuiniela(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, default=date.today)
    recaudacion_bruta = db.Column(db.Float, nullable=False)
    premios_pagados = db.Column(db.Float, default=0.0)
    neto_caja = db.Column(db.Float, nullable=False)

# --- GASTOS (Ahora sabe de qué sucursal salió) ---
class Gasto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, default=date.today)
    sucursal = db.Column(db.String(50), nullable=False) # 'Av. Cba' o 'Los Olmos'
    descripcion = db.Column(db.String(200), nullable=False)
    monto = db.Column(db.Float, nullable=False)

# --- INGRESOS (Ingresos diarios de las despensas) ---
class IngresoDespensa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, default=date.today)
    sucursal = db.Column(db.String(50), nullable=False) # 'Av. Cba' o 'Los Olmos'
    monto = db.Column(db.Float, nullable=False)