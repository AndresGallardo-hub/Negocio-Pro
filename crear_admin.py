from app import create_app, db
from app.models import Usuario

# 1. Fabricamos la aplicación con TODAS tus configuraciones reales
app = create_app()

# 2. Entramos al contexto de tu app
with app.app_context():
    # 3. Buscamos al usuario admin
    admin = Usuario.query.filter_by(username='admin').first()
    
    if not admin:
        # Si no existe, lo creamos
        nuevo_admin = Usuario(username='admin')
        nuevo_admin.set_password('123456')  # Tu contraseña
        db.session.add(nuevo_admin)
        db.session.commit()
        print("¡Éxito total! Usuario 'admin' creado en la base de datos correcta.")
    else:
        # Por si ya lo habías creado y no te acordabas la clave, se la reseteamos
        admin.set_password('123456')
        db.session.commit()
        print("El usuario ya existía. Le reseteamos la clave a '123456' por las dudas.")