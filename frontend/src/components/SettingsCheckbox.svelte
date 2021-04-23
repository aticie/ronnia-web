<script>
  export let checked;
</script>

<label class="switch">
  <input type="checkbox" bind:checked={checked}/>
  <div class="slider" />
</label>

<style scoped>
  .switch {
    position: relative;
    display: inline-block;
    width: 60px;
    height: 34px;
  }

  .switch input {
    display: none;
  }

  .slider {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    cursor: pointer;
    background-color: #ccc;
    border-radius: 34px;
    transition: 0.4s;
  }

  .slider::before {
    position: absolute;
    content: "";
    height: 26px;
    width: 26px;
    left: 4px;
    bottom: 4px;
    background-color: #fff;
    border-radius: 100%;
    transition: 0.4s;
  }
  
  input:checked + .slider {
    background-color: #66bb6a;
  }

  input:checked + .slider::before {
    transform: translateX(26px);
  }
</style>
