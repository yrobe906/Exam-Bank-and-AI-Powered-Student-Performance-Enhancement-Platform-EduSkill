<template>
  <div class="request-access-page">
    <!-- Unlocked Banner -->
    <div v-if="showUnlocked" class="unlocked-banner">
      <div class="banner-icon">✅</div>
      <div>
        <h3>Content Already Unlocked!</h3>
        <p>This premium content is already unlocked for you. You can access it from Available Tests.</p>
        <button @click="$router.push('/available-tests')" class="back-btn">Go to Tests</button>
      </div>
    </div>

    <!-- Unlock Form -->
    <div class="unlock-form" v-if="!showUnlocked">
      <div class="form-header"><div class="header-icon">🔓</div><h3>Request Content Unlock</h3><p>Select your preferred unlock method</p></div>
      
      <div class="form-group">
        <label><span>📄</span> Content Type</label>
        <div class="selected-content" v-if="selectedContentType"><span class="content-badge">{{ formatContentType(selectedContentType) }}</span><span class="content-id">#{{ contentId }}</span></div>
        <div class="content-preview" v-else>Click on any "Subscribe to Access" button to select content</div>
      </div>

      <div class="form-group">
        <label><span>💳</span> Unlock Method</label>
        <div class="method-grid">
          <!-- XP Points Method -->
          <div class="method-card" :class="{ selected: unlockMethod === 'points' }" @click="unlockMethod = 'points'">
            <div class="method-header"><span class="method-icon">💰</span><span class="method-name">Request Points Redemption</span><span class="check-mark" v-if="unlockMethod === 'points'">✓</span></div>
            <div class="method-details"><div><span>Required:</span><span>{{ eligibility?.xp_required || 0 }}</span></div><div><span>Available:</span><span>{{ profile?.xp_points || 0 }}</span></div></div>
            <div class="method-footer"><span class="instant-badge">⏳ Admin Approval Required</span></div>
            <div class="xp-conversion-rates" v-if="unlockMethod === 'points'"><h4>💎 XP Conversion Rates</h4><div class="rates-grid"><div v-for="rate in xpConversionRates" :key="rate.etb" class="rate-item"><span>{{ rate.etb }} ETB</span><span>→</span><span>{{ rate.xp }} XP</span></div></div></div>
          </div>

          <!-- Payment Method -->
          <div class="method-card payment" :class="{ selected: unlockMethod === 'payment' }" @click="unlockMethod = 'payment'">
            <div class="method-header"><span class="method-icon">💳</span><span class="method-name">Bank Transfer</span><span class="check-mark" v-if="unlockMethod === 'payment'">✓</span></div>
            <div class="payment-options" v-if="unlockMethod === 'payment'">
              <div v-for="bank in banks" :key="bank.id" class="payment-option" :class="{ selected: selectedPaymentMethod === bank.id }" @click.stop="selectedPaymentMethod = bank.id">
                <div class="bank-logo" :class="bank.id"><span>{{ bank.icon }}</span><span>{{ bank.name }}</span></div>
                <div class="account-details" v-if="selectedPaymentMethod === bank.id"><div @click="copyToClipboard(bank.accountName)"><span>{{ bank.accountName }}</span><span class="copy-icon">📋</span></div><div @click="copyToClipboard(bank.accountNumber)"><span>{{ bank.accountNumber }}</span><span class="copy-icon">📋</span></div></div>
              </div>
              <div class="payment-instructions"><p>📌 After payment, upload your transaction screenshot</p><p class="note">Payment will be verified within 24 hours</p></div>
              <div v-if="selectedPaymentMethod !== 'telebirr'" class="file-upload-section">
                <label>📸 Upload Payment Screenshot <span class="required">*</span></label>
                <div class="upload-zone" :class="{ 'has-file': paymentProofFile }" @dragover.prevent @drop.prevent="handleDrop" @click="triggerFileInput">
                  <div v-if="!paymentProofFile">
                    <input type="file" ref="paymentProofInput" @change="handleFileUpload" accept="image/*" class="file-input">
                    <small>JPG, PNG, WEBP, GIF (Max 5MB)</small>
                  </div>
                  <div v-else class="file-preview"><span>{{ paymentProofFile.type.includes('pdf') ? '📄' : '🖼️' }}</span><div><p>{{ paymentProofFile.name }}</p><small>{{ formatFileSize(paymentProofFile.size) }}</small></div><button @click.stop="removePaymentProof">✕</button></div>
                </div>
              </div>
              <div v-else class="telebirr-note"><p>✅ No screenshot required - Complete payment and submit</p></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Eligibility Check -->
      <div v-if="eligibility" class="eligibility-check">
        <div class="check-header" :class="{ success: eligibility?.can_unlock, error: !eligibility?.can_unlock }"><span>{{ eligibility?.can_unlock ? '✅' : '❌' }}</span><span>{{ eligibility?.can_unlock ? 'Enough Points' : 'Not Enough Points' }}</span></div>
        <div class="check-details">
          <div><span>XP Required</span><span>{{ eligibility.xp_required }}</span></div>
          <div><span>Your XP</span><span>{{ eligibility.user_xp }}</span></div>
          <div v-if="!eligibility.can_unlock"><span>XP Needed</span><span class="highlight">{{ eligibility.shortage }}</span></div>
          <div v-if="!eligibility?.can_unlock && eligibility?.reason"><span>Reason</span><span class="error-text">{{ eligibility.reason }}</span></div>
        </div>
        <div class="quick-actions" v-if="!eligibility.can_unlock && unlockMethod === 'points'"><button @click="unlockMethod = 'payment'">💳 Switch to Payment</button></div>
      </div>
      <!-- Loading eligibility -->
      <div v-else-if="!eligibility && contentId" class="eligibility-loading bg-blue-50 border-2 border-blue-200 rounded-2xl p-6 text-center">
        <div class="inline-flex items-center gap-2 mb-2">
          <div class="w-6 h-6 border-2 border-blue-200 border-t-blue-500 rounded-full animate-spin"></div>
          <span class="text-sm text-blue-700 font-medium">Checking eligibility...</span>
        </div>
        <p class="text-xs text-blue-600">Exam #{{ contentId }}</p>
      </div>

      <!-- Submit Button (always request-based) -->
      <div v-if="!canSubmit && !submitting" class="submit-disabled-hint">
        <div class="hint-icon">ℹ️</div>
        <div>
          <strong>Complete these steps to unlock:</strong>
          <ul>
            <li v-if="!selectedContentType || !contentId">👆 Click "Subscribe to Access" on premium content</li>
            <li v-if="!eligibility">⏳ Checking eligibility...</li>
            <li v-else-if="!eligibility?.can_unlock && unlockMethod === 'points'">💎 Need {{ eligibility.shortage }} more XP points</li>
