// Slide

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
    methods: {
        sendData() {
            const data = {
                'title-1': {
                    text: this.title
                },
                'subtitle-1': {
                    text: this.subtitle
                },
                'text-1': {
                    text: this.text
                },
                'logo-1': {
                    src: this.logo
                },
                'image-1': {
                    src: this.image
                },
                'background-1': {
                    color: this.background
                },
                duration: this.duration
            };
            this.$emit('data', data)
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
                   v-model="title" type="text" @blur="sendData" required>
        </div>

        <div class="form-group">
            <label>
                Subtitle<br>
            </label>
            <input class="form-control" :name="getChannelId + 'subtitle'" :id="getChannelId + 'subtitle'"
                   v-model="subtitle"
                   type="text" @blur="sendData" required>
        </div>

        <div class="form-group">
            <label>
                Text<br>
            </label>
            <textarea rows="5" class="form-control" :name="getChannelId + 'text'" :id="getChannelId + 'text'"
                      v-model="text"
                      type="text" @blur="sendData" required></textarea>
        </div>

        <div class="form-group">
            <label>
                Logo<br>
            </label>
            <input :name="getChannelId + 'logo'" :id="getChannelId + 'logo'"
                   class="form-control"
                   type="text" @blur="sendData" v-model="logo">
        </div>

        <div class="form-group">
            <label>
                Image<br>
            </label>
            <input :name="getChannelId + 'image'" :id="getChannelId + 'image'"
                   class="form-control"
                   type="text" @blur="sendData" v-model="image">
        </div>

        <div class="form-group">
            <label>
                Background color<br>
            </label>
            <input class="form-control" :name="getChannelId + 'background'"
                   :id="getChannelId + 'background'"
                   v-model="background"
                   type="text" @blur="sendData">
        </div>

        <div class="form-group">
            <label>
                Duration<br>
            </label>
            <input class="form-control" :name="getChannelId + 'duration'" :id="getChannelId + 'duration'"
                   v-model="duration"
                   type="number" @blur="sendData">
        </div>
    </div>
  `
});

// Slides


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
            slides: this.defaultConfig,
            isShowingPreview: false
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
        },
        togglePreview() {
            this.isShowingPreview = !this.isShowingPreview
        },
        setData(event, id) {
            this.slides.splice(id, 1, event);
        }
    },
    computed: {
        nbSlides() {
            return this.slides.length
        },
        textButtonPreview() {
            return this.isShowingPreview ? 'Close' : 'Preview';
        }
    },
    template: `
    <div>
        <transition name="fade">
            <previews :slides="slides" v-if="isShowingPreview" @close="togglePreview"></previews>
        </transition>

        <transition-group name="fade">
            <slide v-for="(slide, id) in slides" :content="slide" :channel="channel" :id="id+1" :key="id+1" @data="setData($event, id)"></slide>
        </transition-group>

        <button type="button" @click="addSlide">
            Add
        </button>

        <button type="button" @click="removeSlide">
            Remove
        </button>

        <button type="button" @click="togglePreview" v-html="textButtonPreview">
            Preview
        </button>
    </div>
    `
});

// Preview


Vue.component('preview', {
    props: {
        slide: {
            type: Object,
            required: true
        },
        idSlide: {
            type: Number,
            required: true
        }
    },
    template: `
    <div class="preview" :style="{backgroundColor: slide['background-1'].color}">
        <picture class="logo">
            <img :src="slide['logo-1'].src" alt="logo">
        </picture>

        <h1 v-html="slide['title-1'].text"></h1>
        <h2 v-html="slide['subtitle-1'].text"></h2>

        <p v-html="slide['text-1'].text"></p>

        <picture class="image">
            <img :src="slide['image-1'].src" alt="image">
        </picture>
        
        <div class="number" v-html="idSlide"></div>
    </div>
    `
});

// previews

Vue.component('previews', {
    props: {
        slides: {
            type: Array,
            default: () => []
        }
    },
    watch: {
        slides(newVal) {
            this.previews = newVal;
            this.currentPreview = 1;
        }
    },
    data() {
        return {
            previews: this.slides,
            currentPreview: 1
        }
    },
    methods: {
        closePreview() {
            this.$emit('close');
        }
    },
    mounted() {
        this.intervalEvent = setInterval(() => {
            this.currentPreview = this.currentPreview === this.previews.length ? 1 : this.currentPreview + 1;
        }, 3000)
    },
    beforeDestroy() {
        clearInterval(this.intervalEvent);
    },
    template: `
    <div class="previews-wrapper">
        <preview v-for="(slide,id) in previews" v-if="currentPreview === id + 1" :slide="slide" :id-slide="id + 1"
                 :key="id+1"></preview>
        <button type="button" @click="closePreview">Close</button>

    </div>
    `
});


vm = new Vue({
    el: "#ictv"
});