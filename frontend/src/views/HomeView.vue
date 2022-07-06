<template>
  <div class="home">
    <HelloWorld msg="Login" />
    <form method="POST" action="/api/users">
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
      <div class="form-floating my-2">
        <input
          class="form-control"
          type="password"
          name="contrasena"
          placeholder="Password"
          required
        />
        <label for="contrasena"> Password </label>
      </div>

      <button id="submit" type="submit" class="btn btn-primary me-2">
        Ingresar
      </button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
// @ is an alias to /src
import HelloWorld from "@/components/HelloWorld.vue";
import { logicalExpression } from '@babel/types';

export default {
  name: "HomeView",
  components: {
    HelloWorld,
  },
};
methods: {
  login()
  {
    let result = axios.get('/api/users').then(response => {
      console.log(response.data);
    });
  }
}
</script>s
