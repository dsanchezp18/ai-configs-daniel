export type Window = { kind: string; percentUsed: number; resetsAt?: string }
export type Usage = {
  windows: Window[]
  contextPercent?: number
  costUsd?: number
}
export type Repo = { branch: string; changed: number; isRepo: boolean }

declare module 'claude-code' {
  interface PluginState {
    'cc-daniel': {
      usage: Usage | null
      repo: Repo | null
      tree: string[]
      commits: string
    }
  }
}
