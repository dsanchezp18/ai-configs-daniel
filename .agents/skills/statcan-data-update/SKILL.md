---
name: statcan-data-update
description: Refresh an article or table with the latest Statistics Canada data using the MapleStats tools. Finds the source table, pulls the new values, compares them with the published text, and updates the numbers. Use when the user says "update this with the new data", "refresh the StatCan table", or gives an Alberta statistics article and a new reference period.
---

# StatCan data update

Use the MapleStats tools (`plan_query`, `search_tools`, `call_tool`, with `wds_` for tables and `statcan_daily_` for release notes). Load them with ToolSearch if they are not available.

## Steps

1. **Find the sources.** Read the article. List every Statistics Canada table number in its source notes, with the measures, geography and period each one feeds.
2. **Pull the new data.** For each table, fetch the latest values with MapleStats. Note the release date. Read the table's revision notes and The Daily release for the period.
3. **Compare.** Build a short table in the chat: each figure in the article, the old value, the new value, and the change. Include revised values for earlier years, not only the new period. Check whether the new release revised history, rebased a series or changed a definition.
4. **Update the article.** Replace the numbers, periods, rankings and headline wording that changed. Use the revised series everywhere. Follow `economic-statistics-insights` for percent and percentage points, rounding, source notes and revision wording. If a finding reversed (a ranking, a direction), tell the user before rewriting the text around it.
5. **Update figures and notes.** Update figure titles, periods and source notes. Say which charts need to be rebuilt.
6. **Offer the code.** MapleStats can return R, Python, Stata or Julia code that pulls the same data (`reproduce_code`). Offer it, and give R by default.

## Rules

- Do not take figures from search snippets. Use the table values.
- If a table is missing, discontinued or renumbered, say so and ask. Do not substitute another table.
- Do not change the article's method or structure. Change data and the wording that depends on it.
- Keep a list of every number you changed, and show it to the user at the end.
