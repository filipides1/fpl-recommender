<template>
  <div class="transfer-container">
    <div class="transfer-section">
      <h3 class="section-title in">
        <span class="icon">📈</span>
        Transfer In
      </h3>
      <ul class="transfer-list">
        <li v-for="(player, index) in transfersIn" :key="'in-' + index" class="transfer-item in">
          {{ player }}
        </li>
      </ul>
    </div>

    <div class="transfer-section">
      <h3 class="section-title out">
        <span class="icon">📉</span>
        Transfer Out
      </h3>
      <ul class="transfer-list">
        <li v-for="(reason, index) in transfersOut" :key="'out-' + index" class="transfer-item out">
          {{ reason }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TransferList',
  props: {
    transfersIn: {
      type: Array,
      required: true
    },
    transfersOut: {
      type: Array,
      required: true
    }
  }
}
</script>

<style scoped>
.transfer-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  margin-top: 32px;
}

.transfer-section {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 3px solid;
}

.section-title.in {
  color: #48bb78;
  border-color: #48bb78;
}

.section-title.out {
  color: #f56565;
  border-color: #f56565;
}

.icon {
  font-size: 24px;
}

.transfer-list {
  list-style: none;
}

.transfer-item {
  padding: 14px 16px;
  margin-bottom: 10px;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 500;
  transition: transform 0.2s;
}

.transfer-item:hover {
  transform: translateX(4px);
}

.transfer-item.in {
  background: #f0fff4;
  color: #22543d;
  border-left: 4px solid #48bb78;
}

.transfer-item.out {
  background: #fff5f5;
  color: #742a2a;
  border-left: 4px solid #f56565;
}

.transfer-item:last-child {
  margin-bottom: 0;
}
</style>
