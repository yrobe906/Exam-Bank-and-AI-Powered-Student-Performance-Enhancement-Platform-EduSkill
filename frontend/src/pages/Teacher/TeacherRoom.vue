<template>
  <div class="teacher-room-container">
    <EduskillHeader>
      <p>Teacher Room</p>
    </EduskillHeader>
    <!-- Enhanced Hero Section with Animated Background -->
    <div class="hero-section">
      <!-- Animated Background Shapes -->
      <div class="hero-bg-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
        <div class="shape shape-4"></div>
      </div>
      
      <div class="hero-content">
        <div class="hero-left">
          <div class="greeting-badge">
            <span class="greeting-icon">{{ greetingIcon }}</span>
            <span class="greeting-text">{{ greetingText }}</span>
          </div>
          <h1 class="hero-title">
            <span class="title-icon">🏫</span>
            Teacher Room
          </h1>
          <p class="hero-subtitle">Connect with your students & share knowledge</p>
          
          <!-- Quick Stats -->
          <div class="quick-stats">
            <div class="stat-item">
              <span class="stat-number">{{ stats.totalPosts }}</span>
              <span class="stat-label">Posts</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <span class="stat-number">{{ stats.totalComments }}</span>
              <span class="stat-label">Comments</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <span class="stat-number">{{ stats.totalLikes }}</span>
              <span class="stat-label">Likes</span>
            </div>
          </div>
        </div>
        
        <div class="hero-right">
          <div class="teacher-card">
            <div class="teacher-avatar-wrapper">
              <img 
                :src="currentUserProfileImage" 
                alt="Teacher" 
                class="teacher-avatar"
                @error="handleImageError"
              />
              <div class="online-indicator"></div>
            </div>
            <div class="teacher-info">
              <h3 class="teacher-name">{{ teacherName }}</h3>
              <p class="teacher-role">👨‍🏫 {{ teacherSubject }}</p>
              <p class="teacher-grade">Grade {{ teacherGrade }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content Area -->
    <main class="main-content">
      <!-- Stats & Quick Actions Bar -->
      <div class="stats-bar">
        <div class="stats-bar-left">
          <!-- Category Tabs -->
          <div class="category-tabs">
            <button 
              v-for="cat in categories" 
              :key="cat.value"
              @click="selectedCategory = cat.value"
              :class="['category-tab', { active: selectedCategory === cat.value }]"
            >
              <span class="tab-icon">{{ cat.icon }}</span>
              <span class="tab-label">{{ cat.label }}</span>
              <span class="tab-count">{{ getCategoryCount(cat.value) }}</span>
            </button>
          </div>
        </div>
        
        <div class="stats-bar-right">
          <!-- Quick Filters -->
          <div class="quick-filters">
            <button 
              v-for="filter in quickFilters" 
              :key="filter.value"
              @click="selectedFilter = filter.value"
              :class="['filter-btn', { active: selectedFilter === filter.value }]"
            >
              <span class="filter-icon">{{ filter.icon }}</span>
              {{ filter.label }}
            </button>
          </div>
        </div>
      </div>

      <!-- Search and Actions Row -->
      <div class="actions-row">
        <!-- Search Bar -->
        <div class="search-container">
          <div class="search-wrapper">
            <MagnifyingGlassIcon class="search-icon" />
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search posts, topics, students..."
              @input="onSearchChange"
              class="search-input"
            />
            <button v-if="searchQuery" @click="clearSearch" class="clear-btn">
              <XMarkIcon class="w-4 h-4" />
            </button>
          </div>
        </div>

        <!-- Create Post Button -->
        <button
          @click="showCreateModal = true"
          class="create-post-btn"
        >
          <PlusIcon class="btn-icon" />
          <span>Create Post</span>
        </button>
      </div>

      <!-- Posts Section -->
      <div class="posts-section">
        <!-- Loading State -->
        <div v-if="loading" class="loading-container">
          <div class="loading-cards">
            <div v-for="i in 3" :key="i" class="skeleton-card">
              <div class="skeleton-header">
                <div class="skeleton-avatar"></div>
                <div class="skeleton-info">
                  <div class="skeleton-line short"></div>
                  <div class="skeleton-line tiny"></div>
                </div>
              </div>
              <div class="skeleton-title"></div>
              <div class="skeleton-content">
                <div class="skeleton-line"></div>
                <div class="skeleton-line"></div>
                <div class="skeleton-line medium"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="filteredPosts.length === 0" class="empty-state">
          <div class="empty-illustration">📭</div>
          <h3 class="empty-title">No posts yet</h3>
          <p class="empty-text">Be the first to start a conversation!</p>
          <button @click="showCreateModal = true" class="empty-action-btn">
            Create First Post
          </button>
        </div>

        <!-- Posts Grid -->
        <div v-else class="posts-grid">
          <div
            v-for="(post, index) in filteredPosts"
            :key="post.id"
            class="post-card"
            :class="{ 'pinned-post': post.is_pinned }"
            :style="{ animationDelay: `${index * 0.05}s` }"
          >
            <!-- Post Header -->
            <div class="post-header">
              <div class="post-badges">
                <span v-if="post.is_pinned" class="badge pinned">
                  <MapPinIcon class="badge-icon" />
                  Pinned
                </span>
                <span v-if="isTrending(post)" class="badge trending">
                  <FireIcon class="badge-icon" />
                  Trending
                </span>
              </div>
              
              <!-- Post Menu -->
              <div class="post-menu" v-if="isOwnPost(post)">
                <button @click="toggleMenu(post)" class="menu-trigger">
                  <EllipsisVerticalIcon class="w-5 h-5" />
                </button>
                <div v-if="post.showMenu" class="menu-dropdown">
                  <button @click="editPost(post)" class="menu-item">
                    <PencilSquareIcon class="w-4 h-4" />
                    Edit
                  </button>
                  <button @click="togglePin(post)" class="menu-item">
                    <MapPinIcon class="w-4 h-4" />
                    {{ post.is_pinned ? 'Unpin' : 'Pin' }}
                  </button>
                  <button @click="deletePost(post)" class="menu-item danger">
                    <TrashIcon class="w-4 h-4" />
                    Delete
                  </button>
                </div>
              </div>
            </div>

            <!-- Post Author -->
            <div class="post-author">
              <div class="author-avatar">
                <img 
                  :src="getProfileImage(post.profile_image, post.username)" 
                  :alt="post.username"
                  @error="handleImageError"
                />
              </div>
              <div class="author-info">
                <div class="author-name-row">
                  <span class="author-name">{{ post.username }}</span>
                  <span :class="['role-badge', post.user_role]">
                    {{ post.user_role === 'teacher' ? '👨‍🏫 Teacher' : '👨‍🎓 Student' }}
                  </span>
                  <span v-if="isOwnPost(post)" class="you-badge">You</span>
                </div>
                <div class="author-meta">
                  <span class="post-date">{{ formatDate(post.date) }}</span>
                  <span class="meta-dot">•</span>
                  <span class="post-category">
                    <span class="category-icon">{{ getCategoryIcon(post.category) }}</span>
                    {{ post.category }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Post Content -->
            <div class="post-content">
              <h3 class="post-title">{{ post.title }}</h3>
              <p class="post-excerpt" :class="{ expanded: post.expanded }">
                {{ post.content }}
              </p>
              <button 
                v-if="post.content.length > 150" 
                @click="post.expanded = !post.expanded"
                class="read-more-btn"
              >
                {{ post.expanded ? 'Show less' : 'Read more...' }}
              </button>
              
              <!-- Post Image Preview -->
              <div v-if="post.image_url" class="post-image">
                <img :src="post.image_url" alt="Post image" />
              </div>
            </div>

            <!-- Post Stats -->
            <div class="post-stats">
              <div class="stat">
                <HeartIcon class="stat-icon" />
                <span>{{ post.likes }}</span>
              </div>
              <div class="stat">
                <ChatBubbleLeftIcon class="stat-icon" />
                <span>{{ post.comments }}</span>
              </div>
            </div>

            <!-- Post Actions -->
            <div class="post-actions">
              <!-- Reactions -->
              <div class="reactions-group">
                <button
                  @click="toggleLike(post)"
                  :class="['action-btn like-btn', { active: post.liked }]"
                >
                  <HeartIcon :class="['action-icon', { filled: post.liked }]" />
                  <span>{{ post.liked ? 'Liked' : 'Like' }}</span>
                </button>
                
                <button
                  @click="toggleReaction(post, 'celebrate')"
                  :class="['action-btn reaction-btn', { active: post.reaction === 'celebrate' }]"
                  title="Celebrate"
                >
                  🎉
                </button>
                
                <button
                  @click="toggleReaction(post, 'insightful')"
                  :class="['action-btn reaction-btn', { active: post.reaction === 'insightful' }]"
                  title="Insightful"
                >
                  💡
                </button>
                
                <button
                  @click="toggleReaction(post, 'love')"
                  :class="['action-btn reaction-btn', { active: post.reaction === 'love' }]"
                  title="Love"
                >
                  ❤️
                </button>
              </div>

              <!-- Other Actions -->
              <div class="actions-right">
                <button 
                  @click="toggleComments(post)"
                  class="action-btn"
                >
                  <ChatBubbleLeftIcon class="action-icon" />
                  <span>Comment</span>
                </button>
                
                <button 
                  @click="toggleBookmark(post)"
                  :class="['action-btn bookmark-btn', { active: post.bookmarked }]"
                >
                  <BookmarkIcon :class="['action-icon', { filled: post.bookmarked }]" />
                </button>
              </div>
            </div>

            <!-- Comments Section -->
            <div v-if="post.showComments" class="comments-section">
              <div class="comments-divider"></div>
              
              <!-- Existing Comments -->
              <div v-if="post.commentsList && post.commentsList.length > 0" class="comments-list">
                <div 
                  v-for="comment in post.commentsList" 
                  :key="comment.id"
                  class="comment-item"
                >
                  <div class="comment-avatar">
                    <img 
                      :src="getProfileImage(comment.profile_image, comment.username)"
                      :alt="comment.username"
                      @error="handleImageError"
                    />
                  </div>
                  <div class="comment-content">
                    <div class="comment-header">
                      <span class="comment-author">{{ comment.username }}</span>
                      <span :class="['comment-role', comment.user_role]">
                        {{ comment.user_role === 'teacher' ? 'Teacher' : 'Student' }}
                      </span>
                      <span class="comment-time">{{ formatDate(comment.created_at) }}</span>
                    </div>
                    <p class="comment-text">{{ comment.content }}</p>
                  </div>
                </div>
              </div>
              <div v-else-if="!post.loadingComments" class="no-comments">
                No comments yet. Be the first to comment!
              </div>

              <!-- Add Comment -->
              <div class="add-comment">
                <div class="comment-input-wrapper">
                  <img 
                    :src="currentUserProfileImage" 
                    alt="Your profile"
                    class="comment-input-avatar"
                    @error="handleImageError"
                  />
                  <input
                    v-model="post.newComment"
                    type="text"
                    placeholder="Write a comment..."
                    class="comment-input"
                    @keyup.enter="submitComment(post)"
                  />
                  <button
                    @click="submitComment(post)"
                    :disabled="!post.newComment?.trim()"
                    class="send-comment-btn"
                  >
                    <PaperAirplaneIcon class="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Create/Edit Post Modal -->
    <div v-if="showCreateModal || showEditModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-container">
        <div class="modal-header">
          <h2 class="modal-title">
            {{ showEditModal ? '✏️ Edit Post' : '📝 Create New Post' }}
          </h2>
          <button @click="closeModal" class="modal-close">
            <XMarkIcon class="w-6 h-6" />
          </button>
        </div>

        <form @submit.prevent="submitPost" class="modal-body">
          <div class="form-group">
            <label class="form-label">Title <span class="required">*</span></label>
            <input
              v-model="newPost.title"
              type="text"
              placeholder="Enter a descriptive title..."
              :class="['form-input', { error: errors.title }]"
            />
            <p v-if="errors.title" class="error-message">{{ errors.title }}</p>
          </div>

          <div class="form-group">
            <label class="form-label">Category <span class="required">*</span></label>
            <div class="category-select-wrapper">
              <select
                v-model="newPost.category"
                :class="['form-select', { error: errors.category }]"
              >
                <option value="">Select a category</option>
                <option value="Announcement">📢 Announcement</option>
                <option value="Class Management">👥 Class Management</option>
                <option value="Exam Schedule">📅 Exam Schedule</option>
                <option value="Study Tips">📚 Study Tips</option>
                <option value="Motivation">💪 Motivation</option>
                <option value="General">💬 General</option>
              </select>
              <ChevronDownIcon class="select-icon" />
            </div>
            <p v-if="errors.category" class="error-message">{{ errors.category }}</p>
          </div>

          <div class="form-group">
            <label class="form-label">Content <span class="required">*</span></label>
            <textarea
              v-model="newPost.content"
              rows="8"
              placeholder="Share your thoughts, knowledge, or announcements..."
              :class="['form-textarea', { error: errors.content }]"
            ></textarea>
            <p v-if="errors.content" class="error-message">{{ errors.content }}</p>
          </div>

          <div class="form-actions">
            <button type="button" @click="closeModal" class="btn-cancel">
              Cancel
            </button>
            <button type="submit" class="btn-submit">
              {{ showEditModal ? '💾 Save Changes' : '🚀 Publish Post' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Toast Notification -->
    <transition name="toast">
      <div v-if="toast.show" :class="['toast', toast.type]">
        <span class="toast-icon">{{ toast.icon }}</span>
        <span class="toast-message">{{ toast.message }}</span>
      </div>
    </transition>
  </div>
</template>

<script>
import forumService from '../../services/forumService.js';
import EduskillHeader from '@/components/Header/EduskillHeader.vue';
import {
  MagnifyingGlassIcon,
  ChevronDownIcon,
  PlusIcon,
  HeartIcon,
  ChatBubbleLeftIcon,
  BookmarkIcon,
  MapPinIcon,
  TrashIcon,
  XMarkIcon,
  PencilSquareIcon,
  PaperAirplaneIcon,
  EllipsisVerticalIcon,
  FireIcon
} from '@heroicons/vue/24/outline';

export default {
  name: 'TeacherRoom',
  components: {
    EduskillHeader,
    MagnifyingGlassIcon,
    ChevronDownIcon,
    PlusIcon,
    HeartIcon,
    ChatBubbleLeftIcon,
    BookmarkIcon,
    MapPinIcon,
    TrashIcon,
    XMarkIcon,
    PencilSquareIcon,
    PaperAirplaneIcon,
    EllipsisVerticalIcon,
    FireIcon
  },
  data() {
    return {
      teacherName: localStorage.getItem('username') || 'Teacher',
      userId: parseInt(localStorage.getItem('user_id')) || null,
      userRole: localStorage.getItem('role') || 'teacher',
      teacherSubject: localStorage.getItem('subject_assigned') || 'General',
      teacherGrade: localStorage.getItem('teaching_grade') || 'N/A',
      currentUserProfileImage: '',
      
      searchQuery: '',
      selectedFilter: 'latest',
      selectedCategory: 'all',
      
      showCreateModal: false,
      showEditModal: false,
      editingPostId: null,
      
      loading: false,
      
      newPost: {
        title: '',
        category: '',
        content: ''
      },
      errors: {},
      
      posts: [],
      
      stats: {
        totalPosts: 0,
        totalComments: 0,
        totalLikes: 0
      },
      
      categories: [
        { value: 'all', label: 'All', icon: '📋', count: 0 },
        { value: 'Announcement', label: 'Announcements', icon: '📢', count: 0 },
        { value: 'Class Management', label: 'Classes', icon: '👥', count: 0 },
        { value: 'Exam Schedule', label: 'Exams', icon: '📅', count: 0 },
        { value: 'Study Tips', label: 'Tips', icon: '📚', count: 0 },
        { value: 'Motivation', label: 'Motivation', icon: '💪', count: 0 },
        { value: 'General', label: 'General', icon: '💬', count: 0 }
      ],
      
      quickFilters: [
        { value: 'latest', label: 'Latest', icon: '🕒' },
        { value: 'my_posts', label: 'My Posts', icon: '📝' },
        { value: 'bookmarked', label: 'Saved', icon: '🔖' },
        { value: 'pinned', label: 'Pinned', icon: '📌' }
      ],
      
      toast: {
        show: false,
        message: '',
        type: 'success',
        icon: '✓'
      }
    };
  },
  
  computed: {
    greetingText() {
      const hour = new Date().getHours();
      if (hour < 12) return 'Good Morning';
      if (hour < 17) return 'Good Afternoon';
      return 'Good Evening';
    },
    
    greetingIcon() {
      const hour = new Date().getHours();
      if (hour < 12) return '🌅';
      if (hour < 17) return '☀️';
      return '🌙';
    },
    
    filteredPosts() {
      let result = [...this.posts];
      
      // Filter by category
      if (this.selectedCategory !== 'all') {
        result = result.filter(post => post.category === this.selectedCategory);
      }
      
      // Filter by search
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(post =>
          post.title.toLowerCase().includes(query) ||
          post.content.toLowerCase().includes(query) ||
          post.username.toLowerCase().includes(query)
        );
      }
      
      // Filter by quick filter
      switch (this.selectedFilter) {
        case 'latest':
          result.sort((a, b) => new Date(b.date) - new Date(a.date));
          break;
        case 'my_posts':
          result = result.filter(post => post.user_id === this.userId);
          break;
        case 'bookmarked':
          result = result.filter(post => post.bookmarked);
          break;
        case 'pinned':
          result = result.filter(post => post.is_pinned);
          result.sort((a, b) => new Date(b.date) - new Date(a.date));
          break;
      }
      
      return result;
    }
  },
  
  methods: {
    getCategoryCount(category) {
      if (category === 'all') return this.posts.length;
      return this.posts.filter(p => p.category === category).length;
    },
    
    getCategoryIcon(category) {
      const icons = {
        'Announcement': '📢',
        'Class Management': '👥',
        'Exam Schedule': '📅',
        'Study Tips': '📚',
        'Motivation': '💪',
        'General': '💬'
      };
      return icons[category] || '💬';
    },
    
    getProfileImage(profileImage, username) {
      if (profileImage && profileImage.startsWith('http')) {
        return profileImage;
      }
      if (profileImage) {
        return `http://127.0.0.1:8000/${profileImage}`;
      }
      return `https://api.dicebear.com/7.x/avataaars/svg?seed=${username}&backgroundColor=fef3c7`;
    },
    
    handleImageError(event) {
      event.target.src = `https://api.dicebear.com/7.x/avataaars/svg?seed=${Math.random()}&backgroundColor=fef3c7`;
    },
    
    isOwnPost(post) {
      return post.user_id === this.userId;
    },
    
    isTrending(post) {
      // Consider a post trending if it has high likes or comments
      return (post.likes > 10 || post.comments > 5) && !post.is_pinned;
    },
    
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      const now = new Date();
      const diffMs = now - date;
      const diffMins = Math.floor(diffMs / 60000);
      const diffHours = Math.floor(diffMs / 3600000);
      const diffDays = Math.floor(diffMs / 86400000);
      
      if (diffMins < 1) return 'Just now';
      if (diffMins < 60) return `${diffMins}m ago`;
      if (diffHours < 24) return `${diffHours}h ago`;
      if (diffDays < 7) return `${diffDays}d ago`;
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    },
    
    toggleMenu(post) {
      // Close other menus
      this.posts.forEach(p => {
        if (p.id !== post.id) p.showMenu = false;
      });
      post.showMenu = !post.showMenu;
    },
    
    toggleLike(post) {
      if (this.userId) {
        forumService.toggleLike(post.id, this.userId).then(result => {
          if (result) {
            post.likes = result.likes_count;
            post.liked = result.is_liked;
            this.updateStats();
          }
        });
      }
    },
    
    toggleReaction(post, reactionType) {
      // For now, just show the reaction
      if (post.reaction === reactionType) {
        post.reaction = null;
      } else {
        post.reaction = reactionType;
        this.showToast(`Reacted with ${reactionType}!`, 'success', '🎉');
      }
    },
    
    async toggleBookmark(post) {
      if (this.userId) {
        const result = await forumService.toggleBookmark(post.id, this.userId);
        if (result) {
          post.bookmarked = result.is_bookmarked;
          this.showToast(
            result.is_bookmarked ? 'Post saved!' : 'Post removed from saved',
            'success',
            result.is_bookmarked ? '🔖' : '📝'
          );
        }
      }
    },
    
    async toggleComments(post) {
      post.showComments = !post.showComments;
      if (post.showComments && !post.commentsList) {
        await this.loadComments(post);
      }
    },
    
    async loadComments(post) {
      post.loadingComments = true;
      try {
        const comments = await forumService.getComments(post.id);
        post.commentsList = comments.map(c => ({
          id: c.id,
          username: c.username,
          user_role: c.user_role,
          profile_image: c.profile_image,
          content: c.content,
          created_at: c.created_at
        }));
      } catch (error) {
        console.error('Error loading comments:', error);
      } finally {
        post.loadingComments = false;
      }
    },
    
    async submitComment(post) {
      if (!post.newComment?.trim() || !this.userId) return;
      
      const comment = await forumService.createComment(post.id, post.newComment, this.userId, this.userRole);
      if (comment) {
        if (!post.commentsList) post.commentsList = [];
        post.commentsList.unshift({
          id: comment.id,
          username: this.teacherName,
          user_role: this.userRole,
          profile_image: this.currentUserProfileImage,
          content: comment.content,
          created_at: comment.created_at
        });
        post.comments = (post.comments || 0) + 1;
        post.newComment = '';
        this.updateStats();
        this.showToast('Comment added!', 'success', '💬');
      }
    },
    
    async togglePin(post) {
      const newPinState = !post.is_pinned;
      const result = await forumService.togglePin(post.id, newPinState, this.userRole);
      if (result) {
        post.is_pinned = newPinState;
        post.showMenu = false;
        this.showToast(
          newPinState ? 'Post pinned!' : 'Post unpinned',
          'success',
          newPinState ? '📌' : '📝'
        );
      }
    },
    
    editPost(post) {
      this.editingPostId = post.id;
      this.newPost = {
        title: post.title,
        category: post.category,
        content: post.content
      };
      this.showEditModal = true;
      post.showMenu = false;
    },
    
    async deletePost(post) {
      if (confirm('Are you sure you want to delete this post? This action cannot be undone.')) {
        const success = await forumService.deletePost(post.id, this.userId, this.userRole);
        if (success) {
          const index = this.posts.findIndex(p => p.id === post.id);
          if (index > -1) {
            this.posts.splice(index, 1);
          }
          this.updateStats();
          this.showToast('Post deleted!', 'success', '🗑️');
        }
      }
    },
    
    sharePost(post) {
      // Copy link to clipboard
      const link = `${window.location.origin}/teacher-room/post/${post.id}`;
      navigator.clipboard.writeText(link).then(() => {
        this.showToast('Link copied to clipboard!', 'success', '🔗');
      });
    },
    
    async loadPosts() {
      this.loading = true;
      try {
        const posts = await forumService.getPosts(
          this.selectedFilter,
          null,
          this.searchQuery,
          this.userId
        );
        this.posts = posts.map(post => ({
          ...post,
          date: post.created_at,
          expanded: false,
          showComments: false,
          commentsList: null,
          newComment: '',
          loadingComments: false,
          showMenu: false,
          reaction: null
        }));
        this.updateStats();
      } catch (error) {
        console.error('Error loading posts:', error);
      } finally {
        this.loading = false;
      }
    },
    
    updateStats() {
      this.stats.totalPosts = this.posts.length;
      this.stats.totalComments = this.posts.reduce((sum, p) => sum + (p.comments || 0), 0);
      this.stats.totalLikes = this.posts.reduce((sum, p) => sum + (p.likes || 0), 0);
    },
    
    onSearchChange() {
      // Debounce search
      clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(() => {
        this.loadPosts();
      }, 300);
    },
    
    clearSearch() {
      this.searchQuery = '';
      this.loadPosts();
    },
    
    onFilterChange() {
      this.loadPosts();
    },
    
    validateForm() {
      this.errors = {};
      if (!this.newPost.title || !this.newPost.title.trim()) {
        this.errors.title = 'Title is required';
      }
      if (!this.newPost.category) {
        this.errors.category = 'Please select a category';
      }
      if (!this.newPost.content || !this.newPost.content.trim()) {
        this.errors.content = 'Content is required';
      }
      return Object.keys(this.errors).length === 0;
    },
    
    async submitPost() {
      if (!this.validateForm()) {
        return;
      }
      
      const postData = {
        title: this.newPost.title,
        content: this.newPost.content,
        category: this.newPost.category
      };

      if (this.showEditModal) {
        const updated = await forumService.updatePost(this.editingPostId, postData, this.userId, this.userRole);
        if (updated) {
          await this.loadPosts();
          this.showToast('Post updated successfully!', 'success', '✅');
        }
      } else {
        const created = await forumService.createPost(postData, this.userId);
        if (created) {
          await this.loadPosts();
          this.showToast('Post created successfully!', 'success', '🎉');
        }
      }
      
      this.closeModal();
    },
    
    closeModal() {
      this.showCreateModal = false;
      this.showEditModal = false;
      this.editingPostId = null;
      this.newPost = { title: '', category: '', content: '' };
      this.errors = {};
    },
    
    showToast(message, type = 'success', icon = '✓') {
      this.toast = { show: true, message, type, icon };
      setTimeout(() => {
        this.toast.show = false;
      }, 3000);
    }
  },
  
  async mounted() {
    const role = localStorage.getItem('role');
    if (role !== 'teacher') {
      this.$router.push('/user_login');
    } else {
      // Load current user profile
      const userProfile = localStorage.getItem('profile_photo');
      this.currentUserProfileImage = userProfile 
        ? `http://127.0.0.1:8000/${userProfile}` 
        : `https://api.dicebear.com/7.x/avataaars/svg?seed=${this.teacherName}&backgroundColor=fef3c7`;
      
      await this.loadPosts();
    }
  },
  
  beforeUnmount() {
    clearTimeout(this.searchTimeout);
  }
};
</script>

<style scoped>
/* ============================
   Base Styles & Variables
   ============================ */
.teacher-room-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

/* ============================
   Hero Section
   ============================ */
.hero-section {
  position: relative;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  padding: 40px;
  overflow: hidden;
  min-height: 280px;
}

.hero-bg-shapes {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.shape {
  position: absolute;
  border-radius: 50%;
  opacity: 0.1;
  animation: float 20s infinite ease-in-out;
}

.shape-1 {
  width: 300px;
  height: 300px;
  background: white;
  top: -100px;
  left: -50px;
  animation-delay: 0s;
}

.shape-2 {
  width: 200px;
  height: 200px;
  background: white;
  top: 50%;
  right: -50px;
  animation-delay: -5s;
}

.shape-3 {
  width: 150px;
  height: 150px;
  background: white;
  bottom: -50px;
  left: 30%;
  animation-delay: -10s;
}

.shape-4 {
  width: 100px;
  height: 100px;
  background: white;
  top: 20%;
  left: 50%;
  animation-delay: -15s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  25% { transform: translate(10px, -20px) rotate(5deg); }
  50% { transform: translate(-5px, 15px) rotate(-5deg); }
  75% { transform: translate(15px, 5px) rotate(3deg); }
}

.hero-content {
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
}

.hero-left {
  flex: 1;
}

.greeting-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  padding: 8px 16px;
  border-radius: 50px;
  margin-bottom: 16px;
}

.greeting-icon {
  font-size: 20px;
}

.greeting-text {
  color: white;
  font-weight: 600;
  font-size: 14px;
}

.hero-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 42px;
  font-weight: 800;
  color: white;
  margin: 0 0 8px 0;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.title-icon {
  font-size: 48px;
}

.hero-subtitle {
  color: rgba(255, 255, 255, 0.9);
  font-size: 18px;
  margin: 0 0 24px 0;
}

.quick-stats {
  display: flex;
  align-items: center;
  gap: 24px;
}

.stat-item {
  display: flex;
  flex-direction: column;
}

.stat-number {
  color: white;
  font-size: 28px;
  font-weight: 700;
}

.stat-label {
  color: rgba(255, 255, 255, 0.8);
  font-size: 13px;
}

.stat-divider {
  width: 1px;
  height: 40px;
  background: rgba(255, 255, 255, 0.3);
}

/* Teacher Card */
.teacher-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 20px 28px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
}

.teacher-avatar-wrapper {
  position: relative;
}

.teacher-avatar {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  object-fit: cover;
  border: 3px solid #667eea;
}

.online-indicator {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 14px;
  height: 14px;
  background: #10b981;
  border: 3px solid white;
  border-radius: 50%;
}

.teacher-name {
  color: #1e293b;
  font-size: 18px;
  font-weight: 700;
  margin: 0 0 4px 0;
}

.teacher-role {
  color: #64748b;
  font-size: 14px;
  margin: 0 0 2px 0;
}

.teacher-grade {
  color: #667eea;
  font-size: 13px;
  font-weight: 600;
  margin: 0;
}

/* ============================
   Main Content
   ============================ */
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px;
}

