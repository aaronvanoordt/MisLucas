<template>
  <div class="d-flex p-3 justify-content-between">
    <h1 style="font-weight: bold">
      Bienvenido {{ usuario.nombre + " " + usuario.apellido }}
      <!-- Bienvenido  -->
    </h1>
    <div>
      <button class="btn btn-danger" @click="logOut">Logout</button>
    </div>
  </div>
  <h2 class="text-center text-success p-2">Tienes acumulado: {{ total }}</h2>
  <div class="alert alert-success" v-if="success.show">
    {{ success.mensaje }}
  </div>
  <div class="alert alert-danger" v-if="fail.show">
    {{ fail.mensaje }}
  </div>
  <div class="row w-100">
    <div class="col-5 p-5">
      <form method="POST" action="#" autocomplete="off" id="crear">
        <h2 v-if="edicion">Editar transacción</h2>
        <h2 v-else>Crear transacción</h2>
        <div class="form-floating my-2">
          <input
            class="form-control"
            type="number"
            name="monto"
            id="monto"
            v-model="transaccion.monto"
          />
          <label for="monto">Monto</label>
        </div>

        <div class="form-floating my-2">
          <input
            class="form-control"
            type="text"
            name="detalle"
            id="detalle"
            v-model="transaccion.detalle"
          />
          <label for="detalle">Detalle</label>
        </div>

        <div class="form-floating my-2">
          <input
            class="form-control"
            type="text"
            name="tipo"
            id="tipo"
            v-model="transaccion.tipo"
          />
          <label for="tipo">Tipo</label>
        </div>

        <input
          type="button"
          value="Submit"
          class="btn btn-primary"
          @click="crearTransaccion"
        />
      </form>
    </div>

    <div class="col-7 p-5">
      <h2>Movimientos</h2>
      <table id="Transacciones" class="table">
        <thead>
          <tr>
            <th scope="col">Fecha</th>
            <th scope="col">Monto</th>
            <th scope="col">Detalle</th>
            <th scope="col">Tipo</th>
            <th scope="col">Modificar</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(t, i) in transacciones" :key="i">
            <th>{{ t.fecha }}</th>
            <th>{{ t.monto }}</th>
            <th>{{ t.detalle }}</th>
            <th>{{ t.tipo }}</th>
            <th>
              <button
                class="btn btn-sm btn-outline-primary"
                @click="editarTransaccion(t.id, t.monto, t.detalle, t.tipo, i)"
              >
                Editar
              </button>
              <button
                class="btn btn-sm btn-outline-danger"
                @click="eliminarTransaccion(t.id)"
              >
                Eliminar
              </button>
            </th>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      usuario: {
        nombre: "",
        apellido: "",
      },
      transacciones: [],
      transaccion: {
        monto: "",
        detalle: "",
        tipo: "",
      },
      edicion: false,
      id: 0,
      index: -1,
      success: {
        show: false,
        mensaje: "",
      },
      fail: {
        show: false,
        mensaje: "",
      },
    };
  },
  methods: {
    logOut() {
      axios
        .post("http://localhost:5000/api/logout", null, {
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then(() => {
          localStorage.removeItem("token");
          this.$router.push("/");
        })
        .catch((error) => {
          this.fail.mensaje = error.response.data.message;
          this.fail.show = true;
        });
    },
    crearTransaccion() {
      if (this.edicion) {
        axios
          .patch(
            "http://localhost:5000/api/transacciones/" + this.id,
            this.transaccion,
            {
              headers: {
                "Content-Type": "application/json",
                Authorization: "Bearer " + localStorage.getItem("token"),
              },
            }
          )
          .then(() => {
            this.transacciones[this.index].monto = this.transaccion.monto;
            this.transacciones[this.index].detalle = this.transaccion.detalle;
            this.transacciones[this.index].tipo = this.transaccion.tipo;
            this.edicion = false;
            this.id = 0;
            this.transaccion.monto = "";
            this.transaccion.detalle = "";
            this.transaccion.tipo = "";
            this.success.mensaje = "Transacción editada correctamente";
            this.success.show = true;
          })
          .catch((error) => {
            this.fail.mensaje = error.response.data.message;
            this.fail.show = true;
          });
      } else {
        axios
          .post("http://localhost:5000/api/transacciones", this.transaccion, {
            headers: {
              "Content-Type": "application/json",
              Authorization: "Bearer " + localStorage.getItem("token"),
            },
          })
          .then((response) => {
            let t = {};
            t.monto = this.transaccion.monto;
            t.detalle = this.transaccion.detalle;
            t.tipo = this.transaccion.tipo;
            t.fecha = response.data.fecha;
            t.id = response.data.id;
            console.log(t);
            this.transacciones.push(t);
            this.transaccion.monto = "";
            this.transaccion.detalle = "";
            this.transaccion.tipo = "";
            this.success.mensaje = "Transacción creada correctamente";
            this.success.show = true;
          })
          .catch((error) => {
            this.fail.mensaje = error.response.data.message;
            this.fail.show = true;
          });
      }
    },
    eliminarTransaccion(id) {
      axios
        .delete("http://localhost:5000/api/transacciones/" + id, {
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then(() => {
          this.transacciones = this.transacciones.filter((t) => t.id != id);
          this.success.mensaje = "Transacción eliminada correctamente";
          this.success.show = true;
        })
        .catch((error) => {
          this.fail.mensaje = error.response.data.message;
          this.fail.show = true;
        });
    },
    editarTransaccion(id, monto, detalle, tipo, idx) {
      this.transaccion.monto = monto;
      this.transaccion.detalle = detalle;
      this.transaccion.tipo = tipo;
      this.edicion = true;
      this.id = id;
      this.index = idx;
    },
  },
  computed: {
    total() {
      let total = 0;
      for (let t of this.transacciones) {
        total += t.monto;
      }
      return total;
    },
  },
  mounted() {
    axios
      .get("http://localhost:5000/api/me", {
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
      })
      .then((response) => {
        this.usuario.nombre = response.data.nombre;
        this.usuario.apellido = response.data.apellidos;
      })
      .catch((error) => {
        this.fail.mensaje = error.response.data.message;
        this.fail.show = true;
      });
    axios
      .get("http://localhost:5000/api/transacciones", {
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
      })
      .then((response) => {
        this.transacciones = response.data.transacciones;
      })
      .catch((error) => {
        this.fail.mensaje = error.response.data.message;
        this.fail.show = true;
      });
  },
};
</script>

<style lang="scss" scoped></style>
