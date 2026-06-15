<script setup lang="ts">
import { ref } from 'vue'
import { useExcelStore } from '@/stores/excelStore'
import { Grid, ChevronUp, ChevronDown, Table2 } from '@lucide/vue'

const excelStore = useExcelStore()
const collapsed = ref(false)

function toggleCollapsed() {
  collapsed.value = !collapsed.value
}
</script>

<template>
  <div
    v-if="excelStore.selectionData"
    class="mx-auto max-w-[800px] mb-3 bg-surface-container-low/95 border border-outline-variant/60 rounded-xl overflow-hidden shadow-[0_4px_12px_rgba(0,0,0,0.03)] backdrop-blur-md transition-all duration-300"
    :class="collapsed ? 'max-h-10' : 'max-h-[300px]'"
  >
    
    <div
      class="flex items-center justify-between px-4 py-2 border-b border-outline-variant/30 bg-surface-container-high/40 cursor-pointer select-none"
      @click="toggleCollapsed"
    >
      <div class="flex items-center gap-2 text-on-surface-variant">
        <Table2 :size="15" class="text-secondary" />
        <span class="text-[12px] font-semibold tracking-wide uppercase font-mono">
          Selection Preview: {{ excelStore.selectedRange }}
        </span>
        <span class="text-[11px] text-on-surface-variant/60">
          ({{ excelStore.selectionData.total_rows }} rows × {{ excelStore.selectionData.total_cols }} cols)
        </span>
      </div>
      <button class="p-1 rounded-md hover:bg-surface-container-high text-on-surface-variant/80 transition-colors">
        <ChevronDown v-if="collapsed" :size="14" />
        <ChevronUp v-else :size="14" />
      </button>
    </div>

    
    <div v-if="!collapsed" class="overflow-auto p-3 max-h-[220px]">
      <table class="w-full border-collapse text-left font-mono text-[11px]">
        <thead>
          <tr>
            <th class="sticky top-0 bg-surface-container-high/70 backdrop-blur-sm border border-outline-variant/30 p-1.5 text-center text-on-surface-variant/50 w-8 select-none">
              
            </th>
            <th
              v-for="header in excelStore.selectionData.headers"
              :key="header"
              class="sticky top-0 bg-surface-container-high/70 backdrop-blur-sm border border-outline-variant/30 p-1.5 text-center text-on-surface-variant/80 font-bold min-w-[70px] select-none"
            >
              {{ header }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(rowVal, rIdx) in excelStore.selectionData.values"
            :key="rIdx"
            class="hover:bg-surface-container-high/30 transition-colors"
          >
            
            <td class="bg-surface-container-high/40 border border-outline-variant/30 p-1.5 text-center font-bold text-on-surface-variant/70 w-8 select-none">
              {{ excelStore.selectionData.row_labels[rIdx] }}
            </td>
            
            <td
              v-for="(cellVal, cIdx) in rowVal"
              :key="cIdx"
              class="border border-outline-variant/20 p-1.5 text-on-surface/90 truncate max-w-[150px]"
              :title="String(cellVal !== null ? cellVal : '')"
            >
              {{ cellVal !== null ? cellVal : '' }}
            </td>
          </tr>
        </tbody>
      </table>
      <div
        v-if="excelStore.selectionData.total_rows > 10 || excelStore.selectionData.total_cols > 5"
        class="mt-2 text-center text-[10px] text-on-surface-variant/50 italic"
      >
        Showing first 10 rows and 5 columns
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
