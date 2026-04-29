<template>
  <div class="exam-builder">
    <AppHeader />
    <div class="container">
      <!-- Step Indicator -->
      <div class="steps-wrapper">
        <div class="step" :class="{ active: currentStep === 1, completed: currentStep > 1 }">
          <div class="step-number">1</div>
          <div class="step-label">Select Sector</div>
        </div>
        <div class="step-line" :class="{ active: currentStep >= 2 }"></div>
        <div class="step" :class="{ active: currentStep === 2, completed: currentStep > 2 }">
          <div class="step-number">2</div>
          <div class="step-label">Select Exam</div>
        </div>
        <div class="step-line" :class="{ active: currentStep >= 3 }"></div>
        <div class="step" :class="{ active: currentStep === 3 }">
          <div class="step-number">3</div>
          <div class="step-label">Customize Test</div>
        </div>
      </div>

      <!-- Loading Overlay -->
      <div v-if="loading.global" class="loading-overlay">
        <div class="spinner"></div>
        <p>{{ loading.message }}</p>
      </div>

      <div class="content-grid">
        <!-- Left Sidebar -->
        <div class="sidebar">
          <div class="sidebar-card">
            <div class="sidebar-step" :class="{ active: currentStep === 1 }" @click="goToStep(1)">
              <div class="step-indicator">
                <span class="step-badge" :class="{ active: currentStep === 1, completed: currentStep > 1 }">
                  <span v-if="currentStep > 1" class="check">✓</span>
                  <span v-else>1</span>
                </span>
                <div class="step-info">
                  <span class="step-title">Step 1</span>
                  <span class="step-name">Select Sector</span>
                </div>
              </div>
              <span v-if="selectedSector && currentStep > 1" class="selected-value">{{ selectedSector.name }}</span>
            </div>
            <div class="sidebar-step" :class="{ active: currentStep === 2 }" @click="goToStep(2)">
              <div class="step-indicator">
                <span class="step-badge" :class="{ active: currentStep === 2, completed: currentStep > 2 }">
                  <span v-if="currentStep > 2" class="check">✓</span>
                  <span v-else>2</span>
                </span>
                <div class="step-info">
                  <span class="step-title">Step 2</span>
                  <span class="step-name">Select Exam</span>
                </div>
              </div>
              <span v-if="selectedExam && currentStep > 2" class="selected-value">{{ selectedExam.name }}</span>
            </div>
            <div class="sidebar-step" :class="{ active: currentStep === 3 }" @click="goToStep(3)">
              <div class="step-indicator">
                <span class="step-badge" :class="{ active: currentStep === 3 }">3</span>
                <div class="step-info">
                  <span class="step-title">Step 3</span>
                  <span class="step-name">Customize Test</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Main Content Area -->
        <div class="main-content">
          <Transition name="fade-slide" mode="out-in">
            <!-- Step 1: Sector Selection -->
            <div v-if="currentStep === 1" key="step1" class="content-card">
              <h2 class="section-title">Choose Your Sector</h2>
              <div v-if="loading.sectors" class="text-center py-8">
                <div class="spinner-small"></div>
                <p class="mt-2 text-gray-500">Loading sectors...</p>
              </div>
              <div v-else class="sector-grid">
                <SectorCard
                  v-for="sector in sectors"
                  :key="sector.id"
                  :sector="sector"
                  :selected="selectedSector?.id === sector.id"
                  @select="selectedSector = sector"
                />
              </div>
              <transition name="fade">
                <button v-if="selectedSector" @click="loadExams" class="continue-btn" :disabled="loading.exams">
                  {{ loading.exams ? 'Loading Exams...' : 'Continue to Exams' }} 
                  <span class="arrow">→</span>
                </button>
              </transition>
            </div>

            <!-- Step 2: Exam Selection -->
            <div v-else-if="currentStep === 2" key="step2" class="content-card">
              <div class="step-header">
                <h2 class="section-title">Select Exam</h2>
                <div class="step-header-actions">
                  <span class="sector-tag">{{ selectedSector?.name }}</span>
                  <button @click="openAddExamModal" class="btn-add">
                    <span class="plus-icon">+</span> Add Exam
                  </button>
                </div>
              </div>
              <div v-if="loading.exams" class="text-center py-8">
                <div class="spinner-small"></div>
                <p class="mt-2 text-gray-500">Loading exams...</p>
              </div>
              <div v-else-if="filteredExams.length === 0" class="empty-state">
                <p>No exams found for this sector.</p>
                <button @click="openAddExamModal" class="btn-add mt-4">
                  <span class="plus-icon">+</span> Add First Exam
                </button>
              </div>
              <div v-else class="exam-list">
                <div v-for="exam in filteredExams" :key="exam.id"
                     class="exam-item"
                     :class="{ 'exam-selected': selectedExam?.id === exam.id }">
                  <div class="exam-content" @click="selectedExam = exam">
                    <h3 class="exam-name">{{ exam.name }}</h3>
                    <div class="exam-meta">
                      <span class="meta-item">
                        <span class="meta-icon">○</span>
                        {{ exam.total_questions }} Qs
                      </span>
                      <span class="meta-item">
                        <span class="meta-icon">○</span>
                        {{ exam.duration }} min
                      </span>
                      <span class="meta-item" v-if="exam.exam_type">
                        <span class="meta-icon">○</span>
                        {{ exam.exam_type }}
                      </span>
                    </div>
                  </div>
                  <div class="exam-actions">
                    <button @click.stop="openEditExamModal(exam)" class="btn-action btn-edit" title="Edit Exam">
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="action-icon">
                        <path d="M2.695 14.763l-1.262 3.154a.5.5 0 00.65.65l3.155-1.262a4 4 0 001.343-.885L17.5 5.5a2.121 2.121 0 00-3-3L3.58 13.42a4 4 0 00-.885 1.343z" />
                      </svg>
                    </button>
                    <button @click.stop="confirmDeleteExam(exam)" class="btn-action btn-delete" title="Delete Exam">
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="action-icon">
                        <path fill-rule="evenodd" d="M8.75 1A2.75 2.75 0 006 3.75v.443c-.795.077-1.584.176-2.365.298a.75.75 0 10.23 1.482l.149-.022.841 10.518A2.75 2.75 0 007.596 19h4.807a2.75 2.75 0 002.742-2.53l.841-10.519.149.023a.75.75 0 00.23-1.482A41.03 41.03 0 0014 4.193V3.75A2.75 2.75 0 0011.25 1h-2.5zM10 4c.84 0 1.673.025 2.5.075V3.75c0-.69-.56-1.25-1.25-1.25h-2.5c-.69 0-1.25.56-1.25 1.25v.325C8.327 4.025 9.16 4 10 4zM8.58 7.72a.75.75 0 00-1.5.06l.3 7.5a.75.75 0 101.5-.06l-.3-7.5zm4.34.06a.75.75 0 10-1.5-.06l-.3 7.5a.75.75 0 101.5.06l.3-7.5z" clip-rule="evenodd" />
                      </svg>
                    </button>
                    <div v-if="selectedExam?.id === exam.id" class="exam-check">
                      <svg class="check-icon" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                      </svg>
                    </div>
                  </div>
                </div>
              </div>
              <div class="action-buttons">
                <button @click="currentStep = 1" class="btn btn-outline">
                  <span class="arrow-left">←</span> Back
                </button>
                <button v-if="selectedExam" @click="loadSections" class="btn btn-primary" :disabled="loading.sections">
                  {{ loading.sections ? 'Loading Sections...' : 'Customize Test' }} 
                  <span class="arrow">→</span>
                </button>
              </div>
            </div>

            <!-- Step 3: Test Builder -->
            <div v-else key="step3" class="space-y-4">
              <!-- Exam Info Form -->
              <ExamInfoForm
                v-model:grade="testForm.grade"
                v-model:subject="testForm.subject"
                v-model:topic="testForm.topic"
                v-model:title="testForm.title"
                v-model:duration="testForm.duration"
                v-model:examType="testForm.examType"
                v-model:totalMarks="testForm.totalMarks"
                :questions="allQuestions"
                :total-marks="totalMarks"
                @update:grade="handleGradeChange"
                @update:subject="handleSubjectChange"
              />

              <!-- Configuration Card -->
              <div class="content-card">
                <h3 class="card-header">
                  <span class="header-indicator"></span>
                  Test Configuration
                </h3>
                <DifficultySlider v-model="testForm.difficulty" />
                
                <!-- Predefined Subject Sections Selection -->
                <div class="sections-group">
                  <h4 class="group-title">Select Sections</h4>
                  <div class="section-dropdown">
                    <select v-model="selectedSectionName" @change="handleSectionNameChange" class="form-input">
                      <option value="">Select a subject section</option>
                      <option v-for="section in predefinedSections" :key="section" :value="section">
                        {{ section }}
                      </option>
                    </select>
                  </div>
                  <div class="selected-sections mt-3">
                    <div v-for="(sec, index) in customSections" :key="index" class="section-tag">
                      <span>{{ sec.name }}</span>
                      <button @click="removeCustomSection(index)" class="remove-btn">×</button>
                    </div>
                    <button v-if="selectedSectionName && !customSections.find(s => s.name === selectedSectionName)" 
                            @click="addCustomSection" class="add-section-btn">
                      + Add {{ selectedSectionName }}
                    </button>
                  </div>
                </div>
              </div>

              <!-- Question Form with Difficulty -->
              <QuestionForm 
                v-if="selectedExam && (sections.length > 0 || customSections.length > 0)"
                :exam-id="selectedExam.id"
                :section-id="getCurrentSectionId()"
                :max-questions="100"
                @add="addCustomQuestion"
              />

              <!-- Questions Preview -->
              <QuestionsList
                :questions="bankQuestions"
                :custom-questions="customQuestions"
                @remove="removeQuestion"
                @remove-custom="removeCustomQuestion"
              />
            </div>
          </Transition>
        </div>

        <!-- Right Preview Panel -->
        <div class="preview-panel">
          <QuestionPalette
            v-if="currentStep === 3"
            :total-questions="totalQuestions"
            :answered-count="answeredCount"
            :marked-questions="markedQuestions"
            :total-marks="totalMarks"
            :duration="testForm.duration"
            :exam-id="selectedExam?.id"  
          />
        </div>
      </div>

      <!-- Action Buttons -->
      <transition name="fade-up">
        <div v-if="currentStep === 3" class="floating-actions">
          <button @click="saveAsDraft" :disabled="saving" class="btn btn-outline">
            {{ saving ? 'Saving...' : 'Save Draft' }}
          </button>
          <button @click="publishTest" :disabled="saving" class="btn btn-primary">
            {{ saving ? 'Creating...' : 'Create Test' }}
          </button>
        </div>
      </transition>
    </div>

    <!-- Error Modal -->
    <div v-if="error" class="modal-overlay" @click.self="error = null">
      <div class="modal-content error-modal">
        <h3 class="text-red-600 mb-2">Error</h3>
        <p>{{ error }}</p>
        <button @click="error = null" class="btn btn-primary mt-4">OK</button>
      </div>
    </div>

    <!-- Exam Modal (Add/Edit) -->
    <div v-if="examModalOpen" class="modal-overlay" @click.self="closeExamModal">
      <div class="modal-content exam-modal">
        <div class="modal-header">
          <h3>{{ editingExam ? 'Edit Exam' : 'Add New Exam' }}</h3>
          <button @click="closeExamModal" class="modal-close">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="close-icon">
              <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
            </svg>
          </button>
        </div>
        <form @submit.prevent="saveExam" class="exam-form">
          <div class="form-group">
            <label class="form-label">Exam Name *</label>
            <input 
              type="text" 
              v-model="examForm.name" 
              class="form-input" 
              required
              placeholder="Enter exam name"
            />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Total Questions *</label>
              <input 
                type="number" 
                v-model.number="examForm.total_questions" 
                class="form-input" 
                required
                min="1"
                placeholder="e.g., 50"
              />
            </div>
            <div class="form-group">
              <label class="form-label">Duration (minutes) *</label>
              <input 
                type="number" 
                v-model.number="examForm.duration" 
                class="form-input" 
                required
                min="1"
                placeholder="e.g., 60"
              />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Exam Type</label>
              <input 
                type="text" 
                v-model="examForm.exam_type" 
                class="form-input" 
                placeholder="e.g., UAEE, Model Exam"
              />
            </div>
            <div class="form-group">
              <label class="form-label">Total Marks</label>
              <input 
                type="number" 
                v-model.number="examForm.total_marks" 
                class="form-input" 
                min="0"
                placeholder="e.g., 100"
              />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Pricing Type</label>
              <select v-model="examForm.pricing_type" class="form-input" @change="handlePricingTypeChange">
                <option value="Free">Free</option>
                <option value="Premium">Premium</option>
              </select>
            </div>
            <div class="form-group" v-if="examForm.pricing_type === 'Premium'">
              <label class="form-label">Amount (ETB)</label>
              <input 
                type="number" 
                v-model.number="examForm.amount" 
                class="form-input" 
                min="0"
                step="0.01"
                placeholder="e.g., 50.00"
              />
            </div>
            <div class="form-group" v-else>
              <label class="form-label">&nbsp;</label>
              <div class="free-badge">Free Exam</div>
            </div>
          </div>
          <div class="modal-actions">
            <button type="button" @click="closeExamModal" class="btn btn-outline">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary" :disabled="savingExam">
              {{ savingExam ? 'Saving...' : (editingExam ? 'Update Exam' : 'Create Exam') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="deleteModalOpen" class="modal-overlay" @click.self="cancelDelete">
      <div class="modal-content delete-modal">
        <div class="modal-header">
          <h3>Delete Exam</h3>
        </div>
        <p class="delete-message">
          Are you sure you want to delete <strong>"{{ examToDelete?.name }}"</strong>? 
          This action cannot be undone and will also delete all associated sections and questions.
        </p>
        <div class="modal-actions">
          <button @click="cancelDelete" class="btn btn-outline">
            Cancel
          </button>
          <button @click="deleteExam" class="btn btn-danger" :disabled="deletingExam">
            {{ deletingExam ? 'Deleting...' : 'Delete Exam' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import SectorCard from '@/components/cards/SectorCard.vue';
import ExamCard from '@/components/cards/ExamCard.vue';
import SectionCard from '@/components/cards/SectionCard.vue';
import ExamInfoForm from '@/components/forms/ExamInfoForm.vue';
import QuestionForm from '@/components/forms/QuestionForm.vue';
import DifficultySlider from '@/components/forms/DifficultySlider.vue';
import QuestionsList from '@/components/preview/QuestionsList.vue';
import QuestionPalette from '@/components/preview/QuestionPalette.vue';
import api from '@/services/api';

export default {
  name: 'ExamBuilder',
  components: {
    SectorCard,
    ExamCard,
    SectionCard,
    ExamInfoForm,
    QuestionForm,
    DifficultySlider,
    QuestionsList,
    QuestionPalette
  },
  setup() {
    const router = useRouter();
    const currentStep = ref(1);

    // Loading states
    const loading = ref({
      global: false,
      sectors: false,
      exams: false,
      sections: false,
      questions: false
    });
    const saving = ref(false);
    const savingExam = ref(false);
    const deletingExam = ref(false);
    const error = ref(null);

    // Modal states
    const examModalOpen = ref(false);
    const deleteModalOpen = ref(false);
    const editingExam = ref(null);
    const examToDelete = ref(null);

    // Data from API
    const sectors = ref([]);
    const exams = ref([]);
    const sections = ref([]);
    const bankQuestions = ref([]);
    const customQuestions = ref([]);
    const markedQuestions = ref([]);
    const customSections = ref([]);
    const selectedSectionName = ref('');

    // Predefined subject sections
    const predefinedSections = [
      'Biology Section',
      'Chemistry Section', 
      'Physics Section',
      'Mathematics Section',
      'Language Section',
      'History Section',
      'Geography Section',
      'Economics Section',
      'Programming Section'
    ];

    // Selection state
    const selectedSector = ref(null);
    const selectedExam = ref(null);
    const selectedSections = ref([]);

    // Form state
    const testForm = ref({
      grade: '',
      subject: '',
      topic: '',
      title: '',
      duration: 60,
      difficulty: 1,
      questionCount: 10,
      examType: '',
      totalMarks: 0
    });

    // Exam form for modal
    const examForm = ref({
      name: '',
      total_questions: 50,
      duration: 60,
      exam_type: '',
      total_marks: 100,
      pricing_type: 'Free',
      amount: 0
    });

    // Handle pricing type change
    const handlePricingTypeChange = () => {
      if (examForm.value.pricing_type === 'Free') {
        examForm.value.amount = 0;
      }
    };

    // Computed
    const filteredExams = computed(() =>
      exams.value.filter(e => e.sector_id === selectedSector.value?.id)
    );
    const allQuestions = computed(() => [...bankQuestions.value, ...customQuestions.value]);
    const totalQuestions = computed(() => allQuestions.value.length);
    const totalMarks = computed(() => allQuestions.value.reduce((sum, q) => sum + (q.marks || 1), 0));
    const answeredCount = computed(() => 0);

    // ============= API CALLS =============
    const fetchSectors = async () => {
      loading.value.sectors = true;
      try {
        const data = await api.get('/api/sectors');
        sectors.value = Array.isArray(data) ? data : [];
      } catch (err) {
        console.error('Error fetching sectors:', err);
        error.value = 'Failed to load sectors';
        sectors.value = [
          { id: 13, name: 'Natural Science', icon: '🔬', description: 'Biology, Chemistry, Physics' },
          { id: 14, name: 'Social Science', icon: '📜', description: 'History, Geography, Economics' },
          { id: 15, name: 'Mathematics', icon: '📐', description: 'Algebra, Calculus, Statistics' }
        ];
      } finally {
        loading.value.sectors = false;
      }
    };

    const loadExams = async () => {
      if (!selectedSector.value) return;
      loading.value.exams = true;
      loading.value.global = true;
      loading.value.message = 'Loading exams...';
      try {
        const data = await api.get(`/api/exams?sector_id=${selectedSector.value.id}`);
        exams.value = data;
        currentStep.value = 2;
      } catch (err) {
        console.error('Error fetching exams:', err);
        error.value = 'Failed to load exams';
        currentStep.value = 2;
      } finally {
        loading.value.exams = false;
        loading.value.global = false;
      }
    };

    const loadSections = async () => {
      if (!selectedExam.value) return;
      loading.value.sections = true;
      loading.value.global = true;
      loading.value.message = 'Loading sections...';
      try {
        const data = await api.get(`/api/sections?exam_id=${selectedExam.value.id}`);
        sections.value = data;
        currentStep.value = 3;
      } catch (err) {
        console.error('Error fetching sections:', err);
        error.value = 'Failed to load sections';
        sections.value = [];
        currentStep.value = 3;
      } finally {
        loading.value.sections = false;
        loading.value.global = false;
      }
    };

    const loadSectionsForExam = async (examId) => {
      if (!examId) return;
      loading.value.sections = true;
      try {
        const data = await api.get(`/api/sections?exam_id=${examId}`);
        sections.value = data;
        if (sections.value.length > 0) {
          selectedSections.value = [sections.value[0].id];
        }
      } catch (err) {
        console.error('Error fetching sections for exam:', err);
        sections.value = [];
      } finally {
        loading.value.sections = false;
      }
    };

    const fetchQuestions = async () => {
      if (selectedSections.value.length === 0) {
        bankQuestions.value = [];
        return;
      }
      loading.value.questions = true;
      try {
        const sectionIds = selectedSections.value.join(',');
        const data = await api.get(`/api/questions?section_ids=${sectionIds}`);
        bankQuestions.value = data;
      } catch (err) {
        console.error('Error fetching questions:', err);
        error.value = 'Failed to load questions';
      } finally {
        loading.value.questions = false;
      }
    };

    // ============= EXAM CRUD OPERATIONS =============
    const openAddExamModal = () => {
      editingExam.value = null;
      examForm.value = {
        name: '',
        total_questions: 50,
        duration: 60,
        exam_type: '',
        total_marks: 100
      };
      examModalOpen.value = true;
    };

    const openEditExamModal = (exam) => {
      editingExam.value = exam;
      examForm.value = {
        name: exam.name,
        total_questions: exam.total_questions,
        duration: exam.duration,
        exam_type: exam.exam_type || '',
        total_marks: exam.total_marks || 0
      };
      examModalOpen.value = true;
    };

    const closeExamModal = () => {
      examModalOpen.value = false;
      editingExam.value = null;
    };

    const saveExam = async () => {
      if (!selectedSector.value) {
        error.value = 'Please select a sector first';
        return;
      }

      savingExam.value = true;
      try {
        if (editingExam.value) {
          const updateData = {
            name: examForm.value.name,
            total_questions: examForm.value.total_questions,
            duration: examForm.value.duration,
            exam_type: examForm.value.exam_type || 'Unknown',
            total_marks: examForm.value.total_marks || 0,
            difficulty: examForm.value.difficulty || 1
          };
          const updatedExam = await api.put(`/api/exams/${editingExam.value.id}`, updateData);
          const index = exams.value.findIndex(e => e.id === editingExam.value.id);
          if (index !== -1) {
            exams.value[index] = { ...exams.value[index], ...updateData };
          }
        } else {
          const examData = {
            sector_id: selectedSector.value.id,
            name: examForm.value.name,
            total_questions: examForm.value.total_questions,
            duration: examForm.value.duration,
            exam_type: examForm.value.exam_type || 'Unknown',
            total_marks: examForm.value.total_marks || 0,
            difficulty: 1,
            pricing_type: examForm.value.pricing_type || 'Free',
            amount: examForm.value.pricing_type === 'Premium' ? (examForm.value.amount || 0) : 0
          };
          const newExam = await api.post('/api/exams', examData);
          if (newExam && newExam.id) {
            exams.value.push(newExam);
            selectedExam.value = newExam;
            await loadSectionsForExam(newExam.id);
          }
        }
        closeExamModal();
      } catch (err) {
        console.error('Error saving exam:', err);
        error.value = `Failed to ${editingExam.value ? 'update' : 'create'} exam: ${err.message || err.response?.data?.detail || 'Unknown error'}`;
      } finally {
        savingExam.value = false;
      }
    };

    const confirmDeleteExam = (exam) => {
      examToDelete.value = exam;
      deleteModalOpen.value = true;
    };

    const cancelDelete = () => {
      deleteModalOpen.value = false;
      examToDelete.value = null;
    };

    const deleteExam = async () => {
      if (!examToDelete.value) return;
      deletingExam.value = true;
      try {
        const response = await api.delete(`/api/exams/${examToDelete.value.id}`);
        exams.value = exams.value.filter(e => e.id !== examToDelete.value.id);
        if (selectedExam.value?.id === examToDelete.value.id) {
          selectedExam.value = null;
          sections.value = [];
          bankQuestions.value = [];
          customQuestions.value = [];
          selectedSections.value = [];
          currentStep.value = 2;
        }
        deleteModalOpen.value = false;
        examToDelete.value = null;
      } catch (err) {
        console.error('Error deleting exam:', err);
        error.value = `Failed to delete exam: ${err.message || err.response?.data?.detail || 'Unknown error'}`;
      } finally {
        deletingExam.value = false;
      }
    };

    // ============= CUSTOM SECTIONS =============
    const handleSectionNameChange = () => {
      // Just update the selected section name
    };

    const addCustomSection = () => {
      if (selectedSectionName.value && !customSections.value.find(s => s.name === selectedSectionName.value)) {
        customSections.value.push({
          name: selectedSectionName.value,
          question_count: 0,
          color: getRandomColor()
        });
      }
    };

    const removeCustomSection = (index) => {
      customSections.value.splice(index, 1);
    };

    const getRandomColor = () => {
      const colors = ['blue', 'green', 'purple', 'orange', 'red', 'pink', 'indigo', 'teal'];
      return colors[Math.floor(Math.random() * colors.length)];
    };

    const getCurrentSectionId = () => {
      if (sections.value.length > 0) {
        return sections.value[0].id;
      }
      return 1;
    };

    // ============= FORM HANDLERS =============
    const handleGradeChange = (grade) => {
      testForm.value.grade = grade;
    };

    const handleSubjectChange = (subject) => {
      testForm.value.subject = subject;
    };

    const toggleSection = (id) => {
      const index = selectedSections.value.indexOf(id);
      if (index === -1) {
        selectedSections.value.push(id);
      } else {
        selectedSections.value.splice(index, 1);
      }
    };

    const addCustomQuestion = (question) => {
      customQuestions.value.push({
        ...question,
        id: Date.now(),
        text: question.text,
        marks: question.marks,
        difficulty: question.difficulty
      });
    };

    const removeQuestion = (index) => {
      bankQuestions.value.splice(index, 1);
    };

    const removeCustomQuestion = (index) => {
      customQuestions.value.splice(index, 1);
    };

    // ============= SAVE TEST =============
    const saveAsDraft = async () => {
      saving.value = true;
      try {
        const testData = {
          title: testForm.value.title || selectedExam.value?.name || 'Untitled Test',
          sector_id: selectedSector.value?.id,
          exam_id: selectedExam.value?.id,
          duration: testForm.value.duration,
          difficulty: testForm.value.difficulty,
          question_count: totalQuestions.value,
          total_marks: totalMarks.value,
          exam_type: testForm.value.examType || selectedExam.value?.exam_type,
          created_by: 1,
          status: 'draft'
        };
        await api.post('/api/tests/draft', testData);
        alert('Test saved as draft successfully!');
        router.push('/tests');
      } catch (err) {
        console.error('Error saving draft:', err);
        error.value = 'Failed to save test';
      } finally {
        saving.value = false;
      }
    };

    const publishTest = async () => {
      saving.value = true;
      try {
        const testData = {
          title: testForm.value.title || selectedExam.value?.name || 'Untitled Test',
          sector_id: selectedSector.value?.id,
          exam_id: selectedExam.value?.id,
          duration: testForm.value.duration,
          difficulty: testForm.value.difficulty,
          question_count: totalQuestions.value,
          total_marks: totalMarks.value,
          exam_type: testForm.value.examType || selectedExam.value?.exam_type,
          created_by: 1,
          status: 'published'
        };
        await api.post('/api/tests', testData);
        alert('Test published successfully!');
        router.push('/tests');
      } catch (err) {
        console.error('Error publishing test:', err);
        error.value = 'Failed to publish test';
      } finally {
        saving.value = false;
      }
    };

    // ============= NAVIGATION =============
    const goToStep = (step) => {
      if (step < currentStep.value) {
        currentStep.value = step;
        if (step === 1) {
          selectedExam.value = null;
          selectedSections.value = [];
        } else if (step === 2) {
          selectedSections.value = [];
        }
      }
    };

    // ============= WATCHERS =============
    watch(selectedSections, () => {
      if (selectedSections.value.length > 0) {
        fetchQuestions();
      } else {
        bankQuestions.value = [];
      }
    }, { deep: true });

    watch(selectedExam, (newExam, oldExam) => {
      if (newExam && newExam.id !== oldExam?.id) {
        testForm.value.duration = newExam.duration;
        testForm.value.examType = newExam.exam_type;
        testForm.value.totalMarks = newExam.total_marks;
        testForm.value.title = newExam.name;
        sections.value = [];
        bankQuestions.value = [];
        customQuestions.value = [];
        selectedSections.value = [];
        loadSectionsForExam(newExam.id);
      }
    });

    // ============= INITIAL LOAD =============
    onMounted(() => {
      fetchSectors();
    });

    return {
      currentStep,
      loading,
      saving,
      savingExam,
      deletingExam,
      error,
      sectors,
      exams,
      sections,
      bankQuestions,
      customQuestions,
      markedQuestions,
      selectedSector,
      selectedExam,
      selectedSections,
      testForm,
      examForm,
      filteredExams,
      totalQuestions,
      totalMarks,
      answeredCount,
      examModalOpen,
      deleteModalOpen,
      editingExam,
      examToDelete,
      predefinedSections,
      selectedSectionName,
      customSections,
      goToStep,
      loadExams,
      loadSections,
      loadSectionsForExam,
      handleGradeChange,
      handleSubjectChange,
      handleSectionNameChange,
      addCustomSection,
      removeCustomSection,
      getCurrentSectionId,
      toggleSection,
      addCustomQuestion,
      removeQuestion,
      removeCustomQuestion,
      saveAsDraft,
      publishTest,
      allQuestions,
      openAddExamModal,
      openEditExamModal,
      closeExamModal,
      saveExam,
      confirmDeleteExam,
      cancelDelete,
      deleteExam
    };
  }
};
</script>

<style scoped>

.exam-builder {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f9ff 0%, #eef2ff 100%);
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

/* Loading States */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(4px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e2e8f0;
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.spinner-small {
  width: 24px;
  height: 24px;
  border: 3px solid #e2e8f0;
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Error Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.modal-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
}

.modal-close {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  color: #64748b;
}

.modal-close:hover {
  color: #1e293b;
}

.close-icon {
  width: 1.5rem;
  height: 1.5rem;
}

.error-modal {
  border-top: 4px solid #ef4444;
}

.exam-modal {
  max-width: 600px;
}

.delete-modal {
  max-width: 450px;
}

.delete-message {
  color: #475569;
  line-height: 1.6;
}

.modal-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

/* Steps Wrapper */
.steps-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2rem;
  padding: 1rem;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: #64748b;
  transition: all 0.3s ease;
}

.step.active .step-number {
  background: #2563eb;
  color: white;
}

.step.completed .step-number {
  background: #10b981;
  color: white;
}

.step-label {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}

.step.active .step-label {
  color: #2563eb;
}

.step.completed .step-label {
  color: #10b981;
}

.step-line {
  width: 80px;
  height: 3px;
  background: #e2e8f0;
  margin: 0 0.5rem;
  margin-bottom: 1.5rem;
  transition: background 0.3s ease;
}

.step-line.active {
  background: #2563eb;
}

/* Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: 280px 1fr 300px;
  gap: 1.5rem;
}

@media (max-width: 1200px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .preview-panel {
    display: none;
  }
}

/* Sidebar */
.sidebar {
  position: sticky;
  top: 2rem;
  height: fit-content;
}

.sidebar-card {
  background: white;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.sidebar-step {
  padding: 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid transparent;
}

.sidebar-step:hover {
  background: #f8fafc;
}

.sidebar-step.active {
  background: #eff6ff;
  border-color: #2563eb;
}

.step-indicator {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.step-badge {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
  color: #64748b;
}

.step-badge.active {
  background: #2563eb;
  color: white;
}

.step-badge.completed {
  background: #10b981;
  color: white;
}

.step-info {
  display: flex;
  flex-direction: column;
}

.step-title {
  font-size: 0.75rem;
  color: #94a3b8;
}

.step-name {
  font-size: 0.875rem;
  font-weight: 500;
  color: #334155;
}

.selected-value {
  display: block;
  font-size: 0.75rem;
  color: #2563eb;
  margin-top: 0.25rem;
  margin-left: 3rem;
}

/* Main Content */
.main-content {
  min-height: 500px;
}

.content-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 1.5rem;
}

/* Sector Grid */
.sector-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

/* Exam List */
.exam-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.exam-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  transition: all 0.2s ease;
  cursor: pointer;
}

.exam-item:hover {
  border-color: #93c5fd;
  background: #f8fafc;
}

.exam-item.exam-selected {
  border-color: #2563eb;
  background: #eff6ff;
}

.exam-content {
  flex: 1;
}

.exam-name {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.exam-meta {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.meta-item {
  font-size: 0.875rem;
  color: #64748b;
}

.meta-icon {
  margin-right: 0.25rem;
  color: #94a3b8;
}

.exam-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-action {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-edit {
  background: #f1f5f9;
  color: #64748b;
}

.btn-edit:hover {
  background: #e2e8f0;
  color: #2563eb;
}

.btn-delete {
  background: #fef2f2;
  color: #fca5a5;
}

.btn-delete:hover {
  background: #fee2e2;
  color: #ef4444;
}

.action-icon {
  width: 16px;
  height: 16px;
}

.exam-check {
  width: 24px;
  height: 24px;
  background: #2563eb;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 0.5rem;
}

.check-icon {
  width: 16px;
  height: 16px;
  color: white;
}

/* Step Header */
.step-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.step-header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.sector-tag {
  padding: 0.25rem 0.75rem;
  background: #f1f5f9;
  border-radius: 9999px;
  font-size: 0.875rem;
  color: #64748b;
}

/* Buttons */
.btn {
  padding: 0.625rem 1.25rem;
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  border: none;
}

.btn-primary {
  background: #2563eb;
  color: white;
}

.btn-primary:hover {
  background: #1d4ed8;
}

.btn-primary:disabled {
  background: #93c5fd;
  cursor: not-allowed;
}

.btn-outline {
  background: white;
  border: 1px solid #e2e8f0;
  color: #475569;
}

.btn-outline:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.btn-danger {
  background: #ef4444;
  color: white;
}

.btn-danger:hover {
  background: #dc2626;
}

.btn-add {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #10b981;
  color: white;
  border-radius: 6px;
  font-weight: 500;
  font-size: 0.875rem;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-add:hover {
  background: #059669;
}

.plus-icon {
  font-size: 1.25rem;
  line-height: 1;
}

.continue-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  padding: 1rem;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.continue-btn:hover {
  background: #1d4ed8;
}

.continue-btn:disabled {
  background: #93c5fd;
  cursor: not-allowed;
}

.action-buttons {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-top: 1rem;
}

.arrow {
  transition: transform 0.2s ease;
}

.arrow-left {
  transition: transform 0.2s ease;
}

.btn-outline:hover .arrow-left {
  transform: translateX(-3px);
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 3rem;
  color: #64748b;
}

.empty-state p {
  margin-bottom: 1rem;
}

/* Form Styles */
.form-group {
  margin-bottom: 1rem;
}

.form-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

.form-input {
  width: 100%;
  padding: 0.625rem 0.875rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.875rem;
  transition: border-color 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

/* Exam Form */
.exam-form {
  padding: 0.5rem;
}

/* Preview Panel */
.preview-panel {
  position: sticky;
  top: 2rem;
  height: fit-content;
}

/* Floating Actions */
.floating-actions {
  position: fixed;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  z-index: 100;
}

/* Card Header */
.card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 1.5rem;
}

.header-indicator {
  width: 4px;
  height: 20px;
  background: #2563eb;
  border-radius: 2px;
}

/* Sections Group */
.sections-group {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e2e8f0;
}

.group-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #475569;
  margin-bottom: 0.75rem;
}

.section-dropdown {
  margin-bottom: 0.5rem;
}

.selected-sections {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.section-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.375rem 0.75rem;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 9999px;
  font-size: 0.875rem;
  color: #1e40af;
}

.remove-btn {
  background: none;
  border: none;
  color: #3b82f6;
  cursor: pointer;
  font-size: 1.25rem;
  line-height: 1;
  padding: 0;
}

.remove-btn:hover {
  color: #1d4ed8;
}

.add-section-btn {
  padding: 0.375rem 0.75rem;
  background: #f1f5f9;
  border: 1px dashed #cbd5e1;
  border-radius: 9999px;
  font-size: 0.875rem;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-section-btn:hover {
  background: #e2e8f0;
  color: #475569;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

.fade-up-enter-active,
.fade-up-leave-active {
  transition: all 0.3s ease;
}

.fade-up-enter-from,
.fade-up-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(20px);
}

/* Utilities */
.text-center {
  text-align: center;
}

.py-8 {
  padding-top: 2rem;
  padding-bottom: 2rem;
}

.mt-2 {
  margin-top: 0.5rem;
}

.mt-3 {
  margin-top: 0.75rem;
}

.mt-4 {
  margin-top: 1rem;
}

.text-gray-500 {
  color: #64748b;
}

.space-y-4 > * + * {
  margin-top: 1rem;
}
</style>