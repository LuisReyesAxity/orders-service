from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# ---- CONEXIÓN (Como el ConnectionString en appsettings.json) ----
# create_engine define a qué base de datos nos conectamos (SQLite en este caso).
engine = create_engine("sqlite:///orders.db")

# SessionLocal es tu 'DbContext'. Es la fábrica que crea conexiones para hacer consultas.
SessionLocal = sessionmaker(bind=engine)


# ---- BASE (Como el DbContext base o una clase Entidad base) ----
class Base(DeclarativeBase):
    pass


# ---- MODELO / ENTIDAD (POCO class en C#) ----
# Aquí definimos la tabla "orders" y sus columnas.
class OrderModel(Base):
    __tablename__ = "orders"

    # Column(String, primary_key=True) es igual al atributo [Key] en C#.
    id = Column(String, primary_key=True)
    # nullable=False es como el atributo [Required].
    customer_id = Column(String, nullable=False)
    status = Column(String, default="pending")


# ---- MIGRACIÓN INICIAL (EnsureCreated en .NET) ----
# Esto crea físicamente el archivo .db y las tablas si no existen.
Base.metadata.create_all(engine)


# ---- OPERACIONES CRUD ----
if __name__ == "__main__":
    # Instanciamos la sesión (Como hacer un 'new MyDbContext()')
    session = SessionLocal()

    # 1. CREATE (Insert)
    nueva_orden = OrderModel(id="3", customer_id="cliente-1", status="pending")
    session.add(nueva_orden) # Prepara el Insert
    session.commit()         # Ejecuta el cambio en la DB (SaveChangesAsync)

    # 2. READ (Select)
    # .filter_by es como el .Where() de LINQ. .first() es igual a .FirstOrDefault().
    orden = session.query(OrderModel).filter_by(id="3").first()
    print(f"Orden encontrada: {orden.customer_id} - {orden.status}")

    # 3. UPDATE (Update)
    # Solo cambiamos la propiedad y commiteamos (Change Tracking automático).
    orden.status = "confirmed"
    session.commit()
    print(f"Status actualizado: {orden.status}")

    # 4. DELETE (Delete)
    session.delete(orden)
    session.commit()
    print("Orden eliminada")

    # Verificación final
    orden_eliminada = session.query(OrderModel).filter_by(id="3").first()
    print(f"Orden después de eliminar: {orden_eliminada}")