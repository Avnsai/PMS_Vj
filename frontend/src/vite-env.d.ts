/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL?: string
  readonly VITE_BACKEND_URL?: string
  readonly VITE_BACKEND_API_URL?: string
  readonly VITE_LOCAL_API_URL?: string
  readonly VITE_PROD_API_URL?: string
  readonly VITE_ALLOWED_HOSTS?: string
  readonly REACT_APP_BACKEND_URL?: string
  readonly REACT_APP_NAME?: string
  readonly REACT_APP_VERSION?: string
  readonly NODE_ENV?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
