<template>
  <div class="row w-100">
    <div class="col-6">
      <img src="@/assets/static/images/register.svg" />
    </div>
    <div class="col-6 px-5">
      <div class="logo">
        <img
          class="logo-size"
          src="@/assets/static/images/logo-light.svg"
          alt=""
          width="170px"
        />
      </div>
      <h1>Registrarse</h1>
      <p>Hola! Registrate para continuar.</p>
      <div>
        <p class="text-secondary">
          Ya tienes cuenta? Ingresa a <router-link to="/">Login</router-link> |
        </p>
      </div>
      <div>
        <p class="text-danger alert alert-danger" v-if="mostrar_mensaje">
          {{ mensaje_error }}
        </p>
      </div>
      <form method="POST">
        <div class="form-floating my-2">
          <input
            class="form-control"
            type="text"
            name="correo"
            placeholder="E-mail Address"
            required
            v-model="email"
          />
          <label for="correo"> Email Address </label>
        </div>
        <div class="form-floating my-2">
          <input
            class="form-control"
            type="text"
            name="nombre"
            placeholder="nombre"
            required
            v-model="nombre"
          />
          <label for="nombre"> Nombre </label>
        </div>
        <div class="form-floating my-2">
          <input
            class="form-control"
            type="text"
            name="apellido"
            placeholder="apellido"
            required
            v-model="apellido"
          />
          <label for="apellido"> Apellido </label>
        </div>
        <div class="form-floating my-2">
          <input
            class="form-control"
            type="password"
            name="contrasena"
            placeholder="Password"
            required
            v-model="password"
          />
          <label for="contrasena"> Password </label>
          <div class="form-text">
            No olvides que tu contraseña debe incluir:
            <ul>
              <li>Tener minimo 8 caracteres</li>
              <li>Tener minimo un numero</li>
            </ul>
          </div>
        </div>
        <br />
        <button
          id="submit"
          type="button"
          class="btn btn-primary me-2"
          @click="registro"
        >
          Registrar
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      email: "",
      password: "",
      nombre: "",
      apellido: "",
      mensaje_error: "",
      mostrar_mensaje: false,
    };
  },
  methods: {
    registro() {
      axios
        .post("http://localhost:5000/api/signup", {
          email: this.email,
          password: this.password,
          name: this.nombre,
          surname: this.apellido,
        })
        .then((response) => {
          localStorage.setItem("token", response.data.token);
          this.$router.push("/dashboard");
        })
        .catch((error) => {
          this.mensaje_error = error.response.data.message;
          this.mostrar_mensaje = true;
        });
    },
  },
};
</script>

<style lang="scss" scoped></style>
