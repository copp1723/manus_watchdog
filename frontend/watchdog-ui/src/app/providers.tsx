'use client'
import { ReactNode } from 'react'
import { ApiProvider } from '@/lib/api'

export function Providers({ children }: { children: ReactNode }) {
  return (
    <ApiProvider>
      {children}
    </ApiProvider>
  )
}
