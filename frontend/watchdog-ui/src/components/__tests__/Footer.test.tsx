import { render, screen } from '@testing-library/react'
import { Footer } from '@/components/Footer'

describe('Footer Component', () => {
  it('renders the footer with copyright information', () => {
    render(<Footer />)
    
    // Check if the component renders correctly with current year
    const currentYear = new Date().getFullYear().toString()
    expect(screen.getByText(new RegExp(`© ${currentYear} Watchdog AI. All rights reserved.`, 'i'))).toBeInTheDocument()
  })
  
  it('renders footer links', () => {
    render(<Footer />)
    
    // Check if all footer links are rendered
    expect(screen.getByText('Privacy Policy')).toBeInTheDocument()
    expect(screen.getByText('Terms of Service')).toBeInTheDocument()
    expect(screen.getByText('Contact')).toBeInTheDocument()
    
    // Check if links have href attributes
    const links = screen.getAllByRole('link')
    expect(links.length).toBe(3)
    links.forEach(link => {
      expect(link).toHaveAttribute('href', '#')
    })
  })
})
