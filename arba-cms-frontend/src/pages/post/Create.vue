<template>
    <div class="d-flex flex-column align-center py-8">
        <span class="text-h3">Create Post</span>
        <v-form ref="form" v-model="valid" lazy-validation>
            <v-card class="py-4" width="400">
                <v-card-title  v-show="image">
                    <v-img  width="400" :src="previewImage" max-width="100%"></v-img>
                </v-card-title>
                <v-card-text class="my-4">
                    <v-file-input v-model="image" label="Upload Image" accept="image/*" prepend-icon="mdi-camera"
                        required></v-file-input>
                    <v-text-field v-model="caption" label="Caption" required></v-text-field>
                    <v-btn class="float-right" :disabled="!valid" color="primary" @click="submit">
                        Post
                    </v-btn>
                </v-card-text>
            </v-card>

        </v-form>
    </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { usePostStore } from '@/stores/post';
import { useRouter } from 'vue-router'

const form = ref(null);
const valid = ref(false);
const image = ref(null);
const caption = ref('');
const previewImage = ref(null);
const postStore = usePostStore();
const router = useRouter();

const submit = async () => {
    if (form.value.validate()) {
        // Handle form submission
        const form = new FormData();
        console.log(image.value)
        form.append('image', image.value);
        form.append('caption', caption.value);
        await postStore.createPost(form);
        router.push('/');
    }
};

watch(image, (newImage) => {
    console.log(newImage);
    previewImage.value = URL.createObjectURL(newImage);
});


</script>

<style scoped>
.v-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
}
</style>