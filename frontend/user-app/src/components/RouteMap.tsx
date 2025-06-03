import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Separator } from "./ui/separator";
import { MapPin, Navigation, ArrowLeft, ArrowRight } from "lucide-react";

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

interface RouteStop {
  merchant_id: number;
  order: number;
  estimated_arrival_time: string;
}

interface Route {
  id: number;
  name: string;
  total_distance: number; // in kilometers
  estimated_time: number; // in minutes
  stops: RouteStop[];
}

interface RouteMapProps {
  merchants: Merchant[];
  userLocation: {
    latitude: number;
    longitude: number;
    address: string;
  };
  onBack: () => void;
}

const RouteMap: React.FC<RouteMapProps> = ({ 
  merchants, 
  userLocation,
  onBack
}) => {
  const [route, setRoute] = useState<Route | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [routeName, setRouteName] = useState<string>('Shopping Trip');
  const [isSaving, setIsSaving] = useState<boolean>(false);

  useEffect(() => {
    const generateRoute = async () => {
      try {
        setLoading(true);
        // In a real implementation, this would be an API call
        const response = await fetch('/api/routes/generate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            merchant_ids: merchants.map(m => m.id),
            start_location: userLocation,
            end_location: userLocation // Return to start
          }),
        });
        
        if (!response.ok) {
          throw new Error('Failed to generate route');
        }
        
        const data = await response.json();
        
        if (data.success) {
          setRoute(data.route);
        } else {
          throw new Error(data.message || 'Failed to generate route');
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An unknown error occurred');
      } finally {
        setLoading(false);
      }
    };
    
    generateRoute();
  }, [merchants, userLocation]);

  const handleSaveRoute = async () => {
    if (!route) return;
    
    try {
      setIsSaving(true);
      // In a real implementation, this would be an API call
      const response = await fetch('/api/routes', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          route_id: route.id,
          name: routeName
        }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to save route');
      }
      
      const data = await response.json();
      
      if (data.success) {
        alert('Route saved successfully!');
      } else {
        throw new Error(data.message || 'Failed to save route');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    } finally {
      setIsSaving(false);
    }
  };

  const formatTime = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours > 0 ? `${hours}h ` : ''}${mins}min`;
  };

  if (loading) {
    return <div className="flex justify-center p-8">Generating optimal route...</div>;
  }

  if (!route) {
    return (
      <div className="w-full max-w-4xl mx-auto">
        <Button variant="outline" onClick={onBack} className="mb-4">
          &larr; Back to Merchant Selection
        </Button>
        
        <div className="text-center p-8 bg-gray-50 rounded-lg">
          <p className="text-red-500">{error || 'Failed to generate route'}</p>
          <Button className="mt-4" onClick={onBack}>
            Try Again
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <Button variant="outline" onClick={onBack}>
          &larr; Back to Merchant Selection
        </Button>
        <div className="flex items-center gap-2">
          <Input
            value={routeName}
            onChange={(e) => setRouteName(e.target.value)}
            placeholder="Route Name"
            className="w-48"
          />
          <Button onClick={handleSaveRoute} disabled={isSaving}>
            {isSaving ? 'Saving...' : 'Save Route'}
          </Button>
        </div>
      </div>
      
      {error && (
        <div className="p-3 mb-4 bg-red-50 border border-red-200 rounded-md text-red-600 text-sm">
          {error}
        </div>
      )}
      
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Optimized Route</CardTitle>
          <CardDescription>
            Total Distance: {route.total_distance.toFixed(1)}km • 
            Estimated Time: {formatTime(route.estimated_time)}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {/* This would be a map in a real implementation */}
            <div className="h-64 bg-gray-200 rounded-md flex items-center justify-center">
              <p className="text-gray-500">Map View Would Appear Here</p>
            </div>
            
            <Separator />
            
            <div className="space-y-2">
              <div className="flex items-start p-3 bg-gray-50 rounded-md">
                <div className="flex items-center justify-center h-8 w-8 rounded-full bg-primary text-primary-foreground mr-3">
                  S
                </div>
                <div className="flex-grow">
                  <div className="font-medium">Starting Point</div>
                  <div className="text-sm text-gray-500">{userLocation.address}</div>
                </div>
              </div>
              
              {route.stops.map((stop, index) => {
                const merchant = merchants.find(m => m.id === stop.merchant_id);
                if (!merchant) return null;
                
                return (
                  <div key={stop.merchant_id} className="flex items-start">
                    <div className="flex flex-col items-center mr-3">
                      <div className="flex items-center justify-center h-8 w-8 rounded-full bg-primary text-primary-foreground">
                        {index + 1}
                      </div>
                      {index < route.stops.length - 1 && (
                        <div className="h-8 w-0.5 bg-gray-200"></div>
                      )}
                    </div>
                    <div className="flex-grow p-3 bg-white border rounded-md">
                      <div className="font-medium">{merchant.business_name}</div>
                      <div className="text-sm text-gray-500">{merchant.location.address}</div>
                      <div className="text-sm mt-1">
                        <span className="text-gray-500">Arrival: </span>
                        {new Date(stop.estimated_arrival_time).toLocaleTimeString()}
                      </div>
                      <div className="text-sm">
                        <span className="text-gray-500">Items: </span>
                        {merchant.available_items} of {merchant.total_items}
                      </div>
                    </div>
                  </div>
                );
              })}
              
              <div className="flex items-start p-3 bg-gray-50 rounded-md">
                <div className="flex items-center justify-center h-8 w-8 rounded-full bg-primary text-primary-foreground mr-3">
                  E
                </div>
                <div className="flex-grow">
                  <div className="font-medium">Ending Point</div>
                  <div className="text-sm text-gray-500">{userLocation.address}</div>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
        <CardFooter className="flex justify-between">
          <Button variant="outline">
            Share Route
          </Button>
          <Button>
            Start Navigation
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
};

export default RouteMap;
