import { writable } from "svelte/store";

function TokenStore() {
  const { subscribe, set, update } = writable("0");

  return {
    subscribe,
    setToken: (value) => set(value),
    delToken: (_) => set(0),
  };
}

export const tokenStore = TokenStore();
