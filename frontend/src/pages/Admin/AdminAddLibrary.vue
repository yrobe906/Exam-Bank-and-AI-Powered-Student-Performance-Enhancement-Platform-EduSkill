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
      <p>Admin - Add Library</p>
    </EduskillHeader>

    <!-- Header -->
    <header class="relative pt-4 pb-8 text-center px-6 z-10">
      <div class="max-w-4xl mx-auto">
        <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-indigo-100 text-indigo-700 text-sm font-medium mb-6 border border-indigo-200">
          <span class="w-2 h-2 bg-indigo-500 rounded-full animate-pulse"></span>
          <span>Admin Access</span>
        </div>
        <h1 class="text-5xl md:text-6xl font-bold mb-4 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
          Digital Library
        </h1>
        <p class="text-xl text-slate-600">Upload educational materials for <span class="text-indigo-600 font-semibold">grades 9-12</span></p>
      </div>
    </header>

    <!-- Main Form -->
    <section class="relative max-w-7xl mx-auto px-6 pb-16 z-10">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <!-- Left Panel - Add Resource Form -->
        <div class="lg:col-span-7">
          <div class="bg-white rounded-2xl p-8 border border-slate-200 shadow-xl">
            
            <div class="flex items-center gap-3 mb-6">
              <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-md">
                <CloudArrowUpIcon class="w-6 h-6 text-white" />
              </div>
              <div>
                <h2 class="text-2xl font-bold text-slate-800">Add New Resource</h2>
                <p class="text-slate-500 text-sm">Create engaging learning materials</p>
              </div>
            </div>

            <!-- Resource Type -->
            <div class="mb-6">
              <label class="block text-sm font-medium mb-3 text-indigo-700">Resource Type *</label>
              <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
                <button v-for="type in resourceTypes" :key="type.id" @click="handleTypeClick(type)"
                  :disabled="isNavigating"
                  :class="[
                    'p-4 rounded-xl border-2 transition-all duration-300 text-center group hover:scale-105 relative overflow-hidden',
                    form.type === type.value
                      ? `border-${type.color.split('-')[1]}-500 bg-${type.color.split('-')[1]}-50 text-${type.color.split('-')[1]}-700`
                      : 'border-slate-200 bg-white hover:border-slate-300 text-slate-600',
                    isNavigating && type.value === 'notes' ? 'opacity-75 cursor-wait' : ''
                  ]">
                  <div v-if="isNavigating && type.value === 'notes'" class="absolute inset-0 flex items-center justify-center bg-white/80 rounded-xl">
                    <ArrowPathIcon class="w-6 h-6 animate-spin text-indigo-500" />
                  </div>
                  <component :is="type.icon" :class="`w-6 h-6 mx-auto mb-2 ${form.type === type.value ? `text-${type.color.split('-')[1]}-600` : 'text-slate-400'} ${isNavigating && type.value === 'notes' ? 'opacity-50' : ''}`" />
                  <span class="text-sm font-medium">{{ type.label }}</span>
                </button>
              </div>
            </div>

            <!-- Premium Toggle - Only show for admin role -->
            <div v-if="showAccessType" class="mb-6">
              <label class="block text-sm font-medium mb-3 text-indigo-700">Access Type</label>
              <div class="grid grid-cols-2 gap-3">
                <button @click="form.isPremium = false" 
                  :class="[
                    'p-4 rounded-xl border-2 transition-all duration-300 text-center hover:scale-105',
                    !form.isPremium 
                      ? 'border-teal-500 bg-teal-50 text-teal-700' 
                      : 'border-slate-200 bg-white hover:border-slate-300 text-slate-600'
                  ]">
                  <LockOpenIcon class="w-6 h-6 mx-auto mb-2 text-teal-600" />
                  <span class="text-sm font-medium">Free</span>
                </button>
                <button @click="form.isPremium = true" 
                  :class="[
                    'p-4 rounded-xl border-2 transition-all duration-300 text-center hover:scale-105',
                    form.isPremium 
                      ? 'border-amber-500 bg-amber-50 text-amber-700' 
                      : 'border-slate-200 bg-white hover:border-slate-300 text-slate-600'
                  ]">
                  <LockClosedIcon class="w-6 h-6 mx-auto mb-2 text-amber-600" />
                  <span class="text-sm font-medium">Premium</span>
                </button>
              </div>
            </div>

            <!-- Form Fields -->
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium mb-2 text-indigo-700">Title *</label>
                <input v-model="form.title" type="text" placeholder="Enter engaging title..." 
                  class="w-full px-4 py-3 rounded-xl border border-slate-200 bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 outline-none transition text-slate-800 placeholder-slate-400">
              </div>

              <div>
                <label class="block text-sm font-medium mb-2 text-indigo-700">Description *</label>
                <textarea v-model="form.description" rows="3" placeholder="Describe the learning content..." 
                  class="w-full px-4 py-3 rounded-xl border border-slate-200 bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 outline-none transition text-slate-800 placeholder-slate-400 resize-none"></textarea>
              </div>

              <div v-if="form.isPremium">
                <label class="block text-sm font-medium mb-2 text-amber-700">Price (ETB) *</label>
                <input v-model.number="form.price" type="number" min="150" step="10" placeholder="150" 
                  class="w-full px-4 py-3 rounded-xl border border-amber-200 bg-amber-50 focus:border-amber-400 focus:ring-2 focus:ring-amber-100 outline-none transition text-slate-800 placeholder-amber-400">
              </div>

              <div>
                <label class="block text-sm font-medium mb-2 text-indigo-700">Main File *</label>
                <div @click="triggerFileUpload" 
                  class="border-2 border-dashed border-slate-300 rounded-xl p-8 text-center cursor-pointer hover:border-indigo-400 hover:bg-indigo-50/50 transition-all">
                  <CloudArrowUpIcon class="w-12 h-12 mx-auto mb-3 text-indigo-400" />
                  <p class="text-slate-600 mb-1"><span class="text-indigo-600 font-semibold">Click to upload</span> or drag and drop</p>
                  <p class="text-sm text-slate-500">{{ getFileTypes(form.type) }} up to 100MB</p>
                  <input ref="fileInput" type="file" @change="handleFileUpload" class="hidden" />
                  <div v-if="uploadedFile" class="mt-4">
                    <div class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-100 border border-indigo-200">
                      <PaperClipIcon class="w-4 h-4 text-indigo-600" />
                      <span class="text-sm text-slate-700">{{ uploadedFile.name }}</span>
                      <button @click.stop="uploadedFile = null" class="text-indigo-500 hover:text-indigo-700"><XMarkIcon class="w-4 h-4" /></button>
                    </div>
                  </div>
                </div>
              </div>

              <div v-if="form.isPremium">
                <label class="block text-sm font-medium mb-2 text-amber-700">Preview File (Optional)</label>
                <div @click="triggerPreviewUpload" 
                  class="border-2 border-dashed border-amber-300 rounded-xl p-6 text-center cursor-pointer hover:border-amber-400 hover:bg-amber-50/50 transition-all">
                  <DocumentDuplicateIcon class="w-10 h-10 mx-auto mb-2 text-amber-500" />
                  <p class="text-slate-600 mb-1">Upload preview/sample</p>
                  <input ref="previewInput" type="file" @change="handlePreviewUpload" class="hidden" />
                  <div v-if="previewFile" class="mt-3">
                    <div class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-amber-100 border border-amber-200">
                      <span class="text-sm text-slate-700">{{ previewFile.name }}</span>
                      <button @click.stop="previewFile = null" class="text-amber-500 hover:text-amber-700"><XMarkIcon class="w-4 h-4" /></button>
                    </div>
                  </div>
                </div>
              </div>

              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium mb-2 text-indigo-700">Grade Level *</label>
                  <select v-model="form.gradeLevel" 
                    class="w-full px-4 py-3 rounded-xl border border-slate-200 bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 outline-none transition text-slate-800">
                    <option value="" class="text-slate-500">Select Grade</option>
                    <option v-for="grade in ['Grade 9', 'Grade 10', 'Grade 11', 'Grade 12']" :key="grade" :value="grade">{{ grade }}</option>
                  </select>
                </div>
                <div>
                  <label class="block text-sm font-medium mb-2 text-indigo-700">Subject *</label>
                  <input v-model="form.subject" type="text" placeholder="e.g., Mathematics" 
                    class="w-full px-4 py-3 rounded-xl border border-slate-200 bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 outline-none transition text-slate-800 placeholder-slate-400">
                </div>
              </div>

              <div class="flex gap-3 pt-2">
                <button @click="submitResource" :disabled="isSubmitting" 
                  class="flex-1 py-3 text-white font-medium rounded-xl transition-all duration-300 flex items-center justify-center gap-2 hover:shadow-lg disabled:opacity-70"
                  :class="form.isPremium ? 'bg-gradient-to-r from-amber-500 to-orange-500' : 'bg-gradient-to-r from-indigo-600 to-purple-600'">
                  <span v-if="isSubmitting" class="flex items-center gap-2">
                    <ArrowPathIcon class="w-5 h-5 animate-spin" />Uploading...</span>
                  <span v-else>{{ form.isPremium ? 'Publish Premium' : 'Publish Free' }}</span>
                </button>
                <button @click="resetForm" :disabled="isSubmitting" 
                  class="px-6 py-3 border-2 border-slate-300 text-slate-600 font-medium rounded-xl hover:bg-slate-50 transition disabled:opacity-50">
                  Reset
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Panel - Library List -->
        <div class="lg:col-span-5">
          <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-xl">
            <div class="flex items-center justify-between mb-6">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-md">
                  <BookOpenIcon class="w-5 h-5 text-white" />
                </div>
                <div>
                  <h2 class="text-xl font-bold text-slate-800">Library Collection</h2>
                  <p class="text-slate-500 text-sm">{{ filteredResources.length }} learning resources</p>
                </div>
              </div>
              <button @click="fetchResources" class="p-2 hover:bg-slate-100 rounded-lg transition">
                <ArrowPathIcon class="w-5 h-5 text-indigo-500" :class="{ 'animate-spin': isFetching }" />
              </button>
            </div>

            <!-- Filters -->
            <div class="space-y-3 mb-4">
              <div class="relative">
                <input v-model="filters.search" type="text" placeholder="Search by title..." 
                  class="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 outline-none transition text-slate-800 placeholder-slate-400">
                <MagnifyingGlassIcon class="w-5 h-5 text-slate-400 absolute left-3 top-3" />
              </div>
              <div class="grid grid-cols-1 gap-2">
                <select v-model="filters.type" class="px-3 py-2 rounded-xl border border-slate-200 bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 outline-none transition text-slate-700 text-sm">
                  <option value="" class="text-slate-500">All Types</option>
                  <option v-for="type in resourceTypes" :key="type.value" :value="type.value">{{ type.label }}</option>
                </select>
              </div>
            </div>

            <!-- Resources List -->
            <div class="space-y-3 max-h-[500px] overflow-y-auto pr-2 custom-scrollbar">
              <div v-if="isFetching" class="text-center py-8">
                <ArrowPathIcon class="w-8 h-8 animate-spin text-indigo-500 mx-auto mb-3" />
                <p class="text-slate-500">Loading resources...</p>
              </div>
              <div v-else-if="filteredResources.length === 0" class="text-center py-8">
                <BookOpenIcon class="w-12 h-12 text-slate-300 mx-auto mb-3" />
                <p class="text-slate-500">No resources found</p>
              </div>
              <div v-for="resource in filteredResources" :key="resource.id" 
                class="bg-slate-50 rounded-xl p-4 hover:bg-slate-100 transition border border-slate-200">
                <div class="flex items-start justify-between mb-2">
                  <div class="flex items-center gap-3">
                    <div :class="getTypeColor(resource.type)" class="w-10 h-10 rounded-lg flex items-center justify-center shadow-sm">
                      <component :is="getTypeIcon(resource.type)" class="w-5 h-5 text-white" />
                    </div>
                    <div>
                      <h3 class="font-semibold text-slate-800 text-sm">{{ resource.title }}</h3>
                      <span :class="resource.is_premium ? 'bg-amber-100 text-amber-700' : 'bg-teal-100 text-teal-700'" 
                        class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium">
                        {{ resource.is_premium ? 'Premium' : 'Free' }}
                      </span>
                    </div>
                  </div>
                  <div class="flex gap-1">
                    <button @click="editResource(resource)" class="p-2 hover:bg-indigo-100 text-indigo-600 rounded-lg transition" title="Edit">
                      <PencilIcon class="w-4 h-4" />
                    </button>
                    <button @click="confirmDelete(resource)" class="p-2 hover:bg-red-100 text-red-500 rounded-lg transition" title="Delete">
                      <TrashIcon class="w-4 h-4" />
                    </button>
                  </div>
                </div>
                <div class="grid grid-cols-2 gap-2 text-xs text-slate-500">
                  <span>{{ resource.subject }}</span>
                  <span>{{ resource.grade_level }}</span>
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
        <h3 class="text-xl font-bold text-slate-800 mb-4">Edit Resource</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-2 text-indigo-700">Access Type</label>
            <div class="grid grid-cols-2 gap-2">
              <button @click="editForm.isPremium = false" 
                :class="['p-3 rounded-xl border-2 transition text-center', !editForm.isPremium ? 'border-teal-500 bg-teal-50 text-teal-700' : 'border-slate-200 text-slate-600']">
                <LockOpenIcon class="w-5 h-5 mx-auto mb-1" />
                <span class="text-sm">Free</span>
              </button>
              <button @click="editForm.isPremium = true" 
                :class="['p-3 rounded-xl border-2 transition text-center', editForm.isPremium ? 'border-amber-500 bg-amber-50 text-amber-700' : 'border-slate-200 text-slate-600']">
                <LockClosedIcon class="w-5 h-5 mx-auto mb-1" />
                <span class="text-sm">Premium</span>
              </button>
            </div>
          </div>
          <div v-if="editForm.isPremium">
            <label class="block text-sm font-medium mb-2 text-amber-700">Price (ETB)</label>
            <input v-model.number="editForm.price" type="number" min="150" step="10"
              class="w-full px-4 py-2 rounded-xl border border-amber-200 bg-amber-50 focus:border-amber-400 focus:ring-2 focus:ring-amber-100 outline-none text-slate-800">
          </div>
          <div>
            <label class="block text-sm font-medium mb-2 text-indigo-700">Grade Level</label>
            <select v-model="editForm.grade_level" 
              class="w-full px-4 py-2 rounded-xl border border-slate-200 bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 outline-none text-slate-800">
              <option v-for="grade in ['Grade 9', 'Grade 10', 'Grade 11', 'Grade 12']" :key="grade" :value="grade">{{ grade }}</option>
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
          <h3 class="text-xl font-bold text-slate-800 mb-2">Delete Resource</h3>
          <p class="text-slate-600 mb-6">Are you sure you want to delete "{{ resourceToDelete?.title }}"?</p>
          <div class="flex gap-3">
            <button @click="deleteResource" :disabled="isDeleting"
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
      class="fixed bottom-6 right-6 text-white px-6 py-4 rounded-xl shadow-xl animate-slide-up flex items-center gap-3 z-50"
      :class="form.isPremium ? 'bg-gradient-to-r from-amber-500 to-orange-500' : 'bg-gradient-to-r from-indigo-600 to-purple-600'">
      <CheckCircleIcon class="w-6 h-6" />
      <div>
        <p class="font-semibold">{{ form.isPremium ? 'Premium Resource Added!' : 'Free Resource Added!' }}</p>
      </div>
    </div>

    <!-- Error Toast -->
    <div v-if="showError" class="fixed bottom-6 right-6 bg-gradient-to-r from-red-500 to-pink-500 text-white px-6 py-4 rounded-xl shadow-xl animate-slide-up flex items-center gap-3 z-50">
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
  BookOpenIcon, PresentationChartBarIcon, VideoCameraIcon, 
  AcademicCapIcon, CloudArrowUpIcon, PaperClipIcon,
  XMarkIcon, CheckCircleIcon, DocumentIcon,
  LockClosedIcon, LockOpenIcon, DocumentDuplicateIcon,
  ArrowPathIcon, XCircleIcon, MagnifyingGlassIcon,
  PencilIcon, TrashIcon
} from "@heroicons/vue/24/solid";

