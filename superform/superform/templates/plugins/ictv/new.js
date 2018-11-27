Vue.component('slide', {
    data() {
        return {
            title: '',
            subtitle: '',
            text: ''
        }
    },
    props: {
        prefix: {
            required:true,
            type:String,
            trim:true
        },
        postfix: {
            required:true,
            type:Number
        }
    },
    template: `
  <div>
    <div>
        <label for="title">
        Title<br>
        <input :name="prefix + '_' + title + - + postfix" :id="prefix + '_' + title + - + postfix" v-model="title" type="text">
        </label>
    </div>
    <div>
        <label for="subtitle">
        Subtitle<br>
        <input :name="prefix + '_' + subtitle + - + postfix" :id="prefix + '_' + subtitle + - + postfix" v-model="subtitle" type="text">
        </label>
    </div>
    <div>
        <label for="title">
        Title<br>
        <input v-model="title" type="text">
        </label>
    </div>
  </div>
  `
});

Vue.component('slides', {

});

vm = new Vue({
    el: "#ictv"
});