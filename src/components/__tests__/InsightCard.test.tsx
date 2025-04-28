import { render, screen } from '@testing-library/react'
import { InsightCard } from '@/components/InsightCard'

describe('InsightCard Component', () => {
  it('renders the insight card with basic information', () => {
    render(
      <InsightCard
        title="Test Insight"
        description="This is a test insight description"
      />
    )
    
    // Check if the component renders correctly
    expect(screen.getByText('Test Insight')).toBeInTheDocument()
    expect(screen.getByText('This is a test insight description')).toBeInTheDocument()
  })

  it('renders employee information when provided', () => {
    render(
      <InsightCard
        title="Test Insight"
        description="This is a test insight description"
        employee="John Doe"
        employeeTitle="Sales Manager"
      />
    )
    
    // Check if employee information is rendered
    expect(screen.getByText('John Doe')).toBeInTheDocument()
    expect(screen.getByText('Sales Manager')).toBeInTheDocument()
    expect(screen.getByText('JO')).toBeInTheDocument() // Initials
  })

  it('renders amount when provided', () => {
    render(
      <InsightCard
        title="Test Insight"
        description="This is a test insight description"
        amount="$10,000"
      />
    )
    
    // Check if amount is rendered
    expect(screen.getByText('$10,000')).toBeInTheDocument()
  })

  it('renders percentage with correct styling for positive values', () => {
    render(
      <InsightCard
        title="Test Insight"
        description="This is a test insight description"
        percentage="15.2%"
      />
    )
    
    // Check if percentage is rendered
    const percentageElement = screen.getByText('15.2%')
    expect(percentageElement).toBeInTheDocument()
    
    // Check if parent element has the correct text color class for positive values
    const parentElement = percentageElement.parentElement
    expect(parentElement).toHaveClass('text-green-600')
  })

  it('renders percentage with correct styling for negative values', () => {
    render(
      <InsightCard
        title="Test Insight"
        description="This is a test insight description"
        percentage="-5.3%"
      />
    )
    
    // Check if percentage is rendered
    const percentageElement = screen.getByText('-5.3%')
    expect(percentageElement).toBeInTheDocument()
    
    // Check if parent element has the correct text color class for negative values
    const parentElement = percentageElement.parentElement
    expect(parentElement).toHaveClass('text-red-600')
  })

  it('renders action items when provided', () => {
    const actionItems = [
      'First action item',
      'Second action item'
    ]
    
    render(
      <InsightCard
        title="Test Insight"
        description="This is a test insight description"
        actionItems={actionItems}
      />
    )
    
    // Check if action items section is rendered
    expect(screen.getByText('Action Items')).toBeInTheDocument()
    
    // Check if individual action items are rendered
    expect(screen.getByText('First action item')).toBeInTheDocument()
    expect(screen.getByText('Second action item')).toBeInTheDocument()
  })
})
