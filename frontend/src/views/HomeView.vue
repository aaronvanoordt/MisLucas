<template>
  <div class="row w-100">
    <div class="col-6">
      <img src="@/assets/static/images/isometric-login.svg" />
    </div>
    <div class="col-6 px-5">
      <a href="/" class="text-end">
        <div class="logo">
          <img
            class="logo-size"
            src="@/assets/static/images/logo-light.svg"
            alt=""
            width="200px"
          />
        </div>
      </a>
      <h1
        style="
          font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
            'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
        "
      >
        Hola,
      </h1>
      <h1
        style="
          font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
            'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
        "
      >
        Bienvenido a Mis Lucas!
      </h1>
      <div>
        <p class="text-secondary">
          Nuevo usuario? <router-link to="/registro">Registro</router-link> |
        </p>
      </div>
      <div>
        <p class="text-danger alert alert-danger" v-if="mostrar_mensaje">
          {{ mensaje_error }}
        </p>
      </div>
      <form method="POST" action="#">
        <div class="form-floating my-2">
          <input
            class="form-control"
            type="text"
            name="usuario"
            placeholder="E-mail Address"
            required
            v-model="email"
          />
          <label for="usuario"> Email Address </label>
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
        </div>

        <button
          id="submit"
          type="button"
          @click="login"
          class="btn btn-primary me-2"
        >
          Ingresar
        </button>
        <router-link to="/recuperar">Te olvidaste la contraseña?</router-link> |
      </form>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from "axios";
export default {
  name: "HomeView",
  components: {},
  data() {
    return {
      email: "",
      password: "",
      mensaje_error: "",
      mostrar_mensaje: false,
    };
  },
  methods: {
    login() {
      axios
        .post("http://localhost:5000/api/login", {
          email: this.email,
          password: this.password,
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
