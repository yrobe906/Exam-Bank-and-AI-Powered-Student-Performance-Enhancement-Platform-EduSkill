<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-gray-50 to-slate-100 text-slate-900">
    <!-- Animated Background - Light version -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-0 left-1/4 w-96 h-96 bg-indigo-100 rounded-full blur-3xl animate-pulse"></div>
      <div class="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-100 rounded-full blur-3xl animate-pulse delay-1000"></div>
      <div class="absolute inset-0 bg-[linear-gradient(rgba(0,0,0,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(0,0,0,0.02)_1px,transparent_1px)] bg-[size:50px_50px]"></div>
    </div>

    <!-- EduSkillHeader -->
    <EduskillHeader>
      <p>Admin - Add Note</p>
    </EduskillHeader>
    
    <!-- Header -->
    <header class="relative pt-4 pb-8 text-center px-6 z-10">
      <div class="max-w-4xl mx-auto">
        <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-indigo-100 text-indigo-700 text-sm font-medium mb-6 border border-indigo-200">
          <span class="w-2 h-2 bg-indigo-500 rounded-full animate-pulse"></span>
          <span>Admin Access</span>
        </div>
        <h1 class="text-5xl md:text-6xl font-bold mb-4 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
          Add Study Notes
        </h1>
        <p class="text-xl text-slate-600">Create and manage learning notes for students</p>
      </div>
    </header>

    <!-- Main Form -->
    <section class="relative max-w-7xl mx-auto px-6 pb-16 z-10">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <!-- Left Panel - Add Note Form -->
        <div class="lg:col-span-7">
          <div class="bg-white rounded-2xl p-8 border border-slate-200 shadow-xl">
            <div class="flex items-center gap-3 mb-6">
              <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-md">
                <DocumentTextIcon class="w-6 h-6 text-white" />
              </div>
              <div>
                <h2 class="text-2xl font-bold text-slate-800">Add New Note</h2>
                <p class="text-slate-500 text-sm">Create engaging learning notes</p>
              </div>
            </div>

            <!-- Form Fields -->
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium mb-2 text-indigo-700">Note Title *</label>
                <input v-model="form.title" type="text" placeholder="Enter note title..." 
                  class="w-full px-4 py-3 rounded-xl border border-slate-200 bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 outline-none transition text-slate-800 placeholder-slate-400">
              </div>

              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium mb-2 text-indigo-700">Subject *</label>
                  <select v-model="form.subject" 
                    class="w-full px-4 py-3 rounded-xl border border-slate-200 bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 outline-none transition text-slate-800">
                    <option value="" class="text-slate-500">Select Subject</option>
                    <option v-for="subj in subjects" :key="subj" :value="subj">{{ subj }}</option>
                  </select>
                </div>
                <div>
                  <label class="block text-sm font-medium mb-2 text-indigo-700">Category *</label>
                  <select v-model="form.category" 
                    class="w-full px-4 py-3 rounded-xl border border-slate-200 bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 outline-none transition text-slate-800">
                    <option value="" class="text-slate-500">Select Category</option>
                    <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
                  </select>
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium mb-2 text-indigo-700">Note Content *</label>
                <textarea v-model="form.content" rows="6" placeholder="Enter note content..." 
                  class="w-full px-4 py-3 rounded-xl border border-slate-200 bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 outline-none transition text-slate-800 placeholder-slate-400 resize-none"></textarea>
              </div>

              <!-- Access Type - Only show for admin role -->
              <div v-if="showAccessType">
                <label class="block text-sm font-medium mb-3 text-indigo-700">Access Type</label>
                <div class="grid grid-cols-2 gap-3">
                  <button @click="form.access_type = 'free'" 
                    :class="[
                      'p-4 rounded-xl border-2 transition-all duration-300 text-center hover:scale-105',
                      form.access_type === 'free' 
                        ? 'border-teal-500 bg-teal-50 text-teal-700' 
                        : 'border-slate-200 bg-white hover:border-slate-300 text-slate-600'
                    ]">
                    <LockOpenIcon class="w-6 h-6 mx-auto mb-2 text-teal-600" />
                    <span class="text-sm font-medium">Free</span>
                  </button>
                  <button @click="form.access_type = 'premium'" 
                    :class="[
                      'p-4 rounded-xl border-2 transition-all duration-300 text-center hover:scale-105',
                      form.access_type === 'premium' 
                        ? 'border-amber-500 bg-amber-50 text-amber-700' 
                        : 'border-slate-200 bg-white hover:border-slate-300 text-slate-600'
                    ]">
                    <LockClosedIcon class="w-6 h-6 mx-auto mb-2 text-amber-600" />
                    <span class="text-sm font-medium">Premium</span>
                  </button>
                </div>
              </div>

              <!-- Price Input -->
              <div v-if="form.access_type === 'premium'">
                <label class="block text-sm font-medium mb-2 text-amber-700">Subscription Price (Birr) *</label>
                <input v-model.number="form.price" type="number" min="1" placeholder="200" 
                  class="w-full px-4 py-3 rounded-xl border border-amber-200 bg-amber-50 focus:border-amber-400 focus:ring-2 focus:ring-amber-100 outline-none transition text-slate-800 placeholder-amber-400">
              </div>

              <!-- Cover Color Theme -->
              <div>
                <label class="block text-sm font-medium mb-2 text-indigo-700">Cover Color Theme</label>
                <select v-model="form.theme_color" 
                  class="w-full px-4 py-3 rounded-xl border border-slate-200 bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 outline-none transition text-slate-800">
                  <option value="blue">Blue</option>
                  <option value="purple">Purple</option>
                  <option value="emerald">Emerald</option>
                  <option value="orange">Orange</option>
                  <option value="rose">Rose</option>
                </select>
              </div>

              <!-- Font Style -->
              <div>
                <label class="block text-sm font-medium mb-2 text-indigo-700">Font Style</label>
                <select v-model="form.font_style" 
                  class="w-full px-4 py-3 rounded-xl border border-slate-200 bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 outline-none transition text-slate-800">
                  <option value="sans-serif">Sans-serif</option>
                  <option value="serif">Serif</option>
                  <option value="monospace">Monospace</option>
                </select>
              </div>

              <div class="flex gap-3 pt-2">
                <button @click="saveNote" :disabled="isSubmitting" 
                  class="flex-1 py-3 text-white font-medium rounded-xl transition-all duration-300 flex items-center justify-center gap-2 hover:shadow-lg disabled:opacity-70 bg-gradient-to-r from-indigo-600 to-purple-600">
                  <span v-if="isSubmitting" class="flex items-center gap-2">
                    <ArrowPathIcon class="w-5 h-5 animate-spin" />Saving...</span>
                  <span v-else>Save Note</span>
                </button>
                <button @click="resetForm" :disabled="isSubmitting" 
                  class="px-6 py-3 border-2 border-slate-300 text-slate-600 font-medium rounded-xl hover:bg-slate-50 transition disabled:opacity-50">
                  Reset
                </button>
                <button @click="$router.push('/admin_dashboard')" :disabled="isSubmitting" 
                  class="px-6 py-3 border-2 border-slate-300 text-slate-600 font-medium rounded-xl hover:bg-slate-50 transition disabled:opacity-50">
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Panel - Notes List -->
        <div class="lg:col-span-5">
          <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-xl">
            <div class="flex items-center justify-between mb-6">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-md">
                  <DocumentTextIcon class="w-5 h-5 text-white" />
                </div>
                <div>
                  <h2 class="text-xl font-bold text-slate-800">Notes Collection</h2>
                  <p class="text-slate-500 text-sm">{{ notes.length }} study notes</p>
                </div>
              </div>
              <button @click="fetchNotes" class="p-2 hover:bg-slate-100 rounded-lg transition">
                <ArrowPathIcon class="w-5 h-5 text-indigo-500" :class="{ 'animate-spin': isFetching }" />
              </button>
            </div>

            <!-- Notes List -->
            <div class="space-y-3 max-h-[600px] overflow-y-auto pr-2 custom-scrollbar">
              <div v-if="isFetching" class="text-center py-8">
                <ArrowPathIcon class="w-8 h-8 animate-spin text-indigo-500 mx-auto mb-3" />
                <p class="text-slate-500">Loading notes...</p>
              </div>
              <div v-else-if="notes.length === 0" class="text-center py-8">
                <DocumentTextIcon class="w-12 h-12 text-slate-300 mx-auto mb-3" />
                <p class="text-slate-500">No notes found</p>
              </div>
              <div v-for="note in notes" :key="note.id" 
                class="bg-slate-50 rounded-xl p-4 hover:bg-slate-100 transition border border-slate-200">
                <div class="flex items-start justify-between mb-2">
                  <div class="flex-1">
                    <h3 class="font-semibold text-slate-800 text-sm mb-1">{{ note.title }}</h3>
                    <div class="flex items-center gap-2 mb-2">
                      <span class="text-xs text-slate-500">{{ note.subject }}</span>
                      <span class="text-xs text-slate-300">•</span>
                      <span class="text-xs text-slate-500">{{ note.category }}</span>
                    </div>
                    <span :class="note.access_type === 'free' ? 'bg-teal-100 text-teal-700' : 'bg-amber-100 text-amber-700'" 
                      class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium">
                      {{ note.access_type === 'free' ? 'Free' : `Premium - ${note.price} Birr` }}
                    </span>
                  </div>
                  <div class="flex gap-1">
                    <button @click="editNote(note)" class="p-2 hover:bg-indigo-100 text-indigo-600 rounded-lg transition" title="Edit">
                      <PencilIcon class="w-4 h-4" />
                    </button>
                    <button @click="confirmDelete(note)" class="p-2 hover:bg-red-100 text-red-500 rounded-lg transition" title="Delete">
                      <TrashIcon class="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl border border-slate-200">
        <h3 class="text-xl font-bold text-slate-800 mb-4">Edit Note</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-2 text-indigo-700">Access Type</label>
            <div class="grid grid-cols-2 gap-2">
              <button @click="editForm.access_type = 'free'" 
                :class="['p-3 rounded-xl border-2 transition text-center', editForm.access_type === 'free' ? 'border-teal-500 bg-teal-50 text-teal-700' : 'border-slate-200 text-slate-600']">
                <LockOpenIcon class="w-5 h-5 mx-auto mb-1" />
                <span class="text-sm">Free</span>
              </button>
              <button @click="editForm.access_type = 'premium'" 
                :class="['p-3 rounded-xl border-2 transition text-center', editForm.access_type === 'premium' ? 'border-amber-500 bg-amber-50 text-amber-700' : 'border-slate-200 text-slate-600']">
                <LockClosedIcon class="w-5 h-5 mx-auto mb-1" />
                <span class="text-sm">Premium</span>
              </button>
            </div>
          </div>
          <div v-if="editForm.access_type === 'premium'">
            <label class="block text-sm font-medium mb-2 text-amber-700">Price (Birr)</label>
            <input v-model.number="editForm.price" type="number" min="1"
              class="w-full px-4 py-2 rounded-xl border border-amber-200 bg-amber-50 focus:border-amber-400 focus:ring-2 focus:ring-amber-100 outline-none text-slate-800">
          </div>
          <div>
            <label class="block text-sm font-medium mb-2 text-indigo-700">Subject</label>
            <select v-model="editForm.subject" 
              class="w-full px-4 py-2 rounded-xl border border-slate-200 bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 outline-none text-slate-800">
              <option v-for="subj in subjects" :key="subj" :value="subj">{{ subj }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium mb-2 text-indigo-700">Category</label>
            <select v-model="editForm.category" 
              class="w-full px-4 py-2 rounded-xl border border-slate-200 bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 outline-none text-slate-800">
              <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
            </select>
          </div>
        </div>
        <div class="flex gap-3 mt-6">
          <button @click="saveEdit" class="flex-1 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl hover:shadow-lg transition">
            Save Changes
          </button>
          <button @click="showEditModal = false" class="px-4 py-2 border-2 border-slate-300 text-slate-600 rounded-xl hover:bg-slate-50 transition">
            Cancel
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl border border-slate-200">
        <div class="text-center">
          <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <TrashIcon class="w-8 h-8 text-red-500" />
          </div>
          <h3 class="text-xl font-bold text-slate-800 mb-2">Delete Note</h3>
          <p class="text-slate-600 mb-6">Are you sure you want to delete "{{ noteToDelete?.title }}"?</p>
          <div class="flex gap-3">
            <button @click="deleteNote" :disabled="isDeleting"
              class="flex-1 py-2 bg-gradient-to-r from-red-500 to-pink-500 text-white rounded-xl hover:shadow-lg transition disabled:opacity-50">
              <span v-if="isDeleting" class="flex items-center justify-center gap-2">
                <ArrowPathIcon class="w-5 h-5 animate-spin" />Deleting...</span>
              <span v-else>Delete</span>
            </button>
            <button @click="showDeleteModal = false" :disabled="isDeleting"
              class="flex-1 py-2 border-2 border-slate-300 text-slate-600 rounded-xl hover:bg-slate-50 transition disabled:opacity-50">
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Success Toast -->
    <div v-if="showSuccess" 
      class="fixed bottom-6 right-6 text-white px-6 py-4 rounded-xl shadow-xl animate-slide-up flex items-center gap-3 bg-gradient-to-r from-indigo-600 to-purple-600">
      <CheckCircleIcon class="w-6 h-6" />
      <div>
        <p class="font-semibold">Note Added Successfully!</p>
      </div>
    </div>

    <!-- Error Toast -->
    <div v-if="showError" class="fixed bottom-6 right-6 bg-gradient-to-r from-red-500 to-pink-500 text-white px-6 py-4 rounded-xl shadow-xl animate-slide-up flex items-center gap-3">
      <XCircleIcon class="w-6 h-6" />
      <div>
        <p class="font-semibold">Error</p>
        <p class="text-sm opacity-90">{{ errorMessage }}</p>
      </div>
      <button @click="showError = false" class="ml-4 hover:opacity-80">
        <XMarkIcon class="w-5 h-5" />
      </button>
    </div>

    <MainFooter class="mt-20" />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import EduskillHeader from "@/components/Header/EduskillHeader.vue";
import MainFooter from "@/components/Footer/MainFooter.vue";
import { 
  DocumentTextIcon, LockClosedIcon, LockOpenIcon,
  ArrowPathIcon, CheckCircleIcon, XCircleIcon,
  PencilIcon, TrashIcon, XMarkIcon
} from "@heroicons/vue/24/solid";

const router = useRouter();

const subjects = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'English', 'Geography', 'History'];
const categories = ['Chapter Notes', 'Formula Sheet', 'Practice Problems', 'Summary', 'Revision Guide'];

