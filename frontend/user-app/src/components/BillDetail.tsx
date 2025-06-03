import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { Separator } from "./ui/separator";
import { format } from 'date-fns';

interface BillItem {
  id: number;
  product_name: string;
  quantity: number;
  unit_price: number;
  tax_rate: number;
  tax_amount: number;
  discount_amount: number;
  total_amount: number;
}

interface Payment {
  id: number;
  payment_method: string;
  amount: number;
  payment_date: string;
  transaction_reference: string | null;
  status: string;
}

interface Merchant {
  id: number;
  business_name: string;
  gst_number: string;
  email: string;
  phone_number: string;
  contact_person: string | null;
  logo_url: string | null;
}

interface Store {
  id: number;
  store_name: string;
  address_line1: string;
  address_line2: string | null;
  city: string;
  state: string;
  postal_code: string;
  contact_number: string | null;
}

interface BillDetail {
  id: number;
  bill_number: string;
  bill_date: string;
  due_date: string | null;
  total_amount: number;
  tax_amount: number;
  discount_amount: number;
  status: string;
  notes: string | null;
  merchant: Merchant;
  store: Store | null;
  items: BillItem[];
  payments: Payment[];
  payment_summary: {
    total_amount: number;
    total_paid: number;
    remaining_amount: number;
    is_fully_paid: boolean;
  };
}

interface BillDetailProps {
  billId: number;
  onBack: () => void;
  onRecordPayment: (billId: number) => void;
}