/* Stats Bar */
.stats-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 16px;
}

.category-tabs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.category-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 50px;
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.category-tab:hover {
  border-color: #667eea;
  color: #667eea;
}

.category-tab.active {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-color: transparent;
  color: white;
}

.tab-icon {
  font-size: 14px;
}

.tab-count {
  background: rgba(0, 0, 0, 0.1);
  padding: 2px 8px;
  border-radius: 20px;
  font-size: 11px;
}

.category-tab.active .tab-count {
  background: rgba(255, 255, 255, 0.2);
}

/* Quick Filters */
.quick-filters {
  display: flex;
  gap: 8px;
}

.filter-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  font-size: 13px;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn:hover {
  border-color: #667eea;
  color: #667eea;
}

.filter-btn.active {
  background: #667eea;
  border-color: #667eea;
  color: white;
}

.filter-icon {
  font-size: 14px;
}

/* Actions Row */
.actions-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.search-container {
  flex: 1;
  max-width: 600px;
}

.search-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 16px;
  width: 20px;
  height: 20px;
  color: #94a3b8;
}

.search-input {
  width: 100%;
  padding: 14px 48px;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 16px;
  font-size: 15px;
  transition: all 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
}

.clear-btn {
  position: absolute;
  right: 12px;
  padding: 6px;
  background: #f1f5f9;
  border-radius: 50%;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.clear-btn:hover {
  background: #e2e8f0;
  color: #1e293b;
}

.create-post-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 28px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 14px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.create-post-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
}

