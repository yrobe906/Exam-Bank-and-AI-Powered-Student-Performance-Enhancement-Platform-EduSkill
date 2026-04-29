// services/gamificationService.js
import axios from 'axios';

const API_BASE = 'http://localhost:8000';

const createApi = (tokenType = 'user') => {
  let token = null;
  if (tokenType === 'admin') {
    token = localStorage.getItem('admin_token') || sessionStorage.getItem('admin_token');
  } else {
    token = localStorage.getItem('token');
  }
  
  return axios.create({
    baseURL: API_BASE,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': token ? `Bearer ${token}` : ''
    }
  });
};

const getUserApi = () => createApi('user');
const getAdminApi = () => createApi('admin');

export default {
  async getProfile() {
    const userApi = getUserApi();
    const response = await userApi.get('/api/gamification/profile');
    return response.data;
  },
  
  async getSummary() {
    const userApi = getUserApi();
    const response = await userApi.get('/api/gamification/summary');
    return response.data;
  },
  
  async getProfileById(userId) {
    const adminApi = getAdminApi();
    const response = await adminApi.get(`/api/gamification/profile/public/${userId}`);
    return response.data;
  },

  // Fixed XP endpoints to match backend router
  async awardExamSubmissionXP(examId) {
    const userApi = getUserApi();
    const response = await userApi.post(`/api/gamification/award-exam-submission/${examId}`);
    console.log('Exam submission XP:', response.data);
    return response.data;
  },
  
  async awardExamResultXP(examId, percentage) {
    const userApi = getUserApi();
    const response = await userApi.post(`/api/gamification/award-exam-result/${examId}`, { percentage });
    console.log('Exam result XP:', response.data);
    return response.data;
  },
  
  async awardPremiumPurchaseXP(contentId) {
    const userApi = getUserApi();
    const response = await userApi.post(`/api/gamification/award-premium-purchase/${contentId}`);
    return response.data;
  },
  
  async getTransactions(limit = 20) {
    const userApi = getUserApi();
    const response = await userApi.get(`/api/gamification/transactions?limit=${limit}`);
    return response.data;
  },

async checkUnlockEligibility(api, examId) {
    const response = await api.get(`/api/unlock/check-eligibility?exam_id=${examId}`);
    return response.data;
  },


async createUnlockRequest(examId, unlockMethod = 'points') {
    const userApi = getUserApi();
    const response = await userApi.post('/api/unlock/requests', {
      exam_id: examId,
      unlock_method: unlockMethod
    });
    return response;
  },

  async createUnlockRequestWithPayment(contentId, contentType, contentTitle, unlockMethod, paymentMethod, paymentProofFile) {
    const userApi = getUserApi();
    const formData = new FormData();
    formData.append('content_id', contentId);
    formData.append('content_type', contentType);
    formData.append('content_title', contentTitle);
    formData.append('unlock_method', unlockMethod);
    formData.append('payment_method', paymentMethod);
    if (paymentProofFile) {
      formData.append('payment_proof', paymentProofFile);
    }
    const response = await userApi.post('/api/unlock/requests', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  },

  async getMyUnlockRequests(api) {
    const response = await api.get('/api/unlock/my-requests');
    return response.data;
  },


  async cancelUnlockRequest(requestId) {
    const userApi = getUserApi();
    const response = await userApi.delete(`/api/gamification/unlock/request/${requestId}`);
    return response.data;
  },

  async recordActivity(activityType, contentId = null, contentType = null, completionPercentage = null) {
    const userApi = getUserApi();
    const response = await userApi.post('/api/gamification/activity/record', {
      activity_type: activityType,
      content_id: contentId,
      content_type: contentType,
      completion_percentage: completionPercentage
    });
    return response.data;
  },

  // Admin methods...
  async getAllUnlockRequests(status = null, limit = 50) {
    const adminApi = getAdminApi();
    const params = status ? `?status=${status}&limit=${limit}` : `?limit=${limit}`;
    const response = await adminApi.get(`/api/admin/gamification/all-requests${params}`);
    return response.data;
  },

  async processUnlockRequest(requestId, action, unlockMethod, transactionReference = null, adminNotes = null, overrideXpCheck = false) {
    const adminApi = getAdminApi();
    const response = await adminApi.post('/api/gamification/admin/approve-request', {
      request_id: requestId,
      action: action,
      unlock_method: unlockMethod,
      transaction_reference: transactionReference,
      admin_notes: adminNotes,
      override_xp_check: overrideXpCheck
    });
    return response.data;
  },

  async getFullUserProfile(userId) {
    const adminApi = getAdminApi();
    const response = await adminApi.get(`/api/gamification/admin/user/${userId}/full-profile`);
    return response.data;
  },

  async verifyPayment(requestId, verified, transactionReference = null) {
    const adminApi = getAdminApi();
    const response = await adminApi.patch(`/api/gamification/admin/verify-payment/${requestId}`, {
      verified: verified,
      transaction_reference: transactionReference
    });
    return response.data;
  },

  async getContentThresholds() {
    const adminApi = getAdminApi();
    const response = await adminApi.get('/api/gamification/admin/content-thresholds');
    return response.data;
  },

  async createContentThreshold(contentType, tierRequired, xpRequired) {
    const adminApi = getAdminApi();
    const response = await adminApi.post('/api/gamification/admin/content-thresholds', {
      content_type: contentType,
      tier_required: tierRequired,
      xp_required: xpRequired
    });
    return response.data;
  },

  async getAllBadges() {
    const adminApi = getAdminApi();
    const response = await adminApi.get('/api/gamification/admin/badges');
    return response.data;
  },

  async createBadge(badgeData) {
    const adminApi = getAdminApi();
    const response = await adminApi.post('/api/gamification/admin/badges', badgeData);
    return response.data;
  }
};

export const TIER_CONFIG = {
  bronze: {
    name: 'Bronze',
    minXP: 0,
    color: '#CD7F32',
    features: []
  },
  silver: {
    name: 'Silver',
    minXP: 300,
    color: '#C0C0C0',
    features: ['Study Notes', 'Videos']
  },
  gold: {
    name: 'Gold',
    minXP: 600,
    color: '#FFD700',
    features: ['Mock Tests', 'Mock Exams']
  },
  diamond: {
    name: 'Diamond',
    minXP: 3000,
    color: '#B9F2FF',
    features: ['All Content', 'Auto-Approval'],
    streakRequired: 10
  }
};

export const XP_RULES = {
  examSubmission: 20,
  examResult: {
    '0-40': 5,
    '40-60': 10,
    '60-90': 15,
    '90+': 20
  },
  premiumPurchase: {
    1: 20,
    2: 50,
    3: 70
  }
};

