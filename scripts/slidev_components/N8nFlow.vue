<template>
  <div class="n8n-canvas">
    <div class="n8n-flow" :class="layout">
      <template v-for="(node, i) in nodes" :key="i">
        <!-- Error branch node -->
        <div v-if="node.branch === 'error'" class="branch-wrapper">
          <div class="branch-line error-line"></div>
          <div class="n8n-node error">
            <div class="node-icon-wrap error">
              <Icon :icon="node.icon" :width="28" :height="28" />
            </div>
            <div class="node-info">
              <div class="node-label">{{ node.label }}</div>
              <div v-if="node.desc" class="node-desc">{{ node.desc }}</div>
            </div>
          </div>
        </div>

        <!-- Regular node -->
        <div v-else class="n8n-node" :class="node.variant || 'default'">
          <div class="node-icon-wrap" :class="node.variant || 'default'">
            <Icon :icon="node.icon" :width="32" :height="32" />
          </div>
          <div class="node-info">
            <div class="node-label">{{ node.label }}</div>
            <div v-if="node.desc" class="node-desc">{{ node.desc }}</div>
          </div>
          <div v-if="node.badge" class="node-badge" :class="node.badgeVariant || ''">
            {{ node.badge }}
          </div>
        </div>

        <!-- Connector arrow -->
        <div v-if="i < nodes.length - 1 && !nodes[i+1].branch" class="n8n-connector">
          <svg width="44" height="12" viewBox="0 0 44 12" fill="none">
            <line x1="0" y1="6" x2="36" y2="6" stroke="#E63946" stroke-width="1.5"
                  stroke-dasharray="3 2" />
            <polygon points="36,2 44,6 36,10" fill="#E63946" />
          </svg>
        </div>
      </template>
    </div>

    <!-- Legend / caption -->
    <div v-if="caption" class="flow-caption">{{ caption }}</div>
  </div>
</template>

<script setup>
import { Icon } from '@iconify/vue'

defineProps({
  nodes: {
    type: Array,
    default: () => []
  },
  layout: {
    type: String,
    default: 'horizontal' // 'horizontal' | 'compact'
  },
  caption: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.n8n-canvas {
  background: #0A1628;
  border-radius: 10px;
  padding: 1.5rem 1.8rem;
  border: 1px solid rgba(255,255,255,0.06);
  box-shadow: 0 8px 32px rgba(0,0,0,0.4);
  position: relative;
  overflow: hidden;
}

/* Subtle grid background like n8n canvas */
.n8n-canvas::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: radial-gradient(rgba(255,255,255,0.04) 1px, transparent 1px);
  background-size: 20px 20px;
  pointer-events: none;
}

.n8n-flow {
  display: flex;
  align-items: center;
  gap: 0;
  flex-wrap: wrap;
  position: relative;
  z-index: 1;
}
.n8n-flow.compact {
  gap: 0.2rem;
}

/* ── NODE ── */
.n8n-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.45rem;
  padding: 0.75rem 0.85rem;
  background: #1E2D40;
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.08);
  min-width: 90px;
  max-width: 105px;
  position: relative;
  transition: transform 0.2s;
}
.n8n-node:hover { transform: translateY(-2px); }

/* Variant top borders */
.n8n-node.trigger   { border-top: 3px solid #F97316; }
.n8n-node.action    { border-top: 3px solid #3B82F6; }
.n8n-node.output    { border-top: 3px solid #22C55E; }
.n8n-node.error     { border-top: 3px solid #EF4444; }
.n8n-node.default   { border-top: 3px solid #E63946; }

/* ── ICON WRAP ── */
.node-icon-wrap {
  width: 44px;
  height: 44px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255,255,255,0.06);
}
.node-icon-wrap.trigger { background: rgba(249,115,22,0.15); }
.node-icon-wrap.action  { background: rgba(59,130,246,0.15); }
.node-icon-wrap.output  { background: rgba(34,197,94,0.15); }
.node-icon-wrap.error   { background: rgba(239,68,68,0.15); }

/* ── LABELS ── */
.node-label {
  font-size: 0.72rem;
  font-weight: 700;
  color: #ffffff;
  text-align: center;
  line-height: 1.2;
}
.node-desc {
  font-size: 0.62rem;
  color: #8096AA;
  text-align: center;
  line-height: 1.3;
}
.node-badge {
  position: absolute;
  top: -8px;
  right: -6px;
  background: #E63946;
  color: white;
  font-size: 0.55rem;
  font-weight: 800;
  padding: 0.1rem 0.35rem;
  border-radius: 999px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.node-badge.success { background: #22C55E; }
.node-badge.warning { background: #F59E0B; }

/* ── CONNECTOR ── */
.n8n-connector {
  display: flex;
  align-items: center;
  padding: 0 0.15rem;
  opacity: 1;
}

/* ── BRANCH (error path) ── */
.branch-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
  margin-left: -0.5rem;
}
.branch-line {
  width: 2px;
  height: 24px;
  background: #EF4444;
  opacity: 1;
}

/* ── CAPTION ── */
.flow-caption {
  margin-top: 0.9rem;
  font-size: 0.68rem;
  color: #8096AA;
  text-align: center;
  font-style: italic;
}
</style>
