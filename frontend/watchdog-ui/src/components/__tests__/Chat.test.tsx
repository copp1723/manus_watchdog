import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { Chat } from '@/components/Chat'

describe('Chat Component', () => {
  it('renders the chat component correctly', () => {
    const mockOnSendQuestion = jest.fn()
    render(<Chat onSendQuestion={mockOnSendQuestion} isLoading={false} />)
    
    // Check if the component renders correctly
    expect(screen.getByText(/Ask a Question/i)).toBeInTheDocument()
    expect(screen.getByPlaceholderText(/e.g., Who is my top sales rep?/i)).toBeInTheDocument()
    expect(screen.getByRole('button')).toBeInTheDocument()
  })

  it('disables input and button when isLoading is true', () => {
    const mockOnSendQuestion = jest.fn()
    render(<Chat onSendQuestion={mockOnSendQuestion} isLoading={true} />)
    
    // Check if input and button are disabled
    const input = screen.getByPlaceholderText(/e.g., Who is my top sales rep?/i)
    const button = screen.getByRole('button')
    
    expect(input).toBeDisabled()
    expect(button).toBeDisabled()
  })

  it('disables input and button when disabled prop is true', () => {
    const mockOnSendQuestion = jest.fn()
    render(<Chat onSendQuestion={mockOnSendQuestion} isLoading={false} disabled={true} />)
    
    // Check if input and button are disabled
    const input = screen.getByPlaceholderText(/e.g., Who is my top sales rep?/i)
    const button = screen.getByRole('button')
    
    expect(input).toBeDisabled()
    expect(button).toBeDisabled()
  })

  it('calls onSendQuestion when form is submitted', async () => {
    const mockOnSendQuestion = jest.fn()
    render(<Chat onSendQuestion={mockOnSendQuestion} isLoading={false} />)
    
    // Type a question
    const input = screen.getByPlaceholderText(/e.g., Who is my top sales rep?/i)
    fireEvent.change(input, { target: { value: 'Who is my top sales rep?' } })
    
    // Submit the form
    const button = screen.getByRole('button')
    fireEvent.click(button)
    
    // Check if onSendQuestion was called with the correct question
    expect(mockOnSendQuestion).toHaveBeenCalledWith('Who is my top sales rep?')
    
    // Check if input was cleared
    await waitFor(() => {
      expect(input).toHaveValue('')
    })
  })

  it('does not call onSendQuestion when form is submitted with empty question', () => {
    const mockOnSendQuestion = jest.fn()
    render(<Chat onSendQuestion={mockOnSendQuestion} isLoading={false} />)
    
    // Submit the form without typing a question
    const button = screen.getByRole('button')
    fireEvent.click(button)
    
    // Check if onSendQuestion was not called
    expect(mockOnSendQuestion).not.toHaveBeenCalled()
  })
})
