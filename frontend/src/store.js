import { writable } from "svelte/store";

function TokenStore(key, startValue) {
  const { subscribe, set, update } = writable(startValue);

  return {
    subscribe,
    setToken: (value) => set(value),
    delToken: (_) => set(0),
    useLocalStorage: () => {
      const json = localStorage.getItem(key);
      if (json) {
        set(JSON.parse(json));
      } 
      subscribe(current => {
        localStorage.setItem(key, JSON.stringify(current));
      });
    }
  };
}

export const tokenStore = TokenStore('token', 0);