const router = useRouter();

// State
const fileInput = ref(null);
const previewInput = ref(null);
const uploadedFile = ref(null);
const previewFile = ref(null);
const showSuccess = ref(false);
const showError = ref(false);
const errorMessage = ref("");
const isNavigating = ref(false);
const isSubmitting = ref(false);
const isFetching = ref(false);
const resources = ref([]);
const showEditModal = ref(false);
const showDeleteModal = ref(false);
const isDeleting = ref(false);
const resourceToDelete = ref(null);

// User role detection - check localStorage for role
const userRole = ref(localStorage.getItem('role') || '');

// Computed properties for role-based access
const isAdmin = computed(() => userRole.value === 'admin');
const isTeacher = computed(() => userRole.value === 'teacher');
const showAccessType = computed(() => userRole.value === 'admin');

const editForm = reactive({ id: null, isPremium: false, price: 0, grade_level: "" });
const filters = reactive({ search: "", type: "", accessType: "" });

const resourceTypes = [
  { id: 1, label: "Notes", value: "notes", icon: BookOpenIcon, color: "bg-blue-500" },
  { id: 2, label: "Reference Books&Slides", value: "slides", icon: PresentationChartBarIcon, color: "bg-purple-500" },
  { id: 3, label: "Videos Lesson", value: "videos", icon: VideoCameraIcon, color: "bg-pink-500" },
  { id: 4, label: "Exam Papers and Worksheets", value: "books", icon: AcademicCapIcon, color: "bg-amber-500" },
];

