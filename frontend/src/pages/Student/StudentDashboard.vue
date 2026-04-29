<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-blue-50/30">
    <!-- Welcome Message -->
    <div class="p-8 text-center">
      <h1 class="text-4xl font-bold text-gray-800 mb-4">Student Dashboard</h1>
      <p class="text-xl text-gray-600">Welcome to your learning dashboard!</p>
      <p class="mt-2 text-lg">Role: Student | Logged in successfully</p>
      <button @click="$router.push('/student/available-tests')" class="mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700">
        Go to Available Tests
      </button>
      <div class="mt-8 p-4 bg-green-100 border border-green-300 rounded-lg">
        <p>✅ Backend login works! This page loads after redirect.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StudentDashboard',
  mounted() {
    console.log('StudentDashboard mounted - login redirect success!');
  }
}
</script>
