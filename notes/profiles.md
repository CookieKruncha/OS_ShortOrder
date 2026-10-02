# Profile Summaries

- `default.toml`: The course profile ("lunch service"). Baseline settings.
- `bake-off.toml`: 2 cooks, switch cost 2. I/O-bound. Almost everything spends most of its life in the oven. Reward keeping cooks busy while dishes bake.
- `banquet-night.toml`: 2 cooks, switch cost 1. Convoy effect: long banquets block short espressos. Preemption is cheap and crucial here.
- `blind.toml`: `known_durations = false`. Durations hidden. Needs per-recipe online means learned from `obs.history`.
- `brigade.toml`: 4 cooks, switch cost 3. High load. Balance work across cooks; avoid unnecessary moves.
- `function.toml`: 4 sittings, 400 ticks apart, no ovens. `wake_in` (alarm) is critical since the engine won't wake up the scheduler for long periods.
- `one-cook.toml`: 1 cook, switch cost 2. Textbook setting. Lower load.
- `rush.toml`: 2 cooks, switch cost 2. More custom than 2 cooks can serve. Deadline awareness and dropping impossible orders is key.
- `service-line.toml`: 4 cooks, switch cost 2, but 1 place at the `pass` station. Resource contention bottleneck.
