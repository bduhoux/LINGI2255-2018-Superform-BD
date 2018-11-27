<template>
    <div>
        <div class="form-group">
            <label>
                Title<br>
                <input :name="getChannelId + 'title'" :id="getChannelId + 'title'"
                       v-model="title" type="text">
            </label>
        </div>

        <div class="form-group">
            <label>
                Subtitle<br>
                <input :name="getChannelId + 'subtitle'" :id="getChannelId + 'subtitle'"
                       v-model="subtitle"
                       type="text">
            </label>
        </div>

        <div class="form-group">
            <label>
                Text<br>
                <input :name="getChannelId + 'text'" :id="getChannelId + 'text'"
                       v-model="text"
                       type="text">
            </label>
        </div>

        <div class="form-group">
            <label>
                Logo<br>
                <input :name="getChannelId + 'logo'" :id="getChannelId + 'logo'"
                       v-model="logo"
                       type="image">
            </label>
        </div>

        <div class="form-group">
            <label>
                Image<br>
                <input :name="getChannelId + 'image'" :id="getChannelId + 'image'"
                       v-model="image"
                       type="image">
            </label>
        </div>

        <div class="form-group">
            <label>
                Background color<br>
                <input :name="getChannelId + 'background-color'" :id="getChannelId + 'background-color'"
                       v-model="backgroundColor"
                       type="text">
            </label>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Slide",
        data() {
            return {
                title: '',
                subtitle: '',
                text: '',
                logo: '',
                image: '',
                background: '',
                backgroundColor:''
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
            }
        },
        computed: {
            getChannelId() {
                return this.channel + '_' + id + '_'
            }
        }
    }
</script>