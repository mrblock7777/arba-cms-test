<template>
    <v-container>
        <div class="d-flex flex-column align-center py-8">
            <span class="text-h3">Edit Post</span>
            <v-form ref="form" v-model="valid" lazy-validation>
                <v-card class="py-4" width="400">
                    <v-card-title v-show="previewImage">
                        <v-img width="400" :src="previewImage" max-width="100%"></v-img>
                    </v-card-title>
                    <v-card-text class="my-4">
                        <v-file-input v-model="image" label="Upload Image" accept="image/*" prepend-icon="mdi-camera"
                            required></v-file-input>
                        <v-text-field v-model="caption" label="Caption" required></v-text-field>
                        <v-btn class="float-right" :disabled="!valid" color="primary" @click="editPost()">
                            Edit Post
                        </v-btn>
                    </v-card-text>
                </v-card>

            </v-form>
        </div>
    </v-container>
</template>
<script setup>
import { ref, onBeforeMount, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router'
import { usePostStore } from '@/stores/post'
import { useAuthStore } from '@/stores/auth'

const caption = ref('');
const image = ref(null);
const post = ref({});
const previewImage = ref(null);
const route = useRoute();
const router = useRouter();
const postStore = usePostStore();
const authStore = useAuthStore();


const editPost = async () => {
    const form = new FormData();
    console.log(image.value)
    form.append('image', image.value ?? post.value.image);
    form.append('caption', caption.value);
    console.log(form)
    await postStore.editPost(form, route.params.id);
    // router.push('/');
}

const getPost = async () => {
    await postStore.getPost(route.params.id);
    post.value = postStore.post;
    caption.value = post.value.caption;
    previewImage.value = post.value.imageURL;
}
watch(image, (newImage) => {
    console.log(newImage);
    previewImage.value = URL.createObjectURL(newImage);
});
onBeforeMount(() => {
    getPost();
})
</script>