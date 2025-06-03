import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./ui/tabs";
import { format } from 'date-fns';

interface Bill {
  id: number;
  bill_number: string;
  merchant_name: string;
  store_name: string | null;
  bill_date: string;
  due_date: string | null;
  total_amount: number;
  status: string;
}

interface BillListProps {
  userId: number;
  onViewBill: (billId: number) => void;
}

const BillList: React.FC<BillListProps> = ({ userId, onViewBill }) => {
  const [bills, setBills] = useState<Bill[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<string>("all");

  useEffect(() => {
    const fetchBills = async () => {
      try {
        setLoading(true);
        // In a real implementation, this would be an API call
        const response = await fetch(`/api/bills?user_id=${userId}`);
        
        if (!response.ok) {
          throw new Error('Failed to fetch bills');
        }
        
        const data = await response.json();
        
        if (data.success) {
          setBills(data.bills);
        } else {
          throw new Error(data.message || 'Failed to fetch bills');
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An unknown error occurred');
      } finally {
        setLoading(false);
      }
    };
    
    fetchBills();
  }, [userId]);

  const getFilteredBills = () => {
    switch (activeTab) {
      case 'pending':
        return bills.filter(bill => bill.status === 'pending');
      case 'paid':
        return bills.filter(bill => bill.status === 'paid');
      case 'partially_paid':
        return bills.filter(bill => bill.status === 'partially_paid');
      case 'overdue':
        return bills.filter(bill => bill.status === 'overdue');
      default:
        return bills;
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

  const formatDate = (dateString: string) => {
    try {
      return format(new Date(dateString), 'dd MMM yyyy');
    } catch (e) {
      return 'Invalid date';
    }
  };

  const filteredBills = getFilteredBills();

  if (loading) {
    return <div className="flex justify-center p-8">Loading bills...</div>;
  }

  if (error) {
    return <div className="text-red-500 p-4">Error: {error}</div>;
  }

  return (
    <div className="w-full max-w-4xl mx-auto">
      <Tabs defaultValue="all" value={activeTab} onValueChange={setActiveTab}>
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold">Your Bills</h2>
          <TabsList>
            <TabsTrigger value="all">All</TabsTrigger>
            <TabsTrigger value="pending">Pending</TabsTrigger>
            <TabsTrigger value="partially_paid">Partially Paid</TabsTrigger>
            <TabsTrigger value="paid">Paid</TabsTrigger>
            <TabsTrigger value="overdue">Overdue</TabsTrigger>
          </TabsList>
        </div>
        
        <TabsContent value={activeTab} className="space-y-4">
          {filteredBills.length === 0 ? (
            <div className="text-center p-8 bg-gray-50 rounded-lg">
              <p className="text-gray-500">No bills found</p>
            </div>
          ) : (
            filteredBills.map(bill => (
              <Card key={bill.id} className="overflow-hidden">
                <CardHeader className="pb-2">
                  <div className="flex justify-between items-start">
                    <div>
                      <CardTitle>{bill.merchant_name}</CardTitle>
                      <CardDescription>
                        {bill.store_name && `Store: ${bill.store_name}`}
                      </CardDescription>
                    </div>
                    <Badge className={getStatusBadgeColor(bill.status)}>
                      {bill.status.replace('_', ' ')}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="pb-2">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-gray-500">Bill Number</p>
                      <p className="font-medium">{bill.bill_number}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Amount</p>
                      <p className="font-medium">₹{bill.total_amount.toFixed(2)}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Bill Date</p>
                      <p className="font-medium">{formatDate(bill.bill_date)}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Due Date</p>
                      <p className="font-medium">
                        {bill.due_date ? formatDate(bill.due_date) : 'N/A'}
                      </p>
                    </div>
                  </div>
                </CardContent>
                <CardFooter className="pt-2 flex justify-end">
                  <Button onClick={() => onViewBill(bill.id)}>
                    View Details
                  </Button>
                </CardFooter>
              </Card>
            ))
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default BillList;
