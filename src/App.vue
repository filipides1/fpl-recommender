<template>
  <div class="app">
    <header class="header">
      <div class="container">
        <h1 class="title">
          <span class="emoji">⚽</span>
          FPL AI Recommender
        </h1>
        <p class="subtitle">Powered by Groq & Llama</p>
      </div>
    </header>

    <main class="container main-content">
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Loading recommendations...</p>
      </div>

      <div v-else-if="error" class="error-message">
        <p>❌ {{ error }}</p>
      </div>

      <div v-else class="content">
        <CaptainCard 
          :captain="picks.gw_captain" 
          :reason="picks.captain_reason" 
        />

        <div class="differential-card">
          <div class="badge-differential">💎 Differential Pick</div>
          <h3>{{ picks.differential }}</h3>
          <p>{{ picks.differential_reason }}</p>
        </div>

        <TransferList 
          :transfersIn="picks.transfers_in" 
          :transfersOut="picks.transfers_out" 
        />

        <div class="advice-card">
          <h3>
            <span class="icon">💡</span>
            General Advice
          </h3>
          <p>{{ picks.general_advice }}</p>
        </div>

        <footer class="update-info">
          <p>🤖 Updated automatically every Friday at 18:00 UTC</p>
        </footer>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import CaptainCard from './components/CaptainCard.vue'
import TransferList from './components/TransferList.vue'

export default {
  name: 'App',
  components: {
    CaptainCard,
    TransferList
  },
  setup() {
    const picks = ref({})
    const loading = ref(true)
    const error = ref(null)

    const fetchPicks = async () => {
      try {
        const response = await fetch('/picks.json')
        if (!response.ok) {
          throw new Error('Failed to load picks')
        }
        picks.value = await response.json()
      } catch (err) {
        error.value = err.message
        console.error('Error fetching picks:', err)
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      fetchPicks()
    })

    return {
      picks,
      loading,
      error
    }
  }
}
</script>

<style>
.app {
  min-height: 100vh;
  padding-bottom: 60px;
}

.header {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  padding: 40px 20px;
  text-align: center;
  color: white;
  margin-bottom: 40px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.title {
  font-size: 48px;
  font-weight: 800;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.emoji {
  font-size: 52px;
}

.subtitle {
  font-size: 18px;
  opacity: 0.95;
  font-weight: 500;
}

.main-content {
  animation: fadeIn 0.6s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.loading {
  text-align: center;
  padding: 60px 20px;
  color: white;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  margin: 0 auto 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-message {
  background: #fed7d7;
  color: #742a2a;
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  font-weight: 600;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.differential-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  text-align: center;
  border-top: 6px solid #f6ad55;
}

.badge-differential {
  display: inline-block;
  background: linear-gradient(135deg, #f6ad55 0%, #ed8936 100%);
  color: white;
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 16px;
}

.differential-card h3 {
  font-size: 28px;
  color: #2d3748;
  margin-bottom: 12px;
}

.differential-card p {
  color: #718096;
  font-size: 15px;
  line-height: 1.6;
}

.advice-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.advice-card h3 {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 22px;
  color: #2d3748;
  margin-bottom: 16px;
  font-weight: 700;
}

.advice-card .icon {
  font-size: 28px;
}

.advice-card p {
  color: #4a5568;
  font-size: 16px;
  line-height: 1.7;
}

.update-info {
  text-align: center;
  padding: 24px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: white;
  font-size: 14px;
  font-weight: 500;
}

@media (max-width: 768px) {
  .title {
    font-size: 32px;
  }
  
  .emoji {
    font-size: 36px;
  }
  
  .subtitle {
    font-size: 16px;
  }
}
</style>
