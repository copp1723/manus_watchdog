'use client'

export function Footer() {
  return (
    <footer className="bg-white border-t border-gray-200 py-6">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <p className="text-sm text-gray-500">
              © {new Date().getFullYear()} Watchdog AI. All rights reserved.
            </p>
          </div>
          
          <div className="flex space-x-6">
            <a href="#" className="text-sm text-gray-500 hover:text-primary">
              Privacy Policy
            </a>
            <a href="#" className="text-sm text-gray-500 hover:text-primary">
              Terms of Service
            </a>
            <a href="#" className="text-sm text-gray-500 hover:text-primary">
              Contact
            </a>
          </div>
        </div>
      </div>
    </footer>
  )
}
