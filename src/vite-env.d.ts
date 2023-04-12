/// <reference types="vite/client" />

interface ImportMetaEnv {
  // readonly VITE_APP_TITLE: string
  // more env variables...

  readonly VITE_TWITCH_AUTH: string
  readonly VITE_OSU_AUTH: string
  readonly VITE_API_BASE: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