const BillDetail: React.FC<BillDetailProps> = ({ billId, onBack, onRecordPayment }) => {
  const [bill, setBill] = useState<BillDetail | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchBillDetail = async () => {
      try {
        setLoading(true);
        // In a real implementation, this would be an API call
        const response = await fetch(`/api/bills/${billId}`);
        
        if (!response.ok) {
          throw new Error('Failed to fetch bill details');
        }
        
        const data = await response.json();
        
        if (data.success) {
          setBill(data.bill);
        } else {
          throw new Error(data.message || 'Failed to fetch bill details');
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An unknown error occurred');
      } finally {
        setLoading(false);
      }
    };
    
    fetchBillDetail();
  }, [billId]);

  const formatDate = (dateString: string) => {
    try {
      return format(new Date(dateString), 'dd MMM yyyy');
    } catch (e) {
      return 'Invalid date';
    }
  };

  const getStatusBadgeColor = (status: string) => {
    switch (status) {
      case 'paid':
        return 'bg-green-500';
      case 'partially_paid':
        return 'bg-yellow-500';
      case 'overdue':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getPaymentMethodIcon = (method: string) => {
    switch (method.toLowerCase()) {
      case 'cash':
        return '💵';
      case 'upi':
        return '📱';
      case 'card':
        return '💳';
      default:
        return '💰';
    }
  };

  if (loading) {
    return <div className="flex justify-center p-8">Loading bill details...</div>;
  }

  if (error) {
    return <div className="text-red-500 p-4">Error: {error}</div>;
  }

  if (!bill) {
    return <div className="text-center p-8">Bill not found</div>;
  }

  return (
    <div className="w-full max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-4">
        <Button variant="outline" onClick={onBack}>
          &larr; Back to Bills
        </Button>
        <Badge className={getStatusBadgeColor(bill.status)}>
          {bill.status.replace('_', ' ')}
        </Badge>
      </div>

      <Card className="mb-6">
        <CardHeader>
          <div className="flex justify-between items-start">
            <div>
              <CardTitle className="text-2xl">Bill #{bill.bill_number}</CardTitle>
              <CardDescription>
                {formatDate(bill.bill_date)}
                {bill.due_date && ` • Due: ${formatDate(bill.due_date)}`}
              </CardDescription>
            </div>
            {bill.merchant.logo_url && (
              <img 
                src={bill.merchant.logo_url} 
                alt={bill.merchant.business_name} 
                className="h-12 w-auto"
              />
            )}
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-semibold mb-2">Merchant Details</h3>
              <p className="font-medium">{bill.merchant.business_name}</p>
              <p className="text-sm">GST: {bill.merchant.gst_number}</p>
              <p className="text-sm">{bill.merchant.email}</p>
              <p className="text-sm">{bill.merchant.phone_number}</p>
              {bill.merchant.contact_person && (
                <p className="text-sm">Contact: {bill.merchant.contact_person}</p>
              )}
            </div>
            
            {bill.store && (
              <div>
                <h3 className="font-semibold mb-2">Store Details</h3>
                <p className="font-medium">{bill.store.store_name}</p>
                <p className="text-sm">{bill.store.address_line1}</p>
                {bill.store.address_line2 && <p className="text-sm">{bill.store.address_line2}</p>}
                <p className="text-sm">
                  {bill.store.city}, {bill.store.state} - {bill.store.postal_code}
                </p>
                {bill.store.contact_number && (
                  <p className="text-sm">Contact: {bill.store.contact_number}</p>
                )}
              </div>
            )}
          </div>
          
          <Separator className="my-6" />
          
          <div>
            <h3 className="font-semibold mb-4">Items</h3>
            <div className="overflow-x-auto">
              <table className="w-full border-collapse">
                <thead>
                  <tr className="bg-gray-50">
                    <th className="text-left p-2">Item</th>
                    <th className="text-right p-2">Qty</th>
                    <th className="text-right p-2">Price</th>
                    <th className="text-right p-2">Tax</th>
                    <th className="text-right p-2">Discount</th>
                    <th className="text-right p-2">Total</th>
                  </tr>
                </thead>
                <tbody>
                  {bill.items.map(item => (
                    <tr key={item.id} className="border-b">
                      <td className="p-2">{item.product_name}</td>
                      <td className="text-right p-2">{item.quantity}</td>
                      <td className="text-right p-2">₹{item.unit_price.toFixed(2)}</td>
                      <td className="text-right p-2">
                        {item.tax_rate > 0 ? (
                          <>
                            ₹{item.tax_amount.toFixed(2)}
                            <span className="text-xs text-gray-500 ml-1">
                              ({item.tax_rate}%)
                            </span>
                          </>
                        ) : (
                          '—'
                        )}
                      </td>
                      <td className="text-right p-2">
                        {item.discount_amount > 0 ? (
                          <>₹{item.discount_amount.toFixed(2)}</>
                        ) : (
                          '—'
                        )}
                      </td>
                      <td className="text-right p-2 font-medium">
                        ₹{item.total_amount.toFixed(2)}
                      </td>
                    </tr>
                  ))}
                </tbody>
                <tfoot>
                  <tr className="bg-gray-50">
                    <td colSpan={4} className="p-2"></td>
                    <td className="text-right p-2 font-medium">Subtotal:</td>
                    <td className="text-right p-2 font-medium">
                      ₹{(bill.total_amount - bill.tax_amount + bill.discount_amount).toFixed(2)}
                    </td>
                  </tr>
                  {bill.tax_amount > 0 && (
                    <tr className="bg-gray-50">
                      <td colSpan={4} className="p-2"></td>
                      <td className="text-right p-2 font-medium">Tax:</td>
                      <td className="text-right p-2 font-medium">
                        ₹{bill.tax_amount.toFixed(2)}
                      </td>
                    </tr>
                  )}
                  {bill.discount_amount > 0 && (
                    <tr className="bg-gray-50">
                      <td colSpan={4} className="p-2"></td>
                      <td className="text-right p-2 font-medium">Discount:</td>
                      <td className="text-right p-2 font-medium">
                        -₹{bill.discount_amount.toFixed(2)}
                      </td>
                    </tr>
                  )}
                  <tr className="bg-gray-100">
                    <td colSpan={4} className="p-2"></td>
                    <td className="text-right p-2 font-bold">Total:</td>
                    <td className="text-right p-2 font-bold">
                      ₹{bill.total_amount.toFixed(2)}
                    </td>
                  </tr>
                </tfoot>
              </table>
            </div>
          </div>
          
          <Separator className="my-6" />
          
          <div>
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-semibold">Payment History</h3>
              {!bill.payment_summary.is_fully_paid && (
                <Button onClick={() => onRecordPayment(bill.id)}>
                  Record Payment
                </Button>
              )}
            </div>
            
            {bill.payments.length === 0 ? (
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <p className="text-gray-500">No payments recorded yet</p>
              </div>
            ) : (
              <div className="space-y-3">
                {bill.payments.map(payment => (
                  <div key={payment.id} className="flex items-center p-3 bg-gray-50 rounded-lg">
                    <div className="text-2xl mr-4">
                      {getPaymentMethodIcon(payment.payment_method)}
                    </div>
                    <div className="flex-grow">
                      <div className="font-medium">
                        {payment.payment_method.charAt(0).toUpperCase() + 
                         payment.payment_method.slice(1)}
                      </div>
                      <div className="text-sm text-gray-500">
                        {formatDate(payment.payment_date)}
                        {payment.transaction_reference && 
                         ` • Ref: ${payment.transaction_reference}`}
                      </div>
                    </div>
                    <div className="font-medium">
                      ₹{payment.amount.toFixed(2)}
                    </div>
                  </div>
                ))}
                
                <div className="flex justify-between p-3 bg-gray-100 rounded-lg font-medium">
                  <div>Payment Summary</div>
                  <div className="text-right">
                    <div>Paid: ₹{bill.payment_summary.total_paid.toFixed(2)}</div>
                    {!bill.payment_summary.is_fully_paid && (
                      <div>
                        Remaining: ₹{bill.payment_summary.remaining_amount.toFixed(2)}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}
          </div>
          
          {bill.notes && (
            <>
              <Separator className="my-6" />
              <div>
                <h3 className="font-semibold mb-2">Notes</h3>
                <p className="text-gray-700">{bill.notes}</p>
              </div>
            </>
          )}
        </CardContent>
        <CardFooter className="flex justify-end">
          <Button variant="outline" className="mr-2">
            Download PDF
          </Button>
          <Button variant="outline">
            Share
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
};

export default BillDetail;
