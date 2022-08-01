<script>
  import RangeSlider from "svelte-range-slider-pips";

  let cooldown_max = 16;

  const onRangeChange = (e, setting) => {
    [setting.range_start, setting.range_end] = e.detail.values;
  }

  const onSliderChange = (e, setting) => {
    setting.value = e.detail.values[0];
  }

  export let settings;
</script>

<div class="flex flex-col gap-4 select-none">
  {#each settings as setting}
    {#if setting.type === "toggle"}
      <label for={setting.id} class="setting-background flex items-center justify-between">
        <p>{setting.description}</p>
        <input id={setting.id} type="checkbox" class="checkbox" bind:checked={setting.value} />
      </label>
    {:else if setting.type === "range"}
      <div class="setting-background">
        <p>{setting.description}</p>
        <RangeSlider 
          float pushy range
          formatter={v => (v === 10 ? "∞" : v)}
          pips
          pipstep={10}
          values={[setting.range_start === -1 ? 0: setting.range_start, setting.range_end === -1 ? 10: setting.range_end]}
          all="label"
          step={0.1} min={0} max={10}
          on:change={e => onRangeChange(e, setting)}
        />
      </div>
    {:else if setting.type === "value"}
      <div class="setting-background">
        <p>{setting.description}</p>
        <RangeSlider 
          range="min"
          values={[setting.value]}
          formatter={v => {
            if (v < 60) return `${v}s`
            if (v % 60 === 0) return `${Math.round(v/60)}m`
            return `${Math.floor(v/60)}m${v%60}s`
          }}
          step={1} min={0} max={cooldown_max * 60}
          pips pipstep={12 * cooldown_max} all="label" float
          on:change={e => onSliderChange(e, setting)}
        />
      </div>
    {/if}
  {/each}
</div>
