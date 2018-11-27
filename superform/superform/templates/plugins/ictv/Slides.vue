<template>
    <div>
        <slide channel="" id=""></slide>
    </div>
</template>

<script>
    import Slide from 'Slide'

    export default {
        name: "Slides",
        components: {Slide},
        props: {
            channel: {
                type:String,
                required:true,
                trim: true
            }
        },
        data() {
            return {
                nbSlides: 1
            }
        },
        methods: {
            addSlide() {
                if(this.nbSlides === this.nbMaxSlides) {
                    alert(`You can't create more than ${this.nbMaxSlides}`)
                }
            },
            removeSlide() {
                if(this.nbSlides === 1) {
                    alert("You must at least fill one slide !");
                } else {
                    this.nbSlides--;
                }
            }
        },
        created() {
            this.nbMaxSlides = 5
        }

    }
</script>

<style scoped>

</style>