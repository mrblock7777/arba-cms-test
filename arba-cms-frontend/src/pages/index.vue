<template>
  <v-container class="d-flex" :class="!lgAndUp ? 'justify-center' : ''">
    <!-- <span class="text-h4">Your Feed</span> -->
    <div v-show="lgAndUp" v-if="authStore.isLogggedIn" class="w-33">
      <v-card width="300" class="mb-4">
        <v-img src="https://salondesmaires-ain.fr/wp-content/uploads/2014/10/speaker-3.jpg" height="150px"></v-img>
        <v-card-subtitle class="mt-4">{{ authStore.currentUser.first_name }} {{ authStore.currentUser.last_name
          }}</v-card-subtitle>
        <v-card-text>
          <v-list>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>Email: {{ authStore.currentUser.email }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
          <v-tooltip text="Add a new post">
            <template v-slot:activator="{ props }">
              <v-btn v-bind="props" color="primary" icon="mdi-plus" @click="$router.push('/post/create')"></v-btn>
            </template>
          </v-tooltip>
          <v-tooltip text="Edit Profile and View Your Posts">
            <template v-slot:activator="{ props }">
              <v-btn v-bind="props" class="mx-2" color="indigo" icon="mdi-panorama"
                @click="$router.push('/profile/' + authStore.currentUser.id)"></v-btn>
            </template>
          </v-tooltip>
        </v-card-text>
      </v-card>
    </div>
    <div class="d-flex flex-column align-center" :class="authStore.isLogggedIn ? '' : 'w-100'">
      <v-card :width="lgAndUp ? 500 : mdAndUp ? 400 : 300" v-for="(post, index) in posts" :key="index" class=" mb-4">
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
          <span v-if="!post.comments.length && !authStore.isLogggedIn"><router-link to="/login">Login</router-link> now
            to
            post your first
            comment</span>
          <v-list v-else>
            <v-list-item v-if="post.comments.length < 3" v-for="(comment, index) in post.comments">
              <v-list-item-content>
                <v-list-item-title>{{ comment.username }}</v-list-item-title>
                <v-list-item-subtitle>
                  {{ comment.text }}
                  <v-tooltip text="Remove comment">
                    <template v-slot:activator="{ props }">
                      <v-btn v-bind="props" variant="plain" class="float-right"
                        v-if="authStore.currentUser.id === comment.user" color="default" icon="mdi-trash-can"
                        @click="deleteComment(comment)"></v-btn>
                    </template>
                  </v-tooltip>
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-list-item v-else v-for="(i) in 2">
              <v-list-item-content>
                <v-list-item-title>{{ post.comments[i].username }}</v-list-item-title>
                <v-list-item-subtitle>
                  {{ post.comments[i].text }}
                  <v-tooltip text="Remove comment">
                    <template v-slot:activator="{ props }">
                      <v-btn v-bind="props" variant="plain" class="float-right"
                        v-if="authStore.currentUser.id === post.comments[i].user" color="default" icon="mdi-trash-can"
                        @click="deleteComment(post.comments[i])"></v-btn>
                    </template>
                  </v-tooltip>
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-hover v-slot="{ isHovering, props }" v-if="post.comments.length > 3">
              <router-link :to="'/post/' + post.id" v-bind="props" class="text-decoration-none my-2"
                :class="isHovering ? 'text-primary cursor-pointer' : 'text-secondary'">Click here to show more
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
import { useDisplay } from 'vuetify'
import { ref, onBeforeMount } from 'vue';
import { useAuthStore } from '@/stores/auth'
import { usePostStore } from '@/stores/post'
const authStore = useAuthStore();
const postStore = usePostStore();
const newComment = ref([]);
const posts = ref([]);
const { lgAndUp, mdAndUp, smAndUp } = useDisplay()

const addComment = async (post, comment) => {
  await postStore.createComment(post.id, authStore.currentUser.id, comment);
  posts.value.find(p => p.id === post.id).comments.push({
    username: authStore.currentUser.username,
    text: comment
  });
}
const deleteComment = async (comment) => {
  await postStore.deleteComment(comment.id);
  posts.value.find(p => p.id === comment.post).comments = posts.value.find(p => p.id === comment.post).comments.filter(c => c.id !== comment.id)
}
const getPosts = async () => {
  await postStore.listPost();
  posts.value = postStore.posts;
}

const deletePost = async (postId) => {
  await postStore.deletePost(postId);
  posts.value = posts.value.filter(p => p.id !== postId);
}
onBeforeMount(() => {
  getPosts();
});
</script>

<style scoped>
.mb-4 {
  margin-bottom: 16px;
}
</style>