const form = reactive({ type: "", title: "", description: "", subject: "", gradeLevel: "", isPremium: false, price: 0 });

// Computed
const filteredResources = computed(() => {
  return resources.value.filter(resource => {
    if (filters.search && !resource.title.toLowerCase().includes(filters.search.toLowerCase())) return false;
    if (filters.type && resource.type !== filters.type) return false;
    if (filters.accessType) {
      const isPremium = filters.accessType === 'premium';
      if (resource.is_premium !== isPremium) return false;
    }
    return true;
  });
});

// Helpers
const getTypeIcon = (type) => resourceTypes.find(t => t.value === type)?.icon || DocumentIcon;
const getTypeColor = (type) => {
  const colorMap = {
    notes: "bg-gradient-to-br from-blue-500 to-blue-600",
    slides: "bg-gradient-to-br from-purple-500 to-purple-600",
    videos: "bg-gradient-to-br from-pink-500 to-pink-600",
    books: "bg-gradient-to-br from-amber-500 to-amber-600"
  };
  return colorMap[type] || "bg-gradient-to-br from-slate-500 to-slate-600";
};
const getTypeLabel = (type) => resourceTypes.find(t => t.value === type)?.label || "Resource";
const getFileTypes = (type) => ({ notes: "PDF, DOC, DOCX", slides: "PPT, PPTX, PDF", videos: "MP4, AVI", books: "PDF, EPUB" }[type] || "PDF, PPT, MP4");

