<template>
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
</template>

<script>
    export default {
        name: "Slide",
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
        }
    }
</script>