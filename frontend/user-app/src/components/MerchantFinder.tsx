import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Separator } from "./ui/separator";
import { MapPin, Navigation, Store } from "lucide-react";

interface Merchant {
  id: number;
  business_name: string;
  distance: number; // in kilometers
  match_percentage: number; // percentage of items available
  location: {
    latitude: number;
    longitude: number;
    address: string;
  };
  available_items: number;
  total_items: number;
}

interface MerchantFinderProps {
  listId: number;
  userLocation: {
    latitude: number;
    longitude: number;
  };
  onBack: () => void;
  onViewRoute: (merchants: Merchant[]) => void;
}

const MerchantFinder: React.FC<MerchantFinderProps> = ({ 
  listId, 
  userLocation,
  onBack,
  onViewRoute
}) => {
  const [merchants, setMerchants] = useState<Merchant[]>([]);
  const [selectedMerchants, setSelectedMerchants] = useState<number[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [searchRadius, setSearchRadius] = useState<number>(10); // Default 10km

  useEffect(() => {
    const fetchNearbyMerchants = async () => {
      try {
        setLoading(true);
        // In a real implementation, this would be an API call
        const response = await fetch(
          `/api/merchants/nearby?list_id=${listId}&latitude=${userLocation.latitude}&longitude=${userLocation.longitude}&radius=${searchRadius}`
        );
        
        if (!response.ok) {
          throw new Error('Failed to fetch nearby merchants');
        }
        
        const data = await response.json();
        
        if (data.success) {
          setMerchants(data.merchants);
        } else {
          throw new Error(data.message || 'Failed to fetch nearby merchants');
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An unknown error occurred');
      } finally {
        setLoading(false);
      }
    };
    
    fetchNearbyMerchants();
  }, [listId, userLocation, searchRadius]);

  const handleToggleMerchant = (merchantId: number) => {
    setSelectedMerchants(prev => {
      if (prev.includes(merchantId)) {
        return prev.filter(id => id !== merchantId);
      } else {
        return [...prev, merchantId];
      }
    });
  };

  const handleViewRoute = () => {
    const selectedMerchantObjects = merchants.filter(merchant => 
      selectedMerchants.includes(merchant.id)
    );
    onViewRoute(selectedMerchantObjects);
  };

  const handleSearchRadiusChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(e.target.value);
    if (!isNaN(value) && value > 0) {
      setSearchRadius(value);
    }
  };

  if (loading) {
    return <div className="flex justify-center p-8">Searching for nearby merchants...</div>;
  }

  return (
    <div className="w-full max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <Button variant="outline" onClick={onBack}>
          &larr; Back to Shopping List
        </Button>
        <div className="flex items-center gap-2">
          <Label htmlFor="search-radius" className="whitespace-nowrap">Search Radius:</Label>
          <Input
            id="search-radius"
            type="number"
            min="1"
            max="50"
            value={searchRadius}
            onChange={handleSearchRadiusChange}
            className="w-20"
          />
          <span>km</span>
        </div>
      </div>
      
      {error && (
        <div className="p-3 mb-4 bg-red-50 border border-red-200 rounded-md text-red-600 text-sm">
          {error}
        </div>
      )}
      
      <h2 className="text-2xl font-bold mb-4">Nearby Merchants</h2>
      
      {merchants.length === 0 ? (
        <div className="text-center p-8 bg-gray-50 rounded-lg">
          <p className="text-gray-500">No merchants found within {searchRadius}km radius</p>
          <p className="text-gray-500 mt-2">Try increasing the search radius</p>
        </div>
      ) : (
        <>
          <div className="mb-4">
            <p className="text-gray-500">
              Found {merchants.length} merchant{merchants.length !== 1 ? 's' : ''} within {searchRadius}km radius
            </p>
            {selectedMerchants.length > 0 && (
              <div className="mt-2 flex justify-between items-center">
                <p>
                  {selectedMerchants.length} merchant{selectedMerchants.length !== 1 ? 's' : ''} selected
                </p>
                <Button onClick={handleViewRoute}>
                  <Navigation className="mr-2 h-4 w-4" />
                  View Route
                </Button>
              </div>
            )}
          </div>
          
          <div className="space-y-4">
            {merchants
              .sort((a, b) => b.match_percentage - a.match_percentage)
              .map(merchant => (
                <Card 
                  key={merchant.id} 
                  className={`overflow-hidden ${
                    selectedMerchants.includes(merchant.id) 
                      ? 'border-2 border-primary' 
                      : ''
                  }`}
                >
                  <CardHeader className="pb-2">
                    <div className="flex justify-between items-start">
                      <div>
                        <CardTitle>{merchant.business_name}</CardTitle>
                        <CardDescription>
                          <div className="flex items-center">
                            <MapPin className="h-4 w-4 mr-1" />
                            {merchant.distance.toFixed(1)}km away
                          </div>
                        </CardDescription>
                      </div>
                      <div className="text-right">
                        <div className="text-lg font-bold">
                          {merchant.match_percentage}%
                        </div>
                        <div className="text-sm text-gray-500">
                          match
                        </div>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="pb-2">
                    <div>
                      <p className="text-sm text-gray-500">Address</p>
                      <p>{merchant.location.address}</p>
                    </div>
                    <div className="mt-2">
                      <p className="text-sm text-gray-500">Available Items</p>
                      <p>
                        {merchant.available_items} of {merchant.total_items} items on your list
                      </p>
                    </div>
                  </CardContent>
                  <CardFooter className="flex justify-between">
                    <Button variant="outline" size="sm">
                      <Store className="h-4 w-4 mr-1" />
                      View Store
                    </Button>
                    <Button 
                      variant={selectedMerchants.includes(merchant.id) ? "default" : "outline"}
                      onClick={() => handleToggleMerchant(merchant.id)}
                    >
                      {selectedMerchants.includes(merchant.id) 
                        ? 'Selected' 
                        : 'Select for Route'}
                    </Button>
                  </CardFooter>
                </Card>
              ))}
          </div>
        </>
      )}
    </div>
  );
};

export default MerchantFinder;
