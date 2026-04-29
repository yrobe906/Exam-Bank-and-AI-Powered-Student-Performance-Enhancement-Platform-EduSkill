<template>
  <header class="eduskill-header">
    <div class="header-content">
      <h1>EduSkill Hub</h1>
      <slot></slot>
    </div>
  </header>
</template>

<script>
export default {
  name: 'EduskillHeader'
}
</script>

<style scoped>
.eduskill-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  margin-bottom: 20px;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.eduskill-header h1 {
  margin: 0;
  font-size: 2rem;
  font-weight: bold;
}
</style>