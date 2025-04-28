'use client'
import { GaugeIcon } from 'lucide-react'
import Link from 'next/link'

export function Header() {
  return (
    <header className="bg-white border-b border-gray-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link href="/" className="flex items-center space-x-2">
            <GaugeIcon className="h-6 w-6 text-primary" />
            <span className="font-bold text-xl">Watchdog AI</span>
          </Link>
          
          <div className="text-sm text-gray-500">
            Dealership Intelligence
          </div>
        </div>
      </div>
    </header>
  )
}
