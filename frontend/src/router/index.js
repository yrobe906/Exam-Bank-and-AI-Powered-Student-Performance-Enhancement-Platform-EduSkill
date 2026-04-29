import { createRouter, createWebHistory } from "vue-router";

/* Pages */
import Home from "@/pages/Home.vue";
import Portfolio from "@/views/portifolio.vue";
import exam_bank from "@/pages/Exam_bank.vue";
import register from "@/pages/Register.vue";
import login from "@/pages/Login.vue";
import StudentDashboard from "@/pages/StudentDashboard.vue";
import users from "@/pages/Users.vue";
import admin_dashboard from "@/pages/Admin/AdminDashboard.vue";
import AdminAddLibrary from "@/pages/Admin/AdminAddLibrary.vue";
import AdminAddFlashcards from "@/pages/Admin/AdminAddFlashcards.vue";
import AdminLogin from "../pages/Admin/AdminLogin.vue";
import PendingUsers from "../pages/Admin/PendingUsers.vue";
import AdminManageForum from "../pages/Admin/AdminManageForum.vue";
import UserNotification from "../pages/Users/UserNotification.vue";
import UserLogin from "../pages/Users/UserLogin.vue";
import UserEdit from "../pages/Users/UserEdit.vue";
import ForgotPassword from "../pages/ForgotPassword.vue";
import ResetPassword from "../pages/ResetPassword.vue";
import TeacherDashboard from "../pages/Teacher/TeacherDashboard.vue";
import TeacherRoom from "../pages/Teacher/TeacherRoom.vue";
import StudentPerformanceLeaderboard from "../pages/Teacher/StudentPerformanceLeaderboard.vue";
import SubjectLeaderboard from "../pages/Teacher/SubjectLeaderboard.vue";
import EducationOfficeDashboard from "../pages/EducationOffice/EducationOfficeDashboard.vue";
import QuestionRepository from "../pages/Admin/ExamRepository/QuestionRepository.vue";
import ExamType from "../pages/Admin/ExamRepository/ExamType.vue";
import ExamRepository from "../pages/Exams/ExamRepository.vue";
import MockExamBuilder from "../pages/Admin/ExamRepository/MockExamBuilder.vue";
import TakeExam from "../pages/Student/TakeExam.vue";
import ExamResult from "../pages/Student/ExamResult.vue";
import ExamAlreadyTaken from "../pages/Student/ExamAlreadyTaken.vue";
import AvailableTests from "../pages/Student/AvailableTests.vue";
import TestGuidelines from "../pages/Student/TestGuidelines.vue";
import StudentRoom from "../pages/Student/StudentRoom.vue";
import FlashHeader from "../components/Header/FlashHeader.vue";
import FlashcardsHome from "@/components/Flashcards/FlashcardsHome.vue";
import FlashcardsSubject from "@/components/Flashcards/FlashcardsSubject.vue";
import FlashcardsPractice from "@/components/Flashcards/FlashcardsPractice.vue";
import Premium_fixed from "../pages/Student/Premium_fixed.vue";
/* Library Main */
import Library from "@/pages/Student/Library.vue";

/* Exam Bank & Mock Test */
import ExamBankOptions from "@/pages/Student/ExamBankOptions.vue";
import MockTestPractice from "@/pages/Student/MockTestPractice.vue";
import MockTestSubject from "@/pages/Student/MockTestSubject.vue";
import AdminAddPracticeMock from "@/pages/Admin/AdminAddPracticeMock.vue";
import AdminAddNote from "@/pages/Admin/AdminAddNote.vue";

/* Announcement Pages */
import EduOfficeAnnouncements from "@/pages/EducationOffice/EduOfficeAnnouncements.vue";
import TeacherAnnouncementsPage from "@/pages/Teacher/TeacherAnnouncementsPage.vue";
import StudentAnnouncementsPage from "@/pages/Student/StudentAnnouncementsPage.vue";

/* Library Pages (FULL PAGES) */
import VideoLesson from "@/pages/Student/LibraryFiles/VideoLesson.vue";
import StudyNoteViewer from "@/components/StudyNoteViewer.vue";
import SlidesView from "@/pages/Student/LibraryFiles/SlidesView.vue";
import BooksView from "@/pages/Student/LibraryFiles/BooksView.vue";

/* Gamification Pages */
import Gamification from "@/pages/Student/Gamification.vue";
import StudentSectionFeedback from "@/pages/Student/StudentSectionFeedback.vue";
import AdminUnlockRequests from "@/pages/Admin/AdminUnlockRequests.vue";

/* Feedback Dashboard */
import FeedbackDashboard from "@/pages/Feedback/FeedbackDashboard.vue";
import EduskillHeader from "../components/Header/EduskillHeader.vue";

