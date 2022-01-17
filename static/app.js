document.addEventListener('DOMContentLoaded', function () {
    agregarItem();
});

var data_impuestos;
function codeAddress() {
    $.ajax({
        type: 'GET',
        url: "/consultarImpuestos",
        success: function (response) {
            console.log("funcione gay",response)
            data_impuestos = response.data;
        },
        error: function (response) {
            console.log("como que falle jajaj")
        }
    })
}
window.onload = codeAddress;

var i = 1;
boton = document.querySelector('.agregar')
function agregarItem() {
    boton.onclick = function(){
        console.log("Click en el boton agregar")
        
        let br1 = document.createElement("br");
        // event.preventDefault();
        let item = "item" + i;

        let div = document.createElement("div");
        div.className = "item" + i;
        div.id = "item" + i;
        // div.innerText = "Item # " + i;

        //Creamos un nuevo atributo
        var a = document.createAttribute("valor");
        a.value = i;

        div.setAttributeNode(a);
        //document.body.appendChild(div);

        // Lo añadimos
        document.getElementById("factura").appendChild(div);

        div.appendChild(br1);

        //Creamos item
        let spanitem = document.createElement("h4");
        spanitem.textContent = "Item # " + i;
        spanitem.className = "h4" + i;
        spanitem.id = "h4" + i;
        div.appendChild(spanitem);

        // Creamos el input de item

        let input1 = document.createElement("input");
        input1.placeholder = "Nombre Item";
        input1.className = "input" + i;
        input1.id = "input" + i;
        input1.name = "input" + i;
        input1.innerText = document.getElementById("getText").innerText;
        div.appendChild(input1);

        // Creamos el input de cantidad
        // Creamos el span del item
        let span1 = document.createElement("span");
        span1.innerText = "Cantidad";
        div.appendChild(span1);
        let input2 = document.createElement("input");
        input2.className = "cantidad" + i;
        input2.id = "cantidad" + i;
        input2.name = "cantidad" + i;
        input2.type = "number";
        input2.innerText = document.getElementById("getText").innerText;
        div.appendChild(input2);

        // Creamos el input de precio
        let span2 = document.createElement("span");

        span2.innerText = "Precio";
        div.appendChild(span2);
        let precio = document.createElement("input");
        precio.className = "precio" + i;
        precio.id = "precio" + i;
        precio.name = "precio" + i;
        precio.type = "number";
        precio.innerText = document.getElementById("getText").innerText;
        div.appendChild(precio);

        // Creamos el span de impuestos
        let spanimp = document.createElement("span");
        spanimp.innerText = "Impuestos";
        div.appendChild(spanimp);


        let da = data_impuestos.length;
        console.log(da)
        console.log("HOLIS data_impuestos",data_impuestos)
        console.log("Este es el primer impuesto gay ",data_impuestos[0])
        console.log("Este es la descripcion del primer impuesto gay gay ",data_impuestos[0][0])
        // Creamos el select de impuestos
        let select = document.createElement("select");
        select.multiple = true;
        select.id = "impuesto" + i;
        select.name = "impuesto" + i;
        select.innerText = document.getElementById("getText").innerText;

        for (let i = 0; i < data_impuestos.length; i++) {
            let option = document.createElement("option");
            option.setAttribute("value", `${data_impuestos[i][1]}`)
            let optionTexto = document.createTextNode(`${data_impuestos[i][0]}`);
            option.appendChild(optionTexto);
            select.appendChild(option);
        }

        div.appendChild(select);

        let span3 = document.createElement("span");

        span3.innerText = "Total ";
        div.appendChild(span3);
        let total = document.createElement("input");

        total.value = 0;
        total.className = "total" + i;
        total.id = "total" + i;
        total.name = "total" + i;
        total.type = "number";
        total.readOnly = true;
        total.innerText = document.getElementById("getText").innerText;

        div.appendChild(total);

        // Actualiza el total con los datos ingresados en cantidad y precio
        let inputcantidad = document.getElementById(`${input2.id}`);
        let inputprecio = document.getElementById(`${precio.id}`);

        // Cuando se digite primero la cantidad pueda hacer el calculo
        inputcantidad.addEventListener("keyup", (event1) => {
            let cantidad = event1.path[0].value;
            console.log(`Este es la cantidad que se escribió: ${cantidad}`);
            inputprecio.addEventListener("keyup", (event2) => {
            let valorprecio = event2.path[0].value;
            console.log(`Este es el precio que se escribió: ${valorprecio}`);
            valorTotal = cantidad * valorprecio;
            document.getElementById(`${total.id}`).innerHTML = valorTotal;
            total.value = valorTotal;
            });
        });

        // Cuando se digite primero el precio pueda hacer el calculo
        inputprecio.addEventListener("keyup", (event1) => {
            let valorprecio = event1.path[0].value;
            console.log(`Este es el precio que se escribió: ${valorprecio}`);
            inputcantidad.addEventListener("keyup", (event2) => {
            let cantidad = event2.path[0].value;
            console.log(`Este es la cantidad que se escribió: ${cantidad}`);
            valorTotal = cantidad * valorprecio;
            document.getElementById(`${total.id}`).innerHTML = valorTotal;
            total.value = valorTotal;
            });
        });

        //Boton eliminar item
        let eliminar = document.createElement("button");

        eliminar.innerText = "Eliminar";
        eliminar.id = "eliminar" + i;
        eliminar.className = "eliminar" + i;
        eliminar.name = "eliminar" + i;

        eliminar.onclick = function () {
            event.preventDefault();
            console.log(eliminar.id);
            let eliminarI = ".item" + eliminar.className;
            $(eliminarI).remove();
            ordernarItems();
        };

        div.appendChild(eliminar);
        i++;
    }
}

