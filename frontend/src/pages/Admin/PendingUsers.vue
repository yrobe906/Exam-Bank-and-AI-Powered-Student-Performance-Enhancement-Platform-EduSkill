<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-6">
    <div class="max-w-7xl mx-auto space-y-8">
      
      <!-- Header Section -->
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">User Management</h1>
          <p class="text-gray-600 mt-2">Manage all users and pending registrations</p>
        </div>
        <div class="flex space-x-3">
          <button class="px-4 py-2 bg-white border border-gray-200 rounded-lg text-gray-700 hover:bg-gray-50 transition-all duration-200 flex items-center space-x-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
            </svg>
            <span>Export</span>
          </button>
          <button @click="redirectToRegister" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all duration-200 flex items-center space-x-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
            </svg>
            <span>Add User</span>
          </button>
        </div>
      </div>

      <!-- Pending Users Cards Section -->
      <div v-if="pendingUsers.length > 0" class="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
        <div class="px-6 py-4 bg-gradient-to-r from-yellow-50 to-orange-50 border-b border-yellow-100">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-yellow-100 rounded-xl flex items-center justify-center">
              <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div>
              <h2 class="text-xl font-bold text-gray-800">Pending Users</h2>
              <p class="text-sm text-gray-600">{{ pendingUsers.length }} users awaiting approval</p>
            </div>
          </div>
        </div>
        
        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="user in pendingUsers" :key="user.id" 
                 class="bg-gradient-to-br from-white to-gray-50 rounded-xl border border-gray-200 p-5 hover:shadow-lg transition-all duration-300">
              <div class="flex items-start justify-between mb-4">
                <div class="flex items-center space-x-3">
                  <div class="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-semibold text-lg shadow-md">
                    {{ user.full_name?.charAt(0) || 'U' }}
                  </div>
                  <div>
                    <h3 class="font-semibold text-gray-900">{{ user.full_name }}</h3>
                    <p class="text-sm text-gray-500">@{{ user.username }}</p>
                  </div>
                </div>
                <span class="px-3 py-1 text-xs font-semibold rounded-full bg-yellow-100 text-yellow-800">
                  Pending
                </span>
              </div>
              
              <div class="space-y-2 mb-4">
                <div class="flex items-center text-sm text-gray-600">
                  <svg class="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                  </svg>
                  {{ user.email }}
                </div>
                <div class="flex items-center text-sm text-gray-600">
                  <svg class="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                  </svg>
                  Role: <span class="font-medium capitalize ml-1">{{ user.role }}</span>
                </div>
              </div>
              
              <div class="flex space-x-3">
                <button @click="approveUser(user.id)" 
                        class="flex-1 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-all duration-200 flex items-center justify-center space-x-2">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  <span>Approve</span>
                </button>
                <button @click="rejectUser(user.id)" 
                        class="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-all duration-200 flex items-center justify-center space-x-2">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                  <span>Reject</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>


      <!-- All Users Table Section -->
      <div class="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
        <!-- Section Header with Stats -->
        <div class="px-6 py-4 bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-blue-100">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-blue-100 rounded-xl flex items-center justify-center">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path>
                </svg>
              </div>
              <div>
                <h2 class="text-xl font-bold text-gray-800">All Users</h2>
                <p class="text-sm text-gray-600">{{ allUsers.length }} total users</p>
              </div>
            </div>
            
            <!-- Quick Stats -->
            <div class="flex space-x-4">
              <div class="px-3 py-1 bg-blue-100 text-blue-800 rounded-lg text-sm">
                Students: {{ countByRole('student') }}
              </div>
              <div class="px-3 py-1 bg-purple-100 text-purple-800 rounded-lg text-sm">
                Teachers: {{ countByRole('teacher') }}
              </div>
              <div class="px-3 py-1 bg-green-100 text-green-800 rounded-lg text-sm">
                EduOffice: {{ countByRole('eduoffice') }}
              </div>
            </div>
          </div>
        </div>

        <!-- Search and Filter Bar -->
        <div class="p-4 bg-gray-50 border-b border-gray-200">
          <div class="flex flex-wrap gap-4 items-center justify-between">
            <div class="flex-1 min-w-[300px]">
              <div class="relative">
                <svg class="w-5 h-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                </svg>
                <input type="text" v-model="searchQuery" placeholder="Search users by name, email, or role..." 
                       class="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              </div>
            </div>
            <div class="flex space-x-2">
              <select v-model="roleFilter" class="px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="">All Roles</option>
                <option value="student">Student</option>
                <option value="teacher">Teacher</option>
                <option value="eduoffice">EduOffice</option>
                <option value="admin">Admin</option>
              </select>
              <select v-model="statusFilter" class="px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="">All Status</option>
                <option value="approved">Approved</option>
                <option value="pending">Pending</option>
                <option value="rejected">Rejected</option>
              </select>
            </div>
          </div>
        </div>

        <!-- All Users Table -->
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gradient-to-r from-gray-50 to-gray-100">
              <tr>
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">User</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Role & Status</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Contact</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Details</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-100">
              <tr v-for="user in paginatedUsers" :key="user.id" 
                  class="hover:bg-gray-50 transition-all duration-200 ease-in-out group">

                
                <!-- User Info with Photo -->
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center space-x-3">
                    <div class="flex-shrink-0">
                      <div class="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-semibold text-lg shadow-md overflow-hidden relative">
                        <img 
                          v-if="user.profile_photo" 
                          :src="getProfilePhotoUrl(user.profile_photo)" 
                          class="w-full h-full rounded-full object-cover absolute inset-0" 
                          alt=""
                          @error="handleImageError($event, user)"
                        >
                        <span v-if="!user.profile_photo || user.imageError" class="relative z-10">{{ user.full_name?.charAt(0) || 'U' }}</span>
                      </div>
                    </div>
                    <div>
                      <div class="font-medium text-gray-900">{{ user.full_name }}</div>
                      <div class="text-sm text-gray-500">@{{ user.username }}</div>
                    </div>
                  </div>
                </td>


                <!-- Role & Status -->
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="space-y-2">
                    <span class="px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full" 
                          :class="getRoleClass(user.role)">
                      {{ user.role }}
                    </span>
                    <span class="px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full block w-fit"
                          :class="getStatusClass(user.status)">
                      {{ user.status || 'approved' }}
                    </span>
                  </div>
                </td>

                <!-- Contact Info -->
                <td class="px-6 py-4">
                  <div class="space-y-1">
                    <div class="flex items-center text-sm text-gray-600">
                      <svg class="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                      </svg>
                      {{ user.email }}
                    </div>
                    <div v-if="user.phone_number" class="flex items-center text-sm text-gray-600">
                      <svg class="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                      </svg>
                      {{ user.phone_number }}
                    </div>
                  </div>
                </td>

                <!-- Role-specific Details -->
                <td class="px-6 py-4">
                  <div class="space-y-1">
                    <!-- Student Details -->
                    <div v-if="user.role === 'student'" class="text-sm">
                      <div class="flex items-center text-gray-600">
                        <svg class="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                        </svg>
                        Gender: {{ user.gender || 'Not specified' }}
                      </div>
                      <div class="flex items-center text-gray-600 mt-1">
                        <svg class="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16l14-7 14 7"></path>
                        </svg>
                        School ID: {{ user.schoolid || 'N/A' }}
                      </div>
                    </div>

                    <!-- Teacher Details -->
                    <div v-if="user.role === 'teacher'" class="text-sm">
                      <div class="flex items-center text-gray-600">
                        <svg class="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                        </svg>
                        Subjects: {{ user.subject_assigned || 'Not assigned' }}
                      </div>
                    </div>

                    <!-- EduOffice Details -->
                    <div v-if="user.role === 'eduoffice'" class="text-sm">
                      <div class="flex items-center text-gray-600">
                        <svg class="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16l14-7 14 7"></path>
                        </svg>
                        Supervising: {{ user.school_supervising || 'All schools' }}
                      </div>
                    </div>

                    <!-- Gender for other roles -->
                    <div v-if="user.role !== 'student' && user.gender" class="flex items-center text-sm text-gray-600">
                      <svg class="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                      </svg>
                      Gender: {{ user.gender }}
                    </div>
                  </div>
                </td>

                <!-- Actions -->
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center space-x-2">
                    <button @click="editUser(user)" 
                            class="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-all duration-200 transform hover:scale-110"
                            title="Edit user">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                      </svg>
                    </button>
                    <button @click="deleteUser(user.id)" 
                            class="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-all duration-200 transform hover:scale-110"
                            title="Delete user">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                      </svg>
                    </button>
                    <button @click="viewUserDetails(user)" 
                            class="p-2 text-gray-600 hover:bg-gray-50 rounded-lg transition-all duration-200 transform hover:scale-110"
                            title="View details">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>

              <!-- No results message -->
              <tr v-if="filteredUsers.length === 0">
                <td colspan="5" class="px-6 py-12 text-center">
                  <div class="flex flex-col items-center justify-center space-y-3">
                    <div class="w-20 h-20 bg-gradient-to-br from-gray-100 to-gray-200 rounded-full flex items-center justify-center">
                      <svg class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                    </div>
                    <p class="text-gray-600 text-lg font-medium">No users found</p>
                    <p class="text-gray-400 text-sm">Try adjusting your search or filter criteria</p>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div class="px-6 py-4 bg-gray-50 border-t border-gray-200 flex items-center justify-between">
          <div class="text-sm text-gray-600">
            Showing {{ (currentPage - 1) * itemsPerPage + 1 }} - {{ Math.min(currentPage * itemsPerPage, filteredUsers.length) }} of {{ filteredUsers.length }} users
          </div>
          <div class="flex space-x-2">
            <button @click="prevPage" class="px-3 py-1 border border-gray-300 rounded-md text-sm hover:bg-gray-50 disabled:opacity-50" :disabled="currentPage === 1">
              Previous
            </button>
            <button v-for="page in totalPages" :key="page" @click="currentPage = page" 
                    class="px-3 py-1 rounded-md text-sm" 
                    :class="currentPage === page ? 'bg-blue-600 text-white' : 'border border-gray-300 hover:bg-gray-50'">
              {{ page }}
            </button>
            <button @click="nextPage" class="px-3 py-1 border border-gray-300 rounded-md text-sm hover:bg-gray-50 disabled:opacity-50" :disabled="currentPage === totalPages || totalPages === 0">
              Next
            </button>
          </div>
        </div>

      </div>

      <!-- Feedback message -->
      <transition name="slide-fade">
        <div v-if="message" 
             :class="[messageType === 'success' ? 'bg-green-50 border-l-4 border-green-500 text-green-800' : 'bg-red-50 border-l-4 border-red-500 text-red-800']"
             class="fixed bottom-6 right-6 p-4 rounded-lg shadow-xl transition-all duration-300 z-50">
          <div class="flex items-center space-x-3">
            <svg v-if="messageType === 'success'" class="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <svg v-else class="w-6 h-6 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <p class="font-semibold">{{ message }}</p>
          </div>
        </div>
      </transition>

      <!-- Edit User Modal -->
      <div v-if="showEditModal" class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50" @click.self="closeEditModal">
        <div class="bg-white rounded-3xl shadow-2xl w-full max-w-lg mx-4 overflow-hidden transform transition-all duration-300">
          <!-- Header -->
          <div class="px-8 py-6 bg-gradient-to-r from-violet-600 via-purple-600 to-fuchsia-500 flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-white/20 rounded-xl flex items-center justify-center">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
              </div>
              <div>
                <h3 class="text-xl font-bold text-white">Edit User</h3>
                <p class="text-xs text-white/70">Update user information</p>
              </div>
            </div>
            <button @click="closeEditModal" class="w-8 h-8 rounded-full bg-white/20 hover:bg-white/30 flex items-center justify-center transition-all duration-200 hover:rotate-90">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
          
          <!-- Form -->
          <div class="p-8 space-y-5" v-if="selectedUser">
            <div class="flex justify-center -mt-4 mb-2">
              <div class="w-20 h-20 rounded-full bg-gradient-to-br from-violet-500 to-fuchsia-500 flex items-center justify-center text-white font-bold text-3xl shadow-lg ring-4 ring-white">
                {{ selectedUser.full_name?.charAt(0) || 'U' }}
              </div>
            </div>
            
            <div class="space-y-1">
              <label class="block text-sm font-semibold text-gray-700 ml-1">Full Name</label>
              <div class="relative group">
                <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <svg class="w-5 h-5 text-gray-400 group-focus-within:text-purple-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                  </svg>
                </div>
                <input v-model="selectedUser.full_name" type="text" class="w-full pl-12 pr-4 py-3 bg-gray-50 border-2 border-gray-100 rounded-xl focus:outline-none focus:border-purple-400 focus:bg-white transition-all duration-300">
              </div>
            </div>
            
            <div class="space-y-1">
              <label class="block text-sm font-semibold text-gray-700 ml-1">Email</label>
              <div class="relative group">
                <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <svg class="w-5 h-5 text-gray-400 group-focus-within:text-purple-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                  </svg>
                </div>
                <input v-model="selectedUser.email" type="email" class="w-full pl-12 pr-4 py-3 bg-gray-50 border-2 border-gray-100 rounded-xl focus:outline-none focus:border-purple-400 focus:bg-white transition-all duration-300">
              </div>
            </div>
            
            <div class="space-y-1">
              <label class="block text-sm font-semibold text-gray-700 ml-1">Username</label>
              <div class="relative group">
                <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <svg class="w-5 h-5 text-gray-400 group-focus-within:text-purple-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 11c0 3.517-1.009 6.799-2.753 9.571m-3.44-2.04l.054-.09A13.916 13.916 0 008 11a4 4 0 118 0c0 1.017-.07 2.019-.203 3m-2.118 6.844A21.88 21.88 0 0015.171 17m3.839 1.132c.645-2.266.99-4.659.99-7.132A8 8 0 008 4.07M3 15.364c.64-1.319 1-2.8 1-4.364 0-1.457.39-2.823 1.07-4"></path>
                  </svg>
                </div>
                <input v-model="selectedUser.username" type="text" class="w-full pl-12 pr-4 py-3 bg-gray-50 border-2 border-gray-100 rounded-xl focus:outline-none focus:border-purple-400 focus:bg-white transition-all duration-300">
              </div>
            </div>
            
            <div class="space-y-1">
              <label class="block text-sm font-semibold text-gray-700 ml-1">Phone Number</label>
              <div class="relative group">
                <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <svg class="w-5 h-5 text-gray-400 group-focus-within:text-purple-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                  </svg>
                </div>
                <input v-model="selectedUser.phone_number" type="text" class="w-full pl-12 pr-4 py-3 bg-gray-50 border-2 border-gray-100 rounded-xl focus:outline-none focus:border-purple-400 focus:bg-white transition-all duration-300">
              </div>
            </div>
            
            <div class="grid grid-cols-2 gap-4">
              <div class="space-y-1">
                <label class="block text-sm font-semibold text-gray-700 ml-1">Role</label>
                <div class="relative">
                  <select v-model="selectedUser.role" class="w-full px-4 py-3 bg-gray-50 border-2 border-gray-100 rounded-xl focus:outline-none focus:border-purple-400 focus:bg-white transition-all duration-300 appearance-none cursor-pointer">
                    <option value="student">Student</option>
                    <option value="teacher">Teacher</option>
                    <option value="eduoffice">EduOffice</option>
                    <option value="admin">Admin</option>
                  </select>
                  <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none">
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                    </svg>
                  </div>
                </div>
              </div>
              <div class="space-y-1">
                <label class="block text-sm font-semibold text-gray-700 ml-1">Status</label>
                <div class="relative">
                  <select v-model="selectedUser.status" class="w-full px-4 py-3 bg-gray-50 border-2 border-gray-100 rounded-xl focus:outline-none focus:border-purple-400 focus:bg-white transition-all duration-300 appearance-none cursor-pointer">
                    <option value="approved">Approved</option>
                    <option value="pending">Pending</option>
                    <option value="rejected">Rejected</option>
                  </select>
                  <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none">
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                    </svg>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Footer -->
          <div class="px-8 py-6 bg-gray-50/50 flex justify-end space-x-4 rounded-b-3xl">
            <button @click="closeEditModal" class="px-6 py-3 border-2 border-gray-200 rounded-xl text-gray-600 font-semibold hover:border-gray-300 hover:bg-gray-100 transition-all duration-300 hover:-translate-y-0.5">
              Cancel
            </button>
            <button @click="saveUserEdit" class="px-8 py-3 bg-gradient-to-r from-violet-600 to-fuchsia-500 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-0.5 hover:scale-105 flex items-center space-x-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
              </svg>
              <span>Save Changes</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  data() {
    return {
      allUsers: [],
      message: "",
      messageType: "success",
      searchQuery: "",
      roleFilter: "",
      statusFilter: "",
      currentPage: 1,
      itemsPerPage: 5,
      showEditModal: false,
      selectedUser: null,
    };
  },

  computed: {
    pendingUsers() {
      return this.allUsers.filter(user => user.status === 'pending');
    },
    filteredUsers() {
      let users = this.allUsers.filter(user => {
        const matchesSearch = this.searchQuery === "" || 
          user.full_name?.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          user.email?.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          user.username?.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          user.role?.toLowerCase().includes(this.searchQuery.toLowerCase());
        
        const matchesRole = this.roleFilter === "" || user.role === this.roleFilter;
        const matchesStatus = this.statusFilter === "" || (user.status || 'approved') === this.statusFilter;
        
        return matchesSearch && matchesRole && matchesStatus;
      });
      
      // Sort pending users to top
      users.sort((a, b) => {
        const statusA = a.status || 'approved';
        const statusB = b.status || 'approved';
        if (statusA === 'pending' && statusB !== 'pending') return -1;
        if (statusA !== 'pending' && statusB === 'pending') return 1;
        return 0;
      });
      
      return users;
    },
    paginatedUsers() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredUsers.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredUsers.length / this.itemsPerPage);
    }
  },

  mounted() {
    this.fetchAllUsers();
  },

  methods: {
    countByRole(role) {
      return this.allUsers.filter(u => u.role === role).length;
    },
    getRoleClass(role) {
      const classes = {
        'admin': 'bg-purple-100 text-purple-800',
        'teacher': 'bg-blue-100 text-blue-800',
        'student': 'bg-green-100 text-green-800',
        'eduoffice': 'bg-orange-100 text-orange-800'
      };
      return classes[role] || 'bg-gray-100 text-gray-800';
    },
    getStatusClass(status) {
      const classes = {
        'approved': 'bg-green-100 text-green-800',
        'pending': 'bg-yellow-100 text-yellow-800',
        'rejected': 'bg-red-100 text-red-800'
      };
      return classes[status] || 'bg-green-100 text-green-800';
    },

    async fetchAllUsers() {
      try {
        const res = await fetch("http://127.0.0.1:8000/api/admin/all-users");
        if (!res.ok) throw new Error("Failed to fetch users");
        this.allUsers = await res.json();
      } catch (err) {
        console.error(err);
        this.message = "Failed to load users.";
        this.messageType = "error";
      }
    },

    editUser(user) {
      this.selectedUser = { ...user };
      this.showEditModal = true;
    },
    closeEditModal() {
      this.showEditModal = false;
      this.selectedUser = null;
    },
async saveUserEdit() {
      try {
        const res = await fetch(`http://127.0.0.1:8000/api/admin/edit-user/${this.selectedUser.id}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            full_name: this.selectedUser.full_name,
            email: this.selectedUser.email,
            role: this.selectedUser.role,
            phone: this.selectedUser.phone_number,
            status: this.selectedUser.status
          })
        });

        if (res.ok) {
          await this.fetchAllUsers();
          this.message = "User updated successfully!";
          this.messageType = "success";
          this.closeEditModal();
        } else {
          const data = await res.json();
          this.message = data.detail || "Failed to update user.";
          this.messageType = "error";
        }
      } catch (err) {
        console.error(err);
        this.message = "Error updating user.";
        this.messageType = "error";
      }
      setTimeout(() => (this.message = ""), 3000);
    },

    async deleteUser(userId) {
      if (confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
        try {
          const res = await fetch(`http://127.0.0.1:8000/api/admin/delete-user/${userId}`, {
            method: "DELETE",
            headers: { "Content-Type": "application/json" }
          });

          if (res.ok) {
            this.allUsers = this.allUsers.filter(u => u.id !== userId);
            this.message = "User deleted successfully!";
            this.messageType = "success";
          } else {
            const data = await res.json();
            this.message = data.detail || "Failed to delete user.";
            this.messageType = "error";
          }
        } catch (err) {
          console.error(err);
          this.message = "Error deleting user.";
          this.messageType = "error";
        }
        setTimeout(() => (this.message = ""), 3000);
      }
    },

    getProfilePhotoUrl(photoPath) {
      if (!photoPath) return null;
      if (photoPath.startsWith('http://') || photoPath.startsWith('https://')) {
        return photoPath;
      }
      // Ensure path starts with /
      const path = photoPath.startsWith('/') ? photoPath : '/' + photoPath;
      return `http://127.0.0.1:8000${path}`;
    },
    handleImageError(event, user) {
      user.imageError = true;
      event.target.style.display = 'none';
    },
    viewUserDetails(user) {
      console.log('View details:', user);
      this.message = "View details - Coming soon!";
      this.messageType = "success";
      setTimeout(() => (this.message = ""), 3000);
    },
    redirectToRegister() {
      this.$router.push('/register');
    },

    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },

    async approveUser(userId) {
      try {
        const res = await fetch(`http://127.0.0.1:8000/api/admin/update-status/${userId}`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ status: "approved" })
        });

        if (res.ok) {
          await this.fetchAllUsers();
          this.message = "User approved successfully!";
          this.messageType = "success";
        } else {
          const data = await res.json();
          this.message = data.detail || "Failed to approve user.";
          this.messageType = "error";
        }
      } catch (err) {
        console.error(err);
        this.message = "Error approving user.";
        this.messageType = "error";
      }
      setTimeout(() => (this.message = ""), 3000);
    },

    async rejectUser(userId) {
      try {
        const res = await fetch(`http://127.0.0.1:8000/api/admin/update-status/${userId}`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ status: "rejected" })
        });

        if (res.ok) {
          await this.fetchAllUsers();
          this.message = "User rejected successfully!";
          this.messageType = "success";
        } else {
          const data = await res.json();
          this.message = data.detail || "Failed to reject user.";
          this.messageType = "error";
        }
      } catch (err) {
        console.error(err);
        this.message = "Error rejecting user.";
        this.messageType = "error";
      }
      setTimeout(() => (this.message = ""), 3000);
    }

  },
};
</script>

<style scoped>
.table-wrapper {
  position: relative;
  overflow: hidden;
}

.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* Hover effects */
.hover-scale {
  transition: transform 0.2s;
}

.hover-scale:hover {
  transform: scale(1.02);
}
</style>
