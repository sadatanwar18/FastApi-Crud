from fastapi import FastAPI, Depends 
from models import Product
from database import session, engine
import database_model, models
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

database_model.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "Welcome"
 

def get_db():
    db = session()
    try:    
        yield db
    finally:
        db.close


# def init_db():
#     db = session()
#     count = db.query(database_model.Product).count
    
#     if count == 0:
#         for product in Product:
#             db.add(database_model.Product(**product.model_dump()))
    
#     db.commit()

# init_db()



@app.get("/products", response_model=list[models.Product])
def get_all_products(db: Session = Depends(get_db)):

    db_products = db.query(database_model.Product).all()

    return db_products
    
@app.get("/product/{id}", response_model=models.Product)
def get_product_by_id(id:int, db: Session = Depends(get_db)):

    db_product = db.query(database_model.Product).filter(database_model.Product.id == id).first()
    if db_product:
        return db_product
    
    return "Product not found"



@app.post("/product", response_model=models.Product)
def add_product(product: models.ProductCreate, db: Session = Depends(get_db)):
    
    db_product = database_model.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product 


@app.put("/product/{id}", response_model=models.Product)
def update_product(id:int, product:models.ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == id).first()
    if not db_product:
        return "No product found"
    
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity

    db.commit()
    db.refresh(db_product)
    return db_product


@app.delete("/product/{id}")
def delete_product(id:int, db: Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == id).first()

    if not db_product:
        return "Product not found"
    
    db.delete(db_product)
    db.commit()
    return {"message": f"Product with id {id} has been deleted"}



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials= True,
    allow_methods=["*"],
    allow_headers=["*"]
)
 