// API Calls
const fetchResources = async () => {
  isFetching.value = true;
  try {
    const adminToken = getToken();
    if (!adminToken) { showErrorAlert("Please login first"); return; }
    const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    
    // Fetch resources
    const resourcesResponse = await fetch(`${API_BASE_URL}/api/resources/`, { headers: { 'Authorization': `Bearer ${adminToken}` } });
    let allItems = [];
    
    if (resourcesResponse.ok) {
      const resourcesData = await resourcesResponse.json();
      // Convert resources to unified format
      allItems = resourcesData.map(r => ({
        ...r,
        item_type: 'resource'
      }));
    }
    
    // Fetch notes
    try {
      const notesResponse = await fetch(`${API_BASE_URL}/api/notes/all`, { headers: { 'Authorization': `Bearer ${adminToken}` } });
      if (notesResponse.ok) {
        const notesData = await notesResponse.json();
        // Convert notes to unified format
        const notesItems = notesData.map(n => ({
          id: n.id,
          title: n.title,
          subject: n.subject,
          grade_level: n.category,
          type: 'notes',
          is_premium: n.access_type === 'premium',
          price: n.price || 0,
          description: n.content,
          item_type: 'note'
        }));
        allItems = [...allItems, ...notesItems];
      }
    } catch (noteError) {
      console.log("Notes fetch skipped:", noteError);
    }
    
    resources.value = allItems;
  } catch (error) { showErrorAlert(`Network error: ${error.message}`); }
  finally { isFetching.value = false; }
};

