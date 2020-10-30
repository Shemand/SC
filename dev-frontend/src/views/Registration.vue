<template>
    <div class="container">
      <div class="row"><h2 class="center-align">Secure Center</h2></div>
      <div class="row"><h4 class="center-align">Регистрация</h4></div>
      <div class="row">
        <form @submit.prevent="registerUser" class="reg-block col s6 offset-s3 center-align grey lighten-5">
          <div class="row">
            <div class="input-field col s6">
              <input id="first_name" type="text" class="validate">
              <label for="first_name">Имя</label>
            </div>
            <div class="input-field col s6">
              <input id="last_name" type="text" class="validate">
              <label for="last_name">Фамилия</label>
            </div>
          </div>
          <div class="row">
            <div class="input-field col s12">
              <input id="login" type="text" class="validate">
              <label for="login">Логин</label>
            </div>
          </div>
          <div class="row">
            <div class="input-field col s12">
              <input id="password" type="password" class="validate">
              <label for="password">Пароль</label>
            </div>
          </div>
          <div class="row">
            <div class="input-field col s12">
              <input id="confirm_password" type="password" class="validate">
              <label for="confirm_password">Повторение пароля</label>
            </div>
          </div>
          <div class="row">
            <div class="input-field col s12">
              <input id="email" type="email" class="validate">
              <label for="email">Адрес электронной почты</label>
            </div>
          </div>
          <div class="submit-block row right">
            <router-link
                tag="a"
                to="/authorization"
            ><a class="waves-effect waves-teal btn-flat blue-text text-darken-3">У меня уже есть аккаунт.</a></router-link>
            <button type="submit" class="btn">Зарегистрироваться</button>
          </div>
        </form>
      </div>
    </div>
</template>

<script>

export default {
  components : { },
  methods : {
    registerUser : () => {
      console.log('dfd')
    }
  }
}
</script>

<style lang="scss" scoped>
.reg-block {
  padding: 2rem;
  margin: 0 auto;
  box-shadow: 0 5px 10px 1px;
}
.container {
  min-height: 95vh;
}

.submit-block {
  padding: 2rem;
}

</style>