// User role and username detection - check localStorage
const userRole = ref(localStorage.getItem('role') || '');
const username = ref(localStorage.getItem('username') || '');

// Debug: log the role and username on mount
console.log('AdminAddNote - User role from localStorage:', userRole.value);
console.log('AdminAddNote - Username from localStorage:', username.value);

// Computed properties for role-based access
// Access type should be shown when username is 'admin', hidden for teacher role
const isAdmin = computed(() => username.value === 'admin');
const isTeacher = computed(() => userRole.value === 'teacher');
const showAccessType = computed(() => username.value === 'admin');

const form = reactive({
  title: '',
  subject: '',
  category: '',
  content: '',
  access_type: 'free',
  price: 0,
  theme_color: 'blue',
  font_style: 'sans-serif'
});

const notes = ref([]);
const isSubmitting = ref(false);
const isFetching = ref(false);
const showEditModal = ref(false);
const showDeleteModal = ref(false);
const isDeleting = ref(false);
const noteToDelete = ref(null);
const showSuccess = ref(false);
const showError = ref(false);
const errorMessage = ref("");

const editForm = reactive({
  id: null,
  access_type: 'free',
  price: 0,
  subject: '',
  category: ''
});

// API helper to get token based on role (admin from sessionStorage, teacher from localStorage)
const getCleanToken = () => {
  // First try admin_token from sessionStorage
  let token = sessionStorage.getItem('admin_token');
  if (token) {
    token = token.replace(/['"]/g, '').trim();
    return token;
  }
  // Then try token from localStorage (for teachers and other users)
  token = localStorage.getItem('token');
  if (token) {
    token = token.replace(/['"]/g, '').trim();
    return token;
  }
  return null;
};

const fetchNotes = async () => {
  isFetching.value = true;
  try {
    const adminToken = getCleanToken();
    const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const response = await fetch(`${API_BASE_URL}/api/notes/`, {
      headers: adminToken ? { 'Authorization': `Bearer ${adminToken}` } : {}
    });
    if (response.ok) {
      notes.value = await response.json();
    } else {
      showErrorMessage("Failed to fetch notes");
    }
  } catch (error) {
    showErrorMessage(`Network error: ${error.message}`);
  } finally {
    isFetching.value = false;
  }
};


const saveNote = async () => {
  if (!form.title || !form.subject || !form.category || !form.content) {
    showErrorMessage("Please fill all required fields");
    return;
  }
  if (form.access_type === 'premium' && (!form.price || form.price < 1)) {
    showErrorMessage("Please set a valid price for premium notes");
    return;
  }

  isSubmitting.value = true;
  try {
    const adminToken = getCleanToken();
    if (!adminToken) {
      showErrorMessage("Please login first");
      isSubmitting.value = false;
      return;
    }
    
    const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const response = await fetch(`${API_BASE_URL}/api/notes/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${adminToken}`
      },
      body: JSON.stringify(form)
    });
    
    if (response.ok) {
      const newNote = await response.json();
      notes.value.push(newNote);
      resetForm();
      showSuccess.value = true;
      setTimeout(() => showSuccess.value = false, 3000);
    } else {
      const errorData = await response.json().catch(() => ({}));
      showErrorMessage(errorData.detail || "Failed to save note");
    }
  } catch (error) {
    showErrorMessage(`Network error: ${error.message}`);
  } finally {
    isSubmitting.value = false;
  }
};


const editNote = (note) => {
  editForm.id = note.id;
  editForm.access_type = note.access_type;
  editForm.price = note.price;
  editForm.subject = note.subject;
  editForm.category = note.category;
  showEditModal.value = true;
};

const saveEdit = async () => {
  try {
    const adminToken = getCleanToken();
    if (!adminToken) {
      showErrorMessage("Please login first");
      return;
    }
    
    const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const response = await fetch(`${API_BASE_URL}/api/notes/${editForm.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${adminToken}`
      },
      body: JSON.stringify({
        access_type: editForm.access_type,
        price: editForm.price,
        subject: editForm.subject,
        category: editForm.category
      })
    });
    
    if (response.ok) {
      const updatedNote = await response.json();
      const index = notes.value.findIndex(n => n.id === editForm.id);
      if (index !== -1) {
        notes.value[index] = updatedNote;
      }
      showEditModal.value = false;
      showSuccess.value = true;
      setTimeout(() => showSuccess.value = false, 3000);
    } else {
      const errorData = await response.json().catch(() => ({}));
      showErrorMessage(errorData.detail || "Failed to update note");
    }
  } catch (error) {
    showErrorMessage(`Network error: ${error.message}`);
  }
};