// File Handlers
const triggerFileUpload = () => fileInput.value?.click();
const triggerPreviewUpload = () => previewInput.value?.click();
const handleFileUpload = (e) => {
  const file = e.target.files[0];
  if (file && file.size <= 100 * 1024 * 1024) uploadedFile.value = file;
  else showErrorAlert("File size exceeds 100MB limit");
};
const handlePreviewUpload = (e) => {
  const file = e.target.files[0];
  if (file && file.size <= 10 * 1024 * 1024) previewFile.value = file;
  else showErrorAlert("Preview file size exceeds 10MB limit");
};

// Token Helper - Get appropriate token based on role
const getToken = () => {
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

// Submit Resource
const submitResource = async () => {
  if (!form.type) { showErrorAlert("Select resource type"); return; }
  if (!form.title || !form.description || !uploadedFile.value || !form.subject || !form.gradeLevel) { showErrorAlert("Fill all required fields"); return; }
  if (form.isPremium && (!form.price || form.price < 150)) { showErrorAlert("Premium: minimum price is ETB 150"); return; }

  isSubmitting.value = true;
  try {
    const adminToken = getToken();
    if (!adminToken) { showErrorAlert("No authentication token found. Please login first."); isSubmitting.value = false; return; }

    const formData = new FormData();
    formData.append('title', form.title);
    formData.append('description', form.description);
    formData.append('type', form.type);
    formData.append('subject', form.subject);
    formData.append('grade_level', form.gradeLevel);
    formData.append('is_premium', form.isPremium.toString());
    formData.append('price', form.price.toString());
    formData.append('file', uploadedFile.value);
    if (form.isPremium && previewFile.value) formData.append('preview_file', previewFile.value);

    const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const response = await fetch(`${API_BASE_URL}/api/resources/`, { method: 'POST', body: formData, headers: { 'Authorization': `Bearer ${adminToken}` } });

    if (response.ok) {
      showSuccess.value = true;
      await fetchResources();
      resetForm();
      setTimeout(() => showSuccess.value = false, 3000);
    } else {
      const errorData = await response.json().catch(() => ({}));
      showErrorAlert(errorData.detail || "Upload failed");
    }
  } catch (error) { showErrorAlert(`Network error: ${error.message}`); }
  finally { isSubmitting.value = false; }
};

// Edit Resource
const editResource = (resource) => {
  editForm.id = resource.id;
  editForm.isPremium = resource.is_premium;
  editForm.price = resource.price || 0;
  editForm.grade_level = resource.grade_level;
  showEditModal.value = true;
};

const saveEdit = async () => {
  try {
    const adminToken = getToken();
    if (!adminToken) { showErrorAlert("Please login first"); return; }
    const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const formData = new FormData();
    formData.append('is_premium', editForm.isPremium.toString());
    formData.append('price', editForm.isPremium ? editForm.price.toString() : '0');
    formData.append('grade_level', editForm.grade_level);

    const response = await fetch(`${API_BASE_URL}/api/resources/${editForm.id}`, { method: 'PUT', headers: { 'Authorization': `Bearer ${adminToken}` }, body: formData });
    if (response.ok) {
      showEditModal.value = false;
      await fetchResources();
      showSuccess.value = true;
      setTimeout(() => showSuccess.value = false, 3000);
    } else { const errorData = await response.json().catch(() => ({})); showErrorAlert(errorData.detail || "Failed to update"); }
  } catch (error) { showErrorAlert(`Network error: ${error.message}`); }
};

// Delete Resource
const confirmDelete = (resource) => { resourceToDelete.value = resource; showDeleteModal.value = true; };
const deleteResource = async () => {
  if (!resourceToDelete.value) return;
  isDeleting.value = true;
  try {
    const adminToken = getToken();
    if (!adminToken) { showErrorAlert("Please login first"); return; }
    const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const response = await fetch(`${API_BASE_URL}/api/resources/${resourceToDelete.value.id}`, { method: 'DELETE', headers: { 'Authorization': `Bearer ${adminToken}` } });
    if (response.ok) { showDeleteModal.value = false; await fetchResources(); showSuccess.value = true; setTimeout(() => showSuccess.value = false, 3000); }
    else showErrorAlert("Failed to delete resource");
  } catch (error) { showErrorAlert(`Network error: ${error.message}`); }
  finally { isDeleting.value = false; resourceToDelete.value = null; }
};

// Handle resource type click - redirect to dedicated pages for specific types
const handleTypeClick = (type) => {
  if (type.value === 'notes') {
    // Add visual feedback and smooth transition before redirect
    form.type = type.value;
    isNavigating.value = true;
    setTimeout(() => {
      router.push('/admin/add-note');
    }, 600);
  } else {
    // For other types, just set the form type normally
    form.type = type.value;
  }
};

// Utilities
const showErrorAlert = (message) => { errorMessage.value = message; showError.value = true; setTimeout(() => showError.value = false, 5000); };
const resetForm = () => { Object.assign(form, { type: "", title: "", description: "", subject: "", gradeLevel: "", isPremium: false, price: 0 }); uploadedFile.value = null; previewFile.value = null; if (fileInput.value) fileInput.value.value = ""; if (previewInput.value) previewInput.value.value = ""; };

onMounted(() => { fetchResources(); });

</script>

<style>
.animate-slide-up { animation: slide-up 0.3s ease-out; }
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: #f1f5f9; border-radius: 3px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
@keyframes slide-up { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
</style>