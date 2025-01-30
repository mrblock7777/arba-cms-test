<template>
    <v-container>
        <div class="d-flex flex-column align-center">
            <v-card width="500" v-for="(post, index) in posts" :key="index" class="mb-4">
                <v-card-title>
                    <router-link :to="'/profile/' + post.user">@{{ post.username }}</router-link>
                    <v-tooltip text="Remove post">
                        <template v-slot:activator="{ props }">
                            <v-btn v-bind="props" v-if="authStore.currentUser.id === post.user" class="float-right" color="primary"
                                @click="deletePost(post.id)" icon="mdi-trash-can"></v-btn>
                        </template>
                    </v-tooltip>
                </v-card-title>
                <v-img class="cursor-pointer" :src="post.imageURL" height="200px"
                    @click="$router.push('/post/' + post.id)"></v-img>
                <v-card-subtitle class="mt-6">{{ post.caption }}</v-card-subtitle>
                <v-card-text>
                    <span class="text-h6">Comment Section</span>
                    <br />
                    <span v-if="!post.comments.length && !authStore.isLogggedIn"><router-link
                            to="/login">Login</router-link> now to
                        post your first
                        comment</span>
                    <v-list v-else>
                        <v-list-item v-if="post.comments.length < 3" v-for="(comment, i) in post.comments">
                            <v-list-item-content>
                                <v-list-item-title>{{ comment.username }}</v-list-item-title>
                                <v-list-item-subtitle>{{ comment.text }}</v-list-item-subtitle>
                            </v-list-item-content>
                        </v-list-item>
                        <v-list-item v-else v-for="(i) in 2">
                            <v-list-item-content>
                                <v-list-item-title>{{ post.comments[i].username }}</v-list-item-title>
                                <v-list-item-subtitle>{{ post.comments[i].text }}</v-list-item-subtitle>
                            </v-list-item-content>
                        </v-list-item>
                        <v-hover v-slot="{ isHovering, props }" v-if="post.comments.length > 3">
                            <router-link :to="'/post/' + post.id" v-bind="props" class="text-decoration-none my-2"
                                :class="isHovering ? 'text-primary cursor-pointer' : 'text-secondary'">Click here to
                                show more
                                comments</router-link>
                        </v-hover>
                    </v-list>
                    <v-text-field v-if="authStore.isLogggedIn" v-model="newComment[index]" label="Add a comment"
                        @keyup.enter="addComment(post, newComment[index]); newComment[index] = ''">
                        <template #append-inner>
                            <v-btn color="primary" variant="plain"
                                @click="addComment(post, newComment[index]); newComment[index] = ''">
                                <v-icon>mdi-send</v-icon>
                            </v-btn>
                        </template>
                    </v-text-field>
                </v-card-text>
            </v-card>
        </div>
    </v-container>
</template>

<script setup>
import { ref, onBeforeMount } from 'vue';
import { useRoute } from 'vue-router'
import { useProfileStore } from '@/stores/profile';
import { usePostStore } from '@/stores/post';
import { useAuthStore } from '@/stores/auth';

const newComment = ref([]);
const posts = ref([]);
const profileStore = useProfileStore();
const postStore = usePostStore();
const authStore = useAuthStore();
const route = useRoute();

const deletePost = async (postId) => {
    await postStore.deletePost(postId);
    posts.value = posts.value.filter(p => p.id !== postId);
}
const deleteComment = async (postId, commentId) => {
    await postStore.deleteComment(commentId);
    posts.value.find(p => p.id === postId).comments = posts.value.find(p => p.id === postId).comments.filter(c => c.id !== commentId);
}
const addComment = async (post, comment) => {
    await postStore.createComment(post.id, authStore.currentUser.id, comment);
    posts.value.find(p => p.id === post.id).comments.push({
        username: authStore.currentUser.username,
        text: comment
    });
}
onBeforeMount(async () => {
    const userId = route.params.id
    await postStore.getPostsByUserId(userId);
    posts.value = postStore.posts;
});
</script>

<style scoped>
.v-list-item {
    margin-bottom: 16px;
}
</style>