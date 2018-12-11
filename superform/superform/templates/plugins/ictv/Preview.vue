<template>
    <div class="preview">
        <picture v-if="slide['logo-1'].src !== ''" class="logo">
            <img :src="slide['logo-1'].src" alt="logo">
        </picture>

        <h1 v-html="slide['title-1'].text"></h1>
        <h2 v-html="slide['subtitle-1'].text"></h2>

        <p v-html="slide['text-1'].text"></p>

        <picture v-if="slide['image-1'].src !== ''" class="image">
            <img :src="slide['image-1'].src" alt="image">
        </picture>
    </div>
</template>

<script>
    export default {
        name: "Preview",
        props: {
            slide: {
                type: Object,
                required: true
            },
            idSlide: {
                type: Number,
                required: true
            }
        }
    }
</script>