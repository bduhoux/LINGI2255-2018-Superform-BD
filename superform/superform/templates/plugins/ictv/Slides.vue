<template>
    <div>
        <transition-group name="fade">
            <slide v-for="i in nbSlides" :channel="channel" :id="i" :key="i"></slide>
        </transition-group>


        <div v-html="getCounter"></div>

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
                type: JSON,
                default: {}
            }
        },
        data() {
            return {
                nbSlides: 1,
                nbMaxSlides: 5
            }
        },
        methods: {
            addSlide() {
                if (this.nbSlides === this.nbMaxSlides) {
                    alert(`You can't create more than ${this.nbMaxSlides} slides`)
                } else {
                    this.nbSlides++;
                }
            },
            removeSlide() {
                if (this.nbSlides === 1) {
                    alert("You must at least fill one slide !");
                } else {
                    this.nbSlides--;
                }
            }
        },
        computed: {
            getCounter() {
                return `${this.nbSlides}/${this.nbMaxSlides}`
            }
        }

    }
</script>