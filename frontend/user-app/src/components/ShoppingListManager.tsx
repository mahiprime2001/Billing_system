import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Checkbox } from "./ui/checkbox";
import { Label } from "./ui/label";
import { Separator } from "./ui/separator";
import { PlusCircle, Trash2, Share2, MapPin } from "lucide-react";

interface ShoppingListItem {
  id: number;
  product_id: number | null;
  custom_item_name: string | null;
  quantity: number;
  is_purchased: boolean;
  notes: string | null;
}

interface ShoppingList {
  id: number;
  name: string;
  description: string | null;
  is_active: boolean;
  items: ShoppingListItem[];
}

interface ShoppingListManagerProps {
  userId: number;
  onFindMerchants: (listId: number) => void;
  onShareList: (listId: number) => void;
}

const ShoppingListManager: React.FC<ShoppingListManagerProps> = ({ 
  userId, 
  onFindMerchants,
  onShareList
}) => {
  const [lists, setLists] = useState<ShoppingList[]>([]);
  const [activeListId, setActiveListId] = useState<number | null>(null);
  const [newItemName, setNewItemName] = useState<string>('');
  const [newItemQuantity, setNewItemQuantity] = useState<number>(1);
  const [newListName, setNewListName] = useState<string>('');
  const [isCreatingList, setIsCreatingList] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchShoppingLists = async () => {
      try {
        setLoading(true);
        // In a real implementation, this would be an API call
        const response = await fetch(`/api/shopping-lists?user_id=${userId}`);
        
        if (!response.ok) {
          throw new Error('Failed to fetch shopping lists');
        }
        
        const data = await response.json();
        
        if (data.success) {
          setLists(data.lists);
          if (data.lists.length > 0) {
            setActiveListId(data.lists[0].id);
          }
        } else {
          throw new Error(data.message || 'Failed to fetch shopping lists');
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An unknown error occurred');
      } finally {
        setLoading(false);
      }
    };
    
    fetchShoppingLists();
  }, [userId]);

  const activeList = lists.find(list => list.id === activeListId);

  const handleCreateList = async () => {
    if (!newListName.trim()) {
      setError('Please enter a list name');
      return;
    }
    
    try {
      // In a real implementation, this would be an API call
      const response = await fetch('/api/shopping-lists', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          name: newListName,
          description: '',
          is_active: true
        }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to create shopping list');
      }
      
      const data = await response.json();
      
      if (data.success) {
        const newList: ShoppingList = {
          id: data.list_id,
          name: newListName,
          description: '',
          is_active: true,
          items: []
        };
        
        setLists([...lists, newList]);
        setActiveListId(data.list_id);
        setNewListName('');
        setIsCreatingList(false);
      } else {
        throw new Error(data.message || 'Failed to create shopping list');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    }
  };

  const handleAddItem = async () => {
    if (!activeListId) return;
    if (!newItemName.trim()) {
      setError('Please enter an item name');
      return;
    }
    
    try {
      // In a real implementation, this would be an API call
      const response = await fetch(`/api/shopping-lists/${activeListId}/items`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          custom_item_name: newItemName,
          quantity: newItemQuantity,
          is_purchased: false,
          notes: ''
        }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to add item to shopping list');
      }
      
      const data = await response.json();
      
      if (data.success) {
        const newItem: ShoppingListItem = {
          id: data.item_id,
          product_id: null,
          custom_item_name: newItemName,
          quantity: newItemQuantity,
          is_purchased: false,
          notes: null
        };
        
        const updatedLists = lists.map(list => {
          if (list.id === activeListId) {
            return {
              ...list,
              items: [...list.items, newItem]
            };
          }
          return list;
        });
        
        setLists(updatedLists);
        setNewItemName('');
        setNewItemQuantity(1);
      } else {
        throw new Error(data.message || 'Failed to add item to shopping list');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    }
  };

  const handleToggleItemPurchased = async (itemId: number, isPurchased: boolean) => {
    if (!activeListId) return;
    
    try {
      // In a real implementation, this would be an API call
      const response = await fetch(`/api/shopping-lists/${activeListId}/items/${itemId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          is_purchased: isPurchased
        }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to update item');
      }
      
      const data = await response.json();
      
      if (data.success) {
        const updatedLists = lists.map(list => {
          if (list.id === activeListId) {
            return {
              ...list,
              items: list.items.map(item => {
                if (item.id === itemId) {
                  return {
                    ...item,
                    is_purchased: isPurchased
                  };
                }
                return item;
              })
            };
          }
          return list;
        });
        
        setLists(updatedLists);
      } else {
        throw new Error(data.message || 'Failed to update item');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    }
  };

  const handleRemoveItem = async (itemId: number) => {
    if (!activeListId) return;
    
    try {
      // In a real implementation, this would be an API call
      const response = await fetch(`/api/shopping-lists/${activeListId}/items/${itemId}`, {
        method: 'DELETE'
      });
      
      if (!response.ok) {
        throw new Error('Failed to remove item');
      }
      
      const data = await response.json();
      
      if (data.success) {
        const updatedLists = lists.map(list => {
          if (list.id === activeListId) {
            return {
              ...list,
              items: list.items.filter(item => item.id !== itemId)
            };
          }
          return list;
        });
        
        setLists(updatedLists);
      } else {
        throw new Error(data.message || 'Failed to remove item');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    }
  };

  if (loading) {
    return <div className="flex justify-center p-8">Loading shopping lists...</div>;
  }

  return (
    <div className="w-full max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Shopping Lists</h2>
        <Button onClick={() => setIsCreatingList(true)} disabled={isCreatingList}>
          <PlusCircle className="mr-2 h-4 w-4" />
          New List
        </Button>
      </div>
      
      {error && (
        <div className="p-3 mb-4 bg-red-50 border border-red-200 rounded-md text-red-600 text-sm">
          {error}
        </div>
      )}
      
      {isCreatingList && (
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Create New Shopping List</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-end gap-4">
              <div className="flex-grow">
                <Label htmlFor="new-list-name">List Name</Label>
                <Input
                  id="new-list-name"
                  value={newListName}
                  onChange={(e) => setNewListName(e.target.value)}
                  placeholder="e.g., Weekly Groceries"
                />
              </div>
              <Button onClick={handleCreateList}>
                Create List
              </Button>
              <Button variant="outline" onClick={() => setIsCreatingList(false)}>
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
      
      {lists.length === 0 ? (
        <div className="text-center p-8 bg-gray-50 rounded-lg">
          <p className="text-gray-500">No shopping lists found</p>
          <Button className="mt-4" onClick={() => setIsCreatingList(true)}>
            Create Your First List
          </Button>
        </div>
      ) : (
        <div className="grid md:grid-cols-[250px_1fr] gap-6">
          <div className="space-y-2">
            <h3 className="font-medium mb-2">Your Lists</h3>
            {lists.map(list => (
              <div
                key={list.id}
                className={`p-3 rounded-md cursor-pointer ${
                  list.id === activeListId
                    ? 'bg-primary text-primary-foreground'
                    : 'hover:bg-gray-100'
                }`}
                onClick={() => setActiveListId(list.id)}
              >
                <div className="font-medium">{list.name}</div>
                <div className="text-sm">
                  {list.items.length} item{list.items.length !== 1 ? 's' : ''}
                </div>
              </div>
            ))}
          </div>
          
          {activeList && (
            <Card>
              <CardHeader className="pb-3">
                <div className="flex justify-between items-start">
                  <div>
                    <CardTitle>{activeList.name}</CardTitle>
                    <CardDescription>
                      {activeList.items.length} item{activeList.items.length !== 1 ? 's' : ''}
                    </CardDescription>
                  </div>
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm" onClick={() => onShareList(activeList.id)}>
                      <Share2 className="h-4 w-4 mr-1" />
                      Share
                    </Button>
                    <Button variant="default" size="sm" onClick={() => onFindMerchants(activeList.id)}>
                      <MapPin className="h-4 w-4 mr-1" />
                      Find Merchants
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-end gap-4">
                    <div className="flex-grow">
                      <Label htmlFor="new-item">Add Item</Label>
                      <Input
                        id="new-item"
                        value={newItemName}
                        onChange={(e) => setNewItemName(e.target.value)}
                        placeholder="e.g., Milk"
                      />
                    </div>
                    <div className="w-20">
                      <Label htmlFor="quantity">Qty</Label>
                      <Input
                        id="quantity"
                        type="number"
                        min="1"
                        value={newItemQuantity}
                        onChange={(e) => setNewItemQuantity(parseInt(e.target.value) || 1)}
                      />
                    </div>
                    <Button onClick={handleAddItem}>
                      Add
                    </Button>
                  </div>
                  
                  <Separator />
                  
                  {activeList.items.length === 0 ? (
                    <div className="text-center p-4 bg-gray-50 rounded-md">
                      <p className="text-gray-500">No items in this list yet</p>
                    </div>
                  ) : (
                    <div className="space-y-2">
                      {activeList.items.map(item => (
                        <div 
                          key={item.id} 
                          className={`flex items-center p-3 rounded-md ${
                            item.is_purchased ? 'bg-gray-50' : 'bg-white'
                          }`}
                        >
                          <Checkbox
                            id={`item-${item.id}`}
                            checked={item.is_purchased}
                            onCheckedChange={(checked) => 
                              handleToggleItemPurchased(item.id, checked === true)
                            }
                            className="mr-3"
                          />
                          <Label
                            htmlFor={`item-${item.id}`}
                            className={`flex-grow cursor-pointer ${
                              item.is_purchased ? 'line-through text-gray-500' : ''
                            }`}
                          >
                            {item.custom_item_name || `Product #${item.product_id}`}
                            {item.quantity > 1 && (
                              <span className="ml-2 text-sm text-gray-500">
                                × {item.quantity}
                              </span>
                            )}
                          </Label>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleRemoveItem(item.id)}
                            className="h-8 w-8 p-0"
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
};

export default ShoppingListManager;
