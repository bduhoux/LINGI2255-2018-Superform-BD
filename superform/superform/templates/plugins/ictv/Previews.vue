<template>
    <div class="previews-wrapper">
        <preview v-for="(slide,id) in previews" v-if="currentPreview === id + 1" :slide="slide" :id-slide="id + 1"
                 :key="id+1"></preview>
        <button type="button" @click="closePreview">Close</button>

    </div>
</template>

<script>
    import Preview from 'Preview'

    export default {
        name: "Previews",
        components: {
            Preview
        },
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
        }
    }
</script>