<template>
  <div class="page-wrapper">
    <div class="card">
      <h2 class="title">Registered Users</h2>

      <div class="table-card">
        <table class="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Full Name</th>
              <th>Email</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="u in users"
              :key="u.id"
            >
              <td>{{ u.id }}</td>
              <td>{{ u.full_name }}</td>
              <td>{{ u.email }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <p v-if="users.length === 0" class="empty-message">
        No users registered yet!
      </p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      users: []
    }
  },
  async mounted() {
    try {
      const res = await fetch("http://127.0.0.1:8000/users");
      this.users = await res.json();
    } catch (err) {
      console.error("Failed to load users:", err);
    }
  }
}
</script>

<style scoped>
/* Page Wrapper */
.page-wrapper {
  min-height: 100vh;
  background: #f6f7fb;
  display: flex;
  justify-content: center;
  padding: 40px 20px;
}

/* Card container */
.card {
  width: 100%;
  max-width: 850px;
  background: rgb(198, 200, 200);
  border-radius: 30px;
  padding: 35px;
  box-shadow: 0 10px 35px rgba(0,0,0,0.07);
  border: 1px solid #e5e7eb;
}

/* Title */
.title {
  text-align: center;
  font-weight: 700;
  font-size: 28px;
  color: #1f2937;
  margin-bottom: 25px;
}

/* Table area wrapped in card */
.table-card {
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid #e5e7eb;
  background: #ffffff;
}

/* Table style */
.table {
  width: 100%;
  border-collapse: collapse;
  font-size: 16px;
  color: #374151;
}

.table thead {
  background: #f3f4f6;
}

.table th {
  padding: 14px;
  font-weight: 600;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.table td {
  padding: 14px;
  border-bottom: 1px solid #f0f0f0;
}

/* Hover row */
.table tbody tr:hover {
  background: #09b3b3;
  transition: 0.25s;
}

/* Empty message */
.empty-message {
  margin-top: 20px;
  text-align: center;
  color: #bd0c14;
  font-size: 18px;
}
</style>
