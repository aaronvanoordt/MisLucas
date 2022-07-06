<template>
  <!-- <div class="row w-100">
    <div class="col-6">
      <div>
        <b-img
          src="src/assets/static/images/billete.svg"
          fluid
          alt="Responsive image"
        ></b-img>
      </div>
    </div>
    <div class="col-6 px-5">
      <a href="/" class="text-end">
        <div class="logo">
          <img
            class="logo-size"
            src="/static/images/logo-light.svg"
            alt=""
            width="170px"
          />
        </div>
      </a>
      <h1>Registrarse</h1>
      <p>Hola! Registrate para continuar.</p>
      <div>
        <p class="text-secondary">
          Ya tienes cuenta? Ingresa a <a href="{{url_for('index')}}">Login</a>
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
          />
          <label for="correo"> Email Address </label>
        </div>
        <div class="form-floating my-2">
          <input
            class="form-control"
            type="text"
            name="nombre"
            placeholder="E-mail Address"
            required
          />
          <label for="nombre"> Nombre </label>
        </div>
        <div class="form-floating my-2">
          <input
            class="form-control"
            type="text"
            name="apellido"
            placeholder="E-mail Address"
            required
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
          />
          <label for="contrasena"> Password </label>
          <div class="form-text">
            No olvides que tu contraseña debe incluir:
            <ul>
              <li>Tener minimo 8 caracteres</li>
              <li>Tener minimo un numero</li>
              <li>Tener minimo una letra mayuscula</li>
            </ul>
          </div>
        </div>
        <br />
        <button id="submit" type="submit" class="btn btn-primary me-2">
          Registrar
        </button>
      </form>
    </div>
  </div> -->
  <div>
    <b-img
      src="https://picsum.photos/1024/400/?image=41"
      fluid
      alt="Responsive image"
    ></b-img>
  </div>
  <img alt="Logo" src="frontend\src\assets\static\images\billetes.svg" />
</template>
