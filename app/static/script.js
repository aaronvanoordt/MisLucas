const crear=document.getElementById("crear")
const editar=document.getElementById("editar")
const eliminar= document.getElementById("eliminar")
const eliminar_all= document.getElementById("eliminar_all")

function editarTransccion(id, monto, detalle, tipo){ 
    //Se esconde el formulario de crear
   crear.classList.add("d-none")
    //se muestra el formulario de editar
    editar.classList.remove("d-none")
    editar["transaccion_id"].value=id
    editar["monto"].value=monto
    editar["detalle"].value=detalle
    editar["tipo"].value=tipo

}
function crearTransaccion(){
    editar.classList.add("d-none")
    crear.classList.remove("d-none")
}

function eliminarTransaccion(id){
    eliminar["transaccion_id"].value=id
    eliminar.submit()
}

function eliminarAll(){
    eliminar_all.submit()
}