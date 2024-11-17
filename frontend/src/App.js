import React, { useState, useEffect } from 'react';
import { Container, CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import { AddressSearch } from './components/AddressSearch';
import { BalanceCard } from './components/BalanceCard';
import { TransactionsTable } from './components/TransactionsTable';
import { CryptoPrices } from './components/CryptoPrices';
import { AlertModal } from './components/AlertModal';
import { getAddressInfo, getPrices } from './services/api';

const theme = createTheme();

function App() {
  const [addressData, setAddressData] = useState(null);
  const [prices, setPrices] = useState({});
  const [alertOpen, setAlertOpen] = useState(false);

  useEffect(() => {
    const fetchPrices = async () => {
      try {
        const data = await getPrices();
        setPrices(data);
      } catch (error) {
        console.error('Error fetching prices:', error);
      }
    };

    fetchPrices();
    const interval = setInterval(fetchPrices, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleSearch = async (address) => {
    try {
      const data = await getAddressInfo(address);
      setAddressData(data);
    } catch (error) {
      console.error('Error fetching address info:', error);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <AddressSearch onSearch={handleSearch} />
        <CryptoPrices prices={prices} />
        {addressData && (
          <>
            <BalanceCard 
              balance={addressData.balance} 
              usdBalance={addressData.balance * (prices.BTC || 0)} 
            />
            <TransactionsTable transactions={addressData.transactions} />
          </>
        )}
        <AlertModal 
          open={alertOpen}
          onClose={() => setAlertOpen(false)}
          cryptocurrencies={Object.keys(prices)}
        />
      </Container>
    </ThemeProvider>
  );
}

export default App;
