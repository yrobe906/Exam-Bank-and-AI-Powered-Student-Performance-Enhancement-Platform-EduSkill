<template>
  <footer class="bg-gray-800 text-white mt-8">
    <div class="container mx-auto px-4 py-8">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <!-- Brand Section -->
        <div class="col-span-1 md:col-span-2">
          <div class="flex items-center space-x-3 mb-4">
            <div class="bg-white p-2 rounded-lg">
              <svg class="w-8 h-8 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10.394 2.08a1 1 0 00-.788 0l-7 3a1 1 0 000 1.84L5.25 8.051a.999.999 0 01.356-.257l4-1.714a1 1 0 11.788 1.838L7.667 9.088l1.94.831a1 1 0 00.787 0l7-3a1 1 0 000-1.838l-7-3zM3.31 9.397L5 10.12v4.102a8.969 8.969 0 00-1.05-.174 1 1 0 01-.89-.89 11.115 11.115 0 01.25-3.762zM9.3 16.573A9.026 9.026 0 007 14.935v-3.957l1.818.78a3 3 0 002.364 0l5.508-2.361a11.026 11.026 0 01.25 3.762 1 1 0 01-.89.89 8.968 8.968 0 00-5.35 2.524 1 1 0 01-1.4 0zM6 18a1 1 0 001-1v-2.065a8.935 8.935 0 00-2-.712V17a1 1 0 001 1z"/>
              </svg>
            </div>
            <div>
              <h2 class="text-xl font-bold">EduSkill Hub</h2>
              <p class="text-gray-400 text-sm">Empowering Education Through Technology</p>
            </div>
          </div>
          <p class="text-gray-400 mb-4">
            A comprehensive e-learning platform designed to enhance student learning experience with interactive tools and resources.
          </p>
        </div>

        <!-- Quick Links -->
        <div>
          <h3 class="text-lg font-semibold mb-4">Quick Links</h3>
          <ul class="space-y-2">
            <li><a href="#" class="text-gray-400 hover:text-white transition">Dashboard</a></li>
            <li><a href="#" class="text-gray-400 hover:text-white transition">Exam Bank</a></li>
            <li><a href="#" class="text-gray-400 hover:text-white transition">Mock Tests</a></li>
            <li><a href="#" class="text-gray-400 hover:text-white transition">Analytics</a></li>
            <li><a href="#" class="text-gray-400 hover:text-white transition">Library</a></li>
          </ul>
        </div>

        <!-- Contact Info -->
        <div>
          <h3 class="text-lg font-semibold mb-4">Contact Us</h3>
          <ul class="space-y-2 text-gray-400">
            <li class="flex items-center">
              <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
                <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
              </svg>
              <a href="mailto:support@eduskillhub.com" class="hover:text-white transition">support@eduskillhub.com</a>
            </li>
            <li class="flex items-center">
              <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15h-2v-6h2v6zm0-8h-2V7h2v2zm6 8h-2v-4c0-1.1-.9-2-2-2s-2 .9-2 2v4h-2v-6h2v1.2c.5-.7 1.3-1.2 2.2-1.2 1.5 0 2.8 1.3 2.8 2.8v3.2z"/>
              </svg>
              <a href="https://t.me/ASikkoo_Mandoo" target="_blank" rel="noopener noreferrer" class="hover:text-blue-400 transition">@ASikkoo_Mandoo on Telegram</a>
            </li>
          </ul>
          
          <!-- Social Media -->
          <div class="mt-6">
            <h4 class="text-lg font-semibold mb-3">Follow Us</h4>
            <div class="flex space-x-4">
              <!-- LinkedIn -->
              <a href="#" target="_blank" rel="noopener noreferrer" class="bg-gray-700 hover:bg-blue-700 p-2 rounded-full transition transform hover:scale-110">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C0.792 0 0 0.774 0 1.729v20.542C0 23.227 0.792 24 1.771 24h20.451c0.979 0 1.771-0.773 1.771-1.729V1.729C24 0.774 23.204 0 22.225 0z"/>
                </svg>
              </a>
              
              <!-- Twitter (X) -->
              <a href="#" target="_blank" rel="noopener noreferrer" class="bg-gray-700 hover:bg-sky-500 p-2 rounded-full transition transform hover:scale-110">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                </svg>
              </a>
              
              <!-- GitHub -->
              <a href="https://github.com/yrobe906" target="_blank" rel="noopener noreferrer" class="bg-gray-700 hover:bg-gray-600 p-2 rounded-full transition transform hover:scale-110">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd"/>
                </svg>
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- Copyright -->
      <div class="border-t border-gray-700 mt-8 pt-6 text-center text-gray-400">
        <p>&copy; 2026 EduSkill Hub. All rights reserved.</p>
        <p class="text-sm mt-1">
          <a href="#" class="hover:text-white transition">Privacy Policy</a> | 
          <a href="#" class="hover:text-white transition">Terms of Service</a>
        </p>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'FooterStud',
};
</script>