Vue.component('slide', {
    data() {
        return {
            title: this.content['title-1'].text,
            subtitle: this.content['subtitle-1'].text,
            text: this.content['text-1'].text,
            background: this.content['background-1'].color,
            duration: this.content.duration,
            image: this.content['image-1'].src,
            logo: this.content['logo-1'].src
        }
    },
    props: {
        channel: {
            required: true,
            type: String,
            trim: true
        },
        id: {
            required: true,
            type: Number
        },
        content: {
            required: true,
            type: Object
        }
    },
    computed: {
        getChannelId() {
            return this.channel + '_' + this.id + '_'
        },
        getChannel() {
            return `Slide n°${this.id}`
        }
    },
    template: `
    <div>
        <h4 v-html="getChannel"></h4>

        <div class="form-group">
            <label>
                Title<br>
            </label>
            <input class="form-control" :name="getChannelId + 'title'" :id="getChannelId + 'title'"
                   v-model="title" type="text" required>
        </div>

        <div class="form-group">
            <label>
                Subtitle<br>
            </label>
            <input class="form-control" :name="getChannelId + 'subtitle'" :id="getChannelId + 'subtitle'"
                   v-model="subtitle"
                   type="text" required>
        </div>

        <div class="form-group">
            <label>
                Text<br>
            </label>
            <textarea rows="5" class="form-control" :name="getChannelId + 'text'" :id="getChannelId + 'text'"
                      v-model="text"
                      type="text" required></textarea>
        </div>

        <div class="form-group">
            <label>
                Logo<br>
            </label>
            <input :name="getChannelId + 'logo'" :id="getChannelId + 'logo'"
                   class="form-control"
                   type="text" v-model="logo">
        </div>

        <div class="form-group">
            <label>
                Image<br>
            </label>
            <input :name="getChannelId + 'image'" :id="getChannelId + 'image'"
                   class="form-control"
                   type="text" v-model="image">
        </div>

        <div class="form-group">
            <label>
                Background color<br>
            </label>
            <input class="form-control" :name="getChannelId + 'background'"
                   :id="getChannelId + 'background'"
                   v-model="background"
                   type="text">
        </div>

        <div class="form-group">
            <label>
                Duration<br>
            </label>
            <input class="form-control" :name="getChannelId + 'duration'" :id="getChannelId + 'duration'"
                   v-model="duration"
                   type="number">
        </div>
    </div>
  `
});

Vue.component('slides', {
    props: {
        channel: {
            type: String,
            required: true,
            trim: true
        },
        defaultConfig: {
            type: Array,
            default: () => {
                return [{
                    'title-1': {
                        text: ''
                    },
                    'subtitle-1': {
                        text: ''
                    },
                    'text-1': {
                        text: ''
                    },
                    'logo-1': {
                        src: ''
                    },
                    'image-1': {
                        src: ''
                    },
                    'background-1': {
                        color: ''
                    },
                    duration: 1000
                }]
            }
        }
    },
    data() {
        return {
            slides: this.defaultConfig
        }
    },
    methods: {
        addSlide() {
            this.slides.push({
                    'title-1': {
                        text: ''
                    },
                    'subtitle-1': {
                        text: ''
                    },
                    'text-1': {
                        text: ''
                    },
                    'logo-1': {
                        src: ''
                    },
                    'image-1': {
                        src: ''
                    },
                    'background-1': {
                        color: ''
                    },
                    duration: 1000
                })
        },
        removeSlide() {
            if (this.nbSlides === 1) {
                alert("You must at least fill one slide !");
            } else {
                this.slides.pop()
            }
        }
    },
    computed: {
        nbSlides() {
            return this.slides.length
        }
    },
    template: `
    <div>
        <transition-group name="fade">
            <slide v-for="(slide, id) in slides" :content="slide" :channel="channel" :id="id+1" :key="id+1"></slide>
        </transition-group>

        <button type="button" @click="addSlide">
            Add
        </button>

        <button type="button" @click="removeSlide">
            Remove
        </button>
    </div>
    `
});

vm = new Vue({
    el: "#ictv"
});