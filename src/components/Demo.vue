<template>
  <div class="my_body">
    <section class="todoapp" id="apps">
      <header class="header">
        <h1>Mylike</h1>
        <input class="new-todo" placeholder="喜欢哪些水果?" v-focuz @keyup.enter="addTodo" >
      </header>
      <div v-if="fruits.length">
        <!-- This section should be hidden by default and shown when there are todos -->
        <section class="main" >
          <input id="toggle-all" class="toggle-all"  @click="toggleall" type="checkbox" v-model = "toggleAllStat.length ===0">
          <label for="toggle-all">Mark all as complete</label>
          <ul class="todo-list">
            <!-- These are here just to show the structure of the list items -->
            <!-- List items should get the class `editing` when editing and `completed` when marked as completed -->
            <li
              v-for="(item,index) in fruitsFilter"
              :class="{completed : item.checkstate,editing:item === editstate}">
              <div class="view">
                <input class="toggle" type="checkbox" v-model="item.checkstate">
                <label @dblclick="editstate = item">{{item.name}}</label>
                <button class="destroy" @click="removeItem(index, item)"></button>
              </div>
              <input class="edit" v-model="item.name" v-dblfocus="item === editstate"
                     @keyup.enter="updateItem(item)"
                     @blur="editstate = null">
            </li>
          </ul>
        </section>
        <!-- This footer should hidden by default and shown when there are todos -->
        <footer class="footer">
          <!-- This should be `0 items left` by default -->
          <span class="todo-count"><strong>{{itemleft}}</strong> item left</span>
          <!-- Remove this if you don't implement routing -->
          <ul class="filters">
            <li>
              <a class="all" @click="test">All</a>
            </li>
            <li>
              <a class="active" @click="test">Active</a>
            </li>
            <li>
              <a class="completed" @click="test">Completed</a>
            </li>
          </ul>
          <!-- Hidden if no completed items are left ↓ -->
          <button class="clear-completed" @click="removeALLDone">Clear completed</button>
        </footer>
      </div>
    </section>
    <footer class="info">
      <p>Double-click to edit a todo</p>
      <!-- Remove the below line ↓ -->
      <p>Template by <a href="http://sindresorhus.com">Sindre Sorhus</a></p>
      <!-- Change this out with your name and url ↓ -->
      <p>Created by <a href="http://todomvc.com">you</a></p>
      <p>Part of <a href="http://todomvc.com">TodoMVC</a></p>
    </footer>
  </div>
</template>

<script>
  import Axios from 'axios'


  export default {
    name: "Demo",
    data() {
      return {
        fruits: [],
        editstate: null,
        filterStat: 'all'
      }
    },
    created(){
      this.request();
    },
    computed: {

      fruitsFilter: function () {
        switch (this.filterStat) {
          case 'active' :
            return this.fruits.filter(function (item) {
              return item.checkstate === false
            });
            break;
          case 'completed' :
            return this.fruits.filter(function (item) {
              return item.checkstate === true
            });
            break;
          default :
            return this.fruits;
            break;
        }
      },
      itemleft: function () {
        return this.fruitsFilter.length;
      },
      toggleAllStat: function () {
        return this.fruits.filter(item => item.checkstate === false);
      }
    },
    methods: {
      test:function(event) {

        switch (event.target.className.toString()) {
          case 'active' :
            this.filterStat = 'active';
            break;
          case 'completed' :
            this.filterStat = 'completed';
            break;
          default :
            this.filterStat = 'all';
            break;
        }
      },
      updateItem: function(item){
        this.editstate = null;
        Axios.get(process.env.VUE_APP_BASE_API+'/update?name='+item.name+'&id='+ item.id).then((response) => {
          if(response.data.status === 'success')
          {
            this.request()
          }else {
            alert(response.data.msg)
          }
        });
      },

      request: function (event) {
        Axios.get(process.env.VUE_APP_BASE_API+'/select/').then((response) => {
          console.log(response.data);
          this.fruits = response.data;
        })
      },

      toggleall: function (event) {
        const check = event.target.checked;
        this.fruits.forEach(function (item) {
          item.checkstate = check;
        })
      },

      addTodo: function (event) {
        const valueStr = event.target.value;
        Axios.get(process.env.VUE_APP_BASE_API+'/add?name='+valueStr).then((response) => {
          if(response.data.status === 'success')
          {
            this.request()
          }else {
            alert(response.data.msg)
          }
        });

        event.target.value = '';
      },

      removeItem: function (index, item) {
        Axios.get(process.env.VUE_APP_BASE_API+'/delete?id='+ item.id).then((response) => {
          if(response.data.status === 'success')
          {
            this.fruits.splice(index, 1);
          }else {
            alert(response.data.msg)
          }
        });

      },

      removeALLDone: function () {

        this.fruits = this.fruits.filter(function (item) {
          if(item.checkstate){
            Axios.get(process.env.VUE_APP_BASE_API+'/delete?id='+ item.id).then((response) => {
              if(response.data.status !== 'success')
              {
                alert(response.data.msg)
              }
            });
          }
          return !item.checkstate
        })
      },

      editInput: function () {
        console.log('editInput');
      },

      editSave: function (item, event) {
        this.editstate = null;
      }
    },
    directives: {
      focuz: {
        inserted: function (el) {
          el.focus();
        }
      },
      dblfocus: {
        update: function (el, binding) {
          console.log(binding.value);
          if (binding.value) {
            console.log('fff');
            el.focus();
          }

        }
      }
    }
  }
</script>

<style scoped>
  @import "../../node_modules/todomvc-common/base.css";
  @import "../../node_modules/todomvc-app-css/index.css";

  .my_body{
    font: 14px 'Helvetica Neue', Helvetica, Arial, sans-serif;
    line-height: 1.4em;
    background: #f5f5f5;
    color: #111111;
    min-width: 230px;
    max-width: 550px;
    margin: 0 auto;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    font-weight: 300;
  }

</style>
