# Premium.vue - Edit Plan

## Information Gathered:

### Current Component State:
1. **Premium.vue** currently displays:
   - Profile XP (`total_xp`), tier, and unlocked content count
   - Tier progress visualization
   - Unlock form with XP Points and Bank Transfer methods
   - Payment options (CBE, Bank of Abyssinia, TeleBirr)
   - Transaction history showing requests

2. **gamificationService.js** provides:
   - `getProfile()` - returns student profile
   - `checkUnlockEligibility(contentType)` - checks unlock capability
   - `createUnlockRequest()` - creates unlock requests
   - `getMyUnlockRequests()` - retrieves user's requests
   - `getTransactions()` - gets XP transaction history

3. **Backend APIs**:
   - Exam model has `pricing_type` and `amount` (price in ETB)
   - Unlock requests track `content_id`, `content_type`, `content_name`, `unlock_method`, `payment_amount`, `payment_proof_url`

### Changes Required:
1. **XP Requirements Logic** - Based on exam price:
   - 50 ETB → 200 XP
   - 100 ETB → 300 XP
   - 150 ETB → 350 XP
   - 250 ETB → 500 XP
   - 300-400 ETB → 600 XP (Gold tier)
   - >400 ETB → 3000 XP (Diamond tier)

2. **Payment Methods** - Add image upload for bank transfer proof

3. **Form Validation** - Disable submit when:
   - Insufficient XP for selected content (XP method)
   - Bank transfer selected but no proof uploaded
   - No payment method selected

4. **Submit Request** - Send full data to backend including payment proof image

5. **Transaction History** - Display real transaction data with approved requests

## Plan:

### Step 1: Update gamificationService.js
- Add `getContentDetails(contentId, contentType)` method to fetch content with price
- Add `createPaymentRequest()` method with payment proof upload support (multipart/form-data)

### Step 2: Update Premium.vue
- Add content selection with price display
- Implement XP requirement calculation based on price
- Add file upload for payment proof
- Update validation for submit button
- Update transaction history display

### Files to Edit:
1. `c:/Users/mame computer/ISSMS Project/Frontend/src/services/gamificationService.js`
2. `c:/Users/mame computer/ISSMS Project/Frontend/src/pages/Student/Premium.vue`

### Note:
- **Admin Approval Workflow** will be implemented later as per user's instruction

