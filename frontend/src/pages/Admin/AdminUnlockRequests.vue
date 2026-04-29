<template>
  <div class="admin-unlock-page">
    <!-- Header with gradient and animation -->
    <div class="page-header">
      <div>
        <h1>🔐 Unlock Request Management</h1>
        <p>Review and manage student content unlock requests</p>
      </div>
      <div class="stats-badge">{{ sortedRequests.length }} Requests</div>
    </div>

    <!-- Filter Bar with glass morphism -->
    <div class="filter-bar">
      <div class="filter-group">
        <select v-model="filterStatus" @change="loadRequests">
          <option value="">All Requests</option>
          <option value="pending">Pending</option>
          <option value="approved">Approved</option>
          <option value="rejected">Rejected</option>
        </select>
      </div>
      <button class="refresh-btn" @click="loadRequests">
        <span>⟳</span> Refresh
      </button>
    </div>

    <!-- Requests Table with modern design -->
    <div class="table-container" v-if="sortedRequests.length">
      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>User</th>
              <th>Content</th>
              <th>Method</th>
              <th>Status</th>
              <th>Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="req in sortedRequests" :key="req.id">
              <td class="user-cell">
                <div class="user-info">
                  <div class="user-avatar">{{ getUserInitial(req.user_name) }}</div>
                  <div class="user-details">
                    <strong>{{ req.user_name || 'Unknown' }}</strong>
                    <small>{{ req.user_email }}</small>
                    <div class="user-badges">
                      <span class="xp-badge">💎 {{ req.user_xp }} XP</span>
                      <span :class="['tier-badge', req.user_tier]">{{ req.user_tier }}</span>
                      <span class="streak-badge">🔥 {{ req.user_streak }}</span>
                    </div>
                  </div>
                </div>
              </td>
              <td class="content-cell">
                <strong>{{ req.exam_name || `ID: ${req.content_id || req.exam_id}` }}</strong>
                <small>{{ formatContentType(req.content_type) }}</small>
              </td>
              <td class="method-cell">
                <span class="method-badge" :class="req.unlock_method">
                  {{ req.unlock_method === 'payment' ? '💳 Payment' : '💰 Points' }}
                </span>
                <span v-if="req.points_used" class="points-used">-{{ req.points_used }} XP</span>
              </td>
              <td class="status-cell">
                <span class="status-badge" :class="req.status">{{ req.status }}</span>
              </td>
              <td class="date-cell">{{ formatDate(req.created_at) }}</td>
              <td class="actions-cell">
                <div class="action-buttons">
                  <button v-if="req.status === 'pending'" @click="openApprovalModal(req)" class="btn-approve" title="Approve Request">
                    ✅ Approve
                  </button>
                  <button v-if="req.status === 'pending'" @click="openApprovalModal(req, 'reject')" class="btn-reject" title="Reject Request">
                    ❌ Reject
                  </button>
                  <button class="btn-view" @click="viewDetails(req)" title="View Details">
                    👁️ View
                  </button>
                  <button class="btn-delete" @click="confirmDelete(req.id)" title="Delete Request">
                    🗑️
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-else class="empty-state">
      <div class="empty-icon">📭</div>
      <p>No unlock requests found</p>
      <small>Try changing the filter</small>
    </div>

    <!-- Enhanced Details Modal -->
    <div v-if="showDetailsModal" class="modal-overlay" @click="closeDetailsModal">
      <div class="modal-container details-modal" @click.stop>
        <div class="modal-header">
          <h2>
            <span class="header-icon">📋</span>
            Request Details
          </h2>
          <button class="close-btn" @click="closeDetailsModal">✕</button>
        </div>
        
        <div class="modal-body" v-if="selectedRequest">
          <!-- User Information Section -->
          <div class="detail-section user-section">
            <div class="section-header">
              <span class="section-icon">👤</span>
              <h3>User Information</h3>
            </div>
            <div class="detail-grid">
              <div class="detail-item">
                <label>Full Name</label>
                <span class="detail-value">{{ selectedRequest.user_name || 'N/A' }}</span>
              </div>
              <div class="detail-item">
                <label>Email Address</label>
                <span class="detail-value">{{ selectedRequest.user_email }}</span>
              </div>
              <div class="detail-item">
                <label>XP Points</label>
                <span class="detail-value xp-value">💎 {{ selectedRequest.user_xp || 0 }}</span>
              </div>
              <div class="detail-item">
                <label>Tier Level</label>
                <span :class="['tier-badge', selectedRequest.user_tier]">{{ selectedRequest.user_tier || 'bronze' }}</span>
              </div>
              <div class="detail-item">
                <label>Streak</label>
                <span class="detail-value streak-value">🔥 {{ selectedRequest.user_streak || 0 }} days</span>
              </div>
            </div>
          </div>

          <!-- Content Information Section -->
          <div class="detail-section content-section">
            <div class="section-header">
              <span class="section-icon">📄</span>
              <h3>Content Information</h3>
            </div>
            <div class="detail-grid">
              <div class="detail-item">
                <label>Content Type</label>
                <span class="content-type-badge">{{ formatContentType(selectedRequest.content_type) }}</span>
              </div>
              <div class="detail-item">
                <label>Content ID</label>
                <span class="detail-value">#{{ selectedRequest.content_id || selectedRequest.exam_id }}</span>
              </div>
              <div class="detail-item full-width">
                <label>Content Name</label>
                <span class="detail-value highlight">{{ selectedRequest.content_name || selectedRequest.exam_name || 'N/A' }}</span>
              </div>
            </div>
          </div>

          <!-- Payment Method Section -->
          <div class="detail-section payment-section">
            <div class="section-header">
              <span class="section-icon">💳</span>
              <h3>Payment Information</h3>
            </div>
            <div class="detail-grid">
              <div class="detail-item">
                <label>Unlock Method</label>
                <span class="method-badge" :class="selectedRequest.unlock_method">
                  {{ selectedRequest.unlock_method === 'payment' ? '💳 Bank Transfer' : '💰 Points Redemption' }}
                </span>
              </div>
              <div class="detail-item" v-if="selectedRequest.unlock_method === 'payment'">
                <label>Amount</label>
                <span class="detail-value amount-value">{{ selectedRequest.price || '0' }} ETB</span>
              </div>
              <div class="detail-item" v-if="selectedRequest.unlock_method === 'payment'">
                <label>Payment Method</label>
                <span class="detail-value">{{ selectedRequest.payment_method || 'Bank Transfer' }}</span>
              </div>
              <div class="detail-item" v-if="selectedRequest.unlock_method === 'payment' && selectedRequest.transaction_ref">
                <label>Transaction Ref</label>
                <span class="detail-value ref-value">{{ selectedRequest.transaction_ref }}</span>
              </div>
              <div class="detail-item" v-if="selectedRequest.unlock_method === 'points'">
                <label>Points Required</label>
                <span class="detail-value points-value">{{ selectedRequest.points_required || 0 }} XP</span>
              </div>
              <div class="detail-item">
                <label>Request Status</label>
                <span class="status-badge" :class="selectedRequest.status">{{ selectedRequest.status }}</span>
              </div>
              <div class="detail-item">
                <label>Request Date</label>
                <span class="detail-value">{{ formatDate(selectedRequest.created_at) }}</span>
              </div>
            </div>
          </div>

          <!-- Payment Proof Section (only for bank transfer) -->
          <div v-if="selectedRequest.unlock_method === 'payment'" class="detail-section proof-section">
            <div class="section-header">
              <span class="section-icon">📸</span>
              <h3>Payment Proof</h3>
              <button 
                v-if="selectedRequest.payment_proof_path"
                @click="openPaymentProofModal"
                class="btn-view-proof"
              >
                View Full Image
              </button>
            </div>
            <div class="proof-preview" v-if="selectedRequest.payment_proof_path" @click="openPaymentProofModal">
              <img 
                :src="getPaymentProofUrl(selectedRequest.payment_proof_path)" 
                alt="Payment Proof Preview"
                @error="previewError = true"
                @load="previewError = false"
                class="proof-thumbnail"
              />
              <div class="proof-overlay">
                <span>🔍 Click to enlarge</span>
              </div>
            </div>
            <div v-else class="no-proof">
              <span>📭</span>
              <p>No payment proof uploaded</p>
            </div>
          </div>

          <!-- Admin Notes -->
          <div v-if="selectedRequest.admin_notes" class="detail-section notes-section">
            <div class="section-header">
              <span class="section-icon">📝</span>
              <h3>Admin Notes</h3>
            </div>
            <p class="admin-notes">{{ selectedRequest.admin_notes }}</p>
          </div>

          <!-- Action Buttons -->
          <div class="modal-actions" v-if="selectedRequest.status === 'pending'">
            <button class="btn-approve-modal" @click="openApprovalModal(selectedRequest, 'approve')">
              ✅ Approve Request
            </button>
            <button class="btn-reject-modal" @click="openApprovalModal(selectedRequest, 'reject')">
              ❌ Reject Request
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Approval Modal -->
    <div v-if="showApprovalModal" class="modal-overlay" @click="showApprovalModal = false">
      <div class="modal-container" @click.stop>
        <div class="modal-header">
          <h2>{{ approvalAction === 'approve' ? 'Approve Request' : 'Reject Request' }}</h2>
          <button class="close-btn" @click="showApprovalModal = false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Action</label>
            <div class="action-toggle">
              <button @click="approvalAction = 'approve'" :class="['toggle-btn', { active: approvalAction === 'approve' }]">✅ Approve</button>
              <button @click="approvalAction = 'reject'" :class="['toggle-btn', { active: approvalAction === 'reject' }]">❌ Reject</button>
            </div>
          </div>
          <div v-if="approvalAction === 'approve'" class="form-group">
            <label>Unlock Method</label>
            <select v-model="approvalMethod" class="form-input">
              <option value="points">💰 Points</option>
              <option value="payment">💳 Payment</option>
            </select>
          </div>
          <div class="form-group">
            <label>Transaction Ref (optional)</label>
            <input v-model="approvalTransactionRef" type="text" class="form-input" placeholder="Enter reference if payment">
          </div>
          <div class="form-group">
            <label>Admin Notes (optional)</label>
            <textarea v-model="adminNotes" class="form-input" rows="3" placeholder="Additional notes..."></textarea>
          </div>
        </div>
        <div class="modal-actions">
          <button class="btn-cancel" @click="showApprovalModal = false">Cancel</button>
          <button class="btn-process" @click="submitApproval" :disabled="loading">Process Request</button>
        </div>
      </div>
    </div>

    <!-- Payment Proof Full Modal -->
    <div v-if="showPaymentProofModal" class="modal-overlay" @click="showPaymentProofModal = false">
      <div class="modal-container proof-modal" @click.stop>
        <div class="modal-header">
          <h2>📸 Payment Proof</h2>
          <div class="header-actions">
            <button 
              v-if="selectedRequest?.payment_proof_path"
              @click="downloadPaymentProof"
              class="btn-download"
            >
              📥 Download
            </button>
            <button class="close-btn" @click="showPaymentProofModal = false">✕</button>
          </div>
        </div>
        <div class="modal-body proof-body">
          <div class="proof-full-container" v-if="selectedRequest?.payment_proof_path && !proofError">
            <img 
              :src="getPaymentProofUrl(selectedRequest.payment_proof_path)" 
              alt="Payment Proof Full"
              @error="onProofError"
              @load="onProofLoad"
              class="proof-full-image"
            />
          </div>
          <div v-else-if="proofError" class="error-state">
            <span>❌</span>
            <p>Failed to load payment proof</p>
            <small>The file may be missing or corrupted</small>
          </div>
          <div v-else-if="proofLoading" class="loading-state">
            <div class="spinner"></div>
            <p>Loading payment proof...</p>
          </div>
          <div v-else class="empty-state">
            <span>📭</span>
            <p>No payment proof available</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirm Modal -->
    <div v-if="showDeleteConfirm" class="modal-overlay" @click="cancelDelete">
      <div class="modal-container" @click.stop>
        <div class="modal-header">
          <h2>Delete Request</h2>
          <button class="close-btn" @click="cancelDelete">✕</button>
        </div>
        <div class="modal-body">
          <p>Are you sure you want to delete this unlock request? This action cannot be undone.</p>
        </div>
        <div class="modal-actions">
          <button class="btn-cancel" @click="cancelDelete">Cancel</button>
          <button class="btn-delete-modal" @click="deleteRequest" :disabled="loading">Delete</button>
        </div>
      </div>
    </div>

    <div v-if="loading" class="global-loading">
      <div class="spinner"></div>
    </div>
  </div>
