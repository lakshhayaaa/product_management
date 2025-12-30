from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from database_models import Base, Product
from schema import ProductCreate, ProductResponse

app = FastAPI()

app.title = "Product Management API"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initial product list (Pydantic)
initial_products = [
    ProductCreate(name="Laptop", price=75000, quantity=5, description="High performance laptop"),
    ProductCreate(name="Smartphone", price=30000, quantity=10, description="Latest smartphone"),
    ProductCreate(name="Headphones", price=5000, quantity=15, description="Noise cancelling"),
]

# Initialize DB only once
def init_db():
    db = SessionLocal()
    try:
        # Avoid duplicates — only initialize if table is empty
        if db.query(Product).count() == 0:
            for p in initial_products:
                db_product = Product(**p.dict())
                db.add(db_product)
            db.commit()
    finally:
        db.close()


init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Product Management API"}

@app.get("/products", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.get("/products/{id}", response_model=ProductResponse | None)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.id == id).first()

@app.post("/products", response_model=ProductResponse)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/products/{id}", response_model=ProductResponse | None)
def update_product(id: int, product: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.price = product.price
        db_product.quantity = product.quantity
        db_product.description = product.description
        db.commit()
        db.refresh(db_product)
        return db_product
    return None

@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return {"message": "Product deleted successfully"}
    return {"message": "Product not found"}
