import React, { useState } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { FaEthereum, FaExchangeAlt } from 'react-icons/fa';
import { Card, Metric, Text, ProgressBar } from '@tremor/react';
import Skeleton from 'react-loading-skeleton';
import 'react-loading-skeleton/dist/skeleton.css';

const SwapForm = () => {
  const [formData, setFormData] = useState({
    inputToken: '',
    outputToken: '',
    amount: '',
    preference: 'best_price'
  });
  const [quotes, setQuotes] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post('http://localhost:8000/api/quotes', {
        input_token: formData.inputToken,
        output_token: formData.outputToken,
        amount: parseFloat(formData.amount),
        preference: formData.preference
      });
      
      setQuotes(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred while fetching quotes');
    } finally {
      setLoading(false);
    }
  };

  const getProviderColor = (provider) => {
    const colors = {
      cowswap: 'bg-purple-500',
      uniswapx: 'bg-pink-500',
      '1inch': 'bg-blue-500'
    };
    return colors[provider] || 'bg-gray-500';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-2xl mx-auto bg-white rounded-2xl shadow-xl overflow-hidden"
    >
      <div className="p-8">
        <motion.form
          onSubmit={handleSubmit}
          className="space-y-6"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <motion.div
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <label className="block text-sm font-medium text-gray-700">
                Input Token
                <div className="mt-1 relative rounded-md shadow-sm">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <FaEthereum className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    type="text"
                    name="inputToken"
                    value={formData.inputToken}
                    onChange={handleInputChange}
                    placeholder="e.g., ETH, BTC"
                    className="pl-10 block w-full rounded-lg border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm p-3"
                    required
                  />
                </div>
              </label>
            </motion.div>

            <motion.div
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <label className="block text-sm font-medium text-gray-700">
                Output Token
                <div className="mt-1 relative rounded-md shadow-sm">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <FaExchangeAlt className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    type="text"
                    name="outputToken"
                    value={formData.outputToken}
                    onChange={handleInputChange}
                    placeholder="e.g., USDT, DAI"
                    className="pl-10 block w-full rounded-lg border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm p-3"
                    required
                  />
                </div>
              </label>
            </motion.div>
          </div>

          <motion.div
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <label className="block text-sm font-medium text-gray-700">
              Amount
              <input
                type="number"
                name="amount"
                value={formData.amount}
                onChange={handleInputChange}
                placeholder="Enter amount"
                className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm p-3"
                required
                step="any"
              />
            </label>
          </motion.div>

          <motion.div
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <label className="block text-sm font-medium text-gray-700">
              Preference
              <select
                name="preference"
                value={formData.preference}
                onChange={handleInputChange}
                className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm p-3"
              >
                <option value="best_price">Best Price</option>
                <option value="lowest_slippage">Lowest Slippage</option>
                <option value="fastest">Fastest Execution</option>
              </select>
            </label>
          </motion.div>

          <motion.button
            type="submit"
            disabled={loading}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 transition-colors duration-200"
          >
            {loading ? 'Fetching Quotes...' : 'Get Quotes'}
          </motion.button>
        </motion.form>

        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="mt-4 p-4 bg-red-50 text-red-700 rounded-lg"
            >
              {error}
            </motion.div>
          )}
        </AnimatePresence>

        <AnimatePresence>
          {loading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="mt-6 space-y-4"
            >
              <Skeleton count={3} height={100} className="my-2" />
            </motion.div>
          )}
        </AnimatePresence>

        <AnimatePresence>
          {quotes && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 20 }}
              className="mt-8 space-y-6"
            >
              <Text className="text-xl font-semibold text-gray-900">Available Quotes</Text>
              <div className="grid gap-6">
                {quotes.quotes.map((quote, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <Card
                      className={`overflow-hidden transition-all duration-200 ${
                        quotes.best_quote.provider === quote.provider
                          ? 'ring-2 ring-indigo-500'
                          : ''
                      }`}
                    >
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center space-x-3">
                          <div className={`w-10 h-10 rounded-full ${getProviderColor(quote.provider)} flex items-center justify-center`}>
                            <Text className="text-white font-bold">
                              {quote.provider.charAt(0).toUpperCase()}
                            </Text>
                          </div>
                          <div>
                            <Text className="font-medium capitalize">{quote.provider}</Text>
                            {quotes.best_quote.provider === quote.provider && (
                              <Text className="text-sm text-indigo-600 font-medium">Best Quote</Text>
                            )}
                          </div>
                        </div>
                        <Metric>{quote.quote.price.toFixed(6)}</Metric>
                      </div>
                      
                      <div className="space-y-4">
                        <div>
                          <Text className="text-sm text-gray-600">Slippage</Text>
                          <ProgressBar value={quote.quote.slippage * 100} color="indigo" className="mt-2" />
                        </div>
                        
                        <div className="grid grid-cols-2 gap-4">
                          <div>
                            <Text className="text-sm text-gray-600">Gas Estimate</Text>
                            <Text className="font-medium">{quote.quote.gas_estimate}</Text>
                          </div>
                          <div>
                            <Text className="text-sm text-gray-600">Execution Time</Text>
                            <Text className="font-medium">{quote.quote.execution_time}s</Text>
                          </div>
                        </div>
                      </div>
                    </Card>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  );
};

export default SwapForm;