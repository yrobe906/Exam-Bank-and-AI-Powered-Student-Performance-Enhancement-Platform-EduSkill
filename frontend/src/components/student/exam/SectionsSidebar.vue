<template>
  <div class="sections-sidebar">
    <div v-for="section in sections" :key="section.name" 
         class="section-item"
         :class="{ 'active-section': currentSection === section.name }"
         @click="$emit('update:current-section', section.name)">
      <div class="section-name">{{ section.name }}</div>
      <div class="section-progress">
        <span>{{ section.completed }}/{{ section.total }}</span>
        <span class="status-text">Done</span>
      </div>
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: (section.completed/section.total)*100 + '%' }"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SectionsSidebar',
  props: {
    sections: Array,
    currentSection: String
  }
}
</script>

<style scoped>

.sections-sidebar {
  background: white;
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  height: fit-content;
}

.section-item {
  padding: 1rem;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 0.75rem;
  border: 2px solid transparent;
}

.section-item:hover {
  background: #f8fafc;
}

.active-section {
  background: #eff6ff;
  border-color: #2563eb;
}

.section-name {
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.section-progress {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: #64748b;
  margin-bottom: 0.5rem;
}

.status-text {
  color: #2563eb;
  font-weight: 500;
}

.progress-bar {
  height: 4px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #2563eb, #7c3aed);
  transition: width 0.3s ease;
}
</style>