<template>
  <div class="gamification-page">
    <!-- EduSkill Header -->
    <EduskillHeader />

    <!-- Premium Banner -->
    <div class="premium-banner">
      <div class="premium-content">
        <div class="premium-icon">👑</div>
        <div class="premium-text">
          <h2>My points</h2>
        </div>
      </div>
      <div class="premium-stats">
        <div class="stat-box">
          <span class="stat-value">{{ profile?.xp_points || 0 }}</span>
          <span class="stat-label">XP</span>
        </div>
        <div class="stat-box tier-box" :class="profile?.tier">
          <span class="stat-value">{{ tierIcon }} {{ profile?.tier?.toUpperCase() || 'BRONZE' }}</span>
          <span class="stat-label">Current Tier</span>
        </div>
        <div class="stat-box">
          <span class="stat-value">🔥 {{ profile?.current_streak || 0 }}</span>
          <span class="stat-label">Day Streak</span>
        </div>
      </div>
    </div>

    <!-- Tier Progress -->
    <div class="tier-progress-section">
      <h3>Tier Progress</h3>
      <div class="tier-progress">
        <div v-for="tier in tiers" :key="tier.name" class="tier-item" :class="{ active: isTierActive(tier.name), completed: isTierCompleted(tier.name) }">
          <div class="tier-circle">
            <span class="tier-emoji">{{ tier.icon }}</span>
          </div>
          <span class="tier-name">{{ tier.name }}</span>
          <span class="tier-xp">{{ tier.minXP }}+ XP</span>
        </div>
      </div>
    </div>

    <!-- Badges Section -->
    <div class="badges-section" v-if="badges.length > 0">
      <h3>🏆 My Badges</h3>
      <div class="badges-grid">
        <div v-for="badge in badges" :key="badge.id" class="badge-item" :class="badge.tier_required">
          <div class="badge-icon">{{ badge.icon || '🏆' }}</div>
          <span class="badge-name">{{ badge.name }}</span>
          <span class="badge-tier">{{ badge.tier_required }}</span>
        </div>
      </div>
    </div>

    <!-- XP Transaction History -->
    <div class="transactions-section">
      <h3>📜 XP Transaction History</h3>
      <div v-if="transactions.length > 0" class="transactions-list">
        <div v-for="tx in transactions" :key="tx.id" class="transaction-item">
          <div class="tx-icon" :class="tx.transaction_type">
            {{ getTxIcon(tx.transaction_type) }}
          </div>
          <div class="tx-details">
            <span class="tx-type">{{ formatTxType(tx.transaction_type) }}</span>
            <span class="tx-date">{{ formatDate(tx.created_at) }}</span>
          </div>
          <div class="tx-amount" :class="tx.xp_amount > 0 ? 'positive' : 'negative'">
            {{ tx.xp_amount > 0 ? '+' : '' }}{{ tx.xp_amount }} XP
          </div>
        </div>
      </div>
      <div v-else class="no-transactions">
        <span class="empty-icon">📭</span>
        <p>No XP transactions yet</p>
        <small>Complete exams and activities to earn XP!</small>
      </div>
    </div>

    <!-- Student Point Earning System -->
    <div class="points-system">
      <div class="points-header">
        <div class="points-icon">⭐</div>
        <h2>How to Earn XP Points</h2>
        <p>Students earn XP points from learning activities. Learn how you can level up!</p>
      </div>

      <!-- Point Category A: Exam Submission -->
      <div class="point-category">
        <div class="category-badge badge-a">A</div>
        <div class="category-content">
          <h3>📝 Exam Submission Points</h3>
          <p class="category-desc">Earn XP for every exam you submit!</p>
          <div class="point-rule">
            <span class="rule-icon">📋</span>
            <span class="rule-text">1 exam submission = <strong>40 XP</strong> points</span>
          </div>
          <div class="formula-box">
            <span class="formula-label">Formula:</span>
            <span class="formula">XP = Number_of_Submissions × 40</span>
          </div>
        </div>
        <div class="category-visual visual-a">
          <span class="visual-number">40</span>
          <span class="visual-unit">XP</span>
        </div>
      </div>

      <!-- Point Category B: Exam Result Performance -->
      <div class="point-category">
        <div class="category-badge badge-b">B</div>
        <div class="category-content">
          <h3>📊 Exam Result Performance Points</h3>
          <p class="category-desc">Bonus XP based on your exam score!</p>
          <div class="score-table">
            <div class="score-row">
              <span class="score-range">0 – 40%</span>
              <span class="score-arrow">➜</span>
              <span class="score-reward">+5 XP</span>
            </div>
            <div class="score-row">
              <span class="score-range">41 – 59%</span>
              <span class="score-arrow">➜</span>
              <span class="score-reward">+10 XP</span>
            </div>
            <div class="score-row">
              <span class="score-range">60 – 90%</span>
              <span class="score-arrow">➜</span>
              <span class="score-reward">+15 XP</span>
            </div>
            <div class="score-row highlight">
              <span class="score-range">Above 90%</span>
              <span class="score-arrow">➜</span>
              <span class="score-reward">+20 XP 🌟</span>
            </div>
          </div>
          <div class="rules-note">
            <span class="note-icon">⚠️</span>
            <span>Points are awarded once per exam attempt. Unanswered questions count as wrong.</span>
          </div>
        </div>
        <div class="category-visual visual-b">
          <span class="visual-number">5-20</span>
          <span class="visual-unit">XP</span>
        </div>
      </div>


      <!-- Call to Action -->
      <div class="cta-box">
        <span class="cta-icon">🚀</span>
        <div class="cta-text">
          <strong>Start earning XP today!</strong>
          <p>Complete exams, score high, and unlock premium content to level up your learning journey.</p>
        </div>
      </div>
    </div>

    <!-- Error Modal -->
    <div v-if="showError" class="modal-overlay" @click="showError = false">
      <div class="modal-content error">
        <h2>❌ Error</h2>
        <p>{{ errorMessage }}</p>
        <button @click="showError = false">Close</button>
      </div>
    </div>

    <!-- Loading Overlay -->
    <div v-if="loading" class="loading-overlay">
      <div class="spinner"></div>
    </div>
  </div>