</template>

<script>
import unlockApi from '@/services/unlockApi.js';
import api from '@/services/api.js';

export default {
  name: 'AdminUnlockRequests',
  data() {
    return {
      adminApi: null,
      requests: [],
      filterStatus: '',
      loading: false,
      deletingId: null,
      showDeleteConfirm: false,
      showDetailsModal: false,
      showApprovalModal: false,
      showPaymentProofModal: false,
      selectedRequest: null,
      approvalAction: 'approve',
      approvalMethod: 'points',
      adminNotes: '',
      approvalTransactionRef: '',
      transactionRef: '',
      proofError: false,
      proofLoading: false,
      previewError: false
    };
  },
  computed: {
    sortedRequests() {
      const activeRequests = this.requests.filter(r => r.status !== 'deleted');
      if (!Array.isArray(activeRequests)) return [];
      const order = { pending: 0, approved: 1, rejected: 2 };
      return [...activeRequests].sort((a, b) => {
        const statusOrder = (order[a.status] || 3) - (order[b.status] || 3);
        return statusOrder || new Date(b.created_at) - new Date(a.created_at);
      });
    }
  },
  mounted() {
    this.adminApi = api;
    this.loadRequests();
  },
  methods: {
    async loadRequests() {
      if (!this.adminApi) return;
      this.loading = true;
      try {
        this.requests = await unlockApi.getAdminRequests(this.adminApi, this.filterStatus);
      } catch(e) {
        console.error('Failed to load requests:', e);
        alert('Failed to load requests: ' + (e.message || e));
        this.requests = [];
      } finally {
        this.loading = false;
      }
    },
    
    getUserInitial(name) {
      if (!name) return '?';
      return name.charAt(0).toUpperCase();
    },
    
    viewDetails(req) {
      this.selectedRequest = { ...req };
      this.previewError = false;
      this.proofError = false;
      this.proofLoading = false;
      this.showDetailsModal = true;
    },
    
    closeDetailsModal() {
      this.showDetailsModal = false;
      this.selectedRequest = null;
    },
    
    openApprovalModal(req, action = 'approve') {
      this.closeDetailsModal();
      this.selectedRequest = req;
      this.approvalAction = action;
      this.approvalMethod = req.unlock_method || 'points';
      this.adminNotes = '';
      this.approvalTransactionRef = req.transaction_reference || '';
      this.showApprovalModal = true;
    },
    
    async submitApproval() {
      if (!this.approvalAction || !this.adminApi) return;
      this.loading = true;
      try {
        await unlockApi.processRequest(this.adminApi, this.selectedRequest.id, this.approvalAction, 
          this.approvalMethod, this.approvalTransactionRef, this.adminNotes);
        alert(this.approvalAction === 'approve' ? 'Request approved!' : 'Request rejected!');
        this.showApprovalModal = false;
        this.loadRequests();
      } catch(e) {
        alert('Failed: ' + (e.message || e));
      } finally {
        this.loading = false;
      }
    },
    
    openPaymentProofModal() {
      this.showDetailsModal = false;
      this.showPaymentProofModal = true;
      this.proofLoading = true;
      this.proofError = false;
    },
    
    downloadPaymentProof() {
      if (!this.selectedRequest?.payment_proof_path) return;
      const url = this.getPaymentProofUrl(this.selectedRequest.payment_proof_path);
      const link = document.createElement('a');
      link.href = url;
      link.download = `payment_proof_${this.selectedRequest.id}.png`;
      link.target = '_blank';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },
    
    getPaymentProofUrl(path) {
      if (!path) return null;
      if (path.startsWith('http')) return path;
      const normalizedPath = path.startsWith('/') ? path : '/' + path;
      return `http://127.0.0.1:8000${normalizedPath}`;
    },
    
    formatContentType(t) {
      const types = {
        study_note: 'Study Note',
        video: 'Video',
        mock_test: 'Mock Test',
        mock_exam: 'Mock Exam'
      };
      return types[t] || t;
    },
    
    formatDate(d) {
      return new Date(d).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    
    confirmDelete(id) {
      this.deletingId = id;
      this.showDeleteConfirm = true;
    },
    
    async deleteRequest() {
      if (!this.deletingId || !this.adminApi) return;
      this.loading = true;
      try {
        await unlockApi.deleteRequest(this.adminApi, this.deletingId);
        this.loadRequests();
        alert('Request deleted successfully');
      } catch(e) {
        alert('Failed to delete: ' + (e.message || e));
      } finally {
        this.loading = false;
        this.deletingId = null;
        this.showDeleteConfirm = false;
      }
    },
    
    cancelDelete() {
      this.deletingId = null;
      this.showDeleteConfirm = false;
    },
    
    onProofLoad() {
      this.proofLoading = false;
      this.proofError = false;
    },
    
    onProofError() {
      this.proofLoading = false;
      this.proofError = true;
    }
  }
};
</script>

<style scoped>
/* Modern CSS Reset & Base Styles - White/Light Theme */
.admin-unlock-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 50%, #e2e8f0 100%);
  padding: 28px 32px;
  color: #1e293b;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* Header Styles */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  flex-wrap: wrap;
  gap: 16px;
}

