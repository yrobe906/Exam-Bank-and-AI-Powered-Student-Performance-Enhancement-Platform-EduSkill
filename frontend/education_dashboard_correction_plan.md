# Education Office Dashboard Correction Plan

## Task
Edit and correct the EducationOfficeDashboard.vue to properly display Subject Leaderboard and Student Performance views with functional data integration.

## Issues Identified
1. Subject Leaderboard view shows placeholder content instead of actual data
2. Student Performance view shows placeholder content instead of actual data
3. Missing API integration for these views
4. Navigation inconsistency

## Plan

### Step 1: Add necessary imports
- Add required Heroicons imports for the new views
- Add Chart.js imports if not present

### Step 2: Add reactive state variables
- Add loading states for both views
- Add section data state for Subject Leaderboard
- Add student performance data state
- Add filter states (grade, category, search)
- Add UI state variables (selectedSection, showChartModal, etc.)

### Step 3: Add API fetching functions
- fetchSectionLeaderboard() - for Subject Leaderboard
- fetchStudentPerformance() - for Student Performance
- fetchAvailableGrades() - for filters
- fetchCategories() - for filters

### Step 4: Update navigation items
- Make Subject Leaderboard internal view
- Make Student Performance internal view
- Update handleNavClick to properly switch views

### Step 5: Implement Subject Leaderboard view template
- Add filter controls
- Add stats summary cards
- Add leaderboard cards with rankings
- Add chart modal for visualization
- Add section details modal

### Step 6: Implement Student Performance view template
- Add performance stats summary
- Add leaderboard table with rankings
- Add grade column for eduoffice view
- Add profile photos and performance indicators

### Step 7: Add computed properties
- filteredSections for Subject Leaderboard
- sortedStudents for Student Performance
- totalAttempts, totalStudents, topSection
- averageClassScore, topPerformer

### Step 8: Add helper functions
- getRankClass, getScoreClass, getScoreBarClass
- getPerformanceBadgeClass, getPerformanceLabel
- selectSection, viewSectionDetails

## Status
- [ ] TODO

