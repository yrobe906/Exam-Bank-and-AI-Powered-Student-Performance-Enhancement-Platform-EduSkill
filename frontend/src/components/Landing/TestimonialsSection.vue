<template>
  <section id="testimonials" class="relative py-24 overflow-hidden bg-gray-50">
    <!-- Background decorations -->
    <div class="absolute top-20 left-10 w-72 h-72 bg-indigo-100 rounded-full blur-3xl opacity-50"></div>
    <div class="absolute bottom-20 right-10 w-96 h-96 bg-purple-100 rounded-full blur-3xl opacity-50"></div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Section Header -->
      <div class="text-center mb-16">
        <span class="inline-block px-4 py-1.5 rounded-full bg-indigo-100 text-indigo-700 text-sm font-semibold mb-4">
          💬 Success Stories
        </span>
        <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          What Our
          <span class="text-indigo-600">Students Say</span>
        </h2>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto">
          Join thousands of satisfied students who have transformed their learning experience.
        </p>
      </div>

      <!-- Testimonials Grid -->
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div
          v-for="testimonial in testimonials"
          :key="testimonial.name"
          class="bg-white rounded-2xl p-6 shadow-md hover:shadow-xl transition-shadow duration-300"
        >
          <!-- Rating -->
          <div class="flex gap-1 mb-4">
            <svg 
              v-for="n in 5" 
              :key="n" 
              class="w-5 h-5" 
              :class="n <= testimonial.rating ? 'text-yellow-400' : 'text-gray-300'"
              fill="currentColor" 
              viewBox="0 0 20 20"
            >
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
            </svg>
          </div>

          <!-- Content -->
          <p class="text-gray-600 mb-6">
            {{ testimonial.content }}
          </p>

          <!-- Author -->
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-semibold text-sm">
              {{ testimonial.name.charAt(0) }}
            </div>
            <div>
              <h4 class="font-semibold text-gray-900">{{ testimonial.name }}</h4>
              <p class="text-sm text-gray-500">{{ testimonial.role }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const testimonials = [
  {
    name: 'Sarah Johnson',
    role: 'Medical Student',
    rating: 5,
    content: 'EduSkill Hub has completely transformed my exam preparation. The AI-powered insights helped me identify my weak areas and improve my scores by 40% in just two months!'
  },
  {
    name: 'Michael Chen',
    role: 'Engineering Student',
    rating: 5,
    content: 'The mock tests are incredibly realistic. I felt completely prepared for my entrance exams. The detailed analytics helped me track my progress effectively.'
  },
  {
    name: 'Emily Davis',
    role: 'High School Student',
    rating: 5,
    content: 'I used to struggle with studying, but the gamification features made learning fun! Now I actually look forward to my study sessions. Highly recommended!'
  },
  {
    name: 'James Wilson',
    role: 'University Student',
    rating: 5,
    content: 'The flashcard system with spaced repetition is a game-changer. I can memorize complex concepts so much faster now. Absolutely worth it!'
  },
  {
    name: 'Lisa Anderson',
    role: 'Pre-Med Student',
    rating: 5,
    content: 'The question bank is extensive and the explanations are thorough. It\'s like having a personal tutor available 24/7. My grades have never been better!'
  },
  {
    name: 'David Brown',
    role: 'Computer Science Student',
    rating: 5,
    content: 'As someone who learns best through practice, EduSkill Hub is perfect. The variety of questions and instant feedback helped me ace my certifications.'
  }
]
</script>


