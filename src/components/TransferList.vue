<template>
  <div class="transfer-container">
    <div class="transfer-section">
      <h3 class="section-title in">
        <span class="icon">📈</span>
        Transfer In
      </h3>
      
      <div v-for="(players, position) in transfersIn" :key="'in-' + position" class="position-group">
        <h4 class="position-header">
          <span class="position-icon">{{ getPositionIcon(position) }}</span>
          {{ getPositionName(position) }}
        </h4>
        <ul class="transfer-list">
          <li v-for="(player, index) in players" :key="'in-' + position + '-' + index" class="transfer-item in">
            <div class="player-info">
              <div class="player-name">{{ player.name }}</div>
              <div class="player-team">{{ player.team }}</div>
            </div>
            <div class="player-reason">{{ player.reason }}</div>
          </li>
        </ul>
      </div>
    </div>

    <div class="transfer-section">
      <h3 class="section-title out">
        <span class="icon">📉</span>
        Transfer Out
      </h3>
      
      <div v-for="(players, position) in transfersOut" :key="'out-' + position" class="position-group">
        <h4 class="position-header">
          <span class="position-icon">{{ getPositionIcon(position) }}</span>
          {{ getPositionName(position) }}
        </h4>
        <ul class="transfer-list">
          <li v-for="(player, index) in players" :key="'out-' + position + '-' + index" class="transfer-item out">
            <div class="player-info">
              <div class="player-name">{{ player.name }}</div>
              <div class="player-team">{{ player.team }}</div>
            </div>
            <div class="player-reason">{{ player.reason }}</div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TransferList',
  props: {
    transfersIn: {
      type: Object,
      required: true
    },
    transfersOut: {
      type: Object,
      required: true
    }
  },
  methods: {
    getPositionIcon(position) {
      const icons = {
        'GKP': '🧤',
        'DEF': '🛡️',
        'MID': '⚡',
        'FWD': '⚽'
      }
      return icons[position] || '👤'
    },
    getPositionName(position) {
      const names = {
        'GKP': 'Goalkeeper',
        'DEF': 'Defenders',
        'MID': 'Midfielders',
        'FWD': 'Forwards'
      }
      return names[position] || position
    }
  }
}
</script>

<style scoped>
.transfer-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
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

.position-group {
  margin-bottom: 24px;
}

.position-group:last-child {
  margin-bottom: 0;
}

.position-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #4a5568;
  margin-bottom: 12px;
  padding: 8px 12px;
  background: #f7fafc;
  border-radius: 8px;
}

.position-icon {
  font-size: 20px;
}

.transfer-list {
  list-style: none;
}

.transfer-item {
  padding: 14px 16px;
  margin-bottom: 10px;
  border-radius: 10px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.transfer-item:hover {
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.transfer-item.in {
  background: #f0fff4;
  border-left: 4px solid #48bb78;
}

.transfer-item.out {
  background: #fff5f5;
  border-left: 4px solid #f56565;
}

.transfer-item:last-child {
  margin-bottom: 0;
}

.player-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.player-name {
  font-weight: 700;
  font-size: 15px;
  color: #2d3748;
}

.transfer-item.in .player-name {
  color: #22543d;
}

.transfer-item.out .player-name {
  color: #742a2a;
}

.player-team {
  font-size: 13px;
  font-weight: 500;
  color: #718096;
  background: rgba(255, 255, 255, 0.7);
  padding: 2px 8px;
  border-radius: 6px;
}

.player-reason {
  font-size: 13px;
  line-height: 1.5;
  color: #4a5568;
  font-style: italic;
}

@media (max-width: 768px) {
  .transfer-container {
    grid-template-columns: 1fr;
  }
  
  .player-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }
}
</style>