<li v-if="unlockMethod === 'payment' && !selectedPaymentMethod">🏦 Select payment method</li>
<li v-if="unlockMethod === 'payment' && (selectedPaymentMethod === 'cbe' || selectedPaymentMethod === 'boa') && !paymentProofFile">📸 Upload payment screenshot</li>
          </ul>
          <button @click="unlockMethod = unlockMethod === 'points' ? 'payment' : 'points'" class="hint-btn">
            {{ unlockMethod === 'points' ? '💳 Switch to Payment' : '💰 Switch to Points' }}
          </button>
        </div>
      </div>
      <button @click="submitRequest" class="submit-btn" :class="{ 'points': unlockMethod === 'points', 'payment': unlockMethod === 'payment' }" :disabled="!canSubmit || submitting" :title="(!canSubmit || submitting) ? 'Select content and check eligibility first' : ''">

        <span v-if="!submitting">{{ unlockMethod === 'points' ? '📝 Submit Points Redemption Request' : '💳 Submit Payment Request' }}</span>
        <span v-else>Processing...</span>
      </button>

    </div>

    <!-- Transaction History -->
    <div class="transaction-history">
      <div class="section-header">
        <h2>📋 Transaction History</h2>
        {{ myRequests?.length ?? 0 }} requests
        <button @click="loadMyRequests" class="refresh-btn" title="Refresh">
          ⟳
        </button>
      </div>
      <div v-if="myRequests.length === 0" class="empty-state"><div>📭</div><h4>No Transactions Yet</h4><p>Your unlock requests will appear here</p></div>
        <div v-else class="transactions-list">
        <div v-for="req in myRequests" :key="req.id" class="transaction-card" :class="req.status">
          <div class="transaction-icon">{{ req.unlock_method === 'points' ? '💰' : '💳' }}</div>
          <div class="transaction-details">
            <div><span>{{ req.content_name || `Content #${req.content_id}` }}</span><span>{{ formatContentType(req.content_type) }}</span></div>
            <div><span>📅</span> {{ formatDate(req.created_at) }}<span v-if="req.points_used > 0">⚡ -{{ req.points_used }} XP</span></div>
          </div>
          <div class="transaction-status">
            <span class="status-badge approved-celebration" :class="req.status" v-if="req.status === 'approved'">✅ Unlocked!</span>
            <span class="status-badge" :class="req.status" v-else>{{ formatStatus(req.status) }}</span>
            <button v-if="req.status === 'approved'" @click="startExamFreely(req)" class="start-freely-btn" title="Start Exam Freely">🚀 Start Freely</button>
            <button v-if="req.status === 'pending'" @click="cancelRequest(req.id)" title="Cancel Pending Request" class="cancel-pending-btn">✕</button>

          </div>
        </div>
      </div>
    </div>

    <!-- Success/Error Modals -->
    <div v-if="showError" class="modal-overlay" @click="closeModals"><div class="modal-content error" @click.stop><div>❌</div><h2>Error</h2><p>{{ errorMessage }}</p><button @click="closeModals">Close</button></div></div>
    <div v-if="loading" class="loading-overlay"><div class="spinner"></div></div>
  </div>
