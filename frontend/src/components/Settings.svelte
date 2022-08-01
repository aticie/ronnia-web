<script>
  import RangeSlider from "svelte-range-slider-pips";

  export let settings;
  export let userExcludes;
  
  let cooldown_max = 16;
  let newItem = "";

  const onRangeChange = (e, setting) => {
    [setting.range_start, setting.range_end] = e.detail.values;
  }

  const onSliderChange = (e, setting) => {
    setting.value = e.detail.values[0];
  }

  const onSubmit = e => {
    if (e.charCode !== 13) return;
    if (!newItem) return;
    
    userExcludes = [...userExcludes, newItem];
  }

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

  <div class="setting-background flex flex-col gap-2">
    <p class="text-center">Excluded Users</p>
    <input class="bg-neutral-800 rounded p-1" placeholder="Excluded Users" on:keypress={onSubmit} bind:value={newItem} />

    <div class="flex-col">
      {#each userExcludes as user}
        <div class="flex flex-1 items-center justify-between px-2 p-1">
          <p>{user}</p>
          <img src="/close.svg" alt="close svg" class="h-5 w-5 hover:bg-red-primary rounded transition-colors" />
        </div>
      {/each}
    </div>
  </div>
</div>
