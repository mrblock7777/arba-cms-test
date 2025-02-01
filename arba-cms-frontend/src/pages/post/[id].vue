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
                                <span v-show="!comment.editable">{{ comment.text }}</span>
                                <span v-show="comment.editable">
                                    <v-text-field v-if="authStore.isLogggedIn" v-model="comment.text"
                                        label="Edit Comment" @keyup.enter="editComment(comment)">
                                        <template #append-inner>
                                            <v-btn color="primary" variant="plain" @click="comment.editable = false">
                                                <v-icon>mdi-close</v-icon>
                                            </v-btn>
                                            <v-btn color="primary" variant="plain" @click="editComment(comment)">
                                                <v-icon>mdi-send</v-icon>
                                            </v-btn>
                                        </template>
                                    </v-text-field>
                                </span>
                                <v-btn v-if="authStore.currentUser.id === comment.user" class="float-right"
                                    variant="text">
                                    <v-icon>mdi-dots-vertical</v-icon>
                                    <v-menu activator="parent">
                                        <v-list>
                                            <v-list-item>
                                                <v-list-item-title class="my-2 cursor-pointer"
                                                    @click="comment.editable = true">
                                                    Edit Comment
                                                </v-list-item-title>
                                                <v-list-item-title class="my-2 cursor-pointer"
                                                    @click="deleteComment(comment)">
                                                    Delete Comment
                                                </v-list-item-title>
                                            </v-list-item>
                                        </v-list>
                                    </v-menu>
                                </v-btn>
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
    // post.value.comments = post.value.comments.filter(c => c.id !== comment.id);
    await getPost()
}
const editComment = async (comment) => {
    await postStore.updateComment(comment);
    // post.value.comments = post.value.comments.find(c => c.id === comment.id).text = comment.text;
    // post.value.comments = post.value.comments.find(c => c.id === comment.id).editable = false;
    await getPost()
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
