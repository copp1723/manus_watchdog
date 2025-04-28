import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { Upload } from '@/components/Upload'

// Mock the fetch function
global.fetch = jest.fn()

describe('Upload Component', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('renders the upload component correctly', () => {
    const mockOnUploadSuccess = jest.fn()
    render(<Upload onUploadSuccess={mockOnUploadSuccess} />)
    
    // Check if the component renders correctly
    expect(screen.getByText(/Drop your CSV file here/i)).toBeInTheDocument()
    expect(screen.getByText(/Or click the button below to browse files/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Select CSV File/i })).toBeInTheDocument()
  })

  it('shows error when non-CSV file is selected', async () => {
    const mockOnUploadSuccess = jest.fn()
    render(<Upload onUploadSuccess={mockOnUploadSuccess} />)
    
    // Create a non-CSV file
    const file = new File(['test content'], 'test.txt', { type: 'text/plain' })
    
    // Get the file input and simulate file selection
    const input = screen.getByRole('button', { name: /Select CSV File/i })
    fireEvent.click(input)
    
    // Simulate file selection (need to access the hidden input)
    const fileInput = document.querySelector('input[type="file"]')
    fireEvent.change(fileInput, { target: { files: [file] } })
    
    // Check if error message is displayed
    await waitFor(() => {
      expect(screen.getByText(/Only CSV files are supported/i)).toBeInTheDocument()
    })
    
    // Verify that the upload function was not called
    expect(global.fetch).not.toHaveBeenCalled()
    expect(mockOnUploadSuccess).not.toHaveBeenCalled()
  })

  it('uploads CSV file successfully', async () => {
    const mockOnUploadSuccess = jest.fn()
    render(<Upload onUploadSuccess={mockOnUploadSuccess} />)
    
    // Create a CSV file
    const file = new File(['header1,header2\nvalue1,value2'], 'test.csv', { type: 'text/csv' })
    
    // Mock successful response
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ upload_id: '123', filename: 'test.csv' }),
    })
    
    // Get the file input and simulate file selection
    const input = screen.getByRole('button', { name: /Select CSV File/i })
    fireEvent.click(input)
    
    // Simulate file selection (need to access the hidden input)
    const fileInput = document.querySelector('input[type="file"]')
    fireEvent.change(fileInput, { target: { files: [file] } })
    
    // Check if loading state is shown
    await waitFor(() => {
      expect(screen.getByText(/Uploading/i)).toBeInTheDocument()
    })
    
    // Check if success callback is called
    await waitFor(() => {
      expect(mockOnUploadSuccess).toHaveBeenCalledWith('123', 'test.csv')
    })
  })

  it('handles upload error correctly', async () => {
    const mockOnUploadSuccess = jest.fn()
    render(<Upload onUploadSuccess={mockOnUploadSuccess} />)
    
    // Create a CSV file
    const file = new File(['header1,header2\nvalue1,value2'], 'test.csv', { type: 'text/csv' })
    
    // Mock error response
    global.fetch.mockResolvedValueOnce({
      ok: false,
      json: async () => ({ detail: 'Server error' }),
    })
    
    // Get the file input and simulate file selection
    const input = screen.getByRole('button', { name: /Select CSV File/i })
    fireEvent.click(input)
    
    // Simulate file selection (need to access the hidden input)
    const fileInput = document.querySelector('input[type="file"]')
    fireEvent.change(fileInput, { target: { files: [file] } })
    
    // Check if error message is displayed
    await waitFor(() => {
      expect(screen.getByText(/Server error/i)).toBeInTheDocument()
    })
    
    // Verify that the success callback was not called
    expect(mockOnUploadSuccess).not.toHaveBeenCalled()
  })
})
