import { render, screen } from '@testing-library/react'
import { Header } from '@/components/Header'

describe('Header Component', () => {
  it('renders the header with logo and title', () => {
    render(<Header />)
    
    // Check if the component renders correctly
    expect(screen.getByText('Watchdog AI')).toBeInTheDocument()
    expect(screen.getByText('Dealership Intelligence')).toBeInTheDocument()
    
    // Check if the logo icon is rendered
    const logoIcon = document.querySelector('svg')
    expect(logoIcon).toBeInTheDocument()
  })
  
  it('has a link to the home page', () => {
    render(<Header />)
    
    // Check if the link to home page exists
    const homeLink = screen.getByRole('link')
    expect(homeLink).toHaveAttribute('href', '/')
  })
})
