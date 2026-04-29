<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50/30">
    <!-- Header -->
    <div class="bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-40">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <button @click="goBack" class="mr-4 p-2 rounded-xl hover:bg-gray-100 transition-colors">
              <ArrowLeftIcon class="h-5 w-5 text-gray-600" />
            </button>
            <h1 class="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
              🛠️ Forum Management
            </h1>
          </div>
          <div class="flex items-center space-x-4">
            <div class="h-10 w-10 rounded-xl overflow-hidden border-2 border-indigo-400">
              <img 
                :src="adminProfileImage" 
                alt="Admin" 
                class="w-full h-full object-cover"
                @error="handleImageError"
              />
            </div>
            <span class="text-sm font-semibold text-gray-700">{{ adminName }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Stats Overview -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-2xl shadow-lg border border-gray-100 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500">Total Posts</p>
              <p class="text-3xl font-bold text-gray-800">{{ stats.totalPosts }}</p>
            </div>
            <div class="h-12 w-12 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-500 flex items-center justify-center">
              <DocumentTextIcon class="h-6 w-6 text-white" />
            </div>
          </div>
        </div>
        <div class="bg-white rounded-2xl shadow-lg border border-gray-100 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500">Total Comments</p>
              <p class="text-3xl font-bold text-gray-800">{{ stats.totalComments }}</p>
            </div>
            <div class="h-12 w-12 rounded-xl bg-gradient-to-r from-blue-500 to-cyan-500 flex items-center justify-center">
              <ChatBubbleLeftRightIcon class="h-6 w-6 text-white" />
            </div>
          </div>
        </div>
        <div class="bg-white rounded-2xl shadow-lg border border-gray-100 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500">Teacher Posts</p>
              <p class="text-3xl font-bold text-gray-800">{{ stats.teacherPosts }}</p>
            </div>
            <div class="h-12 w-12 rounded-xl bg-gradient-to-r from-purple-500 to-pink-500 flex items-center justify-center">
              <AcademicCapIcon class="h-6 w-6 text-white" />
            </div>
          </div>
        </div>
        <div class="bg-white rounded-2xl shadow-lg border border-gray-100 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500">Student Posts</p>
              <p class="text-3xl font-bold text-gray-800">{{ stats.studentPosts }}</p>
            </div>
            <div class="h-12 w-12 rounded-xl bg-gradient-to-r from-green-500 to-emerald-500 flex items-center justify-center">
              <UserGroupIcon class="h-6 w-6 text-white" />
            </div>
          </div>
        </div>
      </div>

      <!-- Search and Filter Section -->
      <div class="bg-white rounded-2xl shadow-lg border border-gray-100 p-6 mb-8">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <!-- Search Bar -->
          <div class="flex-1 relative">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search posts by title, content, username..."
              @input="onSearchChange"
              class="w-full pl-12 pr-4 py-3 bg-gradient-to-r from-gray-50 to-white border-2 border-gray-200 rounded-xl focus:outline-none focus:border-indigo-400 focus:ring-4 focus:ring-indigo-100/50 transition-all duration-300"
            />
            <MagnifyingGlassIcon class="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
          </div>

          <!-- Filter Dropdown -->
          <div class="flex items-center space-x-4">
            <div class="relative">
              <select
                v-model="selectedFilter"
                @change="onFilterChange"
                class="appearance-none w-full md:w-48 pl-4 pr-10 py-3 bg-gradient-to-r from-gray-50 to-white border-2 border-gray-200 rounded-xl focus:outline-none focus:border-indigo-400 focus:ring-4 focus:ring-indigo-100/50 transition-all duration-300 cursor-pointer"
              >
                <option value="latest">📢 Latest</option>
                <option value="oldest">📅 Oldest</option>
                <option value="most_liked">❤️ Most Liked</option>
                <option value="most_commented">💬 Most Commented</option>
                <option value="teachers">👨‍🏫 Teachers Only</option>
                <option value="students">👨‍🎓 Students Only</option>
              </select>
              <ChevronDownIcon class="absolute right-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400 pointer-events-none" />
            </div>

            <!-- Refresh Button -->
            <button
              @click="loadPosts"
              class="px-4 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl hover:shadow-indigo-500/30 hover:scale-105 transition-all duration-300 flex items-center"
            >
              <ArrowPathIcon class="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>

      <!-- Posts Section -->
      <div class="space-y-6">
        <div v-if="loading" class="text-center py-16">
          <div class="relative">
            <div class="animate-spin rounded-full h-16 w-16 border-4 border-indigo-200 border-t-indigo-600 mx-auto"></div>
            <div class="absolute inset-0 flex items-center justify-center">
              <span class="text-2xl">⚙️</span>
            </div>
          </div>
          <p class="text-gray-600 mt-6 font-medium">Loading posts...</p>
        </div>

        <div v-else-if="filteredPosts.length === 0" class="text-center py-16">
          <div class="text-7xl mb-6">📭</div>
          <h3 class="text-2xl font-bold text-gray-800 mb-3">No posts found</h3>
          <p class="text-gray-600">No forum posts match your criteria.</p>
        </div>

        <div
          v-else
          v-for="(post, index) in filteredPosts"
          :key="post.id"
          class="bg-white rounded-3xl shadow-lg border border-gray-100 p-6 hover:shadow-2xl hover:shadow-indigo-100/50 transition-all duration-500"
          :style="{ animationDelay: `${index * 0.05}s` }"
        >
          <!-- Post Header -->
          <div class="flex items-start justify-between mb-5">
            <div class="flex items-center space-x-4">
              <!-- Profile Image -->
              <div class="h-14 w-14 rounded-2xl overflow-hidden border-3 border-gradient-to-r from-indigo-400 to-purple-400 shadow-md">
                <img 
                  :src="getProfileImage(post.profile_image, post.username)" 
                  :alt="post.username" 
                  class="w-full h-full object-cover"
                  @error="handleImageError"
                />
              </div>
              <div>
                <div class="flex items-center space-x-2">
                  <h4 class="font-bold text-gray-800 text-lg">{{ post.username }}</h4>
                  <span
                    :class="[
                      'px-3 py-1 text-xs font-bold rounded-full',
                      post.user_role === 'teacher'
                        ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-md'
                        : 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white shadow-md'
                    ]"
                  >
                    {{ post.user_role === 'teacher' ? '👨‍🏫 Teacher' : '👨‍🎓 Student' }}
                  </span>
                  <span 
                    v-if="post.is_pinned"
                    class="px-2 py-1 bg-gradient-to-r from-amber-500 to-orange-500 text-white text-xs font-semibold rounded-full"
                  >
                    📌 Pinned
                  </span>
                </div>
                <div class="flex items-center space-x-2 mt-1">
                  <p class="text-sm text-gray-500">{{ formatDate(post.date) }}</p>
                  <span class="text-gray-300">•</span>
                  <span class="text-sm text-gray-500">{{ post.category }}</span>
                </div>
              </div>
            </div>

            <!-- Admin Actions -->
            <div class="flex items-center space-x-2">
              <button
                @click="editPost(post)"
                class="flex items-center space-x-2 px-4 py-2 rounded-xl bg-gray-100 text-gray-600 hover:bg-indigo-50 hover:text-indigo-600 transition-all duration-300"
                title="Edit post"
              >
                <PencilSquareIcon class="h-5 w-5" />
              </button>
              <button
                @click="deletePost(post)"
                class="flex items-center space-x-2 px-4 py-2 rounded-xl bg-gray-100 text-gray-600 hover:bg-red-50 hover:text-red-500 transition-all duration-300"
                title="Delete post"
              >
                <TrashIcon class="h-5 w-5" />
              </button>
            </div>
          </div>

          <!-- Post Title -->
          <h3 class="text-xl font-bold text-gray-800 mb-3">{{ post.title }}</h3>

          <!-- Post Content Preview -->
          <p class="text-gray-600 mb-5 leading-relaxed line-clamp-3">{{ post.content }}</p>

          <!-- Category Tag -->
          <div class="flex items-center justify-between mb-5">
            <span
              :class="[
                'px-4 py-1.5 text-xs font-bold rounded-full shadow-sm',
                getCategoryColor(post.category)
              ]"
            >
              {{ post.category }}
            </span>
          </div>

          <!-- Post Actions -->
          <div class="flex items-center justify-between pt-5 border-t border-gray-100">
            <div class="flex items-center space-x-3">
              <!-- Like Button -->
              <button
                @click="toggleLike(post)"
                :class="[
                  'flex items-center space-x-2 px-5 py-2.5 rounded-2xl transition-all duration-300',
                  post.liked
                    ? 'bg-gradient-to-r from-red-500 to-pink-500 text-white shadow-lg shadow-red-500/30'
                    : 'bg-gray-100 text-gray-600 hover:bg-red-50 hover:text-red-500'
                ]"
              >
                <HeartIcon :class="['h-5 w-5', post.liked ? 'fill-current animate-pulse' : '']" />
                <span class="font-semibold">{{ post.likes }}</span>
              </button>

              <!-- Comment Button -->
              <button 
                @click="toggleComments(post)"
                class="flex items-center space-x-2 px-5 py-2.5 rounded-2xl bg-gray-100 text-gray-600 hover:bg-blue-50 hover:text-blue-600 transition-all duration-300"
              >
                <ChatBubbleLeftRightIcon class="h-5 w-5" />
                <span class="font-semibold">{{ post.comments }}</span>
              </button>

              <!-- Pin/Unpin Button -->
              <button
                @click="togglePin(post)"
                :class="[
                  'flex items-center space-x-2 px-5 py-2.5 rounded-2xl transition-all duration-300',
                  post.is_pinned
                    ? 'bg-gradient-to-r from-amber-500 to-orange-500 text-white shadow-lg shadow-amber-500/30'
                    : 'bg-gray-100 text-gray-600 hover:bg-amber-50 hover:text-amber-500'
                ]"
              >
                <MapPinIcon class="h-5 w-5" />
                <span class="font-semibold">{{ post.is_pinned ? 'Unpin' : 'Pin' }}</span>
              </button>
            </div>
          </div>

          <!-- Comments Section -->
          <div v-if="post.showComments" class="mt-6 pt-6 border-t border-gray-100">
            <!-- Existing Comments -->
            <div v-if="post.commentsList && post.commentsList.length > 0" class="space-y-4 mb-4">
              <div 
                v-for="comment in post.commentsList" 
                :key="comment.id"
                class="flex items-start space-x-3 p-4 bg-gradient-to-r from-gray-50 to-white rounded-2xl"
              >
                <div class="h-10 w-10 rounded-xl overflow-hidden border-2 border-gray-200 flex-shrink-0">
                  <img 
                    :src="getProfileImage(comment.profile_image, comment.username)" 
                    :alt="comment.username"
                    class="w-full h-full object-cover"
                    @error="handleImageError"
                  />
                </div>
                <div class="flex-1">
                  <div class="flex items-center space-x-2 mb-1">
                    <span class="font-semibold text-gray-800">{{ comment.username }}</span>
                    <span
                      :class="[
                        'px-2 py-0.5 text-xs font-semibold rounded-full',
                        comment.user_role === 'teacher'
                          ? 'bg-purple-100 text-purple-700'
                          : 'bg-blue-100 text-blue-700'
                      ]"
                    >
                      {{ comment.user_role === 'teacher' ? 'Teacher' : 'Student' }}
                    </span>
                    <span class="text-xs text-gray-400">{{ formatDate(comment.created_at) }}</span>
                  </div>
                  <p class="text-gray-600">{{ comment.content }}</p>
                </div>
              </div>
            </div>
            <div v-else-if="!post.loadingComments" class="text-center py-4 text-gray-500">
              No comments yet.
            </div>

            <!-- Add Comment Form -->
            <div class="flex items-center space-x-3">
              <div class="h-10 w-10 rounded-xl overflow-hidden border-2 border-indigo-400 flex-shrink-0">
                <img 
                  :src="adminProfileImage" 
                  alt="Admin"
                  class="w-full h-full object-cover"
                  @error="handleImageError"
                />
              </div>
              <div class="flex-1 flex items-center space-x-2">
                <input
                  v-model="post.newComment"
                  type="text"
                  placeholder="Write a comment as admin..."
                  class="flex-1 px-4 py-2.5 bg-gray-100 border-2 border-transparent rounded-xl focus:outline-none focus:border-indigo-400 focus:bg-white transition-all duration-300"
                  @keyup.enter="submitComment(post)"
                />
                <button
                  @click="submitComment(post)"
                  :disabled="!post.newComment?.trim()"
                  class="px-4 py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-semibold hover:shadow-lg hover:shadow-indigo-500/30 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300"
                >
                  <PaperAirplaneIcon class="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Post Modal -->
    <div v-if="showEditModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <!-- Backdrop -->
      <div class="absolute inset-0 bg-black/60 backdrop-blur-md" @click="closeModal"></div>

      <!-- Modal Content -->
      <div class="relative bg-white rounded-3xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto animate-scale-in">
        <!-- Modal Header -->
        <div class="sticky top-0 bg-white rounded-t-3xl border-b border-gray-100 p-6">
          <div class="flex items-center justify-between">
            <h2 class="text-2xl font-bold text-gray-800">✏️ Edit Post</h2>
            <button
              @click="closeModal"
              class="p-2 rounded-xl hover:bg-gray-100 transition-colors"
            >
              <XMarkIcon class="h-6 w-6 text-gray-500" />
            </button>
          </div>
        </div>

        <!-- Modal Body -->
        <form @submit.prevent="submitEdit" class="p-6 space-y-6">
          <!-- Title Field -->
          <div>
            <label class="block text-sm font-bold text-gray-700 mb-2">Title</label>
            <input
              v-model="editPostData.title"
              type="text"
              class="w-full px-4 py-3.5 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-indigo-400 focus:ring-4 focus:ring-indigo-100"
            />
          </div>

          <!-- Category Dropdown -->
          <div>
            <label class="block text-sm font-bold text-gray-700 mb-2">Category</label>
            <div class="relative">
              <select
                v-model="editPostData.category"
                class="w-full appearance-none px-4 py-3.5 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-indigo-400 focus:ring-4 focus:ring-indigo-100 cursor-pointer"
              >
                <option value="Q&A">❓ Q&A</option>
                <option value="Study Tips">📚 Study Tips</option>
                <option value="Exam Advice">📝 Exam Advice</option>
                <option value="Motivation">💪 Motivation</option>
                <option value="Stress">🧘 Stress</option>
                <option value="Announcement">📢 Announcement</option>
                <option value="Class Management">👥 Class Management</option>
                <option value="General">💬 General</option>
              </select>
              <ChevronDownIcon class="absolute right-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400 pointer-events-none" />
            </div>
          </div>

          <!-- Content Textarea -->
          <div>
            <label class="block text-sm font-bold text-gray-700 mb-2">Content</label>
            <textarea
              v-model="editPostData.content"
              rows="8"
              class="w-full px-4 py-3.5 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-indigo-400 focus:ring-4 focus:ring-indigo-100 resize-none"
            ></textarea>
          </div>

          <!-- Submit Button -->
          <div class="flex justify-end space-x-4 pt-4">
            <button
              type="button"
              @click="closeModal"
              class="px-6 py-3 bg-gray-100 text-gray-700 rounded-xl font-semibold hover:bg-gray-200 transition-all duration-300"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-8 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl hover:shadow-indigo-500/30 hover:scale-105 transition-all duration-300"
            >
              💾 Save Changes
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import forumService from '../../services/forumService.js';
import {
  MagnifyingGlassIcon,
  ChevronDownIcon,
  ArrowPathIcon,
  ArrowLeftIcon,
  HeartIcon,
  ChatBubbleLeftRightIcon,
  MapPinIcon,
  TrashIcon,
  XMarkIcon,
  PencilSquareIcon,
  PaperAirplaneIcon,
  DocumentTextIcon,
  AcademicCapIcon,
  UserGroupIcon
} from '@heroicons/vue/24/outline';

