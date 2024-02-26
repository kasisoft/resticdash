/// <reference types="vite/client" />

/** @see https://vitejs.dev/guide/env-and-mode.html#env-files */

interface ImportMetaEnv {
    readonly VITE_BACKEND_URL: string,
}
  
interface ImportMeta {
    readonly env: ImportMetaEnv
}
