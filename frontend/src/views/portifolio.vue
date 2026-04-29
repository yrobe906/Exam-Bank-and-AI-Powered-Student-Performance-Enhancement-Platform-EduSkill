<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <LandingHeader />
    
    <!-- Hero Section -->
    <HeroSection />
    
    <!-- Stats Section -->
    <StatsSection />
    
    <!-- Partners Section -->
    <PartnersSection />
    
    <!-- Features Section -->
    <FeatureCardsSection />
    
    <!-- Testimonials Section -->
    <TestimonialsSection />
    
    <!-- Pricing Section -->
    <PricingSection />
    
    <!-- FAQ Section -->
    <FAQSection />
    
    <!-- Footer -->
    <LandingFooter />
    
    <!-- Back to Top Button -->
    <BackToTop />
  </div>
</template>

<script setup>
import LandingHeader from '@/components/Landing/Header.vue'
import HeroSection from '@/components/Landing/HeroSection.vue'
import StatsSection from '@/components/Landing/StatsSection.vue'
import PartnersSection from '@/components/Landing/PartnersSection.vue'
import FeatureCardsSection from '@/components/Landing/FeatureCardsSection.vue'
import TestimonialsSection from '@/components/Landing/TestimonialsSection.vue'
import PricingSection from '@/components/Landing/PricingSection.vue'
import FAQSection from '@/components/Landing/FAQSection.vue'
import LandingFooter from '@/components/Landing/Footer.vue'
import BackToTop from '@/components/Landing/BackToTop.vue'
</script>

