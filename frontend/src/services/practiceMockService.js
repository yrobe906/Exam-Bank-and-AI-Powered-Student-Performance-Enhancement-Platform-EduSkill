const API_URL = 'http://127.0.0.1:8000';

const getAuthHeaders = () => {
  const token = localStorage.getItem('admin_token');
  return {
    'Content-Type': 'application/json',
    'Authorization': token ? `Bearer ${token}` : ''
  };
};

// ============== Practice Mock Tests API ==============

export const practiceMockService = {
  // Get all mock tests
  async getMockTests(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const res = await fetch(`${API_URL}/api/practice-mock/tests?${queryString}`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Failed to fetch mock tests');
    return res.json();
  },

  // Get single mock test with questions
  async getMockTest(testId) {
    const res = await fetch(`${API_URL}/api/practice-mock/tests/${testId}`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Failed to fetch mock test');
    return res.json();
  },

  // Create mock test
  async createMockTest(testData) {
    const res = await fetch(`${API_URL}/api/practice-mock/tests`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(testData)
    });
    if (!res.ok) throw new Error('Failed to create mock test');
    return res.json();
  },

  // Update mock test
  async updateMockTest(testId, testData) {
    const res = await fetch(`${API_URL}/api/practice-mock/tests/${testId}`, {
      method: 'PATCH',
      headers: getAuthHeaders(),
      body: JSON.stringify(testData)
    });
    if (!res.ok) throw new Error('Failed to update mock test');
    return res.json();
  },

  // Delete mock test
  async deleteMockTest(testId) {
    const res = await fetch(`${API_URL}/api/practice-mock/tests/${testId}`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Failed to delete mock test');
    return res.json();
  },

  // Get all subjects
  async getSubjects() {
    const res = await fetch(`${API_URL}/api/practice-mock/tests/subjects`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Failed to fetch subjects');
    return res.json();
  },

  // Get questions for a test
  async getTestQuestions(testId) {
    const res = await fetch(`${API_URL}/api/practice-mock/tests/${testId}/questions`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Failed to fetch questions');
    return res.json();
  },

  // Get single question
  async getQuestion(questionId) {
    const res = await fetch(`${API_URL}/api/practice-mock/questions/${questionId}`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Failed to fetch question');
    return res.json();
  },

  // Create question
  async createQuestion(questionData) {
    const res = await fetch(`${API_URL}/api/practice-mock/questions`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(questionData)
    });
    if (!res.ok) throw new Error('Failed to create question');
    return res.json();
  },

  // Update question
  async updateQuestion(questionId, questionData) {
    const res = await fetch(`${API_URL}/api/practice-mock/questions/${questionId}`, {
      method: 'PATCH',
      headers: getAuthHeaders(),
      body: JSON.stringify(questionData)
    });
    if (!res.ok) throw new Error('Failed to update question');
    return res.json();
  },

  // Delete question
  async deleteQuestion(questionId) {
    const res = await fetch(`${API_URL}/api/practice-mock/questions/${questionId}`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Failed to delete question');
    return res.json();
  },

  // Get questions count
  async getQuestionsCount(testId) {
    const res = await fetch(`${API_URL}/api/practice-mock/tests/${testId}/questions-count`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Failed to fetch questions count');
    return res.json();
  }
};

export default practiceMockService;
