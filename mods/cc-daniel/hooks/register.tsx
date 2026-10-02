import { atom, read } from 'claude-code'
import type { Register } from 'claude-code'

const PANE = 'git-tree'
const usageRef = { plugin: 'cc-daniel', key: 'usage' } as const
const repoRef = { plugin: 'cc-daniel', key: 'repo' } as const
const treeRef = { plugin: 'cc-daniel', key: 'tree' } as const
const commitsRef = { plugin: 'cc-daniel', key: 'commits' } as const
const usage = atom({ plugin: 'cc-daniel', key: 'usage' } as const, null)
const repo = atom({ plugin: 'cc-daniel', key: 'repo' } as const, null)
const tree = atom({ plugin: 'cc-daniel', key: 'tree' } as const, [])
const commits = atom({ plugin: 'cc-daniel', key: 'commits' } as const, '')

const WINDOW_NAMES: Record<string, string> = {
  five_hour: '5-hour limit',
  seven_day: '7-day limit',
  spend_limit: 'Spend limit',
}

// One color per lane, like GitKraken's branch colors.
const LANE_COLORS = [
  '#58a6ff',
  '#3fb950',
  '#d29922',
  '#f778ba',
  '#a371f7',
  '#ff7b72',
  '#39c5cf',
  '#ffa657',
]

const SVG_STYLE = `<style>
  text { font-family: system-ui, -apple-system, 'Segoe UI', sans-serif; }
  .s { fill: #1f2328; font-size: 12px; }
  .m { fill: #656d76; font-size: 10.5px; }
  .h { fill: #1f2328; font-size: 12px; font-weight: 600; }
  .t { fill: #8b949e; fill-opacity: 0.28; }
  @media (prefers-color-scheme: dark) {
    .s, .h { fill: #e6edf3; }
    .m { fill: #8b949e; }
  }
</style>`

const esc = (text: string) =>
  text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')

// Green under 60%, yellow under 85%, red above.
const gaugeColor = (percent: number) =>
  percent < 60 ? '#3fb950' : percent < 85 ? '#d29922' : '#f85149'

const barColor = (percent: number) =>
  percent < 60 ? 'green' : percent < 85 ? 'yellow' : 'red'

const bar = (percent: number, cells = 12) => {
  const filled = Math.round((Math.min(percent, 100) / 100) * cells)

  return '█'.repeat(filled) + '░'.repeat(cells - filled)
}

const untilReset = (resetsAt: string | undefined, now: number) => {
  if (!resetsAt) return ''
  const minutes = Math.max(0, Math.round((Date.parse(resetsAt) - now) / 60000))
  const days = Math.floor(minutes / 1440)
  const hours = Math.floor((minutes % 1440) / 60)

  if (days > 0) return `resets in ${days}d ${hours}h`
  if (hours > 0) return `resets in ${hours}h ${minutes % 60}m`

  return `resets in ${minutes}m`
}

