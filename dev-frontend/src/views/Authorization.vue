<template>
  <div class="container">
    <div class="row"><h2 class="center-align">Secure Center</h2></div>
    <div class="row"><h4 class="center-align">Авторизация</h4></div>
    <div class="row">
      <form @submit.prevent="authUser" class="auth-block col s4 offset-s4 center-align grey lighten-5">
        <div class="row">
          <div class="input-field col s12">
            <input required v-model="login" id="login" type="text" class="validate" >
            <label for="login">Логин</label>
          </div>
        </div>
        <div class="row">
          <div class="input-field col s12">
            <input required v-model="password" id="password" type="password" class="validate">
            <label for="password">Пароль</label>
          </div>
        </div>
        <div class="submit-block row s8 offset-s2">
          <div class="row"><button type="submit" class="btn">Войти</button></div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>

export default {
  components : { },
  data() {
    return {
      login : '',
      password : ''
    }
  },
  methods : {
    authUser : function() {
        let login = this.login
        let password = this.password
        this.$store.dispatch('login', { login, password })
                   .then(() => this.$router.push('/'))
                   .catch(err => console.log(err))
    }
  }
}
</script>

<style lang="scss" scoped>
.auth-block {
  padding: 4rem;
  box-shadow: 0 5px 10px 1px;
}
.container {
  min-height: 95vh;
}

.submit-block {
  padding: 1.25rem;
}

</style>