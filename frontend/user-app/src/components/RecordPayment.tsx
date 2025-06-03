import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { RadioGroup, RadioGroupItem } from "./ui/radio-group";
import { Separator } from "./ui/separator";
import { format } from 'date-fns';

interface RecordPaymentProps {
  billId: number;
  totalAmount: number;
  remainingAmount: number;
  onCancel: () => void;
  onSuccess: () => void;
}

const RecordPayment: React.FC<RecordPaymentProps> = ({ 
  billId, 
  totalAmount,
  remainingAmount,
  onCancel, 
  onSuccess 
}) => {
  const [paymentMethod, setPaymentMethod] = useState<string>('cash');
  const [amount, setAmount] = useState<string>(remainingAmount.toFixed(2));
  const [transactionReference, setTransactionReference] = useState<string>('');
  const [notes, setNotes] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate amount
    const amountValue = parseFloat(amount);
    if (isNaN(amountValue) || amountValue <= 0) {
      setError('Please enter a valid amount');
      return;
    }
    
    if (amountValue > remainingAmount) {
      setError(`Amount cannot exceed the remaining amount (₹${remainingAmount.toFixed(2)})`);
      return;
    }
    
    try {
      setLoading(true);
      setError(null);
      
      // In a real implementation, this would be an API call
      const response = await fetch(`/api/bills/${billId}/payment`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          payment_method: paymentMethod,
          amount: amountValue,
          payment_date: new Date().toISOString(),
          transaction_reference: transactionReference || null,
          notes: notes || null,
          updated_by: 1, // This would be the current user's ID
        }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to record payment');
      }
      
      const data = await response.json();
      
      if (data.success) {
        onSuccess();
      } else {
        throw new Error(data.message || 'Failed to record payment');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle>Record Payment</CardTitle>
        <CardDescription>
          Record a payment for bill #{billId}
        </CardDescription>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4">
          {error && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-md text-red-600 text-sm">
              {error}
            </div>
          )}
          
          <div className="space-y-2">
            <Label htmlFor="amount">Payment Amount</Label>
            <div className="relative">
              <span className="absolute left-3 top-1/2 -translate-y-1/2">₹</span>
              <Input
                id="amount"
                type="number"
                step="0.01"
                min="0.01"
                max={remainingAmount}
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                className="pl-7"
                required
              />
            </div>
            <p className="text-sm text-gray-500">
              Remaining amount: ₹{remainingAmount.toFixed(2)}
            </p>
          </div>
          
          <div className="space-y-2">
            <Label>Payment Method</Label>
            <RadioGroup 
              value={paymentMethod} 
              onValueChange={setPaymentMethod}
              className="flex flex-col space-y-1"
            >
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="cash" id="cash" />
                <Label htmlFor="cash" className="cursor-pointer">Cash</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="upi" id="upi" />
                <Label htmlFor="upi" className="cursor-pointer">UPI</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="card" id="card" />
                <Label htmlFor="card" className="cursor-pointer">Card</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="other" id="other" />
                <Label htmlFor="other" className="cursor-pointer">Other</Label>
              </div>
            </RadioGroup>
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="reference">Transaction Reference (Optional)</Label>
            <Input
              id="reference"
              value={transactionReference}
              onChange={(e) => setTransactionReference(e.target.value)}
              placeholder="e.g., UPI ID, Card last 4 digits"
            />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="notes">Notes (Optional)</Label>
            <Input
              id="notes"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Any additional information"
            />
          </div>
        </CardContent>
        <CardFooter className="flex justify-between">
          <Button type="button" variant="outline" onClick={onCancel}>
            Cancel
          </Button>
          <Button type="submit" disabled={loading}>
            {loading ? 'Processing...' : 'Record Payment'}
          </Button>
        </CardFooter>
      </form>
    </Card>
  );
};

export default RecordPayment;
