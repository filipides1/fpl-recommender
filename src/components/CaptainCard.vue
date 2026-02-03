<template>
  <div class="captain-card">
    <div class="badge">⭐ Captain Pick</div>
    <h2>{{ captain }}</h2>
    <p class="reason">{{ reason }}</p>
  </div>
</template>

<script>
export default {
  name: 'CaptainCard',
  props: {
    captain: {
      type: String,
      required: true
    },
    reason: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
.captain-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  text-align: center;
  position: relative;
  overflow: hidden;
}

.captain-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6px;
  background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
}

.badge {
  display: inline-block;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 20px;
}

h2 {
  font-size: 36px;
  color: #2d3748;
  margin-bottom: 16px;
  font-weight: 700;
}

.reason {
  color: #718096;
  font-size: 16px;
  line-height: 1.6;
  max-width: 500px;
  margin: 0 auto;
}
</style>