</template>

<script>
import EduskillHeader from '@/components/Header/EduskillHeader.vue';
import gamificationService from '@/services/gamificationService';
import { TIER_CONFIG } from '@/services/gamificationService';

export default {
  name: 'Gamification',
  components: {
    EduskillHeader
  },
  
  data() {
    return {
      profile: null,
      badges: [],
      transactions: [],
      loading: false,
      showError: false,
      errorMessage: '',
      tiers: [
        { name: 'bronze', icon: '🥉', minXP: 0 },
        { name: 'silver', icon: '🥈', minXP: 300 },
        { name: 'gold', icon: '🥇', minXP: 600 },
        { name: 'diamond', icon: '💎', minXP: 3000 }
      ]
    };
  },

  computed: {
    tierIcon() {
      const icons = {
        bronze: '🥉',
        silver: '🥈',
        gold: '🥇',
        diamond: '💎'
      };
      return icons[this.profile?.tier] || '🥉';
    },
    
    currentTierFeatures() {
      const tier = this.profile?.tier || 'bronze';
      return TIER_CONFIG[tier]?.features || [];
    }
  },

  async mounted() {
    await this.loadAllData();
  },

  methods: {
    isTierActive(tierName) {
      return this.profile?.tier === tierName;
    },
    
    isTierCompleted(tierName) {
      const tierOrder = ['bronze', 'silver', 'gold', 'diamond'];
      const currentTierIndex = tierOrder.indexOf(this.profile?.tier || 'bronze');
      const tierIndex = tierOrder.indexOf(tierName);
      return tierIndex <= currentTierIndex;
    },
    
    async loadAllData() {
      this.loading = true;
      try {
        await Promise.all([
          this.loadProfile(),
          this.loadSummary(),
          this.loadTransactions()
        ]);
      } catch (error) {
        console.error('Error loading gamification data:', error);
        this.errorMessage = 'Failed to load gamification data';
        this.showError = true;
      } finally {
        this.loading = false;
      }
    },
    
    async loadProfile() {
      try {
        this.profile = await gamificationService.getProfile();
      } catch (error) {
        console.error('Error loading profile:', error);
        // Create empty profile to prevent errors
        this.profile = {
          xp_points: 0,
          tier: 'bronze',
          current_streak: 0,
          longest_streak: 0,
          premium_purchase_count: 0
        };
      }
    },
    
    async loadSummary() {
      try {
        const summary = await gamificationService.getSummary();
        this.badges = summary.earned_badges || [];
      } catch (error) {
        console.error('Error loading summary:', error);
        this.badges = [];
      }
    },
    
    async loadTransactions() {
      try {
        this.transactions = await gamificationService.getTransactions(20);
      } catch (error) {
        console.error('Error loading transactions:', error);
        this.transactions = [];
      }
    },
    
    getTxIcon(type) {
      const icons = {
        exam_submission: '📝',
        exam_result: '📊',
        premium_purchase: '👑',
        streak_bonus: '🔥',
        bonus: '🎁',
        penalty: '❌'
      };
      return icons[type] || '⭐';
    },
    
    formatTxType(type) {
      const types = {
        exam_submission: 'Exam Submission',
        exam_result: 'Exam Result Bonus',
        premium_purchase: 'Premium Purchase',
        streak_bonus: 'Streak Bonus',
        bonus: 'Bonus',
        penalty: 'Penalty'
      };
      return types[type] || type;
    },
    
    formatDate(dateStr) {
      if (!dateStr) return '';
      const date = new Date(dateStr);
      return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    }
  }
};
</script>