// Limits as one row of rounded bars: name and percent, bar, then reset time.
const usageSvg = (data: any, now: number, width: number) => {
  const items: { name: string; percent: number; note: string }[] = [
    ...data.windows.map((w: any) => ({
      name: WINDOW_NAMES[w.kind] ?? w.kind,
      percent: w.percentUsed,
      note: untilReset(w.resetsAt, now),
    })),
    {
      name: 'Context window',
      percent: data.contextPercent ?? 0,
      note: data.costUsd === undefined ? '' : `session cost $${data.costUsd.toFixed(2)}`,
    },
  ]
  const gap = 18
  const cell = (width - gap * (items.length - 1)) / items.length
  const blocks = items
    .map((item, i) => {
      const x = i * (cell + gap)
      const fill = Math.max(0, Math.min(100, item.percent)) * (cell / 100)

      return `<text class="h" x="${x}" y="13">${esc(item.name)}</text>
<text class="h" x="${x + cell}" y="13" text-anchor="end">${item.percent}%</text>
<rect class="t" x="${x}" y="19" width="${cell}" height="9" rx="4.5"/>
<rect x="${x}" y="19" width="${fill}" height="9" rx="4.5" fill="${gaugeColor(item.percent)}"/>
<text class="m" x="${x}" y="42">${esc(item.note)}</text>`
    })
    .join('\n')

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="48" viewBox="0 0 ${width} 48">${SVG_STYLE}${blocks}</svg>`
}

// Turns `git log` rows into lanes, then draws lines, nodes and labels.
const graphSvg = (raw: string, width: number) => {
  const log = raw
    .split('\n')
    .filter(Boolean)
    .map(line => {
      const [hash, parents, refs, subject, age, author] = line.split('\x1f')

      return {
        hash,
        parents: parents ? parents.split(' ') : [],
        refs: refs ? refs.split(', ').filter(Boolean) : [],
        subject: subject ?? '',
        age: age ?? '',
        author: author ?? '',
      }
    })

  const rowHeight = 30
  const laneGap = 16
  const lanes: (string | null)[] = []
  const place = new Map<string, { row: number; col: number }>()
  const laneOf = new Map<string, number>()

  log.forEach((commit, row) => {
    let col = lanes.indexOf(commit.hash)

    if (col < 0) {
      col = lanes.indexOf(null)

      if (col < 0) {
        col = lanes.length
        lanes.push(null)
      }
    }

    place.set(commit.hash, { row, col })
    lanes[col] = null

    commit.parents.forEach((parent, i) => {
      if (lanes.includes(parent)) return

      if (i === 0) {
        lanes[col] = parent
        laneOf.set(parent, col)

        return
      }

      let free = lanes.indexOf(null)

      if (free < 0) {
        free = lanes.length
        lanes.push(null)
      }

      lanes[free] = parent
      laneOf.set(parent, free)
    })
  })

  const laneCount = Math.max(1, ...[...place.values()].map(p => p.col + 1), ...laneOf.values())
  const textX = 14 + laneCount * laneGap + 6
  const x = (col: number) => 12 + col * laneGap
  const y = (row: number) => 16 + row * rowHeight
  const bottom = y(log.length)
  const maxChars = Math.max(10, Math.floor((width - textX - 8) / 6.3))

  const edges = log
    .flatMap((commit, row) =>
      commit.parents.map(parent => {
        const from = place.get(commit.hash)!
        const toCol = place.get(parent)?.col ?? laneOf.get(parent) ?? from.col
        const toY = place.has(parent) ? y(place.get(parent)!.row) : bottom
        const color = LANE_COLORS[toCol % LANE_COLORS.length]
        const x1 = x(from.col)
        const x2 = x(toCol)
        const y1 = y(row)
        const d =
          x1 === x2
            ? `M${x1} ${y1} L${x2} ${toY}`
            : `M${x1} ${y1} C${x1} ${y1 + 14}, ${x2} ${y1 + 4}, ${x2} ${y1 + 18} L${x2} ${toY}`

        return `<path d="${d}" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round"/>`
      }),
    )
    .join('\n')

  const rows = log
    .map((commit, row) => {
      const pos = place.get(commit.hash)!
      const color = LANE_COLORS[pos.col % LANE_COLORS.length]
      const isHead = commit.refs.some(ref => ref.startsWith('HEAD'))
      const cy = y(row)
      let cursor = textX
      const pills = commit.refs
        .slice(0, 3)
        .map(ref => {
          const label = ref.replace('HEAD -> ', '').replace('tag: ', '')
          const isTag = ref.startsWith('tag: ')
          const isRemote = label.includes('/')
          const w = Math.round(label.length * 6.1 + 14)
          const pill = `<rect x="${cursor}" y="${cy - 9}" width="${w}" height="17" rx="8.5" fill="${
            isRemote ? 'none' : isTag ? '#d29922' : color
          }" stroke="${isTag ? '#d29922' : color}" stroke-width="1.2"/>
<text x="${cursor + w / 2}" y="${cy + 3.5}" text-anchor="middle" font-size="10.5" font-weight="600" fill="${
            isRemote ? color : '#ffffff'
          }">${esc(label)}</text>`
          cursor += w + 5

          return pill
        })
        .join('\n')
      const room = Math.max(8, Math.floor((width - cursor - 8) / 6.3))
      const subject =
        commit.subject.length > room ? `${commit.subject.slice(0, room - 1)}…` : commit.subject
      const meta = `${commit.hash.slice(0, 7)} · ${commit.author} · ${commit.age}`.slice(0, maxChars + 8)
      const ring = isHead
        ? `<circle cx="${x(pos.col)}" cy="${cy}" r="9" fill="none" stroke="${color}" stroke-width="2"/>`
        : ''

      return `${ring}<circle cx="${x(pos.col)}" cy="${cy}" r="5.5" fill="${color}"/>
<circle cx="${x(pos.col)}" cy="${cy}" r="2.2" fill="#ffffff" fill-opacity="0.85"/>
${pills}
<text class="s" x="${cursor}" y="${cy + 4}">${esc(subject)}</text>
<text class="m" x="${textX}" y="${cy + 17}">${esc(meta)}</text>`
    })
    .join('\n')

  const height = bottom + 8

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">${SVG_STYLE}${edges}${rows}</svg>`
}

// "* a1b2c3d (HEAD -> main) subject" splits into graph, hash, refs, subject.
const TREE_LINE = /^([\s*|\\/_.-]*)([0-9a-f]{7,}) ?(\([^)]*\))? ?(.*)$/

let lastSignature = ''