const routes = [
  { path: "/", component: Home },
  { path: "/home", component: Home },
  { path: "/my_portifolio", component: Portfolio },
  { path: "/exam_bank", component: exam_bank },
  { path: "/register", component: register },
  { path: "/login", component: login },
  { path: "/student_dashboard", component: StudentDashboard },
  { path: "/users", component: users },
  { path: "/admin_dashboard", component: admin_dashboard },
  { path: "/adminAddLibrary", component: AdminAddLibrary },
  { path: "/admin_add_flashcards", component: AdminAddFlashcards },
  { path: "/admin_login", component: AdminLogin },
  { path: "/admin/add-note", component: AdminAddNote },
  { path: "/pending_users", component: PendingUsers },
  { path: "/admin/manage_forum", component: AdminManageForum },
  { path: "/user_notification", component: UserNotification },
  { path: "/user_login", component: UserLogin },
  { path: "/forgot-password", component: ForgotPassword },
  { path: "/reset-password", component: ResetPassword },
  { path: "/teacher_dashboard", component: TeacherDashboard },
  { path: "/teacher/room", component: TeacherRoom },
  { path: "/teacher/student-performance", component: StudentPerformanceLeaderboard },
  { path: "/teacher/subject-leaderboard", component: SubjectLeaderboard },
  { path: "/education_office_dashboard", component: EducationOfficeDashboard },
  { path: "/question_repository", component: QuestionRepository },
  { path: "/exam_type", component: ExamType },
  { path: "/exam_repository", component: ExamRepository },
  { path: "/flash_header", component: FlashHeader },
  { path: "/flashcards", component: FlashcardsHome },
  { path: "/flashcards/subject/:subject", component: FlashcardsSubject },
  { path: "/flashcards/practice/:subjectId", component: FlashcardsPractice },
  { path: "/exam_builder", component: MockExamBuilder },
{ path: "/premium", component: Premium_fixed },
  {
    path: '/take_exam/:examId',
    name: 'TakeExam',
    component: TakeExam,
    props: true
  },
  {
    path: '/student/exam-result',
    name: 'ExamResult',
    component: ExamResult
  },
  {
    path: '/student/exam-already-taken',
    name: 'ExamAlreadyTaken',
    component: ExamAlreadyTaken
  },
  { path: "/student/available-tests", component: AvailableTests },
  { path: "/student/test-guidelines/:testId", component: TestGuidelines },
  { path: "/student/forum", component: StudentRoom },

  /* Exam Bank Options & Mock Test */
{ path: "/exam-bank-options", component: ExamBankOptions }, 
 { path: "/mock-test-subject", component: MockTestSubject },
   { path: "/mock-test-practice", component: MockTestPractice },

  { path: "/admin_add_practice_mock", component: AdminAddPracticeMock },

  /* Library */
  { path: "/library", component: Library },

  /* FULL PAGES */
  { path: "/library/videos", component: VideoLesson },
  { path: "/library/notes", component: StudyNoteViewer },
  { path: "/library/slides", component: SlidesView },
  { path: "/library/books", component: BooksView },

/* Gamification Routes */
  { path: "/student/gamification", component: Gamification },
  { path: "/student/section-feedback", component: StudentSectionFeedback },
  { path: "/admin/unlock-requests", component: AdminUnlockRequests },

  /* Feedback Dashboard Routes */
  { path: "/teacher/feedback", component: FeedbackDashboard },
  { path: "/eduoffice/feedback", component: FeedbackDashboard },

  /* User Settings Routes */
  { path: "/student/settings", component: UserEdit },
  { path: "/teacher/settings", component: UserEdit },
  { path: "/eduoffice/settings", component: UserEdit },
  { path: "/admin/settings", component: UserEdit },

  /* Announcement Routes */
  { path: "/eduoffice/announcements", component: EduOfficeAnnouncements },
  { path: "/teacher/announcements", component: TeacherAnnouncementsPage },
  { path: "/student/announcements", component: StudentAnnouncementsPage },
  { path: "/eduskill_header", component: EduskillHeader },
];

// Protected routes that require authentication
const protectedRoutes = [
  '/student_dashboard',
  '/student/available-tests',
  '/student/test-guidelines',
  '/student/exam-result',
  '/student/forum',
  '/student/announcements',
  '/take_exam',
  '/teacher_dashboard',
  '/teacher/room',
  '/teacher/student-performance',
  '/teacher/subject-leaderboard',
  '/teacher/announcements',
  '/admin_dashboard',
  '/adminAddLibrary',
  '/admin_add_flashcards',
  '/pending_users',
  '/admin/manage_forum',
  '/question_repository',
  '/exam_type',
  '/exam_repository',
  '/exam_builder',
  '/library',
  '/exam-bank-options',
  '/mock-test-subject',
  '/mock-test-practice',
  '/student/gamification',
  '/student/section-feedback',
  '/teacher/feedback',
  '/eduoffice/feedback',
  '/education_office_dashboard',
  '/eduoffice/announcements',
  '/student/settings',
  '/teacher/settings',
  '/eduoffice/settings',
  '/admin/settings'
];

// Admin routes that require admin authentication
const adminRoutes = [
  '/admin_dashboard',
  '/admin_add_flashcards',
  '/admin/add-note',
  '/pending_users',
  '/admin/manage_forum',
  '/question_repository',
  '/exam_type',
  '/exam_repository',
  '/exam_builder',
  '/admin/unlock-requests'
];

