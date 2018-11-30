<template>
    <div>
        <transition name="fade">
            <previews :slides="slides" v-if="isShowingPreview" @close="togglePreview"></previews>
        </transition>

        <transition-group name="fade">
            <slide v-for="(slide, id) in slides" :content="slide" :channel="channel" :id="id+1" :key="id+1"
                   @data="setData($event, id)"></slide>
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
</template>

<script>
    import Slide from 'Slide'
    import Previews from 'Previews'

    export default {
        name: "Slides",
        components: {Slide, Previews},
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
        }

    }
</script>