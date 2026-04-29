// Unlock API functions - use with api instance
// Import as: import unlockApi from '@/services/unlockApi'
// Then: unlockApi.createRequest(api, examId, method, paymentMethod, file)

export const unlockApi = {
  // Student: Create unlock request
  async createRequest(api, examId, unlockMethod, paymentMethod = null, paymentProofFile = null) {
    const formData = new FormData();
    formData.append('exam_id', examId);
    formData.append('unlock_method', unlockMethod);
    if (paymentMethod) formData.append('payment_method', paymentMethod);
    if (paymentProofFile) formData.append('payment_proof', paymentProofFile);

    return api.post('/api/unlock/requests', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },

  // Student: Get my requests
  async getMyRequests(api, status = null) {
    const params = status ? { status } : {};
    return api.get('/api/unlock/my-requests', { params });
  },

  // Student: Check eligibility for exam
  async checkEligibility(api, examId) {
    return api.get('/api/unlock/check-eligibility', { params: { exam_id: examId } });
  },

  // Student: Check if has access
  async hasAccess(api, examId) {
    return api.get('/api/unlock/has-access', { params: { exam_id: examId } });
  },

  // Student: Calculate XP needed
  async calculateXP(api, amount) {
    return api.get('/api/unlock/calculate-xp', { params: { amount } });
  },

  // Student: Cancel request
  async cancelRequest(api, requestId) {
    return api.delete(`/api/unlock/requests/${requestId}`);
  },

  // Student: Pay with points immediately
  async payWithPoints(api, examId, pointsRequired, sectionId = null) {
    const formData = new FormData();
    formData.append('points_required', pointsRequired);
    if (sectionId !== null) formData.append('section_id', sectionId);
    return api.post(`/api/unlock/pay-points/${examId}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },

  // Admin: Get all requests
  async getAdminRequests(api, status = null) {
    const params = status ? { status } : {};
    return api.get('/api/admin/unlock/requests', { params });
  },

  // Admin: Process request (approve/reject)
  async processRequest(api, requestId, action, method = null, transactionRef = null, adminNotes = null) {
    return api.post(`/api/admin/unlock/process/${requestId}`, {
      action,
      method,
      transaction_ref: transactionRef,
      admin_notes: adminNotes
    });
  },

  // Admin: Verify payment
  async verifyPayment(api, requestId, verified, transactionRef = null) {
    return api.post(`/api/admin/unlock/verify-payment/${requestId}`, {
      verified,
      transaction_ref: transactionRef
    });
  },

  // Admin: Delete request
  async deleteRequest(api, requestId) {
    return api.delete(`/api/admin/unlock/${requestId}`);
  }
};

export default unlockApi;

