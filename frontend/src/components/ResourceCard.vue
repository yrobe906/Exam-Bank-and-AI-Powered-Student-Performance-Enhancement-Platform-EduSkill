<template>
  <article
    class="bg-white/60 dark:bg-slate-800/60 backdrop-blur rounded-xl shadow-md overflow-hidden transform transition-all hover:-translate-y-1 hover:shadow-lg resource-animate"
    :aria-labelledby="`res-${resource.id}-title`"
  >
    <div class="relative">
      <!-- Subject Logo -->
      <img :src="subjectLogo" alt="" class="w-full h-40 object-cover" />

      <!-- Resource Type Badge -->
      <div class="absolute left-3 top-3 flex items-center gap-2">
        <span
          class="px-2 py-1 rounded-full text-xs font-semibold bg-white/80 dark:bg-black/30 text-slate-800"
        >
          {{ resource.type.toUpperCase() }}
        </span>
      </div>

      <!-- Price Badge on Image -->
      <div class="absolute right-3 top-3">
        <span
          class="px-2 py-1 rounded-full text-xs font-bold cursor-pointer transition-transform duration-300 hover:scale-110"
          :class="resource.price > 0 ? 'bg-yellow-400 text-slate-900' : 'bg-emerald-400 text-white'"
        >
          {{ resource.price > 0 ? `PREMIUM ${resource.price} ETB` : 'FREE' }}
        </span>
      </div>
    </div>

    <div class="p-4">
      <h3
        :id="`res-${resource.id}-title`"
        class="font-semibold text-slate-900 dark:text-white text-sm leading-tight hover:text-cyan-500 transition-colors"
      >
        {{ resource.title }}
      </h3>
      <p class="text-xs text-slate-600 dark:text-slate-300 mt-1 line-clamp-2">
        {{ resource.description }}
      </p>

      <!-- Price Under Description -->
      <div
        class="mt-2 text-xs font-semibold transition-transform duration-300 hover:scale-105"
        :class="resource.price > 0 ? 'text-yellow-500' : 'text-emerald-500'"
      >
        {{ resource.price > 0 ? `${resource.price} ETB` : 'FREE' }}
      </div>

      <div class="mt-3 flex items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <div class="text-xs text-slate-500 dark:text-slate-300">
            <span class="font-medium">{{ resource.subject }}</span>
            <span class="mx-1">•</span>
            <span>{{ resource.class_level }}</span>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <button
            class="px-3 py-1 rounded-full text-xs font-semibold bg-white/80 dark:bg-slate-700/60 hover:scale-105 focus:outline-none transition-transform"
            @click="$emit('view', resource)"
            aria-label="View resource details"
          >
            View
          </button>

          <button
            v-if="resource.price > 0"
            class="px-3 py-1 rounded-full text-xs font-semibold bg-gradient-to-br from-cyan-500 to-purple-600 text-white hover:brightness-105 focus:outline-none transition-transform"
            @click="$emit('buy', resource)"
            aria-label="Buy resource"
          >
            Buy
          </button>

          <button
            v-else
            class="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500 text-white hover:brightness-105 focus:outline-none transition-transform"
            @click="$emit('download', resource)"
            aria-label="Download resource"
          >
            Download
          </button>
        </div>
      </div>
    </div>
  </article>
</template>

<script setup>
import mathsLogo from '@/assets/images/maths.png'
import physicsLogo from '@/assets/images/physics.png'
import chemistryLogo from '@/assets/images/chemistry.png'
import biologyLogo from '@/assets/images/biology.png'
import englishLogo from '@/assets/images/english.png'
import entranceLogo from '@/assets/images/videotutor1.png'

const props = defineProps({
  resource: { type: Object, required: true }
})
const emit = defineEmits(["view", "download", "buy"])

// Map subject to logos
const subjectLogos = {
  Mathematics: mathsLogo,
  Physics: physicsLogo,
  Chemistry: chemistryLogo,
  Biology: biologyLogo,
  English: englishLogo,
  Entrance: entranceLogo
}

const subjectLogo = subjectLogos[props.resource.subject] || mathsLogo
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

@keyframes floatIn {
  from { opacity: 0; transform: translateY(8px) scale(0.995); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
.resource-animate {
  animation: floatIn 420ms cubic-bezier(.2,.8,.2,1);
}
</style>