export default {
  name: 'AdminManageForum',
  components: {
    MagnifyingGlassIcon,
    ChevronDownIcon,
    ArrowPathIcon,
    ArrowLeftIcon,
    HeartIcon,
    ChatBubbleLeftRightIcon,
    MapPinIcon,
    TrashIcon,
    XMarkIcon,
    PencilSquareIcon,
    PaperAirplaneIcon,
    DocumentTextIcon,
    AcademicCapIcon,
    UserGroupIcon
  },
  data() {
    return {
      adminName: '',
      adminId: null,
      adminRole: 'admin',
      isAuthenticated: false,
      
      searchQuery: '',
      selectedFilter: 'latest',
      showEditModal: false,
      editingPostId: null,
      loading: false,
      
      editPostData: {
        title: '',
        category: '',
        content: ''
      },

      posts: [],
      stats: {
        totalPosts: 0,
        totalComments: 0,
        teacherPosts: 0,
        studentPosts: 0
      },
      adminProfileImage: ''
    };
  },
  computed: {
    filteredPosts() {
      let result = [...this.posts];
      
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(post =>
          post.title.toLowerCase().includes(query) ||
          post.content.toLowerCase().includes(query) ||
          post.username.toLowerCase().includes(query)
        );
      }

      switch (this.selectedFilter) {
        case 'latest':
          result.sort((a, b) => new Date(b.date) - new Date(a.date));
          break;
        case 'oldest':
          result.sort((a, b) => new Date(a.date) - new Date(b.date));
          break;
        case 'most_liked':
          result.sort((a, b) => b.likes - a.likes);
          break;
        case 'most_commented':
          result.sort((a, b) => b.comments - a.comments);
          break;
        case 'teachers':
          result = result.filter(post => post.user_role === 'teacher');
          break;
        case 'students':
          result = result.filter(post => post.user_role === 'student');
          break;
      }

      return result;
    }
  },
  methods: {
    // Check admin authentication on mount
    checkAuthentication() {
      const adminToken = sessionStorage.getItem('admin_token');
      const adminUser = sessionStorage.getItem('admin_user');
      
      if (!adminToken || !adminUser) {
        console.log('❌ No admin session - redirecting to login')
        this.$router.push('/admin_login');
        return false;
      }
      
      try {
        const user = JSON.parse(adminUser);
        this.adminName = user.full_name || user.username || user.email?.split('@')[0] || 'Admin';
        // admin_id is now stored in sessionStorage by AdminLogin
        this.adminId = user.admin_id;
        this.isAuthenticated = true;
        console.log('✅ Admin authenticated:', this.adminName, 'ID:', this.adminId);
        return true;
      } catch (error) {
        console.error('❌ Error parsing admin user:', error);
        sessionStorage.removeItem('admin_token');
        sessionStorage.removeItem('admin_user');
        this.$router.push('/admin_login');
        return false;
      }
    },
    
    goBack() {
      this.$router.push('/admin_dashboard');
    },
    getProfileImage(profileImage, username) {
      if (profileImage && profileImage.startsWith('http')) {
        return profileImage;
      }
      if (profileImage) {
        return `http://127.0.0.1:8000/${profileImage}`;
      }
      return `https://api.dicebear.com/7.x/avataaars/svg?seed=${username}&backgroundColor=e0e7ff`;
    },
    handleImageError(event) {
      event.target.src = `https://api.dicebear.com/7.x/avataaars/svg?seed=${Math.random()}&backgroundColor=e0e7ff`;
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
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    },
    getCategoryColor(category) {
      const colors = {
        'Q&A': 'bg-gradient-to-r from-blue-100 to-cyan-100 text-blue-700',
        'Study Tips': 'bg-gradient-to-r from-green-100 to-emerald-100 text-green-700',
        'Exam Advice': 'bg-gradient-to-r from-purple-100 to-pink-100 text-purple-700',
        'Motivation': 'bg-gradient-to-r from-amber-100 to-orange-100 text-amber-700',
        'Stress': 'bg-gradient-to-r from-red-100 to-rose-100 text-red-700',
        'Announcement': 'bg-gradient-to-r from-red-100 to-orange-100 text-red-700',
        'Class Management': 'bg-gradient-to-r from-purple-100 to-pink-100 text-purple-700',
        'General': 'bg-gradient-to-r from-gray-100 to-slate-100 text-gray-700'
      };
      return colors[category] || 'bg-gradient-to-r from-gray-100 to-slate-100 text-gray-700';
    },
    async toggleLike(post) {
      if (this.adminId) {
        const result = await forumService.toggleLike(post.id, this.adminId);
        if (result) {
          post.likes = result.likes_count;
          post.liked = result.is_liked;
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
      if (!post.newComment?.trim() || !this.adminId) return;
      
      const comment = await forumService.createComment(post.id, post.newComment, this.adminId, this.adminRole);
      if (comment) {
        if (!post.commentsList) post.commentsList = [];
        post.commentsList.unshift({
          id: comment.id,
          username: this.adminName,
          user_role: this.adminRole,
          profile_image: this.adminProfileImage,
          content: comment.content,
          created_at: comment.created_at
        });
        post.comments = (post.comments || 0) + 1;
        post.newComment = '';
        this.stats.totalComments++;
      }
    },
    async togglePin(post) {
      const newPinState = !post.is_pinned;
      const result = await forumService.togglePin(post.id, newPinState, 'admin');
      if (result) {
        post.is_pinned = newPinState;
      }
    },
    editPost(post) {
      this.editingPostId = post.id;
      this.editPostData = {
        title: post.title,
        category: post.category,
        content: post.content
      };
      this.showEditModal = true;
    },
    async deletePost(post) {
      if (confirm(`Are you sure you want to delete this post by ${post.username}? This action cannot be undone.`)) {
        const success = await forumService.deletePost(post.id, this.adminId, 'admin');
        if (success) {
          const index = this.posts.findIndex(p => p.id === post.id);
          if (index > -1) {
            this.posts.splice(index, 1);
            this.stats.totalPosts--;
          }
        }
      }
    },
    async loadPosts() {
      this.loading = true;
      try {
        const posts = await forumService.getPosts(
          'latest',
          null,
          this.searchQuery,
          this.adminId
        );
        
        this.posts = posts.map(post => ({
          id: post.id,
          user_id: post.user_id,
          username: post.username,
          user_role: post.user_role,
          profile_image: post.profile_image,
          title: post.title,
          content: post.content,
          category: post.category,
          date: post.created_at,
          likes: post.likes_count,
          comments: post.comments_count,
          liked: post.is_liked,
          is_pinned: post.is_pinned,
          showComments: false,
          commentsList: null,
          newComment: '',
          loadingComments: false
        }));

        // Calculate stats
        this.stats.totalPosts = this.posts.length;
        this.stats.totalComments = this.posts.reduce((sum, p) => sum + p.comments, 0);
        this.stats.teacherPosts = this.posts.filter(p => p.user_role === 'teacher').length;
        this.stats.studentPosts = this.posts.filter(p => p.user_role === 'student').length;
      } catch (error) {
        console.error('Error loading posts:', error);
      } finally {
        this.loading = false;
      }
    },
    onSearchChange() {
      this.loadPosts();
    },
    onFilterChange() {
      this.loadPosts();
    },
    async submitEdit() {
      const postData = {
        title: this.editPostData.title,
        content: this.editPostData.content,
        category: this.editPostData.category
      };

      const updated = await forumService.updatePost(this.editingPostId, postData, this.adminId, 'admin');
      if (updated) {
        await this.loadPosts();
      }
      
      this.closeModal();
    },
    closeModal() {
      this.showEditModal = false;
      this.editingPostId = null;
      this.editPostData = { title: '', category: '', content: '' };
    }
  },
  async mounted() {
    // First check authentication before loading anything
    const isAuth = this.checkAuthentication();
    if (!isAuth) {
      return; // Will redirect to login
    }
    
    // Load admin profile using sessionStorage
    const adminUser = sessionStorage.getItem('admin_user');
    if (adminUser) {
      try {
        const user = JSON.parse(adminUser);
        const userProfile = user.profile_photo;
        this.adminProfileImage = userProfile 
          ? `http://127.0.0.1:8000/${userProfile}` 
          : `https://api.dicebear.com/7.x/avataaars/svg?seed=${this.adminName}&backgroundColor=e0e7ff`;
      } catch (error) {
        this.adminProfileImage = `https://api.dicebear.com/7.x/avataaars/svg?seed=${this.adminName}&backgroundColor=e0e7ff`;
      }
    } else {
      this.adminProfileImage = `https://api.dicebear.com/7.x/avataaars/svg?seed=${this.adminName}&backgroundColor=e0e7ff`;
    }
    
    await this.loadPosts();
  }
};
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
* {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-track {
  background: linear-gradient(to bottom, #f8fafc, #e2e8f0);
  border-radius: 10px;
}
::-webkit-scrollbar-thumb {
  background: linear-gradient(to bottom, #6366f1, #8b5cf6);
  border-radius: 10px;
}
@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
.animate-scale-in {
  animation: scaleIn 0.3s ease-out;
}
</style>
