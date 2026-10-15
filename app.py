from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///producto.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return f"<Product '{self.name}', price={self.price}, stock={self.stock}>"

def init_db():
    with app.app_context():
        db.create_all()
        print("Base de datos creada satisfactoriamente.\n") 


# 1. CREATE
def create_product(name, price, stock=0):
    with app.app_context():
        new_product = Product(name=name, price=price, stock=stock)
        db.session.add(new_product)
        db.session.commit()
        print(f"[CREATE] Producto creado: {new_product}")
        return new_product

# 2. READ - Listar TODOS los productos
def get_all_products():
    with app.app_context():
        products = Product.query.all()
        print(f"[READ ALL] Total de productos: {len(products)}")
        for p in products:
            print(f"  {p}")
        return products

# 3. READ - Consultar UNO por ID
def get_product_by_id(product_id):
    with app.app_context():
        product = db.session.get(Product, product_id)
        if product:
            print(f"[READ BY ID] Encontrado: {product}")
        else:
            print(f"[READ BY ID] No se encontró el producto con ID {product_id}")
        return product

# 4. UPDATE 
def update_product(product_id, name=None, price=None, stock=None):
    with app.app_context():
        product = db.session.get(Product, product_id)
        if product:
            if name is not None:
                product.name = name
            if price is not None:
                product.price = price
            if stock is not None:
                product.stock = stock
            
            db.session.commit()
            print(f"[UPDATE] Actualizado: {product}")
            return product
        print(f"[UPDATE] Producto con ID {product_id} no encontrado.")
        return None

# 5. DELETE
def delete_product(product_id):
    with app.app_context():
        product = db.session.get(Product, product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            print(f"[DELETE] Producto con ID {product_id} eliminado exitosamente.")
            return True
        print(f"[DELETE] Producto con ID {product_id} no encontrado.")
        return False


if __name__ == '__main__':
    init_db()

    p1 = create_product("Laptop Gamer", 1200.00, 5)
    p2 = create_product("Mouse", 20.00) # Stock por defecto 0

    print("-" * 40)
    get_all_products()

    print("-" * 40)
    get_product_by_id(1)

    print("-" * 40)
    update_product(2, price=25.00, stock=10)

    print("-" * 40)
    delete_product(1)

    print("-" * 40)
    get_all_products()