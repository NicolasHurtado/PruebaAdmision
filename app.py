from flask import Flask, render_template ,request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


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

    def __init__(self,porcentaje,  base):
        self.porcentaje = porcentaje
        self.base = base
    
    def __repr__(self):
        texto = f'Id Impuesto: {self.id} --> Porcentaje: {self.porcentaje} / Base: {self.base}'
        return texto

@app.route('/')
def Index():
    return render_template('index.html')



@app.route('/factura',methods=["GET","POST"])
def Factura():
    impuestos = Impuesto.query.all()
    if request.method=="POST":
        item = 1 
        while True:
        
            llave = "input{}".format(item)
            llavecantidad = "cantidad{}".format(item)
            llaveprecio = "precio{}".format(item)
            llaveimpuesto = "impuesto{}".format(item)
            llavetotal = "total{}".format(item)
            print(llavetotal)
            
            try:
                print("llave",llave)
                producto = request.form[llave]
                print("El producto es: ", producto)
                cantidad = request.form[llavecantidad]
                print("La cantidad es: ", cantidad)
                precio = request.form[llaveprecio]
                print("El precio es: ", precio)
                impuesto = request.form.getlist(llaveimpuesto)
                print("Los impuestos son: ", impuesto)
                total = request.form[llavetotal]
                print("El total del producto es: ", total)
            except:
                break
            item+=1
    
    
    return render_template('factura.html', impuestos=impuestos)


@app.route('/gestion',methods=["GET","POST"])
def Gestion():
    impuestos = Impuesto.query.all()
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

        return redirect(url_for('Gestion'))

    return render_template('editar.html', impuesto=impuesto)

@app.route('/consultarImpuestos',methods=["GET","POST"])
def consultarImpuestos():
    impuestos = Impuesto.query.all()
    imp = [[i.descripcion,i.porcentaje,i.base] for i in impuestos ]
    if request.method=="POST":
        return redirect(url_for('Factura'))
    return jsonify({"data":imp})



if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")