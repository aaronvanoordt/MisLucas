<template>
  <div class="row w-100">
    <div class="col-6 p-5">
      <img src="@/assets/static/images/security.svg" />
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
      <h3>Bienvenido a Mis Lucas!</h3>
      <p>El poder del control de tu dinero en tus manos.</p>
      <div>
        <router-link to="/">Login</router-link> |
        <router-link to="/registro">Registrarse</router-link>
      </div>
      <div class="alert alert-warning" v-if="show">
        PROXIMAMENTE SE ABRIRÁ LA FUNCIONALIDAD DE RECUPERAR CONTRASEÑA.
      </div>
      <form method="POST" action="#">
        <div class="form-floating my-2">
          <input
            class="form-control"
            type="text"
            name="usuario"
            placeholder="E-mail Address"
            required
          />
          <label for="usuario"> Email Address </label>
        </div>
        <button
          id="submit"
          type="button"
          class="btn btn-primary me-2"
          @click="submit"
        >
          Recuperar Contrasena
        </button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data: () => {
    return {
      show: false,
    };
  },
  methods: {
    submit() {
      this.show = true;
    },
  },
};
</script>

<style lang="scss" scoped></style>
