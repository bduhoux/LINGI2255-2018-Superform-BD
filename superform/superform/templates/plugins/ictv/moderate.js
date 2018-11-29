Vue.component('slide', {
    data() {
        return {
            title: this.content.title,
            subtitle: this.content.subtitle,
            text: this.content.text,
            background: this.content.background,
            duration: this.content.duration,
            image: this.content.image,
            logo: this.content.logo
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
            <input class="form-control" :name="getChannelId + 'title-1'" :id="getChannelId + 'title-1'"
                   v-model="title" type="text" required>
        </div>

        <div class="form-group">
            <label>
                Subtitle<br>
            </label>
            <input class="form-control" :name="getChannelId + 'subtitle-1'" :id="getChannelId + 'subtitle-1'"
                   v-model="subtitle"
                   type="text" required>
        </div>

        <div class="form-group">
            <label>
                Text<br>
            </label>
            <textarea rows="5" class="form-control" :name="getChannelId + 'text-1'" :id="getChannelId + 'text-1'"
                      v-model="text"
                      type="text" required></textarea>
        </div>

        <div class="form-group">
            <label>
                Logo<br>
            </label>
            <input :name="getChannelId + 'logo-1'" :id="getChannelId + 'logo-1'"
                   class="form-control"
                   type="text" v-model="logo">
        </div>

        <div class="form-group">
            <label>
                Image<br>
            </label>
            <input :name="getChannelId + 'image-1'" :id="getChannelId + 'image-1'"
                   class="form-control"
                   type="text" v-model="image">
        </div>

        <div class="form-group">
            <label>
                Background color<br>
            </label>
            <input class="form-control" :name="getChannelId + 'background-1'"
                   :id="getChannelId + 'background-1'"
                   v-model="background"
                   type="text">
        </div>

        <div class="form-group">
            <label>
                Duration<br>
            </label>
            <input class="form-control" :name="getChannelId + 'duration-1'" :id="getChannelId + 'duration-1'"
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
                    title: '',
                    subtitle: '',
                    text: '',
                    logo: '',
                    image: '',
                    background: '',
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
                title: '',
                subtitle: '',
                text: '',
                logo: '',
                image: '',
                background: '',
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