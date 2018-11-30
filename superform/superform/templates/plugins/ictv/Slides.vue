<template>
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
</template>

<script>
    import Slide from 'Slide'

    export default {
        name: "Slides",
        components: {Slide},
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
        }

    }
</script>