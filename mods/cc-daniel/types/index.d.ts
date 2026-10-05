export type Window = { kind: string; percentUsed: number; resetsAt?: string }
export type Usage = {
  windows: Window[]
  contextPercent?: number
}

declare module 'claude-code' {
  interface PluginState {
    'cc-daniel': {
      usage: Usage | null
    }
  }
}