.page-header h1 {
  font-size: clamp(20px, 5vw, 28px);
  font-weight: 700;
  background: linear-gradient(135deg, #4f46e5, #7c3aed, #ec4899);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  margin: 0;
  letter-spacing: -0.3px;
}

.page-header p {
  color: #64748b;
  margin: 6px 0 0;
  font-size: clamp(12px, 3vw, 14px);
}

.stats-badge {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  padding: 8px 20px;
  border-radius: 40px;
  font-weight: 600;
  font-size: 14px;
  color: white;
  white-space: nowrap;
  box-shadow: 0 2px 8px rgba(79, 70, 229, 0.2);
}

/* Filter Bar */
.filter-bar {
  display: flex;
  gap: 16px;
  margin-bottom: 28px;
  flex-wrap: wrap;
}

.filter-group {
  flex: 1;
  min-width: 180px;
  max-width: 280px;
}

.filter-group select {
  width: 100%;
  padding: 10px 20px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  color: #1e293b;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.filter-group select:hover,
.filter-group select:focus {
  border-color: #4f46e5;
  outline: none;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.refresh-btn {
  padding: 10px 24px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  color: #4f46e5;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
  white-space: nowrap;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.refresh-btn:hover {
  background: #4f46e5;
  color: white;
  border-color: #4f46e5;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
}

/* Table Container */
.table-container {
  background: white;
  border-radius: 20px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
  overflow: hidden;
}

.table-wrapper {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

table {
  width: 100%;
  border-collapse: collapse;
  min-width: 800px;
}

th {
  padding: 16px 20px;
  text-align: left;
  color: #64748b;
  font-weight: 600;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
  white-space: nowrap;
}

td {
  padding: 16px 20px;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
}

tr:hover td {
  background: #f8fafc;
}

/* User Cell */
.user-cell {
  min-width: 240px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
  color: white;
  flex-shrink: 0;
}

.user-details {
  flex: 1;
  min-width: 0;
}

.user-details strong {
  display: block;
  color: #1e293b;
  font-size: 14px;
  font-weight: 600;
  word-break: break-word;
}

.user-details small {
  font-size: 11px;
  color: #64748b;
  display: block;
  margin-top: 2px;
  word-break: break-all;
}

.user-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 6px;
}

.xp-badge, .streak-badge {
  font-size: 9px;
  padding: 2px 8px;
  border-radius: 20px;
  background: #f1f5f9;
  color: #475569;
  white-space: nowrap;
}

.tier-badge {
  font-size: 9px;
  padding: 2px 8px;
  border-radius: 20px;
  font-weight: 600;
  text-transform: uppercase;
  white-space: nowrap;
}

.tier-badge.bronze { background: #fef3c7; color: #d97706; }
.tier-badge.silver { background: #f1f5f9; color: #475569; }
.tier-badge.gold { background: #fef3c7; color: #d97706; }
.tier-badge.diamond { background: #cffafe; color: #0891b2; }

/* Content Cell */
.content-cell strong {
  display: block;
  color: #1e293b;
  font-size: 14px;
  word-break: break-word;
}

.content-cell small {
  font-size: 11px;
  color: #64748b;
  display: block;
  margin-top: 2px;
}

/* Method & Status Badges */
.method-badge, .status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.method-badge.points {
  background: #dcfce7;
  color: #166534;
}

.method-badge.payment {
  background: #ede9fe;
  color: #5b21b6;
}

.status-badge.pending {
  background: #fef3c7;
  color: #b45309;
}

.status-badge.approved {
  background: #dcfce7;
  color: #166534;
}

.status-badge.rejected {
  background: #fee2e2;
  color: #991b1b;
}

.points-used {
  font-size: 10px;
  color: #64748b;
  margin-left: 8px;
  white-space: nowrap;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.btn-approve, .btn-reject, .btn-view, .btn-delete {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  white-space: nowrap;
}

.btn-approve {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.btn-approve:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.btn-reject {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
}

.btn-reject:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.btn-view {
  background: #f1f5f9;
  color: #4f46e5;
  border: 1px solid #e2e8f0;
}

.btn-view:hover {
  background: #4f46e5;
  color: white;
  border-color: #4f46e5;
  transform: translateY(-1px);
}

.btn-delete {
  background: #fef2f2;
  color: #ef4444;
  border: 1px solid #fee2e2;
}

.btn-delete:hover {
  background: #ef4444;
  color: white;
  transform: translateY(-1px);
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 20px;
  border: 1px solid #e2e8f0;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state p {
  color: #64748b;
  margin-bottom: 8px;
}

.empty-state small {
  color: #94a3b8;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-container {
  background: white;
  border-radius: 28px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  border: 1px solid #e2e8f0;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.details-modal {
  max-width: 750px;
}

.proof-modal {
  max-width: 900px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e2e8f0;
  position: sticky;
  top: 0;
  background: white;
  z-index: 10;
  flex-wrap: wrap;
  gap: 12px;
}

.modal-header h2 {
  margin: 0;
  font-size: clamp(16px, 4vw, 20px);
  display: flex;
  align-items: center;
  gap: 10px;
  color: #1e293b;
}

.header-icon, .section-icon {
  font-size: 20px;
}

.close-btn {
  background: #f1f5f9;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 10px;
  color: #64748b;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  background: #fee2e2;
  color: #ef4444;
}

.modal-body {
  padding: 24px;
}

/* Detail Sections */
.detail-section {
  background: #f8fafc;
  border-radius: 20px;
  padding: 20px;
  margin-bottom: 20px;
  border: 1px solid #e2e8f0;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 18px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e2e8f0;
  flex-wrap: wrap;
}

.section-header h3 {
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
  flex: 1;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.detail-item.full-width {
  grid-column: 1 / -1;
}

.detail-item label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #64748b;
  font-weight: 600;
}

.detail-value {
  font-size: 14px;
  font-weight: 500;
  color: #1e293b;
  word-break: break-word;
}

.xp-value, .points-value {
  color: #0891b2;
  font-weight: 600;
}

.amount-value {
  color: #d97706;
  font-weight: 600;
}

.ref-value {
  font-family: monospace;
  font-size: 12px;
  background: #f1f5f9;
  padding: 4px 8px;
  border-radius: 6px;
  display: inline-block;
  word-break: break-all;
}

.highlight {
  color: #4f46e5;
  font-weight: 600;
}

/* Proof Preview */
.proof-section .section-header {
  justify-content: space-between;
}

.btn-view-proof {
  background: #ede9fe;
  border: 1px solid #c4b5fd;
  padding: 6px 14px;
  border-radius: 10px;
  color: #5b21b6;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.btn-view-proof:hover {
  background: #4f46e5;
  color: white;
  border-color: #4f46e5;
  transform: translateY(-1px);
}

.proof-preview {
  position: relative;
  cursor: pointer;
  border-radius: 16px;
  overflow: hidden;
  max-width: 100%;
  width: fit-content;
  margin-top: 12px;
}

.proof-thumbnail {
  width: 100%;
  height: auto;
  max-height: 150px;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.proof-preview:hover .proof-thumbnail {
  transform: scale(1.02);
}

.proof-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
  padding: 12px;
  text-align: center;
  opacity: 0;
  transition: opacity 0.2s;
}

.proof-preview:hover .proof-overlay {
  opacity: 1;
}

.proof-overlay span {
  font-size: 12px;
  color: white;
}

.no-proof {
  text-align: center;
  padding: 30px;
  background: #f1f5f9;
  border-radius: 16px;
}

.no-proof span {
  font-size: 48px;
  opacity: 0.5;
}

.no-proof p {
  margin-top: 12px;
  color: #64748b;
  font-size: 13px;
}

/* Admin Notes */
.admin-notes {
  background: #f1f5f9;
  padding: 16px;
  border-radius: 12px;
  font-size: 13px;
  color: #1e293b;
  line-height: 1.5;
  margin: 0;
  border-left: 3px solid #4f46e5;
  word-break: break-word;
}

/* Modal Actions */
.modal-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
  flex-wrap: wrap;
}

.btn-approve-modal, .btn-reject-modal, .btn-process, .btn-cancel, .btn-delete-modal {
  flex: 1;
  padding: 12px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  text-align: center;
}

.btn-approve-modal {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.btn-approve-modal:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.btn-reject-modal {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
}

.btn-reject-modal:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.btn-process {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  color: white;
}

.btn-cancel {
  background: #f1f5f9;
  color: #64748b;
}

.btn-delete-modal {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
}

/* Form Styles */
.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 13px;
  font-weight: 500;
  color: #475569;
}

.form-input, .action-input {
  width: 100%;
  padding: 12px 14px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  color: #1e293b;
  font-size: 14px;
  transition: all 0.2s;
}

.form-input:focus, .action-input:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

textarea.form-input {
  resize: vertical;
  font-family: inherit;
}

.action-toggle {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.toggle-btn {
  flex: 1;
  padding: 10px;
  border-radius: 10px;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
}

.toggle-btn.active {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  color: white;
  border-color: transparent;
}

/* Proof Full Modal */
.proof-body {
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f8fafc;
}

.proof-full-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  padding: 20px;
}

.proof-full-image {
  max-width: 100%;
  max-height: 80vh;
  border-radius: 12px;
  object-fit: contain;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

.btn-download {
  background: linear-gradient(135deg, #0891b2, #06b6d4);
  border: none;
  padding: 8px 16px;
  border-radius: 10px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-download:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(6, 182, 212, 0.3);
}

/* Loading States */
.global-loading {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(79, 70, 229, 0.2);
  border-top-color: #4f46e5;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-state {
  text-align: center;
  padding: 40px;
}

.error-state span {
  font-size: 48px;
  display: block;
  margin-bottom: 16px;
}

.loading-state {
  text-align: center;
  padding: 40px;
}

.loading-state .spinner {
  margin: 0 auto 16px;
}

/* ============================================
   RESPONSIVE STYLES
   ============================================ */

/* Tablet and Medium Screens (768px - 1024px) */
@media (max-width: 1024px) {
  .admin-unlock-page {
    padding: 20px 24px;
  }
  
  .detail-grid {
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  }
}

/* Tablet Portrait (600px - 768px) */
@media (max-width: 768px) {
  .admin-unlock-page {
    padding: 16px;
  }
  
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .stats-badge {
    align-self: flex-start;
  }
  
  .filter-bar {
    flex-direction: column;
  }
  
  .filter-group {
    max-width: 100%;
  }
  
  .refresh-btn {
    justify-content: center;
  }
  
  .table-wrapper {
    margin: 0 -1px;
  }
  
  table {
    min-width: 700px;
  }
  
  th, td {
    padding: 12px 16px;
  }
  
  .modal-container {
    margin: 16px;
    max-height: 85vh;
  }
  
  .modal-header {
    padding: 16px 20px;
  }
  
  .modal-body {
    padding: 20px;
  }
  
  .detail-section {
    padding: 16px;
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .section-header h3 {
    width: 100%;
  }
  
  .proof-section .section-header {
    flex-direction: row;
    flex-wrap: wrap;
  }
  
  .modal-actions {
    flex-direction: column;
  }
  
  .btn-approve-modal, .btn-reject-modal, .btn-process, .btn-cancel, .btn-delete-modal {
    width: 100%;
  }
  
  .action-toggle {
    flex-direction: column;
  }
  
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
}

/* Mobile Small (up to 480px) */
@media (max-width: 480px) {
  .admin-unlock-page {
    padding: 12px;
  }
  
  .page-header h1 {
    font-size: 18px;
  }
  
  .page-header p {
    font-size: 12px;
  }
  
  .stats-badge {
    font-size: 12px;
    padding: 6px 16px;
  }
  
  .filter-group select, .refresh-btn {
    padding: 8px 16px;
    font-size: 13px;
  }
  
  th, td {
    padding: 10px 12px;
  }
  
  .user-avatar {
    width: 32px;
    height: 32px;
    font-size: 14px;
  }
  
  .user-details strong {
    font-size: 13px;
  }
  
  .user-details small {
    font-size: 10px;
  }
  
  .xp-badge, .streak-badge, .tier-badge {
    font-size: 8px;
    padding: 1px 6px;
  }
  
  .method-badge, .status-badge {
    font-size: 10px;
    padding: 3px 10px;
  }
  
  .btn-approve, .btn-reject, .btn-view, .btn-delete {
    padding: 4px 8px;
    font-size: 10px;
  }
  
  .action-buttons {
    gap: 4px;
  }
  
  .modal-header h2 {
    font-size: 16px;
  }
  
  .modal-header {
    padding: 14px 16px;
  }
  
  .modal-body {
    padding: 16px;
  }
  
  .detail-section {
    padding: 14px;
    margin-bottom: 14px;
  }
  
  .section-header h3 {
    font-size: 14px;
  }
  
  .detail-item label {
    font-size: 10px;
  }
  
  .detail-value {
    font-size: 13px;
  }
  
  .proof-thumbnail {
    max-height: 120px;
  }
  
  .btn-view-proof {
    padding: 4px 10px;
    font-size: 11px;
  }
  
  .empty-state {
    padding: 40px 16px;
  }
  
  .empty-icon {
    font-size: 48px;
  }
}

/* Landscape orientation for mobile */
@media (max-width: 768px) and (orientation: landscape) {
  .modal-container {
    max-height: 90vh;
  }
  
  .modal-body {
    max-height: calc(90vh - 60px);
    overflow-y: auto;
  }
  
  .proof-full-image {
    max-height: 70vh;
  }
}

/* Touch device optimizations */
@media (hover: none) and (pointer: coarse) {
  .btn-approve, .btn-reject, .btn-view, .btn-delete,
  .refresh-btn, .filter-group select,
  .btn-view-proof, .btn-download,
  .toggle-btn, .modal-actions button {
    min-height: 44px;
  }
  
  .action-buttons button {
    min-height: 36px;
  }
  
  .proof-preview {
    cursor: pointer;
  }
  
  .proof-overlay {
    opacity: 1;
    background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
  }
  
  .proof-overlay span {
    font-size: 11px;
  }
}

/* Print styles */
@media print {
  .admin-unlock-page {
    background: white;
    padding: 20px;
    color: black;
  }
  
  .filter-bar, .action-buttons, .modal-overlay, .global-loading,
  .btn-view-proof, .btn-download, .modal-actions {
    display: none !important;
  }
  
  .table-container {
    background: white;
    box-shadow: none;
    border: 1px solid #ddd;
  }
  
  th, td {
    color: black;
    border-color: #ddd;
  }
  
  .status-badge, .method-badge {
    border: 1px solid #ccc;
    background: #f5f5f5 !important;
    color: black !important;
  }
}
</style>