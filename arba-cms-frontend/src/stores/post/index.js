import { defineStore } from "pinia";
import axios from "axios";
import { useAuthStore } from "../auth";

const authStore = useAuthStore();
export const usePostStore = defineStore("post", {
  state: () => ({
    post: {},
    posts: [],
    isPostLoading: false,
  }),
  actions: {
    async deletePost(postId) {
      try {
        await axios.delete(`/v1/imagepost/${postId}/`, {
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
        });

        this.posts = this.posts.filter((post) => post.id !== postId);
      } catch (error) {
        console.error("Error deleting post:", error);
      }
    },
    async editPost(formData, postId){
      try {
        const response = await axios.put(`/v1/imagepost/${postId}/` , formData, {
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
        });

        const editedPost = response.data;
        console.log("editedPost:", editedPost);
      } catch (error) {
        console.error("Error creating post:", error);
      }
    },
    async createPost(formData) {
      console.log("formData:", formData);

      try {
        const response = await axios.post("/v1/imagepost/", formData, {
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
        });

        const createdPost = response.data;
        console.log("createdPost:", createdPost);
        // this.posts.push(createdPost);
      } catch (error) {
        console.error("Error creating post:", error);
      }
    },
    async getPostsByUserId(userId) {
      try {
        const response = await axios.get(`/v1/imagepost/user/${userId}/`);
        this.posts = response.data.reverse();
        this.posts = await Promise.all(
          this.posts.map(async (post) => {
            const commentRes = await this.getComments(post.id);
            post = {
              ...post,
              comments: commentRes.data ?? [],
              imageURL: `${import.meta.env.VITE_S3_POST_ENDPOINT}/${
                post.user
              }/${post.image}`,
            };
            return post;
          })
        );
        console.log("fetchedPosts:", this.posts);
      } catch (error) {
        console.error("Error fetching posts:", error);
      }
    },
    async getPost(postId) {
      try {
        const response = await axios.get(`/v1/imagepost/${postId}/`);
        this.post = response.data;
        const comments = await this.getComments(this.post.id);
        this.post = {
          ...this.post,
          comments: comments.data,
          imageURL: `${import.meta.env.VITE_S3_POST_ENDPOINT}/${
            this.post.user
          }/${this.post.image}`,
        };
        console.log("fetchedPosts:", this.post);
      } catch (error) {
        console.error("Error fetching posts:", error);
      }
    },
    async listPost() {
      try {
        const response = await axios.get("/v1/imagepost/");

        this.posts = response.data.reverse();
        this.posts = await Promise.all(
          this.posts.map(async (post) => {
            const commentRes = await this.getComments(post.id);
            post = {
              ...post,
              comments: commentRes.data,
              imageURL: `${import.meta.env.VITE_S3_POST_ENDPOINT}/${
                post.user
              }/${post.image}`,
            };
            return post;
          })
        );
        console.log("fetchedPosts:", this.posts);
      } catch (error) {
        console.error("Error fetching posts:", error);
      }
    },
    async deleteComment(commentId){
      try {
        await axios.delete(`/v1/comment/${commentId}/`, {
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
        });

        console.log("deletedComment");
        // Optionally, you can update the post's comments in the state if needed
      } catch (error) {
        console.error("Error deleting comment:", error);
      }
    },
    async createComment(postId, userId, commentData) {
      console.log(postId, userId, commentData);
      try {
        await axios.post(
          `/v1/comment/`,
          {
            image_post_id: postId,
            user: userId,
            text: commentData,
          },
          {
            headers: {
              Authorization: `Bearer ${authStore.token}`,
            },
          }
        );

        console.log("createdComment");
        // Optionally, you can update the post's comments in the state if needed
      } catch (error) {
        console.error("Error creating comment:", error);
      }
    },
    async getComments(imagePostId) {
      try {
        const response = await axios.get(`/v1/imagepost/comment/${imagePostId}/`);
        return response;
      } catch (error) {
        console.error("Error fetching comments:", error);
      }
    },
  },
});
