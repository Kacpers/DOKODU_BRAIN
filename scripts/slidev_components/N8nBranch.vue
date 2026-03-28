<template>
  <div class="branch-canvas">
    <!-- Root node -->
    <div class="branch-root">
      <div class="branch-node root-node">
        <div class="node-icon-wrap root">
          <Icon :icon="source.icon" :width="30" :height="30" />
        </div>
        <div class="node-label">{{ source.label }}</div>
        <div v-if="source.desc" class="node-desc">{{ source.desc }}</div>
      </div>
    </div>

    <!-- Horizontal lines + branches -->
    <div class="branch-spread">
      <!-- Top connector line across all branches -->
      <div class="spread-bar"></div>

      <div class="branches">
        <div v-for="(branch, i) in branches" :key="i" class="branch-item">
          <!-- Vertical drop line -->
          <div class="drop-line"></div>

          <!-- Branch node -->
          <div class="branch-node leaf-node" :class="branch.variant || 'default'">
            <div class="node-icon-wrap" :class="branch.variant || 'default'">
              <Icon :icon="branch.icon" :width="28" :height="28" />
            </div>
            <div class="node-label">{{ branch.label }}</div>
            <div v-if="branch.desc" class="node-desc">{{ branch.desc }}</div>
          </div>

          <!-- Result tag -->
          <div v-if="branch.result" class="result-tag" :class="branch.variant || 'default'">
            {{ branch.result }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Icon } from '@iconify/vue'

defineProps({
  source: {
    type: Object,
    default: () => ({ icon: 'mdi:lightning-bolt', label: 'START' })
  },
  branches: {
    type: Array,
    default: () => []
  }
})
</script>

<style scoped>
.branch-canvas {
  background: #0A1628;
  border-radius: 10px;
  padding: 1.2rem 1.5rem 1.5rem;
  border: 1px solid rgba(255,255,255,0.06);
  box-shadow: 0 8px 32px rgba(0,0,0,0.4);
  position: relative;
  overflow: hidden;
}
.branch-canvas::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: radial-gradient(rgba(255,255,255,0.04) 1px, transparent 1px);
  background-size: 20px 20px;
  pointer-events: none;
}

/* ── ROOT NODE ── */
.branch-root {
  display: flex;
  justify-content: center;
  margin-bottom: 0;
  position: relative;
  z-index: 1;
}

/* ── SPREAD BAR ── */
.branch-spread {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 1;
}
.spread-bar {
  width: 80%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #E63946 20%, #E63946 80%, transparent);
  opacity: 1;
  margin: 0;
}

/* ── BRANCHES ── */
.branches {
  display: flex;
  gap: 1.2rem;
  justify-content: center;
  align-items: flex-start;
}
.branch-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
}
.drop-line {
  width: 2px;
  height: 20px;
  background: #E63946;
  opacity: 1;
}

/* ── NODES (shared) ── */
.branch-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
  padding: 0.7rem 0.8rem;
  background: #1E2D40;
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.08);
  min-width: 85px;
  max-width: 100px;
}
.root-node {
  border-top: 3px solid #E63946;
}
.leaf-node.trigger  { border-top: 3px solid #F97316; }
.leaf-node.default  { border-top: 3px solid #8096AA; }
.leaf-node.action   { border-top: 3px solid #3B82F6; }

.node-icon-wrap {
  width: 42px;
  height: 42px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255,255,255,0.06);
}
.node-icon-wrap.root    { background: rgba(230,57,70,0.18); }
.node-icon-wrap.trigger { background: rgba(249,115,22,0.15); }
.node-icon-wrap.action  { background: rgba(59,130,246,0.15); }

/* Connector from root to spread bar */
.branch-root::after {
  content: '';
  position: absolute;
  bottom: -14px;
  left: 50%;
  transform: translateX(-50%);
  width: 2px;
  height: 14px;
  background: #E63946;
  opacity: 1;
}

.node-label {
  font-size: 0.7rem;
  font-weight: 700;
  color: #ffffff;
  text-align: center;
  line-height: 1.2;
}
.node-desc {
  font-size: 0.6rem;
  color: #8096AA;
  text-align: center;
  line-height: 1.3;
}

/* ── RESULT TAG ── */
.result-tag {
  font-size: 0.6rem;
  font-weight: 600;
  padding: 0.15rem 0.5rem;
  border-radius: 999px;
  color: white;
  background: #334155;
  text-align: center;
}
.result-tag.trigger { background: rgba(249,115,22,0.4); }
.result-tag.action  { background: rgba(59,130,246,0.3); }
</style>
