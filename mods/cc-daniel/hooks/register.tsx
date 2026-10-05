import type { Register } from 'claude-code'

const WINDOW_NAMES: Record<string, string> = {
  five_hour: '5-hour limit',
  seven_day: '7-day limit',
  spend_limit: 'Spend limit',
}

// Green under 60%, yellow under 85%, red above.
const barColor = (percent: number) =>
  percent < 60 ? 'green' : percent < 85 ? 'yellow' : 'red'

const bar = (percent: number, cells = 10) => {
  const filled = Math.round((Math.min(percent, 100) / 100) * cells)

  return '█'.repeat(filled) + '░'.repeat(cells - filled)
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    let lastSignature = ''

    const tick = async () => {
      const now = await $.session.usage()
      const got = {
        windows: now.rateLimits,
        contextPercent: now.context.percent,
      }
      const signature = JSON.stringify(got)

      if (signature !== lastSignature) {
        lastSignature = signature
        await $.state.set({ plugin: 'cc-daniel', key: 'usage' } as const, got)
      }

      const five = got.windows.find((w: any) => w.kind === 'five_hour')
      $.ui.status(five ? `5h ${five.percentUsed}%` : undefined)
    }

    await tick()
    $.clock.every(5000, () => void tick())

    return next(e)
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const { value: now } = await $.state.get({ plugin: 'cc-daniel', key: 'usage' } as const)

    if (e.props.hasSurvey || !now) return next(e)

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
            <Text color={barColor(item.percent)}>{bar(item.percent)}</Text>
            <Text bold>{`${item.percent}%`}</Text>
          </Box>
        ))}
      </Box>
    )
  })
}