function editarIn(texto, id, nuevo) {
    console.log("ESTE ES EDITAR");
    console.log(texto, id, nuevo);
    let ids = texto + id;
    console.log("ESTE ES EL ids de los inputs", ids);
    let el = document.getElementById(ids);
    console.log(el);
    let nuevoids = texto + nuevo;
    console.log("ESTE ES EL ID -> ", el.id);
    el.id = nuevoids;
    el.name = nuevoids;
    if (texto === "eliminar") {
        el.className = nuevo;
    } else {
        el.className = nuevoids;
    }
}
function editarItem(texto, id, nuevo) {
    console.log("ESTE ES EDITAR");
    console.log(texto, id, nuevo);
    let ids = texto + id;
    console.log("ESTE ES EL ids", ids);
    let el = document.getElementById(ids);
    let nuevoids = texto + nuevo;
    el.id = nuevoids;
    el.className = nuevoids;

    el.setAttribute("valor", nuevo);

    let spanI = "h4" + id;
    console.log("ESTE ES EL SPAN ", spanI);
    let el2 = document.getElementById(spanI); //spanitem
    let nuevoItem = "Item # " + nuevo;
    el2.textContent = nuevoItem;
    el2.id = "h4" + nuevo;
    // $(spanI).html('Edited Value');
}
function ordernarItems() {
    console.log("LLAMADO ORDENAR ITEMS");
    var x = document.getElementById("factura").querySelectorAll("div");
    console.log("la cantidad es ; ", x.length);
    for (let p = 0; p < x.length; p++) {
        console.log("el elemtento  es", x[p].getAttribute("valor"));
        console.log("OPA ssssssssssss ", p);
        editarIn("input", x[p].getAttribute("valor"), p + 1);
        editarIn("precio", x[p].getAttribute("valor"), p + 1);
        editarIn("cantidad", x[p].getAttribute("valor"), p + 1);
        editarIn("total", x[p].getAttribute("valor"), p + 1);
        editarIn("eliminar", x[p].getAttribute("valor"), p + 1);
    }
    for (let p = 0; p < x.length; p++) {
        console.log("EDITANDO ITEM");
        editarItem("item", x[p].getAttribute("valor"), p + 1);
    }
    i = x.length + 1;
}
