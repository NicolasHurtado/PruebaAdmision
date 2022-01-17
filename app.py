from flask import Flask, render_template ,request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime


app = Flask(__name__)

app.config['SECRET_KEY'] = 'clavesecreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://qwovfbgagedxak:5b917a80a55b0f5dd22f2c9213a95a58b3c28c1b7e32de0444bd3d48112f0159@ec2-34-230-198-12.compute-1.amazonaws.com:5432/d9gn1i3p7mdrp5'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Migrate(app, db)

class Impuesto(db.Model):
    __tablename__ = 'Impuestos'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(250))
    porcentaje = db.Column(db.Float)
    base = db.Column(db.Float)

    def __init__(self,descripcion, porcentaje,  base):
        self.descripcion = descripcion
        self.porcentaje = porcentaje
        self.base = base
    
    def __repr__(self):
        texto = f'Id Impuesto: {self.id} --> Porcentaje: {self.porcentaje} / Base: {self.base}'
        return texto

class Factura(db.Model):
    __tablename__ = 'Facturas'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    cliente = db.Column(db.String(50))
    detalle = db.Column(JSON)
    totalimpuestos = db.Column(db.Float)
    totalpagar = db.Column(db.Float)

    def __init__(self,fecha,  cliente,detalle,totalimpuestos, totalpagar ):
        self.fecha = fecha
        self.cliente = cliente
        self.detalle = detalle
        self.totalimpuestos = totalimpuestos
        self.totalpagar = totalpagar
    
    def __repr__(self):
        texto = f'Id Factura: {self.id} --> Fecha: {self.fecha} / Cliente: {self.cliente}'
        return texto

@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/nuevo_impuesto',methods=["GET","POST"])
def NuevoImpuesto():
    if request.method=="POST":
        descripcion = request.form["descripcion"]
        porcentaje = float(request.form["porcentaje"])/100
        base = request.form["base"]
        print(f"Descripcion: {descripcion}")
        print(f"Porcentaje: {porcentaje}")
        print(f"Base: {base}")
        nuevoimp = Impuesto(descripcion,porcentaje,base)
        db.session.add(nuevoimp)
        db.session.commit()
        return redirect(url_for('Gestion'))

    return render_template('impuesto.html')

@app.route('/factura',methods=["GET","POST"])
def Facturas():
    impuestos = Impuesto.query.all()
    if request.method=="POST":
        cliente = request.form["cliente"]
        print("El cliente es: ", cliente)

        fecha = request.form["fecha"]
        print("La fecha es: ", fecha)

        print("".center(50,"-"))
        i = 1 
        listaitems = []

        #Recorre tantos items hayan en la pag
        while True:
            item = {}
            llaveproducto = "input{}".format(i)
            llavecantidad = "cantidad{}".format(i)
            llaveprecio = "precio{}".format(i)
            llaveimpuesto = "impuesto{}".format(i)
            llavetotal = "total{}".format(i)
            print(llavetotal)
            
            try:
                print("llave",llaveproducto)

                producto = request.form[llaveproducto]
                print("El producto es: ", producto)

                cantidad = request.form[llavecantidad]
                print("La cantidad es: ", cantidad)

                precio = request.form[llaveprecio]
                print("El precio es: ", precio)

                impuesto = request.form.getlist(llaveimpuesto)
                print("Los impuestos son: ", impuesto)

                total = request.form[llavetotal]
                print("El total del producto es: ", total)

                item["item"] = producto
                item["cantidad"] = cantidad
                item["precio"] = precio
                item["impuesto"] = impuesto
                item["total"] = total

                listaitems.append(item)
                print("\n")
                print("".center(50,"-"))
            except:
                break
            i+=1
        
        totalimpuestos = request.form["totalimpuestos"]
        print("El totalimpuestos es: ", totalimpuestos)

        totalgeneral = request.form["totalgeneral"]
        print("El totalgeneral es: ", totalgeneral)

        # Crea la nueva factura
        nuevafactura = Factura(fecha,cliente,listaitems,totalimpuestos,totalgeneral)
        db.session.add(nuevafactura)
        db.session.commit()
    
    
    return render_template('factura.html', impuestos=impuestos)


@app.route('/gestion',methods=["GET","POST"])
def Gestion():
    impuestos = Impuesto.query.order_by(Impuesto.id).all()
    return render_template('gestion.html',impuestos=impuestos)

@app.route('/editar/<int:id>',methods=["GET","POST"])
def Editar(id):
    impuesto = Impuesto.query.get(id)
    if request.method=="POST":
        descripcion = request.form["descripcion"]
        porcentaje = request.form["porcentaje"]
        base = request.form["base"]
        print(f"Descripcion: {descripcion}")
        print(f"Porcentaje: {porcentaje}")
        print(f"Base: {base}")
        impuesto.descripcion = descripcion
        impuesto.porcentaje = porcentaje
        impuesto.base = base
        db.session.commit()

        return redirect(url_for('Gestion'))

    return render_template('editar.html', impuesto=impuesto)

@app.route('/lista_facturas',methods=["GET","POST"])
def Listar():
    facturas = Factura.query.order_by(Factura.id).all()
    return render_template('listafacturas.html', facturas=facturas)

@app.route('/consultarImpuestos',methods=["GET","POST"])
def consultarImpuestos():
    impuestos = Impuesto.query.all()
    imp = [[i.descripcion,i.porcentaje,i.base] for i in impuestos ]
    if request.method=="POST":
        return redirect(url_for('Factura'))
    return jsonify({"data":imp})



if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")