</template>

<script>
import api from '@/services/api.js';
import unlockApi from '@/services/unlockApi.js';

export default {
  name: 'Premium',
  data() {
    return {
      profile: null,
      selectedContentType: '',
      contentId: null,
      contentName: '',
      unlockMethod: 'points',
      myRequests: [],
      currentRequestId: null,
      pollingInterval: null,
      isUnlocked: false,
      showUnlocked: false,
      submitting: false,
      showError: false,
      errorMessage: '',
      loading: false,
      eligibility: null,
      selectedPaymentMethod: null,
      paymentProofFile: null,
      xpConversionRates: [
        { etb: 50, xp: 150 },
        { etb: 100, xp: 200 },
        { etb: 150, xp: 350 },
        { etb: 200, xp: 400 },
        { etb: 250, xp: 450 },
        { etb: 300, xp: 500 },
        { etb: 350, xp: 550 },
        { etb: 400, xp: 700 },
        { etb: 500, xp: 3000 }
      ],
      nonTelebirrBanks: ['cbe', 'boa'],
      banks: [
        { id: 'cbe', name: 'CBE', icon: '🏦', accountName: 'Yasin Robe Wako', accountNumber: '1000 503668568' },
        { id: 'boa', name: 'Bank of Abyssinia', icon: '🏛️', accountName: 'Yasin Robe Wako', accountNumber: '241060478' },
        { id: 'telebirr', name: 'TeleBirr', icon: '📱', accountName: 'Yasin Robe Wako', accountNumber: '0952405391' }
      ]
    }
  },
  computed: {
    canSubmit() {
      console.log('canSubmit check:', {
        contentType: this.selectedContentType,
        contentId: this.contentId,
        eligibility: this.eligibility,
        method: this.unlockMethod,
        paymentMethod: this.selectedPaymentMethod,
        hasFile: !!this.paymentProofFile
      });
      // Require basic selection
      if (!this.selectedContentType || !this.contentId || !this.eligibility) return false;
      // Points require enough XP, payment does not
      if (this.unlockMethod === 'points' && !this.eligibility.can_unlock) return false;
      if (this.unlockMethod === 'payment') return this.selectedPaymentMethod && (!['cbe', 'boa'].includes(this.selectedPaymentMethod) || this.paymentProofFile);
      return false;
    }
  },
  async mounted() {
    console.log('Premium mounted, query:', this.$route.query);
    await this.loadProfile();
    await this.loadMyRequests();
    const query = this.$route.query;
    if (query.examId) {
      this.contentId = parseInt(query.examId);
      this.contentName = query.examTitle || 'Premium Content';
      this.selectedContentType = 'mock_exam';
      console.log('Loading eligibility for examId:', this.contentId);
      await this.checkEligibility();
    } else {
      console.warn('No examId in query - button will be disabled');
    }
    window.addEventListener('content-selected', e => {
      this.contentId = e.detail.id;
      this.contentName = e.detail.name;
      this.selectedContentType = 'mock_exam';
      this.checkEligibility();
    });
  },
  beforeUnmount() {
    window.removeEventListener('content-selected', () => {});
    if (this.pollingInterval) clearInterval(this.pollingInterval);
  },
  methods: {
    formatStatus(status) {
      const map = {
        pending: 'Pending',
        approved: 'Approved',
        rejected: 'Rejected'
      };
      return map[status] || status;
    },
    formatContentType(t) {
      return {
        study_note: 'Study Note',
        video: 'Video',
        mock_test: 'Mock Test',
        mock_exam: 'Mock Exam'
      }[t] || t;
    },
    formatDate(s) {
      return new Date(s).toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
    },
    formatFileSize(b) {
      if (!b) return '0 Bytes';
      const k = 1024;
      const i = Math.floor(Math.log(b) / Math.log(k));
      return parseFloat((b / Math.pow(k, i)).toFixed(2)) + ' ' + ['Bytes', 'KB', 'MB', 'GB'][i];
    },
    async copyToClipboard(t) {
      try {
        await navigator.clipboard.writeText(t);
        this.$toast?.success('Copied!');
      } catch(e) {
        console.error(e);
      }
    },
    async loadProfile() {
      try {
        const g = await import('@/services/gamificationService');
        this.profile = await g.default.getProfile();
      } catch(e) {
        console.error(e);
        this.profile = { xp_points: 0, tier: 'bronze', current_streak: 0 };
      }
    },
    async loadMyRequests() {
      try {
        this.myRequests = await unlockApi.getMyRequests(api);
      } catch(e) {
        console.error(e);
        this.myRequests = [];
      }
    },

    async checkEligibility() {
      if (!this.contentId) return;
      try {
        this.eligibility = await unlockApi.checkEligibility(api, this.contentId);
        this.isUnlocked = (await unlockApi.hasAccess(api, this.contentId))?.data?.has_access || false;
        if (this.isUnlocked) this.showUnlocked = true;
      } catch(e) {
        console.error(e);
        this.eligibility = null;  // Ensure null on error to prevent partial state
      }
    },
    handleFileUpload(e) {
      const file = e.target.files[0];
      if (file && file.type.startsWith('image/') && file.size <= 5 * 1024 * 1024) {
        this.paymentProofFile = file;
      } else {
        alert('Please upload a valid image file under 5MB');
      }
    },
    handleDrop(e) {
      const f = e.dataTransfer.files[0];
      if (f && f.type.startsWith('image/') && f.size <= 5 * 1024 * 1024) {
        this.paymentProofFile = f;
      }
    },
    triggerFileInput() {
      this.$refs.paymentProofInput?.click();
    },
    removePaymentProof() {
      this.paymentProofFile = null;
    },
    async submitRequest() {
      if (!this.canSubmit) return;

      this.submitting = true;
      try {
        let response;
        if (this.unlockMethod === 'points') {
          const points_req = this.eligibility?.xp_required || 0;
          response = await unlockApi.payWithPoints(api, this.contentId, points_req);
          this.$toast?.success(`Points redemption request submitted (pending admin approval)`);
        } else {
          response = await unlockApi.createRequest(api, this.contentId, this.unlockMethod, this.selectedPaymentMethod, this.paymentProofFile);
          this.$toast?.success('Payment request submitted successfully');
        }
        // Always reload after submit
        await this.loadMyRequests();
        await this.loadProfile();
        this.currentRequestId = response?.data?.id || response?.id;
        
        await this.loadMyRequests();
        await this.loadProfile(); // Reload to show updated XP
        this.currentRequestId = response.data?.id;
      } catch(e) {
        console.error('Submit error:', e);
        const detail = e.response?.data?.detail || e.message || 'Failed to submit request';
        this.errorMessage = detail;
        this.showError = true;
        this.$toast?.error(`Submit failed: ${detail}`);
      } finally {
        this.submitting = false;
      }
    },
    async cancelRequest(id) {
      if (confirm('Cancel this unlock request?')) {
        try {
          await unlockApi.cancelRequest(api, id);
          this.$toast?.success('Request cancelled successfully');
          await this.loadMyRequests();
        } catch (error) {
          console.error('Cancel failed:', error);
          this.errorMessage = error.response?.data?.detail || 'Failed to cancel request';
          this.showError = true;
        }
      }
    },
startExamFreely(req) {
      this.$router.push(`/take_exam/${req.exam_id || req.content_id}`);
    },
    closeModals() {
      this.showError = false;
    }
  },
  watch: {
    '$route.query'(newQuery) {
      if (newQuery.examId && (!this.contentId || newQuery.examId != this.contentId)) {
        this.contentId = parseInt(newQuery.examId);
        this.contentName = newQuery.examTitle || 'Premium Content';
        this.selectedContentType = 'mock_exam';
        this.currentRequestId = null;
        this.checkEligibility();
      }
    }
  }
}
</script>