<style scoped>
/* ========== GLOBAL STYLES ========== */
.gamification-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 24px;
  background: #f8fafc;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

/* ========== PREMIUM BANNER ========== */
.premium-banner {
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  border-radius: 28px;
  padding: 32px;
  color: white;
  margin-bottom: 32px;
  box-shadow: 0 20px 35px -12px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.premium-content {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 28px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
}

.premium-icon {
  font-size: 56px;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.2));
  animation: subtlePulse 3s infinite;
}

@keyframes subtlePulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.02); opacity: 0.95; }
}

.premium-text h2 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.3px;
}

.premium-stats {
  display: flex;
  gap: 16px;
}

.stat-box {
  flex: 1;
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(4px);
  border-radius: 20px;
  padding: 16px 12px;
  text-align: center;
  transition: all 0.2s ease;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.stat-box:hover {
  background: rgba(255, 255, 255, 0.12);
  transform: translateY(-2px);
}

.stat-box.tier-box {
  background: rgba(0, 0, 0, 0.3);
}

.stat-box.tier-box.bronze { background: linear-gradient(135deg, #b76e2e, #7a431d); }
.stat-box.tier-box.silver { background: linear-gradient(135deg, #94a3b8, #475569); }
.stat-box.tier-box.gold { background: linear-gradient(135deg, #eab308, #b45309); }
.stat-box.tier-box.diamond { background: linear-gradient(135deg, #a5f3fc, #0891b2); color: #0c4a6e; }

.stat-value {
  display: block;
  font-size: 28px;
  font-weight: 800;
  letter-spacing: -0.5px;
  line-height: 1.2;
}

.stat-label {
  display: block;
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  opacity: 0.75;
  margin-top: 6px;
}

/* ========== TIER PROGRESS SECTION ========== */
.tier-progress-section {
  background: white;
  border-radius: 28px;
  padding: 28px 24px;
  margin-bottom: 32px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.05);
  border: 1px solid #eef2f6;
}

.tier-progress-section h3 {
  margin: 0 0 24px 0;
  color: #1e293b;
  font-size: 20px;
  font-weight: 600;
  text-align: center;
  letter-spacing: -0.2px;
}

.tier-progress {
  display: flex;
  justify-content: space-between;
  position: relative;
  gap: 8px;
}

.tier-progress::before {
  content: '';
  position: absolute;
  top: 28px;
  left: 60px;
  right: 60px;
  height: 4px;
  background: #e2e8f0;
  border-radius: 4px;
  z-index: 0;
}

.tier-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 1;
  flex: 1;
}

.tier-circle {
  width: 60px;
  height: 60px;
  border-radius: 60px;
  background: white;
  border: 2px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
  transition: all 0.25s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.02);
}

.tier-item.completed .tier-circle {
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  border-color: #fbbf24;
  box-shadow: 0 8px 20px rgba(245, 158, 11, 0.25);
}

.tier-item.active .tier-circle {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border-color: #3b82f6;
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
  transform: scale(1.08);
}

.tier-emoji {
  font-size: 28px;
}

.tier-name {
  font-size: 13px;
  font-weight: 700;
  color: #475569;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.tier-xp {
  font-size: 11px;
  color: #94a3b8;
  margin-top: 4px;
  font-weight: 500;
}

/* ========== BADGES SECTION ========== */
.badges-section {
  background: white;
  border-radius: 28px;
  padding: 28px 24px;
  margin-bottom: 32px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.05);
  border: 1px solid #eef2f6;
}

.badges-section h3 {
  margin: 0 0 20px 0;
  color: #1e293b;
  font-size: 20px;
  font-weight: 600;
  letter-spacing: -0.2px;
}

.badges-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.badge-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 16px;
  border-radius: 24px;
  background: #f8fafc;
  min-width: 100px;
  transition: all 0.2s ease;
  border: 1px solid #eef2f6;
}

.badge-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px -12px rgba(0, 0, 0, 0.15);
  border-color: #cbd5e1;
}

.badge-item.bronze { border-top: 3px solid #b76e2e; }
.badge-item.silver { border-top: 3px solid #94a3b8; }
.badge-item.gold { border-top: 3px solid #eab308; }
.badge-item.diamond { border-top: 3px solid #06b6d4; }

.badge-icon {
  font-size: 40px;
  margin-bottom: 12px;
}

.badge-name {
  font-size: 13px;
  font-weight: 600;
  color: #1e293b;
  text-align: center;
}

.badge-tier {
  font-size: 10px;
  color: #64748b;
  text-transform: uppercase;
  margin-top: 6px;
  font-weight: 500;
  letter-spacing: 0.3px;
}

/* ========== TRANSACTIONS SECTION ========== */
.transactions-section {
  background: white;
  border-radius: 28px;
  padding: 28px 24px;
  margin-bottom: 32px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.05);
  border: 1px solid #eef2f6;
}

.transactions-section h3 {
  margin: 0 0 20px 0;
  color: #1e293b;
  font-size: 20px;
  font-weight: 600;
  letter-spacing: -0.2px;
}

.transactions-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: 420px;
  overflow-y: auto;
  padding-right: 6px;
}

.transaction-item {
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 14px 20px;
  background: #f8fafc;
  border-radius: 20px;
  transition: all 0.2s;
  border: 1px solid transparent;
}

.transaction-item:hover {
  background: #f1f5f9;
  border-color: #e2e8f0;
}

.tx-icon {
  width: 44px;
  height: 44px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  background: #eef2ff;
}

.tx-icon.exam_submission {
  background: #dbeafe;
  color: #2563eb;
}

.tx-icon.exam_result {
  background: #fef9c3;
  color: #eab308;
}

.tx-icon.premium_purchase {
  background: #e0e7ff;
  color: #7c3aed;
}

.tx-icon.streak_bonus {
  background: #ffedd5;
  color: #f97316;
}

.tx-details {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.tx-type {
  font-weight: 600;
  color: #0f172a;
  font-size: 15px;
}

.tx-date {
  font-size: 12px;
  color: #94a3b8;
  margin-top: 4px;
}

.tx-amount {
  font-weight: 700;
  font-size: 17px;
  letter-spacing: -0.2px;
}

.tx-amount.positive {
  color: #10b981;
}

.tx-amount.negative {
  color: #ef4444;
}

.no-transactions {
  text-align: center;
  padding: 48px 20px;
  background: #f8fafc;
  border-radius: 24px;
}

.no-transactions .empty-icon {
  font-size: 56px;
  display: block;
  margin-bottom: 16px;
  opacity: 0.6;
}

.no-transactions p {
  margin: 0 0 6px 0;
  color: #475569;
  font-weight: 600;
}

.no-transactions small {
  color: #94a3b8;
  font-size: 13px;
}

/* ========== POINTS SYSTEM ========== */
.points-system {
  background: white;
  border-radius: 28px;
  padding: 32px;
  margin-bottom: 32px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.05);
  border: 1px solid #eef2f6;
}

.points-header {
  text-align: center;
  margin-bottom: 40px;
}

.points-icon {
  font-size: 56px;
  margin-bottom: 12px;
  animation: gentleFloat 3s ease-in-out infinite;
}

@keyframes gentleFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

.points-header h2 {
  margin: 0 0 10px 0;
  font-size: 30px;
  font-weight: 700;
  background: linear-gradient(135deg, #1e293b 0%, #3b82f6 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  letter-spacing: -0.5px;
}

.points-header p {
  margin: 0;
  color: #64748b;
  font-size: 16px;
  line-height: 1.5;
}

.point-category {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 28px;
  background: #fefefe;
  border-radius: 24px;
  margin-bottom: 24px;
  border: 1px solid #edf2f7;
  transition: all 0.25s ease;
}

.point-category:hover {
  transform: translateY(-3px);
  box-shadow: 0 20px 30px -15px rgba(0, 0, 0, 0.1);
  border-color: #cbd5e1;
}

.category-badge {
  width: 56px;
  height: 56px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: 800;
  color: white;
  flex-shrink: 0;
  box-shadow: 0 8px 16px -6px rgba(0, 0, 0, 0.1);
}

.badge-a {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
}

.badge-b {
  background: linear-gradient(135deg, #f97316, #ea580c);
}

.badge-c {
  background: linear-gradient(135deg, #8b5cf6, #6d28d9);
}

.category-content {
  flex: 1;
}

.category-content h3 {
  margin: 0 0 6px 0;
  font-size: 20px;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.2px;
}

.category-desc {
  margin: 0 0 20px 0;
  color: #64748b;
  font-size: 14px;
}

.point-rule {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  background: #f1f5f9;
  border-radius: 16px;
  margin-bottom: 16px;
}

.rule-icon {
  font-size: 20px;
}

.rule-text {
  font-size: 15px;
  color: #334155;
}

.rule-text strong {
  color: #3b82f6;
  font-size: 17px;
}

.formula-box {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 8px 20px;
  background: #0f172a;
  border-radius: 40px;
}

.formula-label {
  color: #94a3b8;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 500;
}

.formula {
  color: #a5f3fc;
  font-family: 'JetBrains Mono', 'SF Mono', monospace;
  font-size: 13px;
  font-weight: 500;
}

.score-table {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.score-row {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 10px 16px;
  background: white;
  border-radius: 14px;
  border: 1px solid #e2e8f0;
  transition: all 0.15s;
}

.score-row.highlight {
  background: #fffbeb;
  border-color: #fde047;
}

.score-range {
  flex: 1;
  font-weight: 600;
  color: #334155;
  font-size: 14px;
}

.score-arrow {
  color: #94a3b8;
  font-size: 14px;
}

.score-reward {
  font-weight: 700;
  color: #10b981;
  font-size: 14px;
}

.score-row.highlight .score-reward {
  color: #f59e0b;
}

.rules-note {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 16px;
  background: #fef2f2;
  border-radius: 14px;
  border-left: 3px solid #f87171;
  font-size: 12px;
  color: #b91c1c;
}

.note-icon {
  font-size: 14px;
}

.purchase-tiers {
  display: flex;
  gap: 16px;
}

.purchase-tier {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 18px 12px;
  background: white;
  border-radius: 20px;
  border: 1px solid #e2e8f0;
  text-align: center;
  transition: all 0.2s;
}

.purchase-tier:hover {
  border-color: #cbd5e1;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px -8px rgba(0, 0, 0, 0.1);
}

.tier-count {
  font-size: 32px;
  font-weight: 800;
  color: #3b82f6;
  line-height: 1;
}

.tier-desc {
  font-size: 12px;
  color: #64748b;
  margin: 8px 0 12px 0;
  font-weight: 500;
}

.tier-bonus {
  font-weight: 700;
  color: #10b981;
  font-size: 15px;
}

.tier-bonus.bonus-silver {
  color: #6b7280;
}

.tier-bonus.bonus-gold {
  background: linear-gradient(135deg, #eab308, #f59e0b);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.category-visual {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.2s;
}

.visual-a {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  box-shadow: 0 12px 24px -12px rgba(59, 130, 246, 0.4);
}

.visual-b {
  background: linear-gradient(135deg, #f97316, #ea580c);
  box-shadow: 0 12px 24px -12px rgba(249, 115, 22, 0.4);
}

.visual-c {
  background: linear-gradient(135deg, #8b5cf6, #6d28d9);
  box-shadow: 0 12px 24px -12px rgba(139, 92, 246, 0.4);
}

.visual-number {
  font-size: 28px;
  font-weight: 800;
  color: white;
  line-height: 1;
}

.visual-unit {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 600;
  margin-top: 4px;
}

.cta-box {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px 32px;
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  border-radius: 28px;
  margin-top: 32px;
  box-shadow: 0 12px 30px -12px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.cta-icon {
  font-size: 48px;
  animation: bounceSoft 1.5s infinite;
}

@keyframes bounceSoft {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

.cta-text {
  color: white;
}

.cta-text strong {
  display: block;
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 6px;
  letter-spacing: -0.2px;
}

.cta-text p {
  margin: 0;
  font-size: 14px;
  opacity: 0.8;
  line-height: 1.4;
}

/* ========== LOADING ========== */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid rgba(255, 255, 255, 0.2);
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* ========== MODALS ========== */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-content {
  background: white;
  padding: 36px 32px;
  border-radius: 32px;
  text-align: center;
  max-width: 420px;
  width: 90%;
  animation: slideUp 0.25s cubic-bezier(0.2, 0.9, 0.4, 1.1);
  box-shadow: 0 30px 50px -20px rgba(0, 0, 0, 0.3);
}

@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.modal-content.error h2 {
  color: #dc2626;
  font-weight: 700;
  margin-top: 0;
}

.modal-content p {
  margin: 20px 0;
  color: #334155;
  line-height: 1.5;
}

.modal-content button {
  padding: 12px 28px;
  background: #1e293b;
  border: none;
  border-radius: 40px;
  color: white;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.modal-content button:hover {
  background: #0f172a;
  transform: scale(0.98);
}

/* ========== RESPONSIVE ========== */
@media (max-width: 860px) {
  .gamification-page {
    padding: 20px 16px;
  }
  
  .point-category {
    flex-direction: column;
    text-align: center;
    gap: 24px;
  }
  
  .category-visual {
    width: 90px;
    height: 90px;
  }
  
  .purchase-tiers {
    flex-direction: column;
    gap: 12px;
  }
  
  .score-row {
    flex-wrap: wrap;
    justify-content: center;
    gap: 8px;
  }
  
  .premium-stats {
    flex-direction: column;
    gap: 12px;
  }
  
  .tier-progress {
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
  }
  
  .tier-progress::before {
    display: none;
  }
  
  .tier-item {
    flex: 0 0 auto;
    width: 70px;
  }
  
  .badges-grid {
    justify-content: center;
  }
  
  .points-header h2 {
    font-size: 26px;
  }
}
</style>