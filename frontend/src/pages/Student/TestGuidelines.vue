<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 flex items-center justify-center p-4">
    <div class="max-w-2xl w-full">
      <!-- Back Button -->
      <button @click="goBack" class="flex items-center gap-2 text-gray-600 hover:text-blue-600 mb-4 transition-colors">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        Back to Tests
      </button>
      
      <!-- Guidelines Card -->
      <div class="bg-white rounded-3xl shadow-2xl overflow-hidden">
        <!-- Header -->
        <div class="bg-gradient-to-r from-blue-600 to-indigo-600 p-6 text-white">
          <h1 class="text-2xl font-bold">{{ test?.title || 'Test Guidelines' }}</h1>
          <p class="text-blue-100 mt-1">Please read carefully before starting</p>
        </div>
        
        <!-- Guidelines Content -->
        <div class="p-8">
          <div class="space-y-6">
            <!-- Guidelines List -->
            <div class="space-y-4">
              <div v-for="(guideline, index) in guidelines" :key="index" 
                   class="flex items-start gap-3">
                <div class="w-6 h-6 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span class="text-blue-600 text-sm font-bold">{{ index + 1 }}</span>
                </div>
                <p class="text-gray-700">{{ guideline }}</p>
              </div>
            </div>
            
            <!-- Important Advisory -->
            <div class="mt-8 p-4 bg-yellow-50 border border-yellow-200 rounded-xl">
              <div class="flex items-start gap-3">
                <svg class="w-6 h-6 text-yellow-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <div>
                  <h4 class="font-semibold text-yellow-800">⚠️ Important Advisory</h4>
                  <p class="text-sm text-yellow-700 mt-1">
                    Avoid switching tabs or minimizing the browser. Full-screen mode is recommended for the best experience. Do not refresh the page once the test starts.
                  </p>
                </div>
              </div>
            </div>
            
            <!-- Test Summary -->
            <div class="grid grid-cols-3 gap-4 mt-6">
              <div class="text-center p-3 bg-gray-50 rounded-xl">
                <div class="text-2xl font-bold text-blue-600">{{ test?.questions || 0 }}</div>
                <div class="text-xs text-gray-500">Questions</div>
              </div>
              <div class="text-center p-3 bg-gray-50 rounded-xl">
                <div class="text-2xl font-bold text-green-600">{{ test?.time || 0 }}</div>
                <div class="text-xs text-gray-500">Minutes</div>
              </div>
              <div class="text-center p-3 bg-gray-50 rounded-xl">
                <div class="text-2xl font-bold text-purple-600">{{ test?.marks || 0 }}</div>
                <div class="text-xs text-gray-500">Max Marks</div>
              </div>
            </div>
            
            <!-- Start Button -->
            <button @click="startExam"
                    class="w-full mt-8 py-4 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-xl font-bold text-lg hover:shadow-xl hover:scale-[1.02] transition-all">
              Start Test Now
              <svg class="w-5 h-5 inline ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TestGuidelines',
  data() {
    return {
      test: null,
      guidelines: [
        'Questions are displayed one at a time.',
        'You can skip questions and revisit them later using the Question Palette.',
        'Click \'Save & Next\' to confirm your answer.',
        'Use \'Mark for Review\' if you are unsure but want to come back.',
        'The timer at the top right counts down automatically.',
        'The test auto-submits when time expires.'
      ]
    }
  },
  methods: {
    goBack() {
      this.$router.back()
    },
    
    startExam() {
      this.$router.push({
        name: 'TakeExam',
        params: { testId: this.test.id }
      })
    }
  },
  mounted() {
    if (this.$route.query.test) {
      this.test = JSON.parse(this.$route.query.test)
    } else {
      // Mock data
      this.test = {
        id: 1,
        title: 'SSC JE PAPER I (MECHANICAL)',
        questions: 30,
        time: 18,
        marks: 120
      }
    }
  }
}
</script>

<style scoped>
</style>
