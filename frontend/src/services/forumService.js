const API_BASE = "http://127.0.0.1:8000/api";

export default {
  // Get all posts with filters
  async getPosts(filterType = "latest", category = null, search = null, userId = null) {
    try {
      let url = `${API_BASE}/posts?filter_type=${filterType}`;
      if (category) url += `&category=${category}`;
      if (search) url += `&search=${encodeURIComponent(search)}`;
      if (userId) url += `&user_id=${userId}`;
      
      const response = await fetch(url);
      if (!response.ok) throw new Error("Failed to fetch posts");
      return await response.json();
    } catch (error) {
      console.error("Error fetching posts:", error);
      return [];
    }
  },

  // Get a single post
  async getPost(postId, userId = null) {
    try {
      let url = `${API_BASE}/posts/${postId}`;
      if (userId) url += `?user_id=${userId}`;
      
      const response = await fetch(url);
      if (!response.ok) throw new Error("Failed to fetch post");
      return await response.json();
    } catch (error) {
      console.error("Error fetching post:", error);
      return null;
    }
  },

  // Create a new post
  async createPost(postData, userId) {
    try {
      const response = await fetch(`${API_BASE}/posts?user_id=${userId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(postData)
      });
      if (!response.ok) throw new Error("Failed to create post");
      return await response.json();
    } catch (error) {
      console.error("Error creating post:", error);
      return null;
    }
  },

  // Update a post
  async updatePost(postId, postData, userId, userRole) {
    try {
      const response = await fetch(
        `${API_BASE}/posts/${postId}?user_id=${userId}&user_role=${userRole}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(postData)
        }
      );
      if (!response.ok) throw new Error("Failed to update post");
      return await response.json();
    } catch (error) {
      console.error("Error updating post:", error);
      return null;
    }
  },

  // Delete a post
  async deletePost(postId, userId, userRole) {
    try {
      const response = await fetch(
        `${API_BASE}/posts/${postId}?user_id=${userId}&user_role=${userRole}`,
        { method: "DELETE" }
      );
      if (!response.ok) throw new Error("Failed to delete post");
      return true;
    } catch (error) {
      console.error("Error deleting post:", error);
      return false;
    }
  },

  // Toggle like on a post
  async toggleLike(postId, userId) {
    try {
      const response = await fetch(
        `${API_BASE}/posts/${postId}/like?user_id=${userId}`,
        { method: "POST" }
      );
      if (!response.ok) throw new Error("Failed to toggle like");
      return await response.json();
    } catch (error) {
      console.error("Error toggling like:", error);
      return null;
    }
  },

  // Toggle bookmark on a post
  async toggleBookmark(postId, userId) {
    try {
      const response = await fetch(
        `${API_BASE}/posts/${postId}/bookmark?user_id=${userId}`,
        { method: "POST" }
      );
      if (!response.ok) throw new Error("Failed to toggle bookmark");
      return await response.json();
    } catch (error) {
      console.error("Error toggling bookmark:", error);
      return null;
    }
  },

  // Pin/Unpin a post (teacher or admin)
  async togglePin(postId, isPinned, userRole) {
    try {
      const response = await fetch(
        `${API_BASE}/posts/${postId}/pin?is_pinned=${isPinned}&user_role=${userRole}`,
        { method: "POST" }
      );
      if (!response.ok) throw new Error("Failed to toggle pin");
      return await response.json();
    } catch (error) {
      console.error("Error toggling pin:", error);
      return null;
    }
  },

  // Get comments for a post
  async getComments(postId) {
    try {
      const response = await fetch(`${API_BASE}/posts/${postId}/comments`);
      if (!response.ok) throw new Error("Failed to fetch comments");
      return await response.json();
    } catch (error) {
      console.error("Error fetching comments:", error);
      return [];
    }
  },

  // Create a comment
  async createComment(postId, content, userId, userRole = "student") {
    try {
      const response = await fetch(
        `${API_BASE}/posts/${postId}/comments?user_id=${userId}&user_role=${userRole}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ content })
        }
      );
      if (!response.ok) throw new Error("Failed to create comment");
      return await response.json();
    } catch (error) {
      console.error("Error creating comment:", error);
      return null;
    }
  },

  // Get bookmarked posts
  async getBookmarks(userId) {
    try {
      const response = await fetch(`${API_BASE}/bookmarks?user_id=${userId}`);
      if (!response.ok) throw new Error("Failed to fetch bookmarks");
      return await response.json();
    } catch (error) {
      console.error("Error fetching bookmarks:", error);
      return [];
    }
  }
};
