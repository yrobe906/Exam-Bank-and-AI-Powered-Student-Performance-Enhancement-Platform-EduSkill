# ISSMS Education Dashboard Frontend

A comprehensive Vue.js-based education management system frontend that provides dashboards and tools for students, teachers, administrators, and education offices.

## Features

### Student Features
- **Dashboard**: Personalized student dashboard with announcements, study materials, and progress tracking
- **Exam Management**: Access to exam banks, practice exams, and mock tests
- **Flashcards**: Interactive flashcard system for subject review
- **Study Notes**: Viewer for educational materials and resources
- **Gamification**: Achievement system and progress tracking

### Teacher Features
- **Exam Creation**: Tools for creating and managing exams with question forms
- **Announcement Management**: Create and manage class announcements
- **Resource Management**: Upload and organize educational resources
- **Student Progress Monitoring**: Track student performance and progress

### Admin Features
- **User Management**: Comprehensive user administration system
- **System Configuration**: Admin controls for system settings
- **Analytics Dashboard**: System-wide analytics and reporting

### Education Office Features
- **Institutional Management**: Tools for managing educational institutions
- **Reporting**: Generate reports for educational oversight
- **Compliance Tools**: Features for educational compliance and standards

## Technology Stack

- **Framework**: Vue 3 with Composition API
- **Build Tool**: Vite
- **Styling**: Tailwind CSS with PostCSS
- **Routing**: Vue Router
- **State Management**: Vuex/Pinia (based on implementation)
- **HTTP Client**: Axios (via api.js service)

## Project Structure

```
src/
├── components/          # Reusable Vue components
│   ├── common/         # Shared components (LoadingSpinner, etc.)
│   ├── Cards/          # Card components for exams, sections, sectors
│   ├── Flashcards/     # Flashcard-related components
│   ├── forms/          # Form components for exams and questions
│   ├── Header/         # Header components for different app sections
│   ├── Landing/        # Landing page components
│   ├── layout/         # Layout components (headers, sidebars, etc.)
│   ├── preview/        # Preview components for questions
│   ├── Sidebar/        # Sidebar components for different user roles
│   └── student/        # Student-specific components
├── pages/              # Vue page components
│   ├── Admin/          # Admin dashboard pages
│   ├── Educational Dashboard/  # Education office pages
│   ├── EducationOffice/ # Education office specific pages
│   ├── Exams/          # Exam-related pages
│   ├── Student/        # Student dashboard pages
│   ├── Teacher/        # Teacher dashboard pages
│   └── Users/          # User management pages
├── router/             # Vue Router configuration
├── services/           # API and service layer
│   ├── aiService.js    # AI chat service
│   ├── api.js          # Main API service
│   ├── flashcardService.js
│   ├── forumService.js
│   ├── gamificationService.js
│   └── practiceMockService.js
├── views/              # Additional view components
└── assets/             # Static assets (CSS, images)
```

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd issms-frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Build for production:
```bash
npm run build
```

### Environment Setup

Create a `.env` file in the root directory with the following variables:

```env
VITE_API_BASE_URL=http://localhost:3000/api
VITE_APP_NAME=ISSMS Education Dashboard
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## API Integration

The application integrates with a backend API through the `services/api.js` file. Key services include:

- **Authentication**: Login, registration, password reset
- **User Management**: CRUD operations for users
- **Exam Management**: Create, update, delete exams and questions
- **Flashcard System**: Manage flashcard decks and practice sessions
- **Gamification**: Achievement and progress tracking
- **AI Services**: Chat and AI-powered features

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please contact the development team or create an issue in the repository.
