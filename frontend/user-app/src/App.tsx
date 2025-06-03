import React, { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import BillList from './components/BillList';
import BillDetail from './components/BillDetail';
import RecordPayment from './components/RecordPayment';
import ShoppingListManager from './components/ShoppingListManager';
import MerchantFinder from './components/MerchantFinder';
import RouteMap from './components/RouteMap';
import { Bell, User, LogOut } from "lucide-react";
import { Button } from "./components/ui/button";
import './App.css';

// Mock user data
const MOCK_USER = {
  id: 1,
  name: 'John Doe',
  email: 'john.doe@example.com',
  phone: '+91 9876543210',
  location: {
    latitude: 12.9716,
    longitude: 77.5946,
    address: '123 Main Street, Bangalore, Karnataka'
  }
};

function App() {
  const [activeTab, setActiveTab] = useState('bills');
  const [selectedBillId, setSelectedBillId] = useState<number | null>(null);
  const [isRecordingPayment, setIsRecordingPayment] = useState(false);
  const [paymentDetails, setPaymentDetails] = useState<{
    billId: number;
    totalAmount: number;
    remainingAmount: number;
  } | null>(null);
  const [selectedListId, setSelectedListId] = useState<number | null>(null);
  const [selectedMerchants, setSelectedMerchants] = useState<any[]>([]);
  const [viewMode, setViewMode] = useState<'list' | 'detail' | 'payment' | 'merchants' | 'route'>('list');

  const handleViewBill = (billId: number) => {
    setSelectedBillId(billId);
    setViewMode('detail');
  };

  const handleBackToBills = () => {
    setSelectedBillId(null);
    setViewMode('list');
  };

  const handleRecordPayment = (billId: number) => {
    // In a real app, we would fetch the bill details here
    setPaymentDetails({
      billId,
      totalAmount: 1000, // Mock data
      remainingAmount: 500 // Mock data
    });
    setViewMode('payment');
  };

  const handlePaymentSuccess = () => {
    setViewMode('detail');
    // In a real app, we would refresh the bill details here
  };

  const handleFindMerchants = (listId: number) => {
    setSelectedListId(listId);
    setViewMode('merchants');
  };

  const handleBackToList = () => {
    setViewMode('list');
  };

  const handleViewRoute = (merchants: any[]) => {
    setSelectedMerchants(merchants);
    setViewMode('route');
  };

  const renderContent = () => {
    if (activeTab === 'bills') {
      if (viewMode === 'list') {
        return <BillList userId={MOCK_USER.id} onViewBill={handleViewBill} />;
      } else if (viewMode === 'detail' && selectedBillId) {
        return (
          <BillDetail 
            billId={selectedBillId} 
            onBack={handleBackToBills} 
            onRecordPayment={handleRecordPayment} 
          />
        );
      } else if (viewMode === 'payment' && paymentDetails) {
        return (
          <RecordPayment 
            billId={paymentDetails.billId}
            totalAmount={paymentDetails.totalAmount}
            remainingAmount={paymentDetails.remainingAmount}
            onCancel={() => setViewMode('detail')}
            onSuccess={handlePaymentSuccess}
          />
        );
      }
    } else if (activeTab === 'shopping') {
      if (viewMode === 'list') {
        return (
          <ShoppingListManager 
            userId={MOCK_USER.id} 
            onFindMerchants={handleFindMerchants}
            onShareList={(listId) => console.log('Share list', listId)}
          />
        );
      } else if (viewMode === 'merchants' && selectedListId) {
        return (
          <MerchantFinder 
            listId={selectedListId}
            userLocation={MOCK_USER.location}
            onBack={handleBackToList}
            onViewRoute={handleViewRoute}
          />
        );
      } else if (viewMode === 'route' && selectedMerchants.length > 0) {
        return (
          <RouteMap 
            merchants={selectedMerchants}
            userLocation={MOCK_USER.location}
            onBack={() => setViewMode('merchants')}
          />
        );
      }
    }
    
    return <div>Content not found</div>;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <h1 className="text-xl font-bold">Billing System</h1>
            <div className="flex items-center space-x-4">
              <Button variant="ghost" size="icon">
                <Bell className="h-5 w-5" />
              </Button>
              <div className="flex items-center space-x-2">
                <div className="h-8 w-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground">
                  <User className="h-5 w-5" />
                </div>
                <span className="text-sm font-medium">{MOCK_USER.name}</span>
              </div>
              <Button variant="ghost" size="icon">
                <LogOut className="h-5 w-5" />
              </Button>
            </div>
          </div>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Tabs value={activeTab} onValueChange={(value) => {
          setActiveTab(value);
          setViewMode('list');
        }}>
          <TabsList className="mb-8">
            <TabsTrigger value="bills">Bills</TabsTrigger>
            <TabsTrigger value="shopping">Shopping Lists</TabsTrigger>
            <TabsTrigger value="pickup">Pickup Requests</TabsTrigger>
            <TabsTrigger value="profile">Profile</TabsTrigger>
          </TabsList>
          
          <TabsContent value={activeTab}>
            {renderContent()}
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}

export default App;
