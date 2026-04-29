<template>
  <section id="pricing" class="relative py-24 overflow-hidden">
    <!-- Background -->
    <div class="absolute inset-0 bg-gradient-to-b from-white via-gray-50 to-white -z-10"></div>
    <div class="absolute top-20 right-10 w-72 h-72 bg-indigo-100 rounded-full blur-3xl opacity-50"></div>
    <div class="absolute bottom-20 left-10 w-96 h-96 bg-purple-100 rounded-full blur-3xl opacity-50"></div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Section Header -->
      <div class="text-center mb-16">
        <span class="inline-block px-4 py-1.5 rounded-full bg-indigo-100 text-indigo-600 text-sm font-semibold mb-4">
          💰 Simple Pricing
        </span>
        <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          Choose Your
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600">
            Perfect Plan
          </span>
        </h2>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto">
          Flexible pricing options to match your learning needs. Start free and upgrade when you're ready.
        </p>
      </div>

      <!-- Pricing Cards -->
      <div class="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
        <div
          v-for="plan in plans"
          :key="plan.name"
          class="relative bg-white rounded-3xl p-8 shadow-lg hover:shadow-2xl transition-all duration-500"
          :class="{ 'ring-2 ring-indigo-500 scale-105': plan.popular }"
        >
          <!-- Popular Badge -->
          <div v-if="plan.popular" class="absolute -top-4 left-1/2 -translate-x-1/2">
            <span class="px-4 py-1 bg-gradient-to-r from-indigo-600 to-purple-600 text-white text-sm font-semibold rounded-full">
              Most Popular
            </span>
          </div>

          <!-- Plan Header -->
          <div class="text-center mb-8">
            <h3 class="text-2xl font-bold text-gray-900 mb-2">{{ plan.name }}</h3>
            <p class="text-gray-500 mb-4">{{ plan.description }}</p>
            <div class="flex items-baseline justify-center gap-1">
              <span class="text-4xl font-bold text-gray-900">${{ plan.price }}</span>
              <span class="text-gray-500">/month</span>
            </div>
          </div>

          <!-- Features -->
          <ul class="space-y-4 mb-8">
            <li v-for="feature in plan.features" :key="feature" class="flex items-center gap-3">
              <svg class="w-5 h-5 text-green-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
              <span class="text-gray-600">{{ feature }}</span>
            </li>
          </ul>

          <!-- CTA Button -->
          <button
            class="w-full py-4 rounded-xl font-semibold transition-all duration-300"
            :class="plan.popular 
              ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:shadow-lg hover:shadow-indigo-500/30' 
              : 'bg-gray-100 text-gray-900 hover:bg-gray-200'"
          >
            {{ plan.cta }}
          </button>
        </div>
      </div>

      <!-- Money Back Guarantee -->
      <p class="text-center text-gray-500 mt-8">
        🔒 30-day money-back guarantee. No questions asked.
      </p>
    </div>
  </section>
</template>

<script setup>
const plans = [
  {
    name: 'Free',
    description: 'Perfect for getting started',
    price: 0,
    features: [
      'Access to 1,000+ questions',
      '5 Mock tests per month',
      'Basic flashcard decks',
      'Community support',
      'Progress tracking'
    ],
    cta: 'Get Started Free',
    popular: false
  },
  {
    name: 'Pro',
    description: 'Best for serious learners',
    price: 19,
    features: [
      'Unlimited question access',
      'Unlimited mock tests',
      'Advanced flashcard system',
      'AI-powered insights',
      'Priority support',
      'Performance analytics',
      'Certificate of completion'
    ],
    cta: 'Start Free Trial',
    popular: true
  },
  {
    name: 'Premium',
    description: 'For ultimate success',
    price: 49,
    features: [
      'Everything in Pro',
      '1-on-1 tutoring sessions',
      'Personalized study plan',
      'Early access to new features',
      'Exclusive webinars',
      'Resume review service',
      'Interview preparation'
    ],
    cta: 'Go Premium',
    popular: false
  }
]
</script>

