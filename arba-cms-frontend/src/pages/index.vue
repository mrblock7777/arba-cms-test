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
      <v-card :width="lgAndUp ? 500 : !xs ? 400 : 300" v-for="(post, index) in posts" :key="index" class=" mb-4">
        <v-card-title>
          <router-link :to="'/profile/' + post.user">@{{ post.username }}</router-link>
          <v-btn v-if="authStore.currentUser.id === post.user" class="float-right" variant="text">
            <v-icon>mdi-dots-vertical</v-icon>
            <v-menu activator="parent">
              <v-list>
                <v-list-item>
                  <v-list-item-title class="my-2 cursor-pointer" @click="$router.push('/post/edit/' + post.id)">
                    Edit Post
                  </v-list-item-title>
                  <v-list-item-title class="my-2 cursor-pointer" @click="deletePost(post.id)">
                    Delete Post
                  </v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </v-btn>
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
                  <span v-show="!comment.editable">{{ comment.text }}</span>
                  <span v-show="comment.editable">
                    <v-text-field v-if="authStore.isLogggedIn" v-model="comment.text" label="Edit Comment"
                      @keyup.enter="editComment(comment)">
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
                  <v-btn v-if="authStore.currentUser.id === comment.user" class="float-right" variant="text">
                    <v-icon>mdi-dots-vertical</v-icon>
                    <v-menu activator="parent">
                      <v-list>
                        <v-list-item>
                          <v-list-item-title class="my-2 cursor-pointer" @click="comment.editable = true">
                            Edit Comment
                          </v-list-item-title>
                          <v-list-item-title class="my-2 cursor-pointer" @click="deleteComment(comment)">
                            Delete Comment
                          </v-list-item-title>
                        </v-list-item>
                      </v-list>
                    </v-menu>
                  </v-btn>
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-list-item v-else v-for="(i) in 2">
              <v-list-item-content>
                <v-list-item-title>{{ post.comments[i].username }}</v-list-item-title>
                <v-list-item-subtitle>
                  <span v-show="!post.comments[i].editable">{{ post.comments[i].text }}</span>
                  <span v-show="post.comments[i].editable">
                    <v-text-field v-if="authStore.isLogggedIn" v-model="post.comments[i].text" label="Edit Comment"
                      @keyup.enter="editComment(post.comments[i])">
                      <template #append-inner>
                        <v-btn color="primary" variant="plain" @click="post.comments[i].editable = false">
                          <v-icon>mdi-close</v-icon>
                        </v-btn>
                        <v-btn color="primary" variant="plain" @click="editComment(post.comments[i])">
                          <v-icon>mdi-send</v-icon>
                        </v-btn>
                      </template>
                    </v-text-field>
                  </span>
                  <v-btn v-if="authStore.currentUser.id === post.comments[i].user" class="float-right" variant="text">
                    <v-icon>mdi-dots-vertical</v-icon>
                    <v-menu activator="parent">
                      <v-list>
                        <v-list-item>
                          <v-list-item-title class="my-2 cursor-pointer" @click="post.comments[i].editable = true">
                            Edit Comment
                          </v-list-item-title>
                          <v-list-item-title class="my-2 cursor-pointer" @click="deleteComment(post.comments[i])">
                            Delete Comment
                          </v-list-item-title>
                        </v-list-item>
                      </v-list>
                    </v-menu>
                  </v-btn>
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

const { lgAndUp, xs } = useDisplay()

const addComment = async (post, comment) => {
  await postStore.createComment(post.id, authStore.currentUser.id, comment);
  posts.value.find(p => p.id === post.id).comments.push({
    username: authStore.currentUser.username,
    text: comment
  });
}
const editComment = async (comment) => {
  await postStore.updateComment(comment);
  posts.value.find(p => p.id === comment.image_post).comments.find(c => c.id === comment.id).text = comment.text;
  posts.value.find(p => p.id === comment.image_post).comments.find(c => c.id === comment.id).editable = false;
}
const deleteComment = async (comment) => {
  if (confirm('Are you sure you want to delete this comment?')) {
    await postStore.deleteComment(comment.id);
    // posts.value.find(p => p.id === comment.image_post).comments = posts.value.find(p => p.id === comment.post).comments.filter(c => c.id !== comment.id)
    await getPosts()
  }
}
const getPosts = async () => {
  await postStore.listPost();
  posts.value = postStore.posts;
}

const deletePost = async (postId) => {
  if (confirm('Are you sure you want to delete this post?')) {
    await postStore.deletePost(postId);
    posts.value = posts.value.filter(p => p.id !== postId);
  }
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