const confirmDelete = (note) => {
  noteToDelete.value = note;
  showDeleteModal.value = true;
};

const deleteNote = async () => {
  if (!noteToDelete.value) return;
  isDeleting.value = true;
  try {
    const adminToken = getCleanToken();
    if (!adminToken) {
      showErrorMessage("Please login first");
      isDeleting.value = false;
      return;
    }
    
    const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const response = await fetch(`${API_BASE_URL}/api/notes/${noteToDelete.value.id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${adminToken}`
      }
    });
    
    if (response.ok) {
      notes.value = notes.value.filter(n => n.id !== noteToDelete.value.id);
      showDeleteModal.value = false;
      noteToDelete.value = null;
      showSuccess.value = true;
      setTimeout(() => showSuccess.value = false, 3000);
    } else {
      showErrorMessage("Failed to delete note");
    }
  } catch (error) {
    showErrorMessage(`Network error: ${error.message}`);
  } finally {
    isDeleting.value = false;
  }
};


const resetForm = () => {
  Object.assign(form, {
    title: '',
    subject: '',
    category: '',
    content: '',
    access_type: 'free',
    price: 0,
    theme_color: 'blue',
    font_style: 'sans-serif'
  });
};

const showErrorMessage = (message) => {
  errorMessage.value = message;
  showError.value = true;
  setTimeout(() => showError.value = false, 5000);
};

onMounted(() => {
  fetchNotes();
});
</script>

<style>
.animate-slide-up { animation: slide-up 0.3s ease-out; }
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: #f1f5f9; border-radius: 3px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
@keyframes slide-up { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
</style>