// Reads usage and git state. The hooks below store the values.
async function gather($: any) {
  const now = await $.session.usage()
  const branch = await $.process.run(['git', 'branch', '--show-current'])
  const status = await $.process.run(['git', 'status', '--porcelain'])
  const text = await $.process.run([
    'git',
    'log',
    '--graph',
    '--all',
    '--decorate',
    '--oneline',
    '-n',
    '60',
  ])
  const rich = await $.process.run([
    'git',
    'log',
    '--all',
    '--topo-order',
    '-n',
    '40',
    '--format=%H%x1f%P%x1f%D%x1f%s%x1f%ar%x1f%an',
  ])

  return {
    usage: {
      windows: now.rateLimits,
      contextPercent: now.context.percent,
      costUsd: now.cost?.usd,
    },
    repo: {
      branch: branch.stdout.trim() || 'detached',
      changed: status.stdout.split('\n').filter(Boolean).length,
      isRepo: branch.exitCode === 0,
    },
    tree: text.exitCode === 0 ? text.stdout.split('\n').filter(Boolean) : [],
    commits: rich.exitCode === 0 ? rich.stdout : '',
  }
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({
      name: 'git-tree',
      description: 'Open the git graph and limits pane',
    })

    const tick = async () => {
      const got = await gather($)
      const signature = JSON.stringify(got)

      if (signature !== lastSignature) {
        lastSignature = signature
        await $.state.set(usageRef, got.usage)
        await $.state.set(repoRef, got.repo)
        await $.state.set(treeRef, got.tree)
        await $.state.set(commitsRef, got.commits)
      }

      const five = got.usage.windows.find((w: any) => w.kind === 'five_hour')
      const parts = [
        got.repo.isRepo
          ? `${got.repo.branch}${got.repo.changed ? ` *${got.repo.changed}` : ''}`
          : '',
        five ? `5h ${five.percentUsed}%` : '',
      ].filter(Boolean)
      $.ui.status(parts.length ? parts.join(' · ') : undefined)
    }

    await tick()
    void $.ui.open({ id: PANE, title: 'Git and limits' })
    $.clock.every(5000, () => void tick())

    return next(e)
  })

  on('command.run', { command: 'git-tree' }, async $ => {
    await $.ui.open({ id: PANE, title: 'Git and limits' })

    return { text: 'Git and limits pane opened.' }
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const now = await read($, usage)

    if (e.props.hasSurvey || now === null) return next(e)

    const clock = await $.clock.now()
    const columns = e.viewport?.columns ?? 100

    if (e.surface === 'terminal') {
      const { Box, Text } = $.ui.resolve(e)
      const items = [
        ...now.windows.map(w => ({
          name: WINDOW_NAMES[w.kind] ?? w.kind,
          percent: w.percentUsed,
        })),
        { name: 'Context', percent: now.contextPercent ?? 0 },
      ]

      return (
        <Box gap={3}>
          {items.map(item => (
            <Box gap={1}>
              <Text bold>{item.name}</Text>
              <Text color={barColor(item.percent)}>{bar(item.percent, 10)}</Text>
              <Text bold>{`${item.percent}%`}</Text>
            </Box>
          ))}
        </Box>
      )
    }

    const { Svg } = $.ui.resolve(e)
    const width = Math.min(1000, Math.max(300, Math.round(columns * 7.2)))

    return <Svg source={usageSvg(now, clock, width)} alt="Usage limits" width={width} />
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const info = await read($, repo)
    const lines = await read($, tree)
    const raw = await read($, commits)
    const columns = e.props.bodyColumns ?? 40

    if (e.surface === 'terminal') {
      const { Box, Text } = $.ui.resolve(e)
      const room = Math.max(1, (e.viewport?.rows ?? 24) - 4)

      return (
        <Box flexDirection="column">
          {info !== null && !info.isRepo && (
            <Text dimColor>This folder is not a git repository.</Text>
          )}
          {lines.slice(0, room).map(line => {
            const part = TREE_LINE.exec(line)

            if (!part) return <Text dimColor>{line}</Text>

            return (
              <Box>
                <Text color="magenta">{part[1]}</Text>
                <Text color="yellow">{part[2]} </Text>
                <Text color="cyan">{part[3] ? `${part[3]} ` : ''}</Text>
                <Text>{part[4]}</Text>
              </Box>
            )
          })}
        </Box>
      )
    }

    const { Box, Text, Svg } = $.ui.resolve(e)
    const width = Math.min(560, Math.max(260, Math.round(columns * 7.4)))

    return (
      <Box flexDirection="column">
        {info !== null && !info.isRepo && (
          <Text dimColor>This folder is not a git repository.</Text>
        )}
        {raw !== '' && (
          <Svg source={graphSvg(raw, width)} alt="Git commit graph" width={width} />
        )}
      </Box>
    )
  })
}