.btn-icon {
  width: 20px;
  height: 20px;
}

/* ============================
   Posts Section
   ============================ */
.posts-section {
  min-height: 400px;
}

/* Loading */
.loading-container {
  padding: 20px 0;
}

.loading-cards {
  display: grid;
  gap: 20px;
}

.skeleton-card {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.skeleton-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.skeleton-avatar {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 50%, #f1f5f9 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

.skeleton-info {
  flex: 1;
}

.skeleton-line {
  height: 12px;
  background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 50%, #f1f5f9 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 6px;
  margin-bottom: 8px;
}

.skeleton-line.short {
  width: 40%;
}

.skeleton-line.tiny {
  width: 25%;
  height: 10px;
}

.skeleton-line.medium {
  width: 70%;
}

.skeleton-title {
  height: 24px;
  width: 60%;
  background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 50%, #f1f5f9 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 8px;
  margin-bottom: 12px;
}

.skeleton-content .skeleton-line:last-child {
  margin-bottom: 0;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 24px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
}

.empty-illustration {
  font-size: 80px;
  margin-bottom: 20px;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px); }
}

.empty-title {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 8px 0;
}

.empty-text {
  color: #64748b;
  margin: 0 0 24px 0;
}

.empty-action-btn {
  padding: 14px 32px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.empty-action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

/* Posts Grid */
.posts-grid {
  display: grid;
  gap: 20px;
}

.post-card {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
  animation: slideUp 0.4s ease-out forwards;
  opacity: 0;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.post-card:hover {
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.post-card.pinned-post {
  border: 2px solid #f59e0b;
  background: linear-gradient(135deg, white 0%, #fffbeb 100%);
}

/* Post Header */
.post-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.post-badges {
  display: flex;
  gap: 8px;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.badge.pinned {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
}

.badge.trending {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
}

.badge-icon {
  width: 14px;
  height: 14px;
}

.post-menu {
  position: relative;
}

.menu-trigger {
  padding: 6px;
  background: #f1f5f9;
  border-radius: 8px;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.menu-trigger:hover {
  background: #e2e8f0;
  color: #1e293b;
}

.menu-dropdown {
  position: absolute;
  right: 0;
  top: 100%;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  z-index: 10;
  min-width: 150px;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 12px 16px;
  background: none;
  border: none;
  font-size: 14px;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}

.menu-item:hover {
  background: #f1f5f9;
}

.menu-item.danger {
  color: #ef4444;
}

.menu-item.danger:hover {
  background: #fef2f2;
}

/* Post Author */
.post-author {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.author-avatar {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  overflow: hidden;
  flex-shrink: 0;
}

.author-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.author-info {
  flex: 1;
}

.author-name-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.author-name {
  font-weight: 700;
  color: #1e293b;
  font-size: 16px;
}

.role-badge {
  padding: 2px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
}

.role-badge.teacher {
  background: linear-gradient(135deg, #8b5cf6, #a855f7);
  color: white;
}

.role-badge.student {
  background: linear-gradient(135deg, #3b82f6, #60a5fa);
  color: white;
}

.you-badge {
  padding: 2px 8px;
  background: #fef3c7;
  color: #d97706;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
}

.author-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #64748b;
}

.meta-dot {
  color: #cbd5e1;
}

.post-category {
  display: flex;
  align-items: center;
  gap: 4px;
}

.category-icon {
  font-size: 12px;
}

/* Post Content */
.post-content {
  margin-bottom: 16px;
}

.post-title {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 8px 0;
  line-height: 1.4;
}

.post-excerpt {
  color: #475569;
  line-height: 1.7;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-excerpt.expanded {
  -webkit-line-clamp: unset;
}

.read-more-btn {
  background: none;
  border: none;
  color: #667eea;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
  margin-top: 8px;
}

.read-more-btn:hover {
  text-decoration: underline;
}

.post-image {
  margin-top: 16px;
  border-radius: 12px;
  overflow: hidden;
}

.post-image img {
  width: 100%;
  height: auto;
}

/* Post Stats */
.post-stats {
  display: flex;
  gap: 20px;
  padding: 12px 0;
  border-top: 1px solid #f1f5f9;
  border-bottom: 1px solid #f1f5f9;
  margin-bottom: 12px;
}

.post-stats .stat {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #64748b;
  font-size: 13px;
}

.stat-icon {
  width: 16px;
  height: 16px;
}

/* Post Actions */
.post-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.reactions-group {
  display: flex;
  gap: 8px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  font-size: 13px;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

.action-btn.like-btn.active {
  background: linear-gradient(135deg, #f43f5e, #e11d48);
  border-color: transparent;
  color: white;
}

.action-icon {
  width: 18px;
  height: 18px;
}

.action-icon.filled {
  fill: currentColor;
}

.reaction-btn {
  padding: 8px 10px;
  font-size: 16px;
}

.reaction-btn.active {
  background: #fef3c7;
  border-color: #f59e0b;
  transform: scale(1.1);
}

.actions-right {
  display: flex;
  gap: 8px;
}

.bookmark-btn.active {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  border-color: transparent;
  color: white;
}

.share-btn:hover {
  background: #eff6ff;
  border-color: #3b82f6;
  color: #3b82f6;
}

/* Comments Section */
.comments-section {
  margin-top: 16px;
}

.comments-divider {
  height: 1px;
  background: #f1f5f9;
  margin-bottom: 16px;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.comment-item {
  display: flex;
  gap: 12px;
}

.comment-avatar {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  overflow: hidden;
  flex-shrink: 0;
}

.comment-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.comment-content {
  flex: 1;
  background: #f8fafc;
  border-radius: 12px;
  padding: 12px;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.comment-author {
  font-weight: 600;
  color: #1e293b;
  font-size: 14px;
}

.comment-role {
  padding: 2px 8px;
  border-radius: 20px;
  font-size: 10px;
  font-weight: 600;
}

.comment-role.teacher {
  background: #ede9fe;
  color: #7c3aed;
}

.comment-role.student {
  background: #dbeafe;
  color: #2563eb;
}

.comment-time {
  color: #94a3b8;
  font-size: 12px;
}

.comment-text {
  color: #475569;
  font-size: 14px;
  margin: 0;
  line-height: 1.5;
}

.no-comments {
  text-align: center;
  color: #94a3b8;
  padding: 20px;
  font-size: 14px;
}

.add-comment {
  margin-top: 12px;
}

.comment-input-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
}

.comment-input-avatar {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  object-fit: cover;
}

.comment-input {
  flex: 1;
  padding: 10px 16px;
  background: #f8fafc;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 14px;
  transition: all 0.2s;
}

.comment-input:focus {
  outline: none;
  border-color: #667eea;
  background: white;
}

.send-comment-btn {
  padding: 10px 16px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.send-comment-btn:hover:not(:disabled) {
  transform: scale(1.05);
}

.send-comment-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* ============================
   Modal
   ============================ */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-container {
  background: white;
  border-radius: 24px;
  width: 100%;
  max-width: 560px;
  max-height: 90vh;
  overflow-y: auto;
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 1px solid #f1f5f9;
}

.modal-title {
  font-size: 22px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.modal-close {
  padding: 8px;
  background: #f1f5f9;
  border: none;
  border-radius: 10px;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.modal-close:hover {
  background: #e2e8f0;
  color: #1e293b;
}

.modal-body {
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.required {
  color: #ef4444;
}

.form-input,
.form-select,
.form-textarea {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 15px;
  transition: all 0.2s;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
}

.form-input.error,
.form-select.error,
.form-textarea.error {
  border-color: #ef4444;
}

.form-select {
  appearance: none;
  cursor: pointer;
}

.category-select-wrapper {
  position: relative;
}

.select-icon {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #94a3b8;
  pointer-events: none;
}

.form-textarea {
  resize: vertical;
  min-height: 150px;
}

.error-message {
  color: #ef4444;
  font-size: 13px;
  margin-top: 6px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.btn-cancel {
  padding: 14px 28px;
  background: #f1f5f9;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel:hover {
  background: #e2e8f0;
  color: #1e293b;
}

.btn-submit {
  padding: 14px 28px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-submit:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

/* ============================
   Toast Notification
   ============================ */
.toast {
  position: fixed;
  bottom: 30px;
  right: 30px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 24px;
  background: white;
  border-radius: 14px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  z-index: 2000;
  animation: toastSlideIn 0.3s ease-out;
}

@keyframes toastSlideIn {
  from {
    opacity: 0;
    transform: translateX(100px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.toast.success {
  border-left: 4px solid #10b981;
}

.toast.error {
  border-left: 4px solid #ef4444;
}

.toast-icon {
  font-size: 20px;
}

.toast-message {
  color: #1e293b;
  font-size: 14px;
  font-weight: 500;
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateX(100px);
}

/* ============================
   Responsive
   ============================ */
@media (max-width: 1024px) {
  .hero-content {
    flex-direction: column;
    gap: 24px;
    text-align: center;
  }
  
  .hero-left {
    width: 100%;
  }
  
  .hero-right {
    width: 100%;
    display: flex;
    justify-content: center;
  }
  
  .quick-stats {
    justify-content: center;
  }
  
  .stats-bar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .category-tabs {
    justify-content: center;
  }
  
  .quick-filters {
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: 24px;
    min-height: auto;
  }
  
  .hero-title {
    font-size: 28px;
  }
  
  .title-icon {
    font-size: 32px;
  }
  
  .teacher-card {
    padding: 16px;
  }
  
  .teacher-avatar {
    width: 48px;
    height: 48px;
  }
  
  .main-content {
    padding: 16px;
  }
  
  .actions-row {
    flex-direction: column;
  }
  
  .search-container {
    max-width: 100%;
    width: 100%;
  }
  
  .create-post-btn {
    width: 100%;
    justify-content: center;
  }
  
  .category-tabs {
    overflow-x: auto;
    flex-wrap: nowrap;
    padding-bottom: 8px;
  }
  
  .category-tab {
    flex-shrink: 0;
  }
  
  .post-card {
    padding: 16px;
  }
  
  .post-actions {
    flex-wrap: wrap;
    gap: 8px;
  }
  
  .reactions-group {
    flex-wrap: wrap;
  }
  
  .actions-right {
    flex-wrap: wrap;
  }
}
</style>