<style scoped>
/* All styles from Premium_fixed.vue - same as original */
.request-access-page { max-width: 1000px; margin: 0 auto; padding: 24px; background: linear-gradient(135deg, #f5f7fa, #c3cfe2); min-height: 100vh; }
/* ... (paste all styles from the fixed version - omitted for brevity in this response, but include full in actual) */
.eligibility-check { border: 2px solid #e0e0e0; border-radius: 16px; overflow: hidden; margin-bottom: 24px; }
.check-header { padding: 16px; display: flex; align-items: center; gap: 12px; }
.check-header.success { background: #d4edda; color: #155724; }
.check-header.error { background: #f8d7da; color: #721c24; }
.request-access-page { max-width: 1000px; margin: 0 auto; padding: 24px; background: linear-gradient(135deg, #f5f7fa, #c3cfe2); min-height: 100vh; }
.unlocked-banner { background: linear-gradient(135deg, #d4edda, #c3e6cb); border-radius: 20px; padding: 24px; margin-bottom: 24px; display: flex; align-items: center; gap: 16px; box-shadow: 0 4px 20px rgba(40,167,69,0.2); }
.banner-icon { font-size: 32px; }
.back-btn { background: #28a745; color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; }
.unlock-form { background: white; border-radius: 24px; padding: 32px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); margin-bottom: 24px; }
.form-header { text-align: center; margin-bottom: 32px; }
.header-icon { font-size: 48px; margin-bottom: 16px; animation: bounce 2s infinite; }
.form-header h3 { margin: 0; font-size: 24px; color: #333; }
.form-header p { margin: 8px 0 0; color: #666; }
.form-group { margin-bottom: 24px; }
.form-group label { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; font-weight: 600; color: #333; }
.selected-content { display: flex; align-items: center; gap: 12px; padding: 16px; background: linear-gradient(135deg, #f5f7fa, #e9ecef); border-radius: 12px; }
.content-badge { padding: 6px 12px; background: #667eea; color: white; border-radius: 20px; font-size: 14px; }
.content-id { font-weight: 600; color: #666; }
.content-preview { padding: 16px; background: #f8f9fa; border: 2px dashed #ddd; border-radius: 12px; text-align: center; color: #999; }
.method-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
.method-card { border: 2px solid #e0e0e0; border-radius: 16px; padding: 20px; cursor: pointer; transition: 0.3s; }
.method-card:hover { border-color: #667eea; transform: translateY(-2px); box-shadow: 0 10px 30px rgba(102,126,234,0.2); }
.method-card.selected { border-color: #667eea; background: rgba(102,126,234,0.05); }
.method-header { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }
.method-icon { font-size: 32px; }
.method-name { font-weight: bold; flex: 1; }
.check-mark { width: 24px; height: 24px; border-radius: 50%; background: #667eea; color: white; display: flex; align-items: center; justify-content: center; font-size: 14px; }
.method-details > div { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f0f0f0; }
.method-footer { text-align: center; margin-top: 12px; }
.instant-badge { display: inline-block; padding: 4px 12px; background: linear-gradient(135deg, #667eea, #764ba2); color: white; border-radius: 20px; font-size: 12px; }
.xp-conversion-rates { margin-top: 16px; padding: 12px; background: #f0f9ff; border-radius: 12px; }
.xp-conversion-rates h4 { margin: 0 0 10px; font-size: 13px; color: #0369a1; }
.rates-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
.rate-item { display: flex; align-items: center; gap: 4px; padding: 6px 8px; background: white; border-radius: 6px; font-size: 11px; }
.payment-options { margin-top: 20px; display: flex; flex-direction: column; gap: 12px; }
.payment-option { border: 2px solid #e0e0e0; border-radius: 12px; overflow: hidden; transition: 0.3s; }
.payment-option.selected { border-color: #28a745; }
.bank-logo { padding: 12px; display: flex; align-items: center; gap: 12px; cursor: pointer; background: #f8f9fa; }
.bank-logo.cbe { background: linear-gradient(135deg, #003366, #002244); color: white; }
.bank-logo.boa { background: linear-gradient(135deg, #8B4513, #654321); color: white; }
.bank-logo.telebirr { background: linear-gradient(135deg, #FF6B6B, #FF4949); color: white; }
.account-details { padding: 12px; background: white; border-top: 1px solid #e0e0e0; }
.account-details > div { display: flex; justify-content: space-between; align-items: center; padding: 8px; cursor: pointer; }
.account-details > div:hover { background: #f0f0f0; border-radius: 8px; }
.copy-icon { opacity: 0; }
.account-details > div:hover .copy-icon { opacity: 1; }
.payment-instructions { margin-top: 16px; padding: 12px; background: #fff3cd; border-radius: 8px; color: #856404; }
.payment-instructions .note { font-size: 12px; margin-top: 8px; }
.file-upload-section { margin-top: 16px; }
.file-upload-section label { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; font-weight: 600; }
.required { color: #dc3545; }
.upload-zone { border: 2px dashed #ccc; border-radius: 12px; padding: 24px; text-align: center; cursor: pointer; transition: 0.3s; background: white; }
.upload-zone.has-file { border-color: #28a745; border-style: solid; }
.upload-zone:hover { border-color: #667eea; }
.file-input { position: absolute; width: 100%; height: 100%; opacity: 0; cursor: pointer; }
.upload-placeholder { display: flex; flex-direction: column; align-items: center; gap: 8px; }
.upload-placeholder div { font-size: 48px; }
.file-preview { display: flex; align-items: center; gap: 12px; padding: 8px; background: #f8f9fa; border-radius: 8px; }
.file-preview > button { width: 32px; height: 32px; border-radius: 50%; border: none; background: #dc3545; color: white; cursor: pointer; }
.telebirr-note { margin-top: 16px; padding: 12px; background: #d4edda; border-radius: 8px; color: #155724; text-align: center; }
.eligibility-check { border: 2px solid #e0e0e0; border-radius: 16px; overflow: hidden; margin-bottom: 24px; }
.check-header { padding: 16px; display: flex; align-items: center; gap: 12px; }
.check-header.success { background: #d4edda; }
.check-header.error { background: #f8d7da; }
.check-details { padding: 16px; background: #f8f9fa; }
.check-details > div { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #e0e0e0; }
.check-details > div:last-child { border-bottom: none; }
.highlight { color: #dc3545; }
.error-text { color: #dc3545; }
.quick-actions { display: flex; gap: 12px; padding: 16px; background: white; }
.quick-actions button { flex: 1; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px; background: white; cursor: pointer; }
.submit-btn { width: 100%; padding: 18px; border: none; border-radius: 16px; font-size: 18px; font-weight: bold; cursor: pointer; transition: 0.3s; }
.submit-btn.points { background: linear-gradient(135deg, #667eea, #764ba2); color: white; }
.submit-btn.payment { background: linear-gradient(135deg, #28a745, #20c997); color: white; }
.submit-btn.instant-points { background: linear-gradient(135deg, #10b981, #059669); color: white; }
.submit-btn:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0,0,0,0.2); }
.submit-btn:disabled { 
  opacity: 0.6; 
  cursor: not-allowed; 
  position: relative;
  animation: pulse-disabled 2s infinite;
}
.submit-disabled-hint {
  background: linear-gradient(135deg, #fff3cd, #ffeaa7);
  border: 2px solid #ffc107;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 16px;
  animation: slideDown 0.3s ease;
}
.submit-disabled-hint .hint-icon { font-size: 32px; margin-right: 12px; }
.submit-disabled-hint strong { display: block; margin-bottom: 12px; color: #856404; }
.submit-disabled-hint ul { margin: 0 0 16px 20px; color: #856404; }
.submit-disabled-hint li { margin-bottom: 4px; }
.hint-btn { 
  background: linear-gradient(135deg, #667eea, #764ba2); 
  color: white; 
  border: none; 
  padding: 10px 20px; 
  border-radius: 8px; 
  cursor: pointer;
  font-weight: 600;
}
.hint-btn:hover { transform: translateY(-1px); }
@keyframes pulse-disabled { 0%,100% { opacity: 0.6; } 50% { opacity: 0.4; } }
@keyframes slideDown { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }

.transaction-history { background: white; border-radius: 24px; padding: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.section-header h2 { margin: 0; }
.section-header span { padding: 6px 12px; background: #f0f0f0; border-radius: 20px; font-size: 14px; }
.empty-state { text-align: center; padding: 60px; background: #f8f9fa; border-radius: 16px; }
.empty-state > div { font-size: 64px; opacity: 0.5; }
.transactions-list { display: flex; flex-direction: column; gap: 12px; }
.transaction-card { display: flex; align-items: center; gap: 16px; padding: 16px; background: #f8f9fa; border-radius: 16px; border-left: 4px solid #ccc; }
.transaction-card.pending { border-left-color: #ffc107; }
.transaction-card.approved { border-left-color: #28a745; }
.transaction-card.rejected { border-left-color: #dc3545; }
.transaction-icon { width: 48px; height: 48px; border-radius: 12px; background: white; display: flex; align-items: center; justify-content: center; font-size: 24px; }
.transaction-details { flex: 1; }
.transaction-details > div:first-child { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
.transaction-details > div:first-child span:first-child { font-weight: 600; }
.transaction-details > div:last-child { display: flex; gap: 16px; font-size: 12px; color: #999; }
.transaction-status { display: flex; align-items: center; gap: 12px; }
.status-badge { padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; text-transform: uppercase; }
.status-badge.pending { background: #ffc107; color: #333; }
.status-badge.approved { background: #28a745; color: white; }
.status-badge.rejected { background: #dc3545; color: white; }
.status-badge.approved-celebration { animation: celebrate 2s ease-in-out infinite; box-shadow: 0 0 20px rgba(40, 167, 69, 0.5); }
.start-freely-btn { background: linear-gradient(135deg, #10b981, #059669); color: white; border: none; padding: 8px 16px; border-radius: 20px; font-size: 12px; cursor: pointer; font-weight: 600; }
.start-freely-btn:hover { transform: scale(1.05); }
.refresh-btn { background: #4f46e5; color: white; border: none; border-radius: 50%; width: 32px; height: 32px; cursor: pointer; margin-left: 12px; }
.refresh-btn:hover { background: #3730a3; }
.celebration-banner { position: fixed; top: 20px; right: 20px; background: linear-gradient(135deg, #10b981, #34d399); color: white; padding: 16px 24px; border-radius: 16px; box-shadow: 0 10px 30px rgba(16, 185, 129, 0.4); z-index: 10000; animation: slideInRight 0.5s ease; display: flex; flex-direction: column; gap: 4px; }
.modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.6); backdrop-filter: blur(5px); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal-content { background: white; padding: 32px; border-radius: 24px; text-align: center; max-width: 400px; width: 90%; }
.modal-content.error h2 { color: #dc3545; }
.modal-content > div:first-child { font-size: 64px; margin-bottom: 16px; }
.modal-content button { padding: 12px 32px; background: linear-gradient(135deg, #667eea, #764ba2); border: none; border-radius: 8px; color: white; font-weight: bold; cursor: pointer; margin-top: 16px; }
.loading-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.spinner { width: 50px; height: 50px; border: 5px solid #f3f3f3; border-top: 5px solid #667eea; border-radius: 50%; animation: spin 1s linear infinite; }
@keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
@keyframes bounce { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes celebrate { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
@keyframes slideInRight { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
@media (max-width: 768px) { .premium-stats { grid-template-columns: 1fr; } .method-grid { grid-template-columns: 1fr; } .tier-markers { display: none; } }
</style>
