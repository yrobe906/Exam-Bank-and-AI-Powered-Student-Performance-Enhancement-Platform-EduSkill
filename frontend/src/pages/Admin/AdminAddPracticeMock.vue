<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50/30">
    <!-- EduSkillHeader -->
    <EduskillHeader>
      <p>Admin - Add Practice Mock</p>
    </EduskillHeader>

    <div>
      <!-- Main Content -->
      <main class="p-6 md:p-8">
        <!-- Page Header -->
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-slate-800">Practice Mock Test Builder</h1>
          <p class="text-slate-600 mt-2">Create and manage practice mock tests with questions</p>
        </div>

        <!-- Tabs -->
        <div class="flex gap-4 mb-6 border-b border-slate-200">
          <button
            @click="activeTab = 'tests'"
            :class="[
              'pb-3 px-4 font-medium transition-colors border-b-2',
              activeTab === 'tests'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-slate-500 hover:text-slate-700'
            ]"
          >
            📋 Mock Tests
          </button>
          <button
            @click="activeTab = 'questions'"
            :class="[
              'pb-3 px-4 font-medium transition-colors border-b-2',
              activeTab === 'questions'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-slate-500 hover:text-slate-700'
            ]"
          >
            ❓ Questions
          </button>
          <button
            @click="activeTab = 'create-test'"
            :class="[
              'pb-3 px-4 font-medium transition-colors border-b-2',
              activeTab === 'create-test'
                ? 'border-green-600 text-green-600'
                : 'border-transparent text-slate-500 hover:text-slate-700'
            ]"
          >
            ➕ Create Test
          </button>
        </div>

        <!-- Mock Tests Tab -->
        <div v-if="activeTab === 'tests'" class="space-y-6">
          <!-- Filters -->
          <div class="flex flex-wrap gap-4 mb-6">
            <select
              v-model="filterSubject"
              class="px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Subjects</option>
              <option v-for="subject in subjects" :key="subject" :value="subject">{{ subject }}</option>
            </select>
            <button
              @click="loadMockTests"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              🔍 Filter
            </button>
          </div>

          <!-- Tests Grid -->
          <div v-if="loading" class="text-center py-12">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p class="text-slate-500 mt-4">Loading mock tests...</p>
          </div>

          <div v-else-if="mockTests.length === 0" class="text-center py-12 bg-white rounded-xl border border-slate-200">
            <p class="text-slate-500">No mock tests found. Create your first test!</p>
          </div>

          <div v-else class="grid gap-4">
            <div
              v-for="test in mockTests"
              :key="test.id"
              class="bg-white rounded-xl border border-slate-200 p-6 hover:shadow-lg transition-shadow"
            >
              <div class="flex justify-between items-start">
                <div>
                  <h3 class="text-lg font-semibold text-slate-800">{{ test.title }}</h3>
                  <p class="text-slate-600 mt-1">{{ test.subject }}</p>
                  <p v-if="test.description" class="text-sm text-slate-500 mt-2">{{ test.description }}</p>
                  <div class="flex gap-4 mt-3 text-sm">
                    <span :class="test.is_active ? 'text-green-600' : 'text-red-500'">
                      {{ test.is_active ? '✅ Active' : '❌ Inactive' }}
                    </span>
                    <span class="text-slate-500">📅 {{ formatDate(test.created_at) }}</span>
                  </div>
                </div>
                <div class="flex gap-2">
                  <button
                    @click="viewQuestions(test.id)"
                    class="px-3 py-2 bg-purple-100 text-purple-600 rounded-lg hover:bg-purple-200 transition-colors"
                  >
                    👁️ Questions
                  </button>
                  <button
                    @click="deleteTest(test.id)"
                    class="px-3 py-2 bg-red-100 text-red-600 rounded-lg hover:bg-red-200 transition-colors"
                  >
                    🗑️ Delete
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Questions Tab -->
        <div v-if="activeTab === 'questions'" class="space-y-6">
          <div v-if="!selectedTest" class="bg-yellow-50 border border-yellow-200 rounded-xl p-4 text-yellow-800">
            Please select a mock test from the Tests tab to view its questions.
          </div>

          <div v-else>
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-xl font-semibold text-slate-800">
                Questions for: {{ selectedTest.title }}
              </h2>
              <button
                @click="openAddQuestionModal"
                class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                ➕ Add Question
              </button>
            </div>

            <div v-if="testQuestions.length === 0" class="text-center py-12 bg-white rounded-xl border border-slate-200">
              <p class="text-slate-500">No questions yet. Add some questions!</p>
            </div>

            <div v-else class="space-y-4">
              <div
                v-for="(question, index) in testQuestions"
                :key="question.id"
                class="bg-white rounded-xl border border-slate-200 p-6"
              >
                <div class="flex justify-between items-start">
                  <div class="flex-1">
                    <p class="font-medium text-slate-800 mb-3">
                      <span class="text-blue-600">{{ index + 1 }}.</span> {{ question.question_text }}
                    </p>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm">
                      <div :class="question.correct_answer === 'a' ? 'text-green-600 font-semibold' : 'text-slate-600'">
                        A. {{ question.option_a }}
                      </div>
                      <div :class="question.correct_answer === 'b' ? 'text-green-600 font-semibold' : 'text-slate-600'">
                        B. {{ question.option_b }}
                      </div>
                      <div :class="question.correct_answer === 'c' ? 'text-green-600 font-semibold' : 'text-slate-600'">
                        C. {{ question.option_c }}
                      </div>
                      <div :class="question.correct_answer === 'd' ? 'text-green-600 font-semibold' : 'text-slate-600'">
                        D. {{ question.option_d }}
                      </div>
                    </div>
                    <div v-if="question.explanation" class="mt-3 p-3 bg-blue-50 rounded-lg text-sm text-blue-800">
                      <strong>Explanation:</strong> {{ question.explanation }}
                    </div>
                  </div>
                  <div class="flex gap-2 ml-4">
                    <button
                      @click="editQuestion(question)"
                      class="px-3 py-2 bg-blue-100 text-blue-600 rounded-lg hover:bg-blue-200 transition-colors"
                    >
                      ✏️
                    </button>
                    <button
                      @click="deleteQuestion(question.id)"
                      class="px-3 py-2 bg-red-100 text-red-600 rounded-lg hover:bg-red-200 transition-colors"
                    >
                      🗑️
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Create Test Tab -->
        <div v-if="activeTab === 'create-test'" class="max-w-2xl">
          <div class="bg-white rounded-xl border border-slate-200 p-6">
            <h2 class="text-xl font-semibold text-slate-800 mb-6">Create New Mock Test</h2>
            
            <form @submit.prevent="createMockTest" class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">Test Title *</label>
                <input
                  v-model="newTest.title"
                  type="text"
                  required
                  class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="e.g., Biology Mid-Term Practice"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">Subject *</label>
                <select
                  v-model="newTest.subject"
                  required
                  class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Select Subject</option>
                  <option value="Biology">Biology</option>
                  <option value="Chemistry">Chemistry</option>
                  <option value="Physics">Physics</option>
                  <option value="Mathematics">Mathematics</option>
                  <option value="English">English</option>
                  <option value="Geography">Geography</option>
                  <option value="History">History</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">Description</label>
                <textarea
                  v-model="newTest.description"
                  rows="3"
                  class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Optional description for this test"
                ></textarea>
              </div>

              <div class="flex items-center gap-2">
                <input
                  v-model="newTest.is_active"
                  type="checkbox"
                  id="is_active"
                  class="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                />
                <label for="is_active" class="text-sm text-slate-700">Active (visible to students)</label>
              </div>

              <div class="pt-4">
                <button
                  type="submit"
                  :disabled="creating"
                  class="w-full px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50"
                >
                  {{ creating ? 'Creating...' : '✅ Create Mock Test' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </main>
    </div>

    <!-- Add/Edit Question Modal -->
    <div v-if="showAddQuestion || editingQuestion" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6">
        <h3 class="text-xl font-semibold text-slate-800 mb-6">
          {{ editingQuestion ? 'Edit Question' : 'Add New Question' }}
        </h3>

        <form @submit.prevent="saveQuestion" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">Question Text *</label>
            <textarea
              v-model="newQuestion.question_text"
              required
              rows="3"
              class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter your question here"
            ></textarea>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">Option A *</label>
              <input
                v-model="newQuestion.option_a"
                type="text"
                required
                class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Option A"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">Option B *</label>
              <input
                v-model="newQuestion.option_b"
                type="text"
                required
                class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Option B"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">Option C *</label>
              <input
                v-model="newQuestion.option_c"
                type="text"
                required
                class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Option C"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">Option D *</label>
              <input
                v-model="newQuestion.option_d"
                type="text"
                required
                class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Option D"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">Correct Answer *</label>
            <select
              v-model="newQuestion.correct_answer"
              required
              class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="a">A</option>
              <option value="b">B</option>
              <option value="c">C</option>
              <option value="d">D</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">Explanation</label>
            <textarea
              v-model="newQuestion.explanation"
              rows="3"
              class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Explain why the answer is correct"
            ></textarea>
          </div>

          <div class="flex gap-4 pt-4">
            <button
              type="button"
              @click="closeQuestionModal"
              class="flex-1 px-6 py-3 border border-slate-200 text-slate-700 rounded-lg hover:bg-slate-50 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="savingQuestion"
              class="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
            >
              {{ savingQuestion ? 'Saving...' : (editingQuestion ? 'Update Question' : 'Add Question') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import EduskillHeader from '@/components/Header/EduskillHeader.vue';

const API_URL = 'http://127.0.0.1:8000';

export default {
  name: 'AdminAddPracticeMock',
  components: {
    EduskillHeader
  },
  data() {
    return {
      activeTab: 'tests',
      loading: false,
      creating: false,
      savingQuestion: false,
      mockTests: [],
      subjects: [],
      filterSubject: '',
      selectedTest: null,
      testQuestions: [],
      showAddQuestion: false,
      editingQuestion: null,
      newTest: {
        title: '',
        subject: '',
        description: '',
        is_active: true
      },
      newQuestion: {
        question_text: '',
        option_a: '',
        option_b: '',
        option_c: '',
        option_d: '',
        correct_answer: 'a',
        explanation: '',
        order_index: 0
      }
    };
  },
  mounted() {
    this.loadMockTests();
    this.loadSubjects();
  },
  methods: {
    async loadMockTests() {
      this.loading = true;
      try {
        const token = localStorage.getItem('admin_token');
        const params = new URLSearchParams();
        if (this.filterSubject) params.append('subject', this.filterSubject);
        
        const res = await fetch(`${API_URL}/api/practice-mock/tests?${params}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        if (res.ok) {
          this.mockTests = await res.json();
        }
      } catch (error) {
        console.error('Error loading mock tests:', error);
      } finally {
        this.loading = false;
      }
    },
    async loadSubjects() {
      try {
        const token = localStorage.getItem('admin_token');
        const res = await fetch(`${API_URL}/api/practice-mock/tests/subjects`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        if (res.ok) {
          this.subjects = await res.json();
        }
      } catch (error) {
        console.error('Error loading subjects:', error);
      }
    },
    async createMockTest() {
      this.creating = true;
      try {
        const token = localStorage.getItem('admin_token');
        const res = await fetch(`${API_URL}/api/practice-mock/tests`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(this.newTest)
        });
        
        if (res.ok) {
          alert('✅ Mock test created successfully!');
          this.newTest = {
            title: '',
            subject: '',
            description: '',
            is_active: true
          };
          this.loadMockTests();
          this.loadSubjects();
        } else {
          alert('Failed to create mock test');
        }
      } catch (error) {
        console.error('Error creating mock test:', error);
        alert('Error creating mock test');
      } finally {
        this.creating = false;
      }
    },
    async viewQuestions(testId) {
      this.selectedTest = this.mockTests.find(t => t.id === testId);
      this.activeTab = 'questions';
      await this.loadTestQuestions(testId);
    },
    async loadTestQuestions(testId) {
      try {
        const token = localStorage.getItem('admin_token');
        const res = await fetch(`${API_URL}/api/practice-mock/tests/${testId}/questions`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        if (res.ok) {
          this.testQuestions = await res.json();
        }
      } catch (error) {
        console.error('Error loading questions:', error);
      }
    },
    async deleteTest(testId) {
      if (!confirm('Are you sure you want to delete this mock test and all its questions?')) return;
      
      try {
        const token = localStorage.getItem('admin_token');
        const res = await fetch(`${API_URL}/api/practice-mock/tests/${testId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        if (res.ok) {
          alert('✅ Mock test deleted successfully!');
          this.loadMockTests();
        } else {
          alert('Failed to delete mock test');
        }
      } catch (error) {
        console.error('Error deleting mock test:', error);
      }
    },
    openAddQuestionModal() {
      this.showAddQuestion = true;
      this.editingQuestion = null;
      this.newQuestion = {
        question_text: '',
        option_a: '',
        option_b: '',
        option_c: '',
        option_d: '',
        correct_answer: 'a',
        explanation: '',
        order_index: 0
      };
    },
    editQuestion(question) {
      this.editingQuestion = question;
      this.newQuestion = {
        question_text: question.question_text,
        option_a: question.option_a,
        option_b: question.option_b,
        option_c: question.option_c,
        option_d: question.option_d,
        correct_answer: question.correct_answer,
        explanation: question.explanation || '',
        order_index: question.order_index || 0
      };
    },
    async saveQuestion() {
      if (!this.selectedTest) {
        alert('Please select a mock test first');
        return;
      }

      this.savingQuestion = true;
      try {
        const token = localStorage.getItem('admin_token');
        
        const payload = {
          ...this.newQuestion,
          mock_test_id: this.selectedTest.id
        };

        let res;
        if (this.editingQuestion) {
          res = await fetch(`${API_URL}/api/practice-mock/questions/${this.editingQuestion.id}`, {
            method: 'PATCH',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(this.newQuestion)
          });
        } else {
          res = await fetch(`${API_URL}/api/practice-mock/questions`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(payload)
          });
        }

        if (res.ok) {
          alert(this.editingQuestion ? '✅ Question updated!' : '✅ Question added!');
          this.closeQuestionModal();
          this.loadTestQuestions(this.selectedTest.id);
        } else {
          alert('Failed to save question');
        }
      } catch (error) {
        console.error('Error saving question:', error);
      } finally {
        this.savingQuestion = false;
      }
    },
    async deleteQuestion(questionId) {
      if (!confirm('Are you sure you want to delete this question?')) return;

      try {
        const token = localStorage.getItem('admin_token');
        const res = await fetch(`${API_URL}/api/practice-mock/questions/${questionId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (res.ok) {
          alert('✅ Question deleted!');
          this.loadTestQuestions(this.selectedTest.id);
        } else {
          alert('Failed to delete question');
        }
      } catch (error) {
        console.error('Error deleting question:', error);
      }
    },
    closeQuestionModal() {
      this.showAddQuestion = false;
      this.editingQuestion = null;
      this.newQuestion = {
        question_text: '',
        option_a: '',
        option_b: '',
        option_c: '',
        option_d: '',
        correct_answer: 'a',
        explanation: '',
        order_index: 0
      };
    },
    formatDate(dateStr) {
      if (!dateStr) return '';
      return new Date(dateStr).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    }
  }
};
</script>

<style scoped>
.max-h-\[90vh\]::-webkit-scrollbar {
  width: 8px;
}

.max-h-\[90vh\]::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 4px;
}

.max-h-\[90vh\]::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

.max-h-\[90vh\]::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
