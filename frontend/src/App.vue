<template>
  <nav>
    <img alt="Logo" src="frontend\src\assets\logo.png" />
    <router-link to="/">Login</router-link> |
    <router-link to="/about">Signup</router-link>
    <h1>Bienvenido a MisLucas</h1>
  </nav>
  hola
  <router-view />
  chau
  <footer>
    <p>&copy; MisLucas</p>
  </footer>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: blue;
}
</style>
