'use client'
import { Card } from '@/components/ui/card'
import { ArrowUpIcon, ArrowDownIcon, InfoIcon } from 'lucide-react'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip'

interface InsightCardProps {
  title: string
  description: string
  employee?: string
  employeeTitle?: string
  amount?: string
  percentage?: string | number
  actionItems?: string[]
}

export function InsightCard({
  title,
  description,
  employee,
  employeeTitle,
  amount,
  percentage,
  actionItems = []
}: InsightCardProps) {
  // Determine if percentage is positive, negative, or neutral
  const percentageValue = typeof percentage === 'string' 
    ? parseFloat(percentage.replace('%', '')) 
    : percentage
  
  const isPositive = percentageValue && percentageValue > 0
  const isNegative = percentageValue && percentageValue < 0
  
  // Format percentage for display
  const displayPercentage = typeof percentage === 'number' 
    ? `${percentage.toFixed(1)}%` 
    : percentage

  return (
    <Card className="overflow-hidden">
      <div className="p-6">
        <div className="flex justify-between items-start mb-4">
          <h3 className="text-lg font-medium">{title}</h3>
          
          {displayPercentage && (
            <div 
              className={`flex items-center text-sm font-medium ${
                isPositive ? 'text-green-600' : isNegative ? 'text-red-600' : 'text-gray-600'
              }`}
            >
              {isPositive && <ArrowUpIcon className="h-4 w-4 mr-1" />}
              {isNegative && <ArrowDownIcon className="h-4 w-4 mr-1" />}
              {displayPercentage}
            </div>
          )}
        </div>
        
        <p className="text-gray-600 mb-4">{description}</p>
        
        {(employee || amount) && (
          <div className="flex items-center justify-between mb-4">
            {employee && (
              <div className="flex items-center">
                <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center text-primary font-medium">
                  {employee.substring(0, 2).toUpperCase()}
                </div>
                <div className="ml-3">
                  <p className="font-medium">{employee}</p>
                  {employeeTitle && (
                    <p className="text-xs text-gray-500">{employeeTitle}</p>
                  )}
                </div>
              </div>
            )}
            
            {amount && (
              <div className="text-right">
                <p className="text-lg font-bold">{amount}</p>
              </div>
            )}
          </div>
        )}
        
        {actionItems.length > 0 && (
          <div className="mt-4">
            <div className="flex items-center mb-2">
              <h4 className="text-sm font-medium">Action Items</h4>
              <TooltipProvider>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <InfoIcon className="h-4 w-4 ml-1 text-gray-400" />
                  </TooltipTrigger>
                  <TooltipContent>
                    <p className="text-xs">Recommended actions based on this insight</p>
                  </TooltipContent>
                </Tooltip>
              </TooltipProvider>
            </div>
            <ul className="space-y-1">
              {actionItems.map((item, index) => (
                <li key={index} className="text-sm text-gray-600 flex items-start">
                  <span className="text-primary mr-2">•</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </Card>
  )
}
