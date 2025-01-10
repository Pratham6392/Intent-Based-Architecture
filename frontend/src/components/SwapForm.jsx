import React, { useState } from 'react';

const SwapForm = () => {
  const [formData, setFormData] = useState({
    inputToken: '',
    outputToken: '',
    amount: '',
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Format the intent string
    const intent = `Swap ${formData.amount} ${formData.inputToken} to ${formData.outputToken} across blockchains`;
    
    // Log the intent (for demonstration)
    console.log('Generated Intent:', intent);
    
    // Here you would typically send this to your backend
    // For now, we'll just alert the intent
    alert(`Intent captured: ${intent}`);
  };

  return (
    <div className="max-w-md mx-auto bg-white rounded-xl shadow-md overflow-hidden md:max-w-2xl p-6">
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Input Token
            <input
              type="text"
              name="inputToken"
              value={formData.inputToken}
              onChange={handleInputChange}
              placeholder="e.g., ETH, BTC"
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
              required
            />
          </label>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">
            Output Token
            <input
              type="text"
              name="outputToken"
              value={formData.outputToken}
              onChange={handleInputChange}
              placeholder="e.g., USDT, DAI"
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
              required
            />
          </label>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">
            Amount
            <input
              type="number"
              name="amount"
              value={formData.amount}
              onChange={handleInputChange}
              placeholder="Enter amount"
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
              required
              step="any"
            />
          </label>
        </div>

        <button
          type="submit"
          className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Generate Swap Intent
        </button>
      </form>
    </div>
  );
};

export default SwapForm;