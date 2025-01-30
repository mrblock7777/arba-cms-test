<template>
    <v-container>
        <div class="d-flex flex-column align-center">
            <v-card width="500">
                <v-card-title>
                    <router-link :to="'/profile/' + post.user">@{{ post.username }}</router-link>
                </v-card-title>
                <v-img :src="post.imageURL" aspect-ratio="16/9"></v-img>
                <v-card-subtitle class="my-4">{{ post.caption }}</v-card-subtitle>
            </v-card>

            <v-card class="my-4" width="500">
                <v-card-title class="my-4">Comments</v-card-title>
                <v-list>
                    <v-list-item v-for="comment in post.comments" :key="comment.id">
                        <v-list-item-content>
                            <v-list-item-title>{{ comment.username }}</v-list-item-title>
                            <v-list-item-subtitle>
                                {{ comment.text }}
                                <v-tooltip text="Remove comment">
                                    <template v-slot:activator="{ props }">
                                        <v-btn v-bind="props" variant="plain" class="float-right"
                                            v-if="authStore.currentUser.id === comment.user" color="default"
                                            icon="mdi-trash-can" @click="deleteComment(comment)"></v-btn>
                                    </template>
                                </v-tooltip>
                            </v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>
                </v-list>
                <v-text-field v-if="authStore.isLogggedIn" v-model="newComment" label="Add a comment"
                    @keyup.enter="addComment()">
                    <template #append-inner>
                        <v-btn color="primary" variant="plain" @click="addComment()">
                            <v-icon>mdi-send</v-icon>
                        </v-btn>
                    </template>
                </v-text-field>
            </v-card>
        </div>
    </v-container>
</template>

<script setup>
import { ref, onBeforeMount } from 'vue';
import { useRoute } from 'vue-router'
import { usePostStore } from '@/stores/post'
import { useAuthStore } from '@/stores/auth'

const post = ref({});
const route = useRoute();
const postStore = usePostStore();
const authStore = useAuthStore();

const newComment = ref('');

const deleteComment = async (comment) => {
    await postStore.deleteComment(comment.id);
    post.value.comments = post.value.comments.filter(c => c.id !== comment.id);
}
const addComment = async () => {
    await postStore.createComment(route.params.id, authStore.currentUser.id, newComment.value);
    post.value.comments.push({
        username: authStore.currentUser.username,
        text: newComment.value
    });
    newComment.value = '';
}
const getPost = async () => {
    await postStore.getPost(route.params.id);
    post.value = postStore.post;
}

onBeforeMount(() => {
    getPost();
})
</script>
