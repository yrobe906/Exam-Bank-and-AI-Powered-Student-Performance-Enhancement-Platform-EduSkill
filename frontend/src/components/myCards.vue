<template>
  <section id="projects" class="relative py-24 px-6">
    <div class="max-w-7xl mx-auto">

      <!-- Title -->
      <h2 class="text-5xl font-bold text-center mb-16">
        My
        <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-500">
          Projects
        </span>
      </h2>

      <!-- Cards -->
      <div class="grid gap-10 md:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="project in projects"
          :key="project.title"
          class="group relative rounded-2xl bg-white/5 backdrop-blur-xl border border-white/10 p-7
                 transition-all duration-500 ease-out
                 hover:-translate-y-3 hover:shadow-2xl hover:shadow-indigo-500/30"
        >

          <!-- Glow border -->
          <div class="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition duration-500
                      bg-gradient-to-br from-indigo-500/20 to-purple-600/20 blur-xl -z-10"></div>

          <!-- Icon -->
          <div
            class="w-16 h-16 mb-6 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600
                   flex items-center justify-center text-3xl
                   shadow-lg shadow-indigo-500/40
                   transition-transform duration-500 group-hover:rotate-6 group-hover:scale-110"
          >
            {{ project.icon }}
          </div>

          <!-- Content -->
          <h3 class="text-2xl font-semibold mb-3 transition-colors duration-300 group-hover:text-indigo-400">
            {{ project.title }}
          </h3>

          <p class="text-gray-400 mb-6 leading-relaxed">
            {{ project.description }}
          </p>

          <!-- Tech stack -->
          <div class="flex flex-wrap gap-2">
            <span
              v-for="tech in project.tech"
              :key="tech"
              class="px-3 py-1 text-sm rounded-full
                     bg-white/5 border border-white/10
                     text-gray-300
                     transition-all duration-300
                     group-hover:border-indigo-400/40 group-hover:text-indigo-300"
            >
              {{ tech }}
            </span>
          </div>

        </div>
      </div>

    </div>
  </section>
</template>

<script>
export default {
  name: 'MyCards',
  data() {
    return {
      projects: [
        {
          title: 'Jtech LMS',
          icon: '📚',
          description: 'LMS platform with courses, students, and backend integration.',
          tech: ['HTML', 'CSS', 'JavaScript', 'PHP', 'MySQL']
        },
        {
          title: 'Awetu Kebele Registration',
          icon: '🏛️',
          description: 'Digital registration system for local government administration.',
          tech: ['HTML', 'CSS', 'JavaScript', 'PHP', 'MySQL']
        },
        {
          title: 'EduSkill Hub',
          icon: '🤖',
          description: 'AI-powered exam bank and student performance enhancement platform.',
          tech: ['Vue.js', 'FastAPI', 'PostgreSQL', 'AI', 'REST API']
        }
      ]
    }
  }
}
</script>
