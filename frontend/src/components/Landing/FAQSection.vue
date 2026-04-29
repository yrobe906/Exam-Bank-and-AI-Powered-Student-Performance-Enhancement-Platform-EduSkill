<template>
  <section id="faq" class="relative py-24 overflow-hidden bg-gray-50">
    <div class="absolute top-40 left-20 w-64 h-64 bg-indigo-100 rounded-full blur-3xl opacity-50"></div>
    <div class="absolute bottom-40 right-20 w-64 h-64 bg-purple-100 rounded-full blur-3xl opacity-50"></div>

    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
      <!-- Section Header -->
      <div class="text-center mb-16">
        <span class="inline-block px-4 py-1.5 rounded-full bg-indigo-100 text-indigo-700 text-sm font-semibold mb-4">
          Frequently Asked Questions
        </span>
        <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          Got Questions?
          <span class="text-indigo-600">We've Got Answers</span>
        </h2>
      </div>

      <!-- FAQ Accordion -->
      <div class="space-y-4">
        <div
          v-for="(faq, index) in faqs"
          :key="index"
          class="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow duration-300 overflow-hidden"
        >
          <button
            @click="toggleFAQ(index)"
            class="w-full px-5 py-4 text-left flex items-center justify-between transition-colors duration-200 hover:bg-gray-50"
          >
            <span class="font-semibold text-gray-900 pr-4">{{ faq.question }}</span>
            <svg
              class="w-5 h-5 text-indigo-600 transform transition-transform duration-200 flex-shrink-0"
              :class="{ 'rotate-180': openIndex === index }"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </button>
          
          <div
            class="transition-all duration-200 overflow-hidden"
            :class="openIndex === index ? 'max-h-40 opacity-100' : 'max-h-0 opacity-0'"
          >
            <div class="px-5 pb-4 text-gray-600">
              {{ faq.answer }}
            </div>
          </div>
        </div>
      </div>

      <!-- Contact CTA -->
      <div class="mt-10 text-center">
        <p class="text-gray-600 mb-4">Still have questions?</p>
        <button class="px-6 py-3 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700 transition-colors">
          Contact Support
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const openIndex = ref(0)

const toggleFAQ = (index) => {
  openIndex.value = openIndex.value === index ? -1 : index
}

const faqs = [
  {
    question: 'What is EduSkill Hub?',
    answer: 'EduSkill Hub is an AI-powered learning platform that helps students prepare for exams through comprehensive question banks, mock tests, flashcards, gamification, and performance analytics.'
  },
  {
    question: 'How does the AI integration help me?',
    answer: 'Our AI analyzes your performance patterns to provide personalized learning recommendations, identify weak areas, suggest relevant study materials, and offer instant help through our AI chat assistant.'
  },
  {
    question: 'Is EduSkill Hub free to use?',
    answer: 'We offer both free and premium plans. The free plan includes access to basic features, while our premium plans unlock advanced analytics, unlimited mock tests, and personalized coaching.'
  },
  {
    question: 'How accurate are the mock tests?',
    answer: 'Our mock tests are designed by expert educators and closely simulate the actual exam format, timing, and difficulty level. Many students report that our practice tests closely matched what they encountered in the real exams.'
  },
  {
    question: 'Can I track my progress over time?',
    answer: 'Absolutely! Our comprehensive performance analytics dashboard lets you track your progress, view detailed reports, identify trends, and measure improvement across all subjects and topics.'
  }
]
</script>