// Teacher-admin shared routes (accessible by both admin and teacher with valid token)
const teacherAdminSharedRoutes = [
  '/adminAddLibrary',
  '/admin_add_practice_mock'
];

// Role-specific routes (student-only)
const studentRoutes = [
  '/student_dashboard',
  '/student/available-tests',
  '/student/test-guidelines',
  '/student/exam-result',
  '/take_exam',
  '/exam-bank-options',
  '/mock-test-subject',
  '/mock-test-practice'
];


const router = createRouter({
  history: createWebHistory('/'),
  routes,
});

// FIXED ENHANCED NAVIGATION GUARD WITH DEBUG & RELAXED CHECKS
router.beforeEach((to, from, next) => {
  console.log(`[Router] 🛡️  Guard: ${from.path} → ${to.path}`);
  
  // **BYPASS 1: Login to dashboard (direct allow)**
  const isFromLogin = from.path === '/user_login' || from.path === '/login';
  const isDashboardRedirect = to.path === '/student_dashboard' || 
                             to.path === '/teacher_dashboard' || 
                             to.path === '/admin_dashboard' ||
                             to.path === '/education_office_dashboard';
  
  if (isFromLogin && isDashboardRedirect) {
    console.log('[Router] ✅ BYPASS: Login → dashboard direct allow');
    next();
    return;
  }
  
  // Normalize double slashes
  if (to.path.startsWith('//')) {
    console.warn(`[Router] Normalizing double slash: ${to.path}`);
    const normalizedPath = to.path.replace(/^\/\//, '/');
    return next({ path: normalizedPath, query: to.query, hash: to.hash });
  }
  
  // **DEBUG LOG STORAGE STATE**
  const username = localStorage.getItem('username');
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');
  const adminToken = localStorage.getItem('admin_token') || sessionStorage.getItem('admin_token');
  
  console.log('[Router DEBUG] Storage:', {
    username: !!username,
    token: !!token ? token.slice(0,20) + '...' : null,
    role,
    adminToken: !!adminToken
  });
  
  // Allow public paths
  if (to.path === '/' || to.path === '') {
    next();
    return;
  }
  
  // Skip auth for login pages
  if (to.path === '/user_login' || to.path === '/login' || to.path === '/admin_login') {
    next();
    return;
  }
  
  const isProtectedRoute = protectedRoutes.some(route => to.path.startsWith(route));
  if (!isProtectedRoute) {
    next();
    return;
  }
  
  // **RELAXED TOKEN CHECK FOR DASHBOARDS (ANTI-RACE)**
  const isDashboardPath = isDashboardRedirect || to.path === '/student_dashboard';
  if (isDashboardPath && token) {
    console.log('[Router] ✅ RELAXED ALLOW: Dashboard + token exists');
    // Will check role below
  } else if (!token && !adminToken) {
    console.log('[Router] 🚫 No token - redirect login');
    sessionStorage.setItem('redirectAfterLogin', to.fullPath);
    next('/user_login');
    return;
  }
  
  const isAdminRoute = adminRoutes.some(route => to.path.startsWith(route));
  if (isAdminRoute) {
    if (adminToken) {
      next();
      return;
    } else {
      sessionStorage.setItem('redirectAfterLogin', to.fullPath);
      next('/admin_login');
      return;
    }
  }
  
  const isTeacherAdminShared = teacherAdminSharedRoutes.some(route => to.path.startsWith(route));
  if (isTeacherAdminShared && username && token && (role === 'teacher' || role === 'admin' || role === 'eduoffice')) {
    next();
    return;
  }
  
  // Role-specific redirects (if logged in but wrong dashboard)
  if (!username || !token || !role) {
    console.log('[Router] 🚫 Incomplete auth data - login');
    sessionStorage.setItem('redirectAfterLogin', to.fullPath);
    next('/user_login');
    return;
  }
  
  // Student routes check
  if (studentRoutes.some(route => to.path.startsWith(route))) {
    if (role !== 'student') {
      console.log('[Router] 🔄 Wrong role for student route:', role);
      if (role === 'teacher') next('/teacher_dashboard');
      else if (role === 'admin' || role === 'eduoffice') next('/admin_dashboard');
      else next('/user_login');
      return;
    }
  }
  
  // Teacher routes
  if (to.path.startsWith('/teacher_') && role !== 'teacher' && role !== 'eduoffice') {
    if (role === 'student') next('/student_dashboard');
    else if (role === 'admin') next('/admin_dashboard');
    else next('/user_login');
    return;
  }
  
  // Education office
  if (to.path.startsWith('/education_office_dashboard') && role !== 'eduoffice') {
    if (role === 'student') next('/student_dashboard');
    else if (role === 'teacher') next('/teacher_dashboard');
    else next('/user_login');
    return;
  }
  
  console.log('[Router] ✅ Full auth pass');
  next();
});